function checkAndValidatePassword() {
    var isPasswordValid = checkPassword();
    var doPasswordsMatch = validatePassword();
    
    return isPasswordValid && doPasswordsMatch;
}

function checkPassword() {
    var password = document.getElementById('password').value;
    var passwordMessage = document.getElementById('message2');

    var hasNumber = /\d/;
    var hasUppercase = /[A-Z]/;
    var hasLowercase = /[a-z]/;

    if (password.length >= 8 && hasNumber.test(password) && hasUppercase.test(password) && hasLowercase.test(password)) {
        passwordMessage.textContent = 'Password is in the correct format';
        passwordMessage.style.color = 'green';
        return true;
    } else {
        passwordMessage.textContent = 'Password must contain at least one number and one uppercase and lowercase letter, and at least 8 or more characters';
        passwordMessage.style.color = 'red';
        return false;
    }
}

function validatePassword() {
    var pass = document.getElementById('password').value;
    var confirm_pass = document.getElementById('confPass').value;
    if (pass != confirm_pass) {
        document.getElementById('message1').style.color = 'red';
        document.getElementById('message1').innerHTML
        = 'Use same password';
        document.getElementById('message1').disabled = true;
        return false;
    } else {
        document.getElementById('message1').style.color = 'green';
        document.getElementById('message1').innerHTML =
            'Password Matched';
        document.getElementById('message1').disabled = false;
        return true;
    }
}

