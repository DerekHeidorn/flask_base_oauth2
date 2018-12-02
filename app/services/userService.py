import uuid
import time
import hashlib
from datetime import datetime
from app.models.user import User
from app.persist import baseDao, userDao, securityDao, oauth2Dao
from app.services import emailService, encryptionService, commonService
from app.services.utils import userUtils


def is_user_valid(username, password):
    user = userDao.get_user_by_username(username)
    if user is not None:
        return userUtils.is_user_valid(user, password)
    else:
        return False


def delete_user(user_id):
    return userDao.delete_user(user_id)


def update_user_names(user_uuid, first_name, last_name):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session=session)
    if user is None:
        return None

    user.first_name = first_name
    user.last_name = last_name

    session.commit()

    return user


def update_user_private_fl(user_uuid, is_private):
    session = baseDao.get_session()

    user = userDao.get_user_by_uuid(user_uuid, session=session)
    if user is None:
        return None

    user.is_private = is_private

    session.commit()

    return user


def update_user(user_id, user_to_be_updated):
    updated_user = None
    session = baseDao.get_session()

    user = userDao.get_user_by_id(user_id, session=session)
    if user is None:
        return updated_user

    user.first_name = user_to_be_updated["first_name"]
    user.last_name = user_to_be_updated["last_name"]
    user.username = user_to_be_updated["username"]

    session.commit()
    updated_user = userDao.get_user_by_id(user_id)

    return updated_user


def get_public_users():
    return userDao.get_public_users()


def get_users():
    return userDao.get_users()


def get_user_by_id(user_id):
    return userDao.get_user_by_id(user_id)


def get_user_by_username(username):
    return userDao.get_user_by_username(username)


def get_user_by_uuid(user_uuid):
    return userDao.get_user_by_uuid(user_uuid)


def get_users_by_uuid_list(user_uuid_list):

    session = baseDao.get_session()
    users = []

    for u in user_uuid_list:
        user = userDao.get_user_by_uuid(u, session)
        users.append(user)

    return users


def is_username_unique(username, exclude_user_id=None):
    return userDao.is_username_unique(username, exclude_user_id)


def is_alias_unique(alias, exclude_user_id=None):
    return userDao.is_alias_unique(alias, exclude_user_id)


def get_user_by_username_and_validate(username, password):
    user = userDao.get_user_by_username(username)
    if user is not None:
        return {"user": user, "is_password_valid": userUtils.is_user_valid(user, password)}
    else:
        return {"user": None, "is_password_valid": False}


def add_public_user(client_id, alias, username, password, first_name=None, last_name=None):

    session = baseDao.get_session()
    security_group = securityDao.get_security_group_by_name(securityDao.SECURITY_GROUP_CUSTOMER_NAME,
                                                            session=session)

    oauth2_client = oauth2Dao.query_client(client_id, session=session)

    new_user = User()
    new_user.created_ts = datetime.now()
    new_user.first_name = first_name
    new_user.last_name = last_name
    new_user.username = username
    new_user.alias = alias
    new_user.user_uuid = uuid.uuid4()
    new_user.status_cd = 'A'
    new_user.type_cd = 'C'
    new_user.is_private = True
    new_user.failed_attempt_count = 0
    new_user.private_key = userUtils.random_user_private_key(32)
    new_user.password_salt = userUtils.random_user_private_key(32)
    new_user.password_hash = userUtils.get_hashed_password(password, new_user.password_salt)

    new_user.security_groups.append(security_group)
    new_user.oauth2_clients.append(oauth2_client)
    user_id = userDao.add_user(new_user, session=session)
    if user_id:
        return userDao.get_user_by_id(user_id)
    else:
        return None


def reset_user_password(username):
    # get the base url
    base_url = commonService.get_config_by_key('app.base_url')

    # create a new session
    session = baseDao.get_session()

    # get the current user
    user = userDao.get_user_by_username(username, session)
    user_formatted_name = user.get_formatted_name()

    # if a reset code doesn't exist, create it.
    if user.reset_code is None:
        user.reset_code = userUtils.random_user_private_key(32)
        userDao.update_user(user, session)

    # new code is encrypted using the user's private key
    encrypted_reset_code = encryptionService.encrypt_string(user.reset_code, user.private_key)

    reset_info = {'username': user.username, 'code': encrypted_reset_code}
    encrypted_reset_info = encryptionService.encrypt_dictionary_with_base64(reset_info)

    # used for informational only, it'll show up in the error logs at the web layer if 500 error happens
    epoch_time = int(time.time())
    time_string = str(epoch_time)

    # used for informational only, simple hashCode to compare if the encrypted values have been changed the user
    reset_digest = hashlib.md5(encrypted_reset_info.encode()).hexdigest()

    print("base_url=" + str(base_url))
    print("time_string=" + str(time_string))
    print("reset_digest=" + str(reset_digest))
    print("encrypted_reset_info=" + str(encrypted_reset_info))
    reset_url = base_url + '/reset?e=' + encrypted_reset_info + '&t=' + time_string + '&h=' + reset_digest

    # email to the user
    emailService.send_reset_password_email(user_formatted_name, user.username, user.reset_code, reset_url)

    return user.reset_code


