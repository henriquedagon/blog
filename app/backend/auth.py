import jwt
import datetime
import pandas as pd
from flask import current_app as app
from cryptography.fernet import Fernet, InvalidToken
import json
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def encode_auth_token(system, user, password, group):
    """
    Generates the Auth Token
    :return: string
    """
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'iat': datetime.datetime.utcnow(),
        'sys': system,
        'usr': user,
        'psw': password,
        'grp': group
    }
    return jwt.encode(
        payload,
        config['DEFAULT']['SECRET_KEY'],
        algorithm='HS256'
    ).decode()


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token (str):
    :return: integer|string
    """
    payload = jwt.decode(auth_token.encode(), config['DEFAULT']['SECRET_KEY'])
    return {
            'sys': payload['sys'],
            'usr': payload['usr'],
            'psw': payload['psw'],
            'grp': payload['grp']
            }


def encrypt(msg):
    key = config['DEFAULT']['SECRET_KEY'].encode() #Fernet.generate_key()
    cipher_suite = Fernet(key)
    cipher_text = cipher_suite.encrypt(msg.encode())
    return cipher_text.decode()


def decrypt(cipher_text):
    try:
        key = config['DEFAULT']['SECRET_KEY'].encode()
    except Exception as e:
        raise e
    cipher_suite = Fernet(key)
    plain_text = cipher_suite.decrypt(cipher_text.encode())
    if (datetime.datetime.now() 
                - pd.to_datetime(json.loads(plain_text)['tme'], dayfirst=True) 
                            > datetime.timedelta(days=1)):
        raise InvalidToken
    return plain_text.decode()


def get_token(credentials):
    call = eval(decrypt(credentials))
    print(json.loads(decrypt(credentials)))
    jwt_token = encode_auth_token( call['sys'], call['usr'], call['psw'], call['grp'])
    return jwt_token


# json.dumps({'sys': 'blog', 'usr': 'administrador', 'psw': '12345', 'grp': '2', 'tme': str(pd.to_datetime('now'))})
