import smtplib 
from email.message import EmailMessage 

def enviar(email_destino,mensaje):
    email_origen=""
    password=""
    email = EmailMessage()
    email["From"] = email_origen
    email["To"] = email_destino
    email["Subject"] = "Codigo de Activacion"
    email.set_content(mensaje)

    # Send Email
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(email_origen, password)
    smtp.sendmail(email_origen, email_destino, email.as_string())
    smtp.quit()