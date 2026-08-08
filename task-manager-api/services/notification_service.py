import smtplib
from datetime import datetime, timezone
from config import Config

class NotificationService:
    def __init__(self, host=None, port=None, user=None, password=None):
        self.email_host = host or Config.SMTP_HOST
        self.email_port = port or Config.SMTP_PORT
        self.email_user = user or Config.SMTP_USER
        self.email_password = password or Config.SMTP_PASSWORD

    def send_email(self, to: str, subject: str, body: str) -> bool:
        if not self.email_user or not self.email_password:
            # Mock or log when SMTP credentials are not configured
            print(f"[NOTIFICATION] Mock Email sent to {to} | Subject: {subject}")
            return True
        try:
            server = smtplib.SMTP(self.email_host, self.email_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            message = f"Subject: {subject}\n\n{body}"
            server.sendmail(self.email_user, to, message)
            server.quit()
            print(f"[NOTIFICATION] Email sent to {to}")
            return True
        except Exception as e:
            print(f"[NOTIFICATION ERROR] Failed to send email to {to}: {str(e)}")
            return False

    def notify_task_assigned(self, user, task):
        subject = f"Nova task atribuída: {task.title}"
        body = f"Olá {user.name},\n\nA task '{task.title}' foi atribuída a você.\n\nPrioridade: {task.priority}\nStatus: {task.status}"
        return self.send_email(user.email, subject, body)

    def notify_task_overdue(self, user, task):
        subject = f"Task atrasada: {task.title}"
        body = f"Olá {user.name},\n\nA task '{task.title}' está atrasada!\n\nData limite: {task.due_date}"
        return self.send_email(user.email, subject, body)
