import re
from classes.user import User
import random
import smtplib
from email.mime.text import MIMEText

class Model:
    def __init__(self):
        self.users = {}

    def create_account(self, username, email, password, phone_number):
        errors = []

        if username == "":
            errors.append(("Input something", "label_12"))

        if not self.validate_email(email):
            errors.append(("Invalid email", "label_14"))

        if not self.is_strong_password(password):
            errors.append(("Password is weak", "label_13"))

        if not self.is_valid_phone_number(phone_number):
            errors.append(("Invalid phone number", "label_15"))

        if errors:
            return {"success": False, "errors": errors}

        user = User(username, password, email, phone_number)
        self.users[username] = user
        return {"success": True, "message": "Account created successfully"}


    def is_strong_password(self, password):
        if len(password) < 8:
            return False
        if not any(char.isdigit() for char in password):
            return False
        if not any(char.isupper() for char in password):
            return False
        if not any(char.islower() for char in password):
            return False
        if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
            return False
        return True


    def validate_email(self, email):
        regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return True if re.match(regex, email) else False

    def len_of_username(self,username):
        return username[:7]

    def send_reset_password(self,email):
        reset_code = random.randint(1000, 9999)

        smtp_host = "smtp.gmail.com"
        smtp_port = 587
        sender_email = "argenwant@gmail.com"
        sender_password = "tlxalexdzizjjnld"

        subject = "Your Password Reset Code"
        body = f"Your password reset code is: {reset_code}"

        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email

        try:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email, msg.as_string())

            return reset_code
        except Exception as e:
            print("Error sending email:", e)
            return None

    def validate_date_format(self, date_str):
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%Y-%m-%d, %H:%M:%S")
            return True
        except ValueError:
            return False

    def is_valid_phone_number(self, phone_number):
        return re.match(r'^0\d{9}$', phone_number) is not None
