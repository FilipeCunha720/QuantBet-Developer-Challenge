import requests
import re
import heapq
from fractions import gcd

COOKIE_NAME = "laravel_session"


def challenge_result():
    challenge_page = requests.get("http://quantbet.com/quiz/dev")
    cookie = challenge_page.cookies.get_dict()[COOKIE_NAME]
    gcd_result = calculate_gcd(challenge_page.text)
    challenge_response = submit_response(gcd_result, cookie)
    print challenge_response.content


def calculate_gcd(challenge_page_html):
    challenge_page_string = challenge_page_html.encode('ascii', 'ignore')
    number_list = [int(s) for s in re.findall(r'\b\d+\b', challenge_page_string)]
    challenge_numbers = heapq.nlargest(2, number_list)
    return gcd(challenge_numbers[0], challenge_numbers[1])


def submit_response(gcd_result, cookie):
    cookies = {COOKIE_NAME: cookie}
    header = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = "divisor=" + str(gcd_result)
    return requests.post(url="http://quantbet.com/submit", data=payload, cookies=cookies,
                             headers=header)


challenge_result()
