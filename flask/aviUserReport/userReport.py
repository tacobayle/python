from flask import Flask, render_template, request, send_file
import os
import json
import csv
from avi.sdk.avi_api import ApiSession
#
# Variables
#
controllerFqdn = ["******", "******", "********"]
csv_file = 'test.csv'
passwordContraint = 13
adminUser = "****"
tenant = "*****"
#
# Avi class
#
class aviSession:
  def __init__(self, fqdn, username, password, tenant):
    self.fqdn = fqdn
    self.username = username
    self.password = password
    self.tenant = tenant

  def debug(self):
    print("controller is {0}, username is {1}, password is {2}, tenant is {3}".format(self.fqdn, self.username, self.password, self.tenant))

  def useractivity(self):
    api = ApiSession.get_session(self.fqdn, self.username, self.password, self.tenant)
    useractivityJson = api.get('useractivity')
    userSignedIn = []
    userNotSignedIn = []
    for item in useractivityJson.json()['results']:
        if item['name'] != 'admin':
            if 'last_login_timestamp' in item:
                userSignedIn.append(item['name'])
            else:
                userNotSignedIn.append(item['name'])
    return userSignedIn, userNotSignedIn

#
# Flask
#
app = Flask(__name__)

@app.route('/')
def hello_world():
    return """Hello, World!
           <br>
           My name is """ + str(os.uname()[1])


@app.route('/aviuser', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'GET':
        return render_template('login.html', message=message)

    if request.method == 'POST':
        try:
            password = request.form.get('password')
            if len(password) != passwordContraint:
                raise ValueError('A very specific bad thing happened.')
            userSignedIn = []
            userNotSignedIn = []
            for item in controllerFqdn:
                defineClass = aviSession(item, adminUser, password, tenant)
                controllerUserSignedIn, controllerUserUsNotSignedIn = defineClass.useractivity()
                userSignedIn = userSignedIn + list(set(controllerUserSignedIn) - set(userSignedIn))
                userNotSignedIn = userNotSignedIn + list(set(controllerUserUsNotSignedIn) - set(userNotSignedIn))
            userNotSignedIn = list(set(userNotSignedIn) - set(userSignedIn))
            with open(csv_file, 'w') as csvfile:
                fieldnames = ['username', 'Signedin']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                for item in userSignedIn:
                        writer.writerow({'username': item, 'Signedin': 'true'})
                for item in userNotSignedIn:
                        writer.writerow({'username': item, 'Signedin': 'false'})
            return send_file(csv_file, attachment_filename=csv_file)
        except:
            message = "!!!Error!!!"
            return render_template('login.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
