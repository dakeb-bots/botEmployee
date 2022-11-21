import os
from dotenv import dotenv_values

path = '.env'

TOKEN = dotenv_values(path).get('token')
email = dotenv_values(path).get('email')
email_pass = dotenv_values(path).get('email_pass')
email_to = dotenv_values(path).get('email_to')
