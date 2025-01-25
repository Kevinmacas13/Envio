import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def orden_mail():
    smtp_server = "webmail.devzone.ec"  # Verifica que este sea el servidor correcto
    port = 465  # Asegúrate de que el puerto es correcto para SSL
    correo = "kevin.macas@devzone.ec"
    password = "-Kevin7-#1992"

    # Datos del correo
    destinatario = ["alexandermacash@gmail.com"]
    asunto = "Orden Registrada"
    nombre = "KEVIN"

    # Crear el mensaje de correo
    mensaje = MIMEMultipart("mixed")
    mensaje["From"] = "KEVIN MACAS <kevin.macas@devzone.ec>"
    mensaje["To"] = ", ".join(destinatario)
    mensaje["Subject"] = asunto

    # Contenido del correo
    texto = f"Hola {nombre},\n\nSe ha registrado una nueva orden.\n\nSaludos,\nEquipo PRINDELA"
    mensaje.attach(MIMEText(texto, "plain"))

    try:
        print("Estableciendo conexión con el servidor SMTP...")
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            print("Conectado al servidor SMTP.")
            server.login(correo, password)
            print("Inicio de sesión exitoso.")
            server.sendmail(correo, destinatario, mensaje.as_string())
            print("Correo enviado exitosamente.")
    except smtplib.SMTPConnectError:
        print("Error: No se pudo conectar al servidor SMTP.")
    except smtplib.SMTPAuthenticationError:
        print("Error: Fallo en la autenticación. Verifica el usuario y la contraseña.")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")


orden_mail()