def process_reset_user_password(encrypted_reset_info):
    reset_info = encryptionService.decrypt_dictionary_with_base64(encrypted_reset_info)

    if 'username' in reset_info and 'code' in reset_info:
        # create a new session
        session = baseDao.get_session()

        user = userDao.get_user_by_username(reset_info['username'], session)
        reset_code = encryptionService.decrypt_string(reset_info['code'], user.private_key)

        if user.reset_code == reset_code:
            return reset_code

    return None


def complete_reset_user_password(username, password, user_reset_code):

    # create a new session
    session = baseDao.get_session()

    user = userDao.get_user_by_username(username, session)

    if user.reset_code == user_reset_code:

        # set the user to active
        user.status_cd = 'A'

        # reset the failed attempts
        user.failed_attempt_count = 0

        # create a new salt
        user.password_salt = userUtils.random_user_private_key(32)

        # create a new hash
        user.password_hash = userUtils.get_hashed_password(password, user.password_salt)

        # reset the code
        user.reset_code = None

        userDao.update_user(user, session)

        # send an email about the password changed
        emailService.send_update_password_email(user.get_formatted_name(), user.username)


def deactivate_account(user_id):
    # get the base url
    base_url = commonService.get_config_by_key('app.base_url')

    # create a new session
    session = baseDao.get_session()

    user = userDao.get_user_by_id(user_id, session)

    if user.activation_code is None or user.status_cd == 'A':

        # set the user to inactive
        user.status_cd = 'I'

        # reset the code
        if user.activation_code is None:
            user.activation_code = userUtils.random_user_private_key(32)

        userDao.update_user(user, session)

        user_formatted_name = user.get_formatted_name()

        # new code is encrypted using the user's private key
        encrypted_activation_code = encryptionService.encrypt_string(user.activation_code, user.private_key)

        reset_info = {'username': user.username, 'code': encrypted_activation_code}
        encrypted_activation_info = encryptionService.encrypt_dictionary_with_base64(reset_info)

        # used for informational only, it'll show up in the error logs at the web layer if 500 error happens
        epoch_time = int(time.time())
        time_string = str(epoch_time)

        # used for informational only, simple hashCode to compare if the encrypted values have been changed the user
        reset_digest = hashlib.md5(encrypted_activation_info.encode()).hexdigest()

        reactivate_url = base_url + '/reactivate?e=' + encrypted_activation_info \
                                  + '&t=' + time_string + '&h=' + reset_digest

        emailService.send_reactivate_email(user_formatted_name, user.username, user.activation_code, reactivate_url)


def process_reactivate_account(encrypted_account_info):
    reactivate_info = encryptionService.decrypt_dictionary_with_base64(encrypted_account_info)

    if 'username' in reactivate_info and 'code' in reactivate_info:
        # create a new session
        session = baseDao.get_session()

        user = userDao.get_user_by_username(reactivate_info['username'], session)
        reactivate_code = encryptionService.decrypt_string(reactivate_info['code'], user.private_key)

        if user.activation_code == reactivate_code:
            return reactivate_code

    return None


def complete_reactivate_account(username, reactivate_code):

    # create a new session
    session = baseDao.get_session()

    user = userDao.get_user_by_username(username, session)

    if user.activation_code == reactivate_code:

        # set the user to active
        user.status_cd = 'A'

        # reset the failed attempts
        user.failed_attempt_count = 0

        # reset the code
        user.activation_code = None

        userDao.update_user(user, session)


def update_username_with_required_password(user_id, new_username, password):
    # create a new session
    session = baseDao.get_session()

    user = userDao.get_user_by_id(user_id, session)
    if user:
        if user.username.lower() != new_username.lower():
            if userUtils.is_user_valid(user, password):
                user.username = new_username.lower()
                userDao.update_user(user, session)

                # send an email to the user about the change
                emailService.send_update_username_email(user.get_formatted_name(), user.username, new_username)

                return user
            else:
                raise Exception('password is invalid')
        else:
            raise Exception('Username is the same')
    else:
        raise Exception('No user found by username')


def update_user_password(user_id, old_password, new_password):
    # create a new session
    session = baseDao.get_session()

    user = userDao.get_user_by_id(user_id, session)
    if user:
        if userUtils.is_user_valid(user, old_password):
            # reset the failed attempts
            user.failed_attempt_count = 0

            # create a new salt
            user.password_salt = userUtils.random_user_private_key(32)

            # create a new hash
            user.password_hash = userUtils.get_hashed_password(new_password, user.password_salt)

            userDao.update_user(user, session)

            # send an email to the user about the change
            emailService.send_update_password_email(user.get_formatted_name(), user.username)
        else:
            raise Exception('Password is invalid')
    else:
        raise Exception('No user found')
