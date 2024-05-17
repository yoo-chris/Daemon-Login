from flask import Flask, render_template

# JWT 확장 라이브러리 임포트하기
from flask_jwt_extended import *

app = Flask(__name__)

#토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
app.config.update(
    DEBUG = True,
    JWT_SECRET_KEY = "TeamDaemonSet"
)

#JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    app.debug = True
    app.run()