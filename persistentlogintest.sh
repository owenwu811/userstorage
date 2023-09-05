export MY_APP_ENV=test
python3 -m unittest testlogin.py
unset MY_APP_ENV
flask run

