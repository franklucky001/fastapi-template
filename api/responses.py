# -*- coding:utf-8 -*-
import json
from project_dummy.errors import SerializedException, ErrorFiled


def result(err_no, err_msg, data=None):
    result_body = {
        "code": err_no,
        "message": err_msg,
        "data": data
    }
    return result_body


def json_content(file_path):
    with open(file_path, 'r') as f:
        content = json.load(f)
    return content


def success(data=None, err_msg="成功"):
    return result(err_no=0, err_msg=err_msg, data=data)


def failed(err_msg):
    return result(err_no=1, err_msg=err_msg, data={})


def error(err_no, err_msg):
    return result(err_no=err_no, err_msg=err_msg)


def exception(error_field: ErrorField, exc: Exception):
    return SerializedException(error_field, exc)
