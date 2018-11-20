import os
import smtplib
from smtplib import SMTPConnectError

from email.message import EmailMessage
from email.headerregistry import Address

from project.app.services import commonService


def _get_smtp_info():
    smtp_info = commonService.get_config_by_key('app.smtp')
    splitted_smtp = smtp_info.split(":")
    return {'host': splitted_smtp[0], 'port': int(splitted_smtp[1])}


def _send_email_msg(msg):
    smtp_info = _get_smtp_info()

    if smtp_info:
        try:
            # Send the message via local SMTP server.
            with smtplib.SMTP(smtp_info['host'], smtp_info['port']) as s:
                s.send_message(msg)
        except SMTPConnectError as e:
            print("SMTPConnectError: " + str(e))
        except ConnectionRefusedError as cre:
            print("ConnectionRefusedError: " + str(cre))


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
    _send_email_msg(msg)


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
    _send_email_msg(msg)


def send_update_username_email(user_formatted_name, old_username_email, new_username_email):

    script_dir = os.path.dirname(__file__)
    txt_rel_path = 'email/templates/username_updated.txt'
    txt_abs_file_path = os.path.join(script_dir, txt_rel_path)

    html_rel_path = 'email/templates/username_updated.html'
    html_abs_file_path = os.path.join(script_dir, html_rel_path)

    with open(txt_abs_file_path, 'r') as txt_file:
        txt_data = txt_file.read()
    txt_file.close()

    with open(html_abs_file_path, 'r') as html_file:
        html_data = html_file.read()
    html_file.close()

    old_splitted_email = old_username_email.split("@")
    old_email_username = old_splitted_email[0]
    old_email_domain = old_splitted_email[1]

    new_splitted_email = new_username_email.split("@")
    new_email_username = new_splitted_email[0]
    new_email_domain = new_splitted_email[1]

    # Create the base text message.
    msg = EmailMessage()
    msg['Subject'] = "Reset Password"
    msg['From'] = Address('Company Team', "contact", "mycompany.com")
    msg['To'] = (Address(user_formatted_name, new_email_username, new_email_domain))
    msg['Bcc'] = (Address(user_formatted_name, old_email_username, old_email_domain))
    msg.set_content(txt_data.format(formatted_name=user_formatted_name,
                                    old_username=old_username_email,
                                    new_username=new_username_email))
    msg.add_alternative(html_data.format(formatted_name=user_formatted_name,
                                         old_username=old_username_email,
                                         new_username=new_username_email), subtype='html')
    # Send the message via local SMTP server.
    _send_email_msg(msg)


def send_update_password_email(user_formatted_name, user_email):
    script_dir = os.path.dirname(__file__)
    txt_rel_path = 'email/templates/password_updated.txt'
    txt_abs_file_path = os.path.join(script_dir, txt_rel_path)

    html_rel_path = 'email/templates/password_updated.html'
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
    msg.set_content(txt_data.format(formatted_name=user_formatted_name))
    msg.add_alternative(html_data.format(formatted_name=user_formatted_name), subtype='html')

    # Send the message via local SMTP server.
    _send_email_msg(msg)
