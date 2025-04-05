import smtplib
from email.mime.text import MIMEText
class SendEmailUseCase:
    def __init__(self, email,subject, body, to_email) :
        self.email = email
        self.subject = subject
        self.body = body
        self.to_email = to_email
        
    def execute(self):
        sender_email = "your_email@gmail.com"
        sender_password = "your_password"

        msg = MIMEText(self.body)
        msg["Subject"] = self.subject
        msg["From"] = sender_email
        msg["To"] = self.to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, self.to_email, msg.as_string())
            print("Email sent successfully!")