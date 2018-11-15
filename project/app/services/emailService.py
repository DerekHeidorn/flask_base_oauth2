import os
import smtplib

from email.message import EmailMessage
from email.headerregistry import Address


def send_reset_password_email(user_formatted_name, user_email, reset_code, reset_url):
    script_dir = os.path.dirname(__file__)
    txt_rel_path = 'email/templates/reset_password.txt'
    txt_abs_file_path = os.path.join(script_dir, txt_rel_path)

    html_rel_path = 'email/templates/reset_password.html'
    html_abs_file_path = os.path.join(script_dir, html_rel_path)

    with open(txt_abs_file_path, 'r') as txt_file:
        txt_data = txt_file.read()
    txt_file.close()

    with open(html_abs_file_path, 'r') as html_file:
        html_data = html_file.read()
    html_file.close()

    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Reset Password"
    msg['From'] = Address('Company Team', "contact", "mycompany.com")
    msg['To'] = (Address(user_email, "penelope", "example.com"))
    msg.set_content(txt_data.format(formatted_name=user_formatted_name, reset_password_link=reset_url))
    msg.add_alternative(html_data.format(formatted_name=user_formatted_name,
                                         reset_password_link=reset_url,
                                         reset_password_code=reset_code), subtype='html')

    # Send the message via local SMTP server.
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
