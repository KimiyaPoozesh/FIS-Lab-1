from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)
limiter.message = "Too many requests, please try again later."

login_attempts = {}
n=3
@app.route("/login", methods=["POST"])
@limiter.limit("3 per minute")
def login():
    ip_address = request.remote_addr
    if ip_address not in login_attempts:
        login_attempts[ip_address] = 1
    else:
        login_attempts[ip_address] += 1

    username = request.form.get("username")
    password = request.form.get("password")
    print(f"IP address {ip_address} has attempted {login_attempts[ip_address]} logins.")

    if username == "user" and password == "pass":
        login_attempts[ip_address] = 0
        return "Login successful"
    else:
        if login_attempts[ip_address] >=n:
            login_attempts[ip_address] = 0
            return limiter.message
        else:
            return "Incorrect username or password"


if __name__ == "__main__":
    app.run(debug=True)