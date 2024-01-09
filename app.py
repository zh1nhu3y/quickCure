from flask import Flask, render_template, request, session, flash, redirect, url_for, jsonify
from flask_mysqldb import MySQL, MySQLdb
import base64
from flask_session import Session
from datetime import datetime, timedelta


app = Flask(__name__)

app.secret_key = '123'
app.jinja_env.filters['zip'] = zip

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "quickcure"
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/ourDoctors')
def ourDoctors():
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM doctor")

        results = cur.fetchall()
        user_id = session.get('id')
        
        doctor_data = []
        
        for result in results:
            doctor_id = result['doctor_id']
            doctor_name = result['doctor_name']
            doctor_position = result['doctor_position']

            doctor_img_base64 = base64.b64encode(result['doctor_img']).decode('utf-8') if result['doctor_img'] and result['doctor_img'] != b'' else None
            
            doctor_data.append({
                'doctor_id': doctor_id,
                'doctor_name': doctor_name,
                'doctor_position': doctor_position,
                'doctor_img_base64': doctor_img_base64,
            })
            
        cur.close()
            
    return render_template('ourDoctors.html', doctor_data=doctor_data, user_id=user_id)


@app.route('/doctorProfile/<int:doctor_id>')
def doctorProfile(doctor_id):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM doctor JOIN first_aid_title ON doctor.doctor_id = first_aid_title.doctor_id WHERE doctor.doctor_id = %s", (doctor_id,))
        results = cur.fetchall()
        
        user_id = session.get('id')
        doc_data = {}
        
        for result in results:
            doctor_id = result['doctor_id']
            if doctor_id not in doc_data:
                doctor_name = result['doctor_name']
                doctor_img_base64 = base64.b64encode(result['doctor_img']).decode('utf-8') if result['doctor_img'] and result['doctor_img'] != b'' else None
                doctor_position = result['doctor_position']
                doctor_email = result['doctor_email']
                doctor_qualification = result['doctor_qualification']


                doc_data[doctor_id] = {
                    'doctor_id': doctor_id,
                    'doctor_name': doctor_name,
                    'doctor_img_base64': doctor_img_base64,
                    'doctor_position': doctor_position,
                    'doctor_email': doctor_email,
                    'doctor_qualification': doctor_qualification,
                    'verified_procedure': [],
                }
            
            doc_data[doctor_id]['verified_procedure'].append({
                'fa_id': result['fa_id'],
                'fa_title': result['fa_title'],
            })

        cur.close()
    return render_template('doctorProfile.html', doc_data=list(doc_data.values()), user_id=user_id)


