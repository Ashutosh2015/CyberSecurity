import argparse
from unittest import result
from django import forms
import validators
import requests
import yaml
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from bs4 import Comment


parser = argparse.ArgumentParser(description='the ashu version 1.0')

parser.add_argument('-v', '--verson', action='version', version='%(prog)s 1.0')
parser.add_argument('url', type=str, help="the url of html ")
args = parser.parse_args()
r = ''
url = args.url
if(validators.url(url)):
    result_html = requests.get(url).text
    parsed_html = BeautifulSoup(result_html, 'html.parser')
    forms = (parsed_html.find_all('form'))
    password_inputs = parsed_html.find_all('input', {'name': 'password'})
    comments = (parsed_html.find_all(
        string=lambda text: isinstance(text, Comment)))
    for form in forms:  # in order to check wether any form having password or username is not vernarialble
        if((form.get('action').find('https') < 0) and (urlparse(url).scheme != 'https')):
            r += 'Form Issue: Insecure from action' + \
                form.get('action')+' found in document\n'

    for comment in comments:  # in order to check such that no comment have any key vale left at the time of testing
        if(comment.find('key: ') > -1):
            r += 'Comment Issue: Key is found in HTML comments,please remove'

    for password_input in password_inputs:  # in order to check wether any form plaintext is not storing password 
        if(password_input.get('type') != 'password'):
            r += 'Input Issue : Plaintext password input is found please change it to password input'
else:
    print('Invalid URL please include full URL')

if(r):
    print(r)
else:
    print('Page is good to go')
