import datetime
import hashlib
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session
from config import MyClass
import secrets

# Generate a secure random secret key
secret_key = secrets.token_hex(16)

# Set the secret key in your Flask application


app = Flask(__name__)
app.secret_key = secret_key

cred = MyClass()
username = MyClass.username
password = MyClass.password

data = {}
name = ''
passw = ''


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/get_details_downloads', methods=['GET', 'POST'])
def get_details_download():
    if request.method == 'POST':
        get_data("download")
    return render_template('thanks.html')


@app.route('/get_details_visit', methods=['GET', 'POST'])
def get_details_visit():
    if request.method == 'POST':
        get_data("visit")
    return render_template('thanks.html')


@app.route('/get_details_floor', methods=['GET', 'POST'])
def get_details_floor():
    if request.method == 'POST':
        get_data("floor")
    return render_template('thanks.html')


@app.route('/get_details_gallery', methods=['GET', 'POST'])
def get_details_gallery():
    if request.method == 'POST':
        get_data("gallery")
    return render_template('thanks.html')


@app.route('/get_details_costing', methods=['GET', 'POST'])
def get_details_costing():
    if request.method == 'POST':
        get_data("costing")
    return render_template('thanks.html')


@app.route('/get_details_instant', methods=['GET', 'POST'])
def get_details_instant():
    if request.method == 'POST':
        get_data("instant")
    return render_template('thanks.html')


@app.route('/get_details_register', methods=['GET', 'POST'])
def get_details_register():
    if request.method == 'POST':
        get_data("register")
    return render_template('thanks.html')


@app.route('/get_details_fixed', methods=['GET', 'POST'])
def get_details_fixed():
    if request.method == 'POST':
        get_data("fixed")
    return render_template('thanks.html')


def get_data(name_type):
    name = request.form[f"{name_type}-name"]
    phone = request.form.get(f"{name_type}-phone")
    email = request.form.get(f"{name_type}-email")
    time = datetime.datetime.now().strftime("%b %d, %Y")
    print(time)
    data = pd.DataFrame({"Name": [name], "Phone": [phone], "Email": [email], "Time": [time]})
    reader = pd.read_excel("Customer Data.xlsx")
    writer = pd.ExcelWriter('Customer Data.xlsx', engine='openpyxl', mode='a', if_sheet_exists="overlay")
    data.to_excel(writer, index=False, header=False, startrow=len(reader) + 1)
    writer.close()


@app.route('/admin', methods=["GET", "POST"])
def admin():
    global data
    if 'name' in session:
        if request.method == 'POST':
            start_date = datetime.datetime.strptime(request.form['start'], "%b %d, %Y")
            end_date = datetime.datetime.strptime(request.form['end'], "%b %d, %Y")
            print(start_date)
            print(end_date)
            file = pd.read_excel("Customer Data.xlsx")
            print(len(file.values))
            table_data = []
            for i in range(0, len(file.values)):
                c_date = datetime.datetime.strptime(file.values[i][3], "%b %d, %Y")
                if start_date <= c_date <= end_date:
                    print(file.values[i][3])
                    table_data.append(file.values[i])
            data = {
                'table_data': table_data
            }
            return render_template('admin.html', data=data)
        return render_template('admin.html', data=data)
    else:
        return redirect(url_for('admin_login'))


@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    global name, passw, username, password
    if request.method == 'POST':
        name = str(hashlib.sha256(request.form['name'].encode()).hexdigest())
        passw = str(hashlib.sha256(request.form['password'].encode()).hexdigest())

        if name == username and passw == password:
            session['name'] = name
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('admin_login'))
    return render_template('admin-login.html')


@app.route('/logout', methods=['POST'])
def logout():
    del session['name']
    return redirect(url_for('admin_login'))


if __name__ == '__main__':
    app.run()