@app.route('/')
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM first_aid_title ORDER BY fa_datetime LIMIT 4")
    procedures = cur.fetchall()
    cur.close()

    user_id = session.get('id')

    if user_id:
        return render_template('home.html', user_id=user_id, procedures=procedures)
    else:
        return render_template('home.html', procedures=procedures)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE user_email = %s AND user_password = %s", (email, password))
        user = cur.fetchone()
        cur.close()

        if user:
            username = email.split('@')[0]
            session["username"] = username
            session['id'] = user['user_id']
        else:
            flash('Invalid Email or Password. Please try again.', 'error')

    return redirect(url_for('home'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if role == 'user':
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `user` (`user_email`, `user_password`) VALUES (%s, %s)", (email, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('home'))

        elif role == 'doctor':
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO `doctor` (`doctor_email`, `doctor_password`) VALUES (%s, %s)", (email, password))
            mysql.connection.commit()
            cur.close()
            return redirect(url_for('home'))

    return render_template('home.html')


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/ajaxlivesearch', methods=['POST', 'GET'])
def ajaxlivesearch():
    search_word = request.form.get('query', '')

    if search_word:
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            query = "SELECT * FROM first_aid_title WHERE fa_title LIKE %s LIMIT 5"
            cur.execute(query, ('%' + search_word + '%',))
            titles = cur.fetchall()
            cur.close()

            return jsonify({'htmlresponse': render_template('response.html', titles=titles)})

        except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': str(e)})

    return jsonify({'htmlresponse': ''})


@app.route('/contentPage/<int:id>')
def contentPage(id):
    with mysql.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
        cur.execute("SELECT * FROM first_aid_title JOIN doctor ON first_aid_title.doctor_id = doctor.doctor_id JOIN first_aid_content ON first_aid_title.fa_id = first_aid_content.fa_id WHERE first_aid_title.fa_id = %s", (id,))
        content_results = cur.fetchall()
        
        content = {}
        
        for result in content_results:
            fa_id = result['fa_id']
            if fa_id not in content:
                fa_title = result['fa_title']
                doctor_name = result['doctor_name']
                doctor_id = result['doctor_id']
                
                content[fa_id] = {
                    'fa_id': fa_id,
                    'fa_title': fa_title,
                    'doctor_name': doctor_name,
                    'doctor_id': doctor_id,
                    'content': [],
                }
            
            if result['content']:
                content_img_base64 = base64.b64encode(result['content_image']).decode('utf-8') if result['content_image'] and result['content_image'] != b'' else None
                content[fa_id]['content'].append((content_img_base64, result['content']))
        
        # Comment Section
        
        cur.execute("SELECT * FROM comment LEFT JOIN user ON comment.user_id = user.user_id WHERE fa_id = %s ORDER BY comment_datetime DESC", (id,))
        comments = cur.fetchall()
        
        user_id = session.get('id')

        # Query to get save information
        query_save = "SELECT * FROM save_procedure WHERE fa_id = %s AND user_id = %s"
        cur.execute(query_save, (id, user_id))
        saved = cur.fetchall()

        # Query to get the count of all saves for the procedure
        query_save_count = "SELECT COUNT(*) as save_count FROM save_procedure WHERE fa_id = %s"
        cur.execute(query_save_count, (id,))
        save_count = cur.fetchone()['save_count']

        cur.close()
            
    return render_template('contentPage.html', content=list(content.values()), comments=comments, user_id=user_id, saved=saved, save_count=save_count, id=id)


@app.route('/save_comment/<int:id>', methods=['POST', 'GET'])
def save_comment(id):
    if request.method == 'POST':
        comment = request.form['comment']
        user_id = session.get('id')
        current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO comment (comment_content, comment_datetime, user_id, fa_id) VALUES (%s, %s, %s, %s)", (comment, current_datetime, user_id, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('contentPage', id=id))
    else:
        return redirect(url_for('contentPage', id=id))


@app.route('/toggle_save/<int:id>', methods=['POST'])
def toggle_save(id):
    if request.method == 'POST':
        user_id = session.get('id')
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM save_procedure WHERE fa_id = %s AND user_id = %s", (id, user_id))
        saved = cur.fetchone()

        if saved:
            cur.execute("DELETE FROM save_procedure WHERE user_id = %s AND fa_id = %s", (user_id, id))
        else:
            cur.execute("INSERT INTO save_procedure (fa_id, user_id) VALUES (%s, %s)", (id, user_id))

        mysql.connection.commit()
        cur.close()

    return redirect(url_for('contentPage', id=id))


def format_datetime(comment_datetime):
    current_time = datetime.now()
    comment_time = comment_datetime  

    time_difference = current_time - comment_time

    if time_difference < timedelta(minutes=1):
        return 'Just now'
    elif time_difference < timedelta(hours=1):
        minutes = int(time_difference.total_seconds() / 60)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif time_difference < timedelta(days=1):
        hours = int(time_difference.total_seconds() / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif time_difference < timedelta(days=30):
        days = int(time_difference.total_seconds() / (24 * 3600))
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        return comment_time.strftime('%Y-%m-%d %H:%M:%S')

app.jinja_env.globals.update(format_datetime=format_datetime)


@app.route("/saved_procedure")
def saved_procedure():
    user_id = session.get('id')
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cur.execute("SELECT * FROM save_procedure LEFT JOIN first_aid_title ON first_aid_title.fa_id = save_procedure.fa_id WHERE user_id = %s", (user_id,))
    saved_procedures = cur.fetchall()
    cur.close()

    return render_template('savedProcedure.html', user_id=user_id, saved_procedures=saved_procedures)


@app.route("/send_help")
def sendHelp():
    return render_template('sendHelp.html')


if __name__ == "__main__":
    app.run(debug=True)