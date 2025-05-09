import smtplib
from email.mime.text import MIMEText

sender = "Frentdenis1997@gmail.com"
receiver = "Frentdenis1997@gmail.com"
subject = "Test alertă"
body = "Acesta este un test pentru verificarea trimiterii emailurilor din aplicație."

msg = MIMEText(body)
msg["Subject"] = subject
msg["From"] = sender
msg["To"] = receiver

try:
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "czgtczhfxyrjrdwc")
        server.send_message(msg)
        print("Email trimis cu succes!")
except Exception as e:
    print("Eroare la trimiterea emailului:", e)
