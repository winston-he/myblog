#!/usr/bin/env python
# encoding: utf-8
'''
@Author: winston he
@Email: winston.wz.he@gmail.com
@File: utils.py
@Time: 2020/5/3 16:37
'''
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.exc import BadSignature, SignatureExpired


def generate_token(obj) -> str:
    s = Serializer('secret-key', expires_in=3600 * 24)
    return s.dumps(obj).decode("utf-8")


def load_token(token: str):
    '''
    '-1' and '-2' cannot be the serialized content as they serve as error code here.
    :param token:
    :return:
    '''
    s = Serializer('secret-key', expires_in=3600 * 24)
    try:
        obj = s.loads(token)
    except SignatureExpired:
        return -1
    except BadSignature:
        return -2
    return obj
