import smtplib


def send_email(
    yahoo_email: str,
    yahoo_app_password: str,
    subject: str,
    content: str,
    to: str) -> None:
    
    username = yahoo_email
    password = yahoo_app_password

    subject = f'Subject: {subject}\n\n'
    content = f'{content}\n\n'

    conn = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
    conn.ehlo()
    conn.login(username, password)
    conn.sendmail(yahoo_email,
                  to,
                  subject + content)

