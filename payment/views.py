import base64
import hashlib
import json
from django.shortcuts import render
from rest_framework.views import APIView
import requests
from Crypto.Cipher import DES3
from rest_framework.response import Response
from rest_framework import status


# Flutter wave integration code #

class PaymentGateWay(object):
    """this is the getKey function that generates an encryption Key for you by passing your Secret Key as a
    parameter. """

    def __init__(self):
        pass

    def getKey(self, secret_key):
        hashed_sec_key = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
        hashed_sec_key_last12 = hashed_sec_key[-12:]
        sec_key_adjusted = secret_key.replace('FLWSECK-', '')
        sec_key_adjusted_first12 = sec_key_adjusted[:12]
        return sec_key_adjusted_first12 + hashed_sec_key_last12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""

    def encryptData(self, key, plain_text):
        block_size = 8
        pad_diff = block_size - (len(plain_text) % block_size)
        cipher = DES3.new(key, DES3.MODE_ECB)
        plain_text = "{}{}".format(plain_text, "".join(chr(pad_diff) * pad_diff))
        # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte
        # strings, hence the need for the conversion below
        test = plain_text.encode('utf-8')
        encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
        return encrypted

    def pay_via_card(self):
        # pub_key = "FLWPUBK_TEST-dada39fd560b01abd22ff26c56579ac5-X"
        pub_key = "FLWPUBK-59e436ff1d3d434836cd995064541437-X"
        # data = {
        #     'PBFPubKey': pub_key,
        #     # "cardno": "4187622708990799",
        #     "cardno": "4833160207804037",
        #     # "cvv": "211",
        #     "cvv": "197",
        #     # "expirymonth": "11",
        #     # "expiryyear": "21",
        #     "expirymonth": "02",
        #     "expiryyear": "25",
        #     "currency": "USD",
        #     "country": "US",
        #     # 'suggested_auth': 'pin',
        #     # 'pin': '3310',
        #     "amount": "4.3408",
        #     'txRef': 'MC-TESTREF-1234',
        #     "email": "nminuifuong@bongalo.co",
        #     "phonenumber": "+250783190311",
        #     "firstname": "Nghombombong",
        #     "lastname": "Minuifuong",
        #     # "IP": "355426087298442",
        #     # "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
        # }
        data = {

                "PBFPubKey": pub_key,
                "cardno": "4833160207804037",
                "cvv": "197",
                "expirymonth": "02",
                "expiryyear": "25",
                "currency": "USD",
                "country": "US",
                "amount": "4",
                "email": "nminuifuong@bongalo.co",
                "phonenumber": "+250783190311",
                "firstname": "Nghombombong",
                "lastname": "Minuifuong",
                # "IP": "355426087298442",
                'txRef': 'MC-TESTREF-1234',
                # "meta": [{metaname: "flightID", metavalue: "123949494DC"}],
                "suggested_auth": "NOAUTH_INTERNATIONAL",
                "billingzip": "94102",
                "billingcity": "San Francisco",
                "billingaddress": "16 Turk Street",
                "billingstate": "California",
                "billingcountry": "US",
                # "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
                # "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"

        }

        # sec_key = 'FLWSECK_TEST-87f10137771e46086ffd9ecc06188572-X'
        sec_key = 'FLWSECK-7a06d9a2d7d8c798ebe7dda9b6a63ff6-X'

        # hash the secret key with the get hashed key function
        hashed_sec_key = self.getKey(sec_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

        encrypt_3DES_key = self.encryptData(hashed_sec_key, json.dumps(data))

        # payment payload
        payload = {
            "PBFPubKey": pub_key,
            "client": encrypt_3DES_key,
            "alg": "3DES-24"
        }

        # card charge endpoint
        # endpoint = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/charge"
        endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/charge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        print(response.json())
        return response.json()

    def pay_mobile_money(self, locale):
        pub_key = "FLWPUBK-59e436ff1d3d434836cd995064541437-X"
        if locale == "rw":
            data = {
              "PBFPubKey": pub_key,
              "currency": "RWF",
              "payment_type": "mobilemoneygh",
              "country": "NG",
              "amount": "50",
              "email": "user@example.com",
              "phonenumber": "054709929220",
              "network": "RWF",
              "firstname": "temi",
              "lastname": "desola",
              # "IP": "355426087298442",
              "txRef": "MC-",
              "orderRef": "MC_",
              "is_mobile_money_gh": 1,
              "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
              "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
            }

        elif locale == "franco":
            data = {
              "PBFPubKey": pub_key,
              "currency": "XAF",
              "country": "NG",
              "payment_type": "mobilemoneyfranco",
              "amount": "100",
              "email": "user@example.com",
              "phonenumber": "+237654112668",
              "firstname": "temi",
              "lastname": "desola",
              "IP": "355426087298442",
              "txRef": "MC-HADFJKH",
              "orderRef": "MC_JHDFSVHJSV",
              "is_mobile_money_franco": 1,
              # "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
            }
        elif locale == "ghana":
            data = {
              "PBFPubKey": pub_key,
              "currency": "GHS",
              "payment_type": "mobilemoneygh",
              "country": "GH",
              "amount": "50",
              "email": "user@example.com",
              "phonenumber": "054709929220",
              "network": "MTN",
              "firstname": "temi",
              "lastname": "desola",
              "voucher": "128373",
              "IP": "355426087298442",
              "txRef": "MC-",
              "orderRef": "MC_",
              "is_mobile_money_gh": 1,
              "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
              "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
            }
        elif locale == "mpesa":
            data = {
                "PBFPubKey": pub_key,
                "currency": "KES",
                "country": "KE",
                "amount": "100",
                "phonenumber": "0926420185",
                "email": "user@exampe",
                "firstname": "jsksk",
                "lastname": "ioeoe",
                "IP": "40.14.290",
                "narration": "funds payment",
                "txRef": "jw-222",
                # "meta": [{metaname: "extra info", metavalue: "a pie"}],
                "device_fingerprint": "89191918hgdgdg99191", #(optional)
                "payment_type": "mpesa",
                "is_mpesa": "1",
                "is_mpesa_lipa": 1
            }
        elif locale == "uganda":
            data = {
              "PBFPubKey": pub_key,
              "currency": "UGX",
              "payment_type": "mobilemoneyuganda",
              "country": "NG",
              "amount": "50",
              "email": "user@example.com",
              "phonenumber": "054709929220",
              "network": "UGX",
              "firstname": "temi",
              "lastname": "desola",
              "IP": "355426087298442",
              "txRef": "MC-",
              "orderRef": "MC_",
              "is_mobile_money_ug": 1,
              "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
              "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
            }
        elif locale == "zambia":
            data = {
              "PBFPubKey": pub_key,
              "currency": "ZMW",
              "payment_type": "mobilemoneyzambia",
              "country": "NG",
              "amount": "50",
              "email": "user@example.com",
              "phonenumber": "054709929220",
              "network": "MTN",
              "firstname": "temi",
              "lastname": "desola",
              "IP": "355426087298442",
              "txRef": "MC-",
              "orderRef": "MC_",
              "is_mobile_money_ug": 1,
              "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
              "device_fingerprint": "69e6b7f0b72037aa8428b70fbe03986c"
            }

        sec_key = 'FLWSECK-7a06d9a2d7d8c798ebe7dda9b6a63ff6-X'

        # hash the secret key with the get hashed key function
        hashed_sec_key = self.getKey(sec_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

        encrypt_3DES_key = self.encryptData(hashed_sec_key, json.dumps(data))

        # payment payload
        payload = {
            "PBFPubKey": pub_key,
            "client": encrypt_3DES_key,
            "alg": "3DES-24"
        }

        # card charge endpoint
        # endpoint = "https://ravesandboxapi.flutterwave.com/flwv3-pug/getpaidx/api/charge"
        endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/charge"

        # set the content type to application/json
        headers = {
            'content-type': 'application/json',
        }

        response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
        print(response.json())
        return response.json()

# Flutter wave integration code #


class PaymentView(APIView):
    def post(self, request):
        country_locale = request.data['locale']
        rave = PaymentGateWay()
        # res = rave.pay_via_card()
        res = rave.pay_mobile_money(country_locale)
        # if res['status'] == "success" and res['data']['authModelUsed'] == "NOAUTH_INTERNATIONAL":
        #     pass
        #
        # # / * * card requires AVS authentication so you need to * 1. Update payload with billing info - billingzip,
        # # billingcity, billingaddress, billingstate, billingcountry and the suggested_auth returned * 2. Re-encrypt
        # # the payload * 3. Call the charge endpoint once again with this updated encrypted payload * /
        # elif res['status'] == "success" and res['data']['authModelUsed'] == "PIN":
        #     pass
        # # / *
        # # * card requires pin authentication so you need to
        # # * 1. Update payload with pin and the suggested_auth returned
        # # * 2. Re-encrypt the payload
        # # * 3. Call the charge endpoint once again with this updated encrypted payload
        # # * /
        # elif res['status'] == "success" and res['data']['authModelUsed'] == "VBVSECURECODE":
        #     print("okay so what")
        # # / *
        # # * card requires OTP authentication so you need to
        # # * 1. Collect OTP from user
        # # * 2. Call Rave Validate endpoint
        # # * /
        # elif res['status'] == "success" and res['data']['authModelUsed'] != 'N/A':
        #     pass
        # # / *
        # # * card requires 3dsecure authentication so you need to
        # # * 1. Load the authurl in an iframe for your user to complete the transaction
        # # * /
        # else:
        #     pass
        # // an error has probably occurred.

        return Response(data=res, status=status.HTTP_200_OK)
