import sys
import json
import hashlib
from datetime import datetime
from django.conf import settings

# 以下是兼容python2和python3的导入
if str(sys.version[0]) == "3":
    from urllib.parse import quote_plus
    from urllib.request import urlopen
else:
    from urllib import quote_plus
    from urllib2 import urlopen


class MESSAGE:
    def __init__(self, ):
        self.app_key = settings.MES_APPKEY
        self.MES_SECRET = settings.MES_SECRET
        self.AliDAYUGateway = settings.MES_URL

    def __ordered_data(self, data):
        """
        对参数的参数做排序处理的，不用关心
        """
        complex_keys = []
        for key, value in data.items():
            if isinstance(value, dict):
                complex_keys.append(key)

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, parameters):
        unsign_par = "{0}{1}{0}".format(self.MES_SECRET, parameters)
        sign = hashlib.md5(unsign_par.encode("utf8")).hexdigest().upper()
        return sign

    def SMS_SEND(self):
        self.method = "alibaba.aliqin.fc.sms.num.send"
        sys_parameters = {
            'app_key': self.app_key,
            'sign_method': self.sign_method,
            'method': self.method,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'v': '2.0',
            'format': 'json',
            'extend': self.extend,
            'sms_type': self.sms_type,
            'sms_free_sign_name': self.sms_free_sign_name,
            'sms_param': self.sms_param,
            'rec_num': self.rec_num,
            'sms_template_code': self.sms_template_code,
        }
        unsigned_items = self.__ordered_data(sys_parameters)
        unsigned_string = "".join("{}{}".format(k, v) for k, v in unsigned_items)
        sign = self.sign(unsigned_string)
        quoted_string = "&".join("{}={}".format(k, quote_plus(v)) for k, v in unsigned_items)
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        url = self.AliDAYUGateway + "?" + signed_string
        r = urlopen(url)
        print(r.read().decode("utf-8"))

if __name__ == "__main__":
    req = MESSAGE()
    req.extend = ""
    req.sms_type = "normal"
    self.sign_method = "md5"
    req.sms_free_sign_name = "test"
    req.sms_param = {"xxx": "test"}
    req.rec_num = "xxxxxx"
    req.sms_template_code = "SMS_5xxxx"
    req.SMS_SEND()
