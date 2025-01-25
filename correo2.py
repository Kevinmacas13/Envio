import smtplib
import ssl

smtp_server = "mail.prindela.com"
port = 465
correo = "administrador@prindela.com"
password = "@dminps0506"

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(correo, password)
    print("Conexión exitosa al servidor SMTP.")
except Exception as e:
    print(f"Error al conectarse al servidor SMTP: {e}")
