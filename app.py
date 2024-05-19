from flask import Flask, render_template, request, redirect, url_for, session
# JWT 확장 라이브러리 임포트하기
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

#토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "TeamDaemonSet"
)
#JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)

#############Database#################
app.secret_key ='TeamDaemonSet'# 세션 보안을 위한 secret key 설정
app.config['MYSQL_HOST'] ='localhost'# MySQL 호스트 설정
app.config['MYSQL_USER'] ='root'# MySQL 유저 설정
app.config['MYSQL_PASSWORD'] ='test123'# MySQL 비밀번호 설정
app.config['MYSQL_DB'] ='login'# MySQL 데이터베이스 설정
mysql= MySQL(app)# MySQL 객체 생성

#로그인
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')

    else:
        email = request.form.get('email')
        password = request.form.get('password')
        cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('SELECT * FROM member WHERE email=%s AND password=%s', (email,password,))
        user = cursor.fetchone()

        if user:
            session['loggedin'] =True # 로그인 상태를 True로 변경            
            session['email'] = user['email'] # 세션에 account 값을 저장            
            session['password'] =user['password'] # 세션에 password 값을 저장
            msg = "Login Success!!"
            return render_template('success.html', msg=msg, username=user['username'])

        else:
            msg = "Incorrect email or password"
            return render_template('login.html', msg=msg)



#회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # GET 요청이 들어왔을 때, signup.html 페이지로 이동한다.
    if request.method == "GET":
        return render_template('signup.html')
    
    # POST 요청이 들어왔을 때, 모든 필드가 채워졌는지 확인하고, 채워졌다면 해당 값을 변수에 저장한다.
    else:
        if 'username' in request.form and 'email' in request.form and 'password' in request.form and 're_password' in request.form:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')

            # 다음 코드는 MySQL 데이터베이스에 연결하고, 입력한 계정이 이미 존재하는지 확인한다.
            cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM member WHERE email = %s', (email, ))
            user=cursor.fetchone()

            # 회원가입 불가능한 조건 설정 거는 곳 ( 중간에 elif 로 조건 추가하면 된다.)
            if user:
                msg = "이미 존재하는 계정입니다."
            else:
                cursor.execute('INSERT INTO member VALUES (default ,%s,%s,%s)',(username,email,password))
                mysql.connection.commit()
                msg = '!!회원가입 성공!!'
                return redirect('/')
        else:
            msg = '칸을 전부 채워주세요!!'
        return render_template('signup.html', msg=msg)
        


        



#로그인 성공 메인페이지 이동
@app.route('/success')
def success():
    if 'loggedin' in session:
        return render_template('success.html')
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.debug = True
    app.run()