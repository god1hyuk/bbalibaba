from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://god1hyuk:gkdgo11wh@bbalibaba.pcvsk.mongodb.net/?retryWrites=true&w=majority')
db = client.bbalibaba

# import jwt
# import datetime
import hashlib

# @app.route('/')
# def home():
#     return render_template('index.html')

# 회원가입
@app.route("/signup", methods=["POST"])
def web_signup_post():
    set_id_receive = request.form['set_id_give']
    set_password_receive = request.form['set_pw_give']
    call_receive = request.form['call_give']
    birth_receive = request.form['birth_give']
    e_mail_receive = request.form['email_give']

    pw_hash = hashlib.sha256(set_password_receive.encode('utf-8')).hexdigest()

    doc = {
        'id': set_id_receive,
        'password': pw_hash,
        'call_number': call_receive,
        'birth': birth_receive,
        'e_mail': e_mail_receive,
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '가입이 완료되었습니다!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)