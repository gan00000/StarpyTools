import json
import os

if __name__ == '__main__':

    f = open('/Users/gan/Downloads/xx.txt')
    content = f.read()
    f.close()
    if content:
        parsed_json = json.loads(content)
        items_list = parsed_json.get('BillingItems')
        for item in items_list:
            PaymentType = item.get('PaymentType')
            PaymentTypeDesc = item.get('PaymentTypeDesc')
            print PaymentType + ' = ' + PaymentTypeDesc