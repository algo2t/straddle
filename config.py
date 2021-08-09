from alphatrade import *
import logging
import os


login_id = "SA514"
password = "popular@1234"
twofa = "1"

try:
    access_token = open('access_token.txt', 'r').read().rstrip()
except Exception as e:
    print('Exception occurred :: {}'.format(e))
    access_token = None


print(access_token)