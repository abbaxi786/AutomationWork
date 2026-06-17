import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# userName: abbasinabeelahmed58@gmail.com
# password: rrjo zmfv jmuc yejw


class Email:

    def __init__(self, taskName, taskType, receiver, subject, message):
        self.taskName = taskName
        self.taskType = taskType
        self.receiver = receiver
        self.subject = subject
        self.message = message
        self.sender_email = "abbasinabeelahmed58@gmail.com"
        self.app_password = "rixymkqrdvjgqdml"

    def send_email(self):

        msg = MIMEMultipart()
        msg["From"] = self.sender_email
        msg["To"] = self.receiver
        msg["Subject"] = self.subject

        msg.attach(MIMEText(self.message, "plain"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()

            server.login(self.sender_email, self.app_password)

            server.sendmail(
                self.sender_email,
                self.receiver,
                msg.as_string()
            )

            server.quit()

            print("Email sent successfully")

        except Exception as e:
            print("Error sending email:", e)