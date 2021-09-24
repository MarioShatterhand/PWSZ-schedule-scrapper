import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ssl
import os
from dotenv import load_dotenv

class Mail:
    def __init__(self) -> None:
        load_dotenv()
        self.port = 465  # For SSL
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = os.getenv("MAIL_ADDRESS")
        self.password = os.getenv("MAIL_PASSWORD")

    def send_mail(self, files, new_date=""):
        print(new_date)
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = self.smtp_server
        message["To"] = "mario.pierzchala@outlook.com"
        message["Subject"] = "Nowy harmonogram zajęć na PWSZ"
        # message["Bcc"] = receiver_email  # Recommended for mass emails

        # Add body to email
        message.attach(MIMEText(new_date))

        # filename = "document.pdf"  # In same directory as script
        for filename in files:
            # Open PDF file in binary mode
            with open(filename, "rb") as attachment:
                # Add file as application/octet-stream
                # Email client can usually download this automatically as attachment
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())

            # Encode file in ASCII characters to send by email
            encoders.encode_base64(part)

            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename}",
            )

            # Add attachment to message and convert message to string
            message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(self.sender_email, "mario.pierzchala@outlook.com", text)
