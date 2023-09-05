#these tests are supposed to run everytime a new feature is added
bash persistentlogintest.sh #good
python3 -m unittest testregistration.py #good
python3 -m unittest testlogout.py #good 
python3 -m unittest testlogin.py #good 
python3 -m unittest test10triesout.py #not working only when runnning python3 -m unittest test10triesout.py but works with python3 test10triesout.py even with if name == '__main__': unittest.... at bottom
flask run
python3 seltests.py #good and dosen't need -m unittest because is a selenium test


