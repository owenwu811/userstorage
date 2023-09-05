#these tests are supposed to run everytime a new feature is added
bash persistentlogintest.sh
python3 testregistration.py
python3 testlogout.py
python3 testroute.py
python3 testlogin.py
python3 test10triesout.py


