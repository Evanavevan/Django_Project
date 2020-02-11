"""
支付工具类
"""
import base64
import hashlib
from datetime import datetime
import time
from random import Random
from urllib import parse

import OpenSSL
import requests
from alipay import AliPay
from bs4 import BeautifulSoup
from django.conf import settings


class _AliPay:
    """
    支付宝工具类
    """

    def __init__(self):
        self.alipay = AliPay(
            appid=settings.ALIPAY_APPID,  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_string=settings.APP_PRIVATE_KEY_STRING,
            alipay_public_key_string=settings.ALIPAY_PUBLIC_KEY_STRING,
            # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False
        )

    def pay(self, out_trade_no, total_amount, subject):
        try:
            order_string = self.alipay.api_alipay_trade_page_pay(
                out_trade_no=out_trade_no,  # 订单id
                total_amount=total_amount,  # 支付总金额
                subject=subject,
                return_url=None,
                notify_url=None  # 可选, 不填则使用默认notify url
            )
            return order_string
        except Exception as e:
            print(e)
            return None

    def check_pay(self, out_trade_no):
        # 调用支付宝的交易查询接口
        while True:
            response = self.alipay.api_alipay_trade_query(out_trade_no)

            # response = {
            #         "trade_no": "2017032121001004070200176844", # 支付宝交易号
            #         "code": "10000", # 接口调用是否成功
            #         "invoice_amount": "20.00",
            #         "open_id": "20880072506750308812798160715407",
            #         "fund_bill_list": [
            #             {
            #                 "amount": "20.00",
            #                 "fund_channel": "ALIPAYACCOUNT"
            #             }
            #         ],
            #         "buyer_logon_id": "csq***@sandbox.com",
            #         "send_pay_date": "2017-03-21 13:29:17",
            #         "receipt_amount": "20.00",
            #         "out_trade_no": "out_trade_no15",
            #         "buyer_pay_amount": "20.00",
            #         "buyer_user_id": "2088102169481075",
            #         "msg": "Success",
            #         "point_amount": "0.00",
            #         "trade_status": "TRADE_SUCCESS", # 支付结果
            #         "total_amount": "20.00"
            # }

            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                return True, trade_no
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # 等待买家付款
                # 业务处理失败，可能一会就会成功
                time.sleep(5)
                continue
            else:
                # 支付出错
                print(code)
                return


