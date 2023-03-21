from flask import  Flask,render_template,request,redirect,session
import  mysql.connector
import os
from instamojo_wrapper import Instamojo
# API_KEY = "test_0c3e8d5d70b73babe8dbe96d579"
API_KEY = "test_9268e9e315d1931a213d368b0a7"
# AUTH_TOKEN = "test_bd978fa626dab9e8646cfb8870b"
AUTH_TOKEN = "test_d371bdd21cf9dd97e7587989e6d"
SALT = "fb7b35de1c094da193d601ecf4116eb4"

api = Instamojo(api_key=API_KEY ,auth_token=AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')
app = Flask(__name__)
app.secret_key =os.urandom(24)

conn = mysql.connector.connect( host ="localhost",port = '3308' ,user = "root", password = "", database = "car")
cursor = conn.cursor();

@app.route('/')
def login():
    return render_template('login.html')
@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')
    return render_template('home.html')
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/vehicle')
def vehicle():
    return render_template('vehicle.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')
    cursor.execute("""INSERT INTO `users`(`user_id`, `name`, `email`, `password`) VALUES(NULL, '{}', '{}', '{}')""".format(name,email, password))
    conn.commit();

    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}'""".format(email))
    myuser = cursor.fetchall();
    session['user_id'] = myuser[0][0]
    return redirect('/home')


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/payment')
def paymentpage():
    return render_template('payment.html')



@app.route('/pay',methods=['POST','GET'])
def pay():
    if request.method == 'POST':
        name = request.form.get('bname')
        amount = request.form.get('amount')
        mail = request.form.get('email')
        purpose = request.form.get('purpose')
        # return "name {} price {}".format(name,amount)
        response = api.payment_request_create(
            amount=amount,
            purpose=purpose,
            buyer_name=name,
            send_email=False,
            email=mail,
            redirect_url="http://127.0.0.1:5000/success"
        )

        return redirect(response['payment_request']['longurl'])

    else:
        return redirect('/')

@app.route('/login_validation', methods= ['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')
    a = email;
    cursor.execute("""SELECT * FROM `users` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    users = cursor.fetchall();
    if len(users)>0:
        session['user_id'] = users[0][0]
        return redirect('/home')
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
if __name__ == "__main__":
    app.run(debug=True)