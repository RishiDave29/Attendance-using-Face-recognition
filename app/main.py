from flask import Flask,render_template,Response,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

db = SQLAlchemy(app)

def gen(camera):
    while True:
        data = camera.get_frame()
        frame = data[0]
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        #yield (b'...' + frame + b'\r\n\r\n')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login_validation',methods=['POST'])
def logi_validation():
    username=request.form.get('username')
    password = request.form.get('password')
    return "The username is {} and password is {}".format(username,password)


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    return render_template('home.html')



@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__== "__main__":
    app.run(debug=True)