# https://blog.csdn.net/yulei_qq/article/details/45197543
class UnionPay:
    """
    银联支付接口（PC端）
    """
    def __init__(self, version=settings.VERSION, mer_id=settings.MER_ID, front_url=settings.FRONT_URL,
                 back_url=settings.BACK_URL, backend_url=settings.BACK_URL, cert_path=settings.CERT_URL,
                 debug=settings.UNION_DEBUG):
        self.version = version
        self.mer_id = mer_id
        self.front_url = front_url
        self.back_url = back_url
        self.backend_url = backend_url
        self.cert = {}
        self.cert_id = self.__get_cert_id(cert_path)

        if debug is True:
            # 支付网关
            self.gateway = "https://gateway.test.95516.com/gateway/api/frontTransReq.do"
            # 查询网关
            self.query_gateway = "https://gateway.test.95516.com/gateway/api/queryTrans.do"
        else:
            self.gateway = "https://gateway.95516.com/gateway/api/frontTransReq.do"
            self.query_gateway = "https://gateway.95516.com/gateway/api/queryTrans.do"

    def build_request_data(self, order_id, txn_amt, **kwargs):
        """
        构建请求数据
        :param order_id: 商户订单号
        :param txn_amt: 交易金额(单位: 分)
        :return:
        """
        request_data = {
            "version": self.version,  # 版本
            "encoding": "utf-8",  # 编码
            "txnType": "01",  # 交易类型  01：消费
            "txnSubType": "01",  # 交易子类  01：自助消费
            "bizType": "000201",  # 产品类型  000201：B2C网关支付
            "frontUrl": self.front_url,  # 前台通知地址
            "backUrl": self.back_url,  # 后台通知地址 需外网
            "signMethod": "01",  # 签名方法  01：RSA签名
            "channelType": "07",  # 渠道类型  07：互联网
            "accessType": "0",  # 接入类型  0：普通商户直连接入
            "currencyCode": "156",  # 交易币种  156：人民币
            "merId": self.mer_id,  # 商户代码
            "txnAmt": txn_amt,  # 订单金额(单位: 分)
            "txnTime": datetime.now().strftime("%Y%m%d%H%M%S"),  # 订单发送时间
            "certId": self.cert_id,
            "orderId": order_id,
            "signature": ""
        }
        request_data.update(**kwargs)
        self.get_sign(request_data)
        return request_data

    def pay_url(self, request_data):
        payment_url = "{}?{}".format(self.backend_url, parse.urlencode(request_data))
        return payment_url

    def pay_html(self, request_data):
        result = """<!DOCTYPE html>
                    <html lang="en">
                 <head>
                     <meta charset="UTF-8">
                 </head>
                 <body onload="document.forms[0].submit();">
                     <form id="pay_form" name="pay_form" action="%s" method="post">""" % self.gateway
        for key, value in request_data.items():
            result += """<input type="hidden" name="{0}" id="{0}" value="{1}"/>""".format(key, value)
        result = result + """</form></body></html>"""
        return result

    def get_sign(self, data):
        """
        获取签名
        :param data:
        :return:
        """
        sha256 = hashlib.sha256(self.build_sign_str(data).encode("utf-8")).hexdigest()
        private = OpenSSL.crypto.sign(self.cert["pkey"], sha256, "sha256")
        data["signature"] = str(base64.b64encode(private), encoding="utf-8")

    def verify_sign(self, data):
        """
        银联回调签名校验
        """
        signature = data.pop('signature')  # 获取签名
        link_string = self.build_sign_str(data)
        digest = hashlib.sha256(bytes(link_string, encoding="utf-8")).hexdigest()
        signature = base64.b64decode(signature)
        sign_pubkey_cert = data.get("signPubKeyCert", None)

        try:
            x509_ert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, sign_pubkey_cert)
            OpenSSL.crypto.verify(x509_ert, signature, digest, 'sha256')
            return True
        except Exception as e:
            print(e)
            return False

    def verify_query(self, order_num, txn_time):
        """
        验证查询的交易状态
        :param order_num: 订单号
        :param txn_time: 交易时间
        :return: True or False
        """
        request_data = {
            "version": self.version,
            "encoding": "utf-8",
            "txnType": "00",  # 00:查询
            "txnSubType": "00",
            "bizType": "000201",
            "signMethod": "01",  # 签名方法  01：RSA签名
            "accessType": "0",
            "merId": self.mer_id,
            "txnTime": txn_time,
            "orderId": order_num,
            "certId": self.cert_id,
        }

        self.get_sign(request_data)
        request_data['signature'] = parse.urlencode({'signature': request_data['signature']})[10:]
        req_string = self.build_sign_str(request_data)

        res = requests.post(
            url=self.query_gateway,
            data=req_string,
            headers={
                'content-type': 'application/x-www-form-urlencoded'
            }
        )
        if res.status_code != requests.codes.ok:
            query_status = False
        else:
            content = self.parse_arguments(res.content.decode('utf-8'))
            if content.get('origRespCode', '') == '00':
                query_status = True
            else:
                query_status = False
        return query_status

    def __get_cert_id(self, cert_path):
        """
        获取证书ID(签名KEY)
        :param cert_path:
        :return:
        """
        with open(cert_path, "rb") as f:
            certs = OpenSSL.crypto.load_pkcs12(f.read(), settings.CERT_PASSWORD)
            x509data = certs.get_certificate()
            self.cert["certid"] = x509data.get_serial_number()
            self.cert["pkey"] = certs.get_privatekey()

        return self.cert["certid"]

    @staticmethod
    def build_sign_str(data):
        """
        排序
        :param data:
        :return:
        """
        req = []
        for key in sorted(data.keys()):
            if data[key] != '':
                req.append("%s=%s" % (key, data[key]))

        return '&'.join(req)

    @staticmethod
    def parse_arguments(raw):
        """
        :param raw: raw data to parse argument
        :return:
        """
        data = {}
        qs_params = parse.parse_qs(str(raw))
        for name in qs_params.keys():
            data[name] = qs_params.get(name)[-1]
        return data


class WeixinPay:
    """
    微信支付
    """
    def __init__(self, app_id=settings.APP_ID, mch_id=settings.MCH_ID, create_ip=settings.CREATE_IP,
                 notify_url=settings.NOTIFY_URL, api_key=settings.WX_MCH_KEY, order_url=settings.ORDER_URL):
        self.app_id = app_id
        self.mch_id = mch_id
        self.create_ip = create_ip
        self.notify_url = notify_url
        self.api_key = api_key
        self.order_url = order_url

    def get_sign(self, data_dict, key):
        """
        签名函数
        :param data_dict: 需要签名的参数，格式为字典
        :param key: 密钥 ，即上面的API_KEY
        :return: 字符串
        """
        params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
        params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
        # 组织参数字符串并在末尾添加商户交易密钥
        md5 = hashlib.md5()  # 使用MD5加密模式
        md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
        sign = md5.hexdigest().upper()  # 完成加密并转为大写
        return sign

    def random_str(self, random_length=8):
        """
        生成随机字符串
        :param random_length: 字符串长度
        :return:
        """
        strs = ''
        chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
        length = len(chars) - 1
        random = Random()
        for i in range(random_length):
            strs += chars[random.randint(0, length)]
        return strs

    def trans_dict_to_xml(self, data_dict):
        """
        定义字典转XML的函数
        :param data_dict:
        :return:
        """
        data_xml = []
        for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
            v = data_dict.get(k)  # 取出字典中key对应的value
            if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
                v = v.encode('utf-8')
                v = '<![CDATA[{}]]>'.format(v)
            data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
        return '<xml>{}</xml>'.format(''.join(data_xml))  # 返回XML

    def trans_xml_to_dict(self, data_xml):
        """
        定义XML转字典的函数
        :param data_xml:
        :return:
        """
        soup = BeautifulSoup(data_xml, features='xml')
        xml = soup.find('xml')  # 解析XML
        if not xml:
            return {}
        data_dict = dict([(item.name, item.text) for item in xml.find_all()])
        return data_dict

    def pay(self, order_id, total_pay, subject):
        """
        支付主程序
        :param order_id: 订单id
        :param total_pay: 总金额
        :param subject: 描述
        :return:
        """
        nonce_str = self.random_str()  # 拼接出随机的字符串即可，我这里是用  时间+随机数字+5个随机字母

        params = {
            'appid': self.app_id,  # APPID
            'mch_id': self.mch_id,  # 商户号
            'nonce_str': nonce_str,  # 随机字符串
            'out_trade_no': order_id,  # 订单编号，可自定义
            'total_fee': total_pay,  # 订单总金额，单位是分，必须是整数
            'spbill_create_ip': self.create_ip,  # 自己服务器的IP地址
            'notify_url': self.notify_url,  # 回调地址，微信支付成功后会回调这个url，告知商户支付结果
            'body': '天天生鲜公司'.encode('utf-8'),  # 公司描述
            'detail': subject,  # 商品描述
            'trade_type': 'NATIVE',  # 扫码支付类型
        }

        sign = self.get_sign(params, self.api_key)  # 获取签名
        params['sign'] = sign  # 添加签名到参数字典
        xml = self.trans_dict_to_xml(params)  # 转换字典为XML
        # print(xml)
        response = requests.request('post', self.order_url, data=xml)  # 以POST方式向微信公众平台服务器发起请求
        data_dict = self.trans_xml_to_dict(response.content)  # 将请求返回的数据转为字典
        print(data_dict)
        return data_dict

    def notify(self, request):
        """
         微信支付成功后会自动回调
         返回参数为：
         {'mch_id': '',
         'time_end': '',
         'nonce_str': '',
         'out_trade_no': '',
         'trade_type': '',
         'openid': '',
         'return_code': '',
         'sign': '',
         'bank_type': '',
         'appid': '',
         'transaction_id': '',
         'cash_fee': '',
         'total_fee': '',
         'fee_type': '', '
         is_subscribe': '',
         'result_code': 'SUCCESS'}
        ​
         :param request:
         :return:
        """
        data_dict = self.trans_xml_to_dict(request.body)  # 回调数据转字典
        # print('支付回调结果', data_dict)
        sign = data_dict.pop('sign')  # 取出签名
        back_sign = self.get_sign(data_dict, self.api_key)  # 计算签名
        # 验证签名是否与回调签名相同
        if sign == back_sign and data_dict['return_code'] == 'SUCCESS':
            # 检查对应业务数据的状态，判断该通知是否已经处理过，如果没有处理过再进行处理，如果处理过直接返回结果成功。
            print('微信支付成功会回调！')
            # 处理支付成功逻辑
            # 返回接收结果给微信，否则微信会每隔8分钟发送post请求
            return self.trans_dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'})
        return self.trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'})
