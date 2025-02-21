import smtplib
from email.mime.text import MIMEText
from config import SMTP_SERVER, SMTP_PORT, SENDER_EMAIL, RECEIVER_EMAIL, EMAIL_PASSWORD

def send_alert(product, old_price, new_price, url):
    subject = f"Price Drop Alert for {product}!"
    body = f"The price for {product} has dropped from ${old_price} to ${new_price}!\nCheck it here: {url}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg["To"] = RECEIVER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, EMAIL_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        print(f"Alert sent for {product}!")
    except Exception as e:
        print(f"Failed to send email: {e}")
