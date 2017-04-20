#!/usr/bin/env python
# -*- coding:utf8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def sendsms(phone, param_string, access_key_id, access_key_secret, template_code, sign_name):
    from datetime import datetime
    import uuid
    import requests

    url = 'https://sms.aliyuncs.com/'
    ts = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    once = str(uuid.uuid4())
    data = {
        'Action': 'SingleSendSms',
        'SignName': sign_name,
        'TemplateCode': template_code,
        'RecNum': phone,
        'ParamString': param_string,
        'Format': 'JSON',
        'Version': '2016-09-27',
        'AccessKeyId': access_key_id,
        'SignatureMethod': 'HMAC-SHA1',
        'Timestamp': ts,
        'SignatureVersion': '1.0',
        'SignatureNonce': once,
    }

    def __percent_encode(s):
        import urllib
        s = str(s)
        s = urllib.quote(s.decode('utf8').encode('utf8'), '')
        s = s.replace('+', '%20')
        s = s.replace('*', '%2A')
        s = s.replace('%7E', '~')
        return s

    def __gen_signature(data, req_method, secret):
        import hashlib
        import hmac
        import base64

        sorted_data = sorted(data, key=lambda v: v[0])
        vals = []
        for k, v in sorted_data:
            vals.append(__percent_encode(k) + '=' + __percent_encode(v))

        params = '&'.join(vals)
        string_to_sign = req_method + '&%2F&' + __percent_encode(params)
        key = secret + '&'
        signature = base64.encodestring(hmac.new(key, string_to_sign, hashlib.sha1).digest()).strip()
        return signature

    try:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        signature = __gen_signature(data.items(), 'POST', access_key_secret)
        data['Signature'] = signature

        r = requests.post(url, data=data, headers=headers)
        print r.text
    except Exception, e:
        print 'EXCEPT:', e


if __name__ == '__main__':
    pass
