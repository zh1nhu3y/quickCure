# Quick Cure README

This README file provides guidance on how to run the code for Quick Cure. The project utilizes MySQL for the database, PHPMyAdmin for database management, and XAMPP as the local server environment. The web development components include HTML, JavaScript, and CSS. Additionally, it employs the Flask framework, Bootstrap, and Python for backend functionalities.

## Prerequisites

Before running the code, ensure you have the following installed:

- XAMPP: Download and install XAMPP from [here](https://www.apachefriends.org/index.html).
- Python: Download and install Python from [here](https://www.python.org/downloads/).
- MySQL: Install MySQL server and client from [here](https://dev.mysql.com/downloads/).
- PHPMyAdmin: PHPMyAdmin comes bundled with XAMPP. Ensure it's accessible through your XAMPP installation.

## Setup Instructions

1. **Clone the Repository:**
   Clone this repository to your local machine using the following command:

   ```bash
   git clone https://github.com/your_username/your_project.git
   ```

2. **Start XAMPP:**
   Launch XAMPP and start the Apache and MySQL services.

3. **Database Setup:**
   - Open PHPMyAdmin by navigating to `http://localhost/phpmyadmin` in your browser.
   - Create a new database named `quickcure`.
   - Import the provided SQL dump file (`database.sql`) into this database. The file can be found in the `database` directory of this repository.

4. **Python Environment Setup:**
   - Navigate to the project directory in your terminal.
   - Create a virtual environment (optional but recommended):

     ```bash
     python -m venv venv
     ```

   - Activate the virtual environment:

     - On Windows:

       ```bash
       venv\Scripts\activate
       ```

     - On macOS and Linux:

       ```bash
       source venv/bin/activate
       ```

   - Install the required Python packages:

     ```bash
     pip install -r requirements.txt
     ```

5. **Run the Application:**
   - Start the Flask server:

     ```bash
     python app.py
     ```

   - Access the application in your web browser at `http://localhost:5000`.

## Additional Notes

- Modify the database connection settings in the Python files (`config.py`, `app.py`) if necessary.
- Customize the frontend and backend code according to your requirements.
- For any issues or inquiries, please contact [panzhinhuey@gmail.com].