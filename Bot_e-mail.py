import smtplib
from email.mime.text import MIMEText

def trimite_email(subiect, mesaj, destinatar="Frentdenis1997@gmail.com"):
    expeditor = "adresa_ta@gmail.com"
    parola = "parola_ta_de_aplicatie"  # folosește parola generată, NU parola normală!

    msg = MIMEText(mesaj)
    msg["Subject"] = subiect
    msg["From"] = expeditor
    msg["To"] = destinatar

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(expeditor, parola)
        server.send_message(msg)
        server.quit()
        print("Email trimis cu succes!")
    except Exception as e:
        print(f"Eroare la trimiterea emailului: {e}")
