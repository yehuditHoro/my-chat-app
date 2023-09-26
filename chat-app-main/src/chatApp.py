from flask import Flask, render_template, redirect, request, session
import csv
from datetime import datetime
import base64
import os

app = Flask(__name__)
app.secret_key = "ABC"
room_names = []
my_path = os.environ.get('path')


# Function to check if a username exists in the users.csv file
def username_exists(username):
    with open("users.csv", "r") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            if username in row:
                return True
    return False

# Function to register a new user
def register_user(username, userpass):
    userpass=encode_password(userpass)
    data = [[username, userpass]]
    with open("users.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(data)

# Function to log in a user
def login_user(username, userpass):
    with open('users.csv', 'r') as users:
        users_arr = csv.reader(users)
        for user in users_arr:
            if user[0] == username:
                userp=decode_password(user[1])
                if userp != userpass:
                    return "wrong password, try again"
                else:
                    session['username'] = username
                    return None
        return "no such username, try again or register"

# Function to create a new chat room
def create_chat_room(room_name):
    room_file = open(f'{my_path}/{room_name}.txt', 'w')  
    room_file.close()


@app.route('/')
def set_rout_register():
  return redirect("/register")


@app.route('/register',methods=['GET', 'POST'])
def homePage():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        
        if username_exists(username):
            return redirect("/login")
        else:
            register_user(username, userpass)
            
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        login_result = login_user(username, userpass)
        
        if login_result is None:
            return redirect("/lobby")
        else:
            return login_result
            
    return render_template('login.html')


@app.route('/lobby', methods=['GET', 'POST'])
def lobbyPage():
    if request.method == 'POST':
        new_room = request.form['new_room']
        if new_room not in room_names:
            room_names.append(new_room)
            create_chat_room(new_room)
    return render_template('lobby.html', room_names=room_names)


@app.route('/chat/<id>', methods=['GET', 'POST'])
def chat(id):
    return render_template('chat.html', room=id)


@app.route('/api/chat/<id>', methods=['GET', 'POST'])
def update_chat(id):
    if request.method == "POST":
        message = request.form['msg']
        username = session.get('username') 
    
        if not username:
            return "You are not logged in.", 403     
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
        with open(f'{my_path}/{id}.txt', 'a') as file:
            file.write(f'[{timestamp}] {username}: {message}\n')

    with open(f'{my_path}/{id}.txt', 'r') as file:
        all_data = file.read()
    return all_data

@app.route('/api/chat/<id>/clear', methods=['POST'])
def clear_rooms(id):
    if request.method == "POST":
        with open(f'{my_path}/{id}.txt', 'w') as file:
            file.write(f"")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')


def encode_password(user_pass):
   pass_bytes = user_pass.encode('ascii')
   base64_bytes = base64.b64encode(pass_bytes)
   base64_message = base64_bytes.decode('ascii')
   return base64_message

def decode_password(user_pass):
   base64_bytes = user_pass.encode('ascii')
   pass_bytes = base64.b64decode(base64_bytes)
   user_pass = pass_bytes.decode('ascii')
   return user_pass
  


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000', debug='True')