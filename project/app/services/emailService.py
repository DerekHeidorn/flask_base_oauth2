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

    splitted_email = user_email.split("@")
    email_username = splitted_email[0]
    email_domain = splitted_email[1]

    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Reset Password"
    msg['From'] = Address('Company Team', "contact", "mycompany.com")
    msg['To'] = (Address(user_email, email_username, email_domain))
    msg.set_content(txt_data.format(formatted_name=user_formatted_name,
                                    reset_password_link=reset_url,
                                    reset_password_code=reset_code))
    msg.add_alternative(html_data.format(formatted_name=user_formatted_name,
                                         reset_password_link=reset_url,
                                         reset_password_code=reset_code), subtype='html')

    # Send the message via local SMTP server.
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)


def send_reactivate_email(user_formatted_name, user_email, reactivate_code, reactivate_url):
    script_dir = os.path.dirname(__file__)
    txt_rel_path = 'email/templates/reactivate.txt'
    txt_abs_file_path = os.path.join(script_dir, txt_rel_path)

    html_rel_path = 'email/templates/reactivate.html'
    html_abs_file_path = os.path.join(script_dir, html_rel_path)

    with open(txt_abs_file_path, 'r') as txt_file:
        txt_data = txt_file.read()
    txt_file.close()

    with open(html_abs_file_path, 'r') as html_file:
        html_data = html_file.read()
    html_file.close()

    splitted_email = user_email.split("@")
    email_username = splitted_email[0]
    email_domain = splitted_email[1]

    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Reactivate Account"
    msg['From'] = Address('Company Team', "contact", "mycompany.com")
    msg['To'] = (Address(user_email, email_username, email_domain))
    msg.set_content(txt_data.format(formatted_name=user_formatted_name,
                                    reactivate_link=reactivate_url,
                                    reactivate_code=reactivate_code))
    msg.add_alternative(html_data.format(formatted_name=user_formatted_name,
                                         reactivate_link=reactivate_url,
                                         reactivate_code=reactivate_code), subtype='html')

    # Send the message via local SMTP server.
    with smtplib.SMTP('localhost') as s:
        s.send_message(msg)
