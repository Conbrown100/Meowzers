# Documentation for 'requests' library can be found at:
# https://requests.readthedocs.io/en/master/user/quickstart/

import requests
import os

port = os.environ['FLASK_PORT']
if not port:
    port = 5000

r = requests.get('http://10.92.21.107:{}/'.format(port))
print(r.text)
