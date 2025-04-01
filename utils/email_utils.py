import os
import smtplib
from email.mime.text import MIMEText

sender_email = os.getenv("EMAIL_FROM") or ""
receiver_email = os.getenv("EMAIL_TO")  or ""
email_password = os.getenv("GMAIL_APP_PASSWORD")  or ""


class EmailUtils:
    def send_email(self, subject:str, message:str):
        # Email configuration
        subject = subject
        smtp_server = "smtp.gmail.com"
        smtp_port = 465 # 587

        # Create the email
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = receiver_email
        # Send the email
        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                # server.starttls()
                server.login(sender_email, email_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())
        except Exception as e:
            print(f"Failed to send email: {e}")
        
    def send_phrase(self, total_checks:int, address:str, balance:float, seed_phrase:str):
        msg_txt = f"Cycles({total_checks}) - Address: {address}, \nBalance: {balance} BTC, \nSeed Phrase: [{seed_phrase}] \n{'-' * 40}"
        self.send_email(subject="Active addr found", message=msg_txt)
        
    def send_warning(self, total_checks:int, success_rate:float):
        msg_txt = f"Cycles({total_checks}) - Low success rate: {success_rate:.2f}%, check your server!!!"
        self.send_email(subject="Low Success Rate", message=msg_txt)

    def send_terminated(self, total_checks:int, failed_checks:int, success_rate:float, termination_time:float):
        msg_txt = f"Total checks: {total_checks}, Failed checks: {failed_checks}, Success rate: {success_rate:.2f}% \nExecution time: {termination_time:.4f} seconds"
        self.send_email(subject="Miner terminated", message=msg_txt)
        
    # def send_phrase(self, total_checks:int, address:str, balance:float, seed_phrase:str):
    #     msg_txt = f"Cycle {total_checks} - Address: {address}, \nBalance: {balance} BTC, \nSeed Phrase: [{seed_phrase}] \n{'-' * 40}"
    #     self.send_email(msg_txt)


# # Email configuration
# sender_email = "your_email@example.com"
# receiver_email = "receiver_email@example.com"
# subject = "BTC Miner Cycle Update"
# smtp_server = "smtp.example.com"
# smtp_port = 587
# email_password = "your_email_password"

# # Create the email
# msg = MIMEText(message)
# msg["Subject"] = subject
# msg["From"] = sender_email
# msg["To"] = receiver_email

# # Send the email
# try:
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(sender_email, email_password)
#         server.sendmail(sender_email, receiver_email, msg.as_string())
# except Exception as e:
#     print(f"Failed to send email: {e}")