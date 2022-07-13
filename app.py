from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://god1hyuk:gkdgo11wh@bbalibaba.pcvsk.mongodb.net/?retryWrites=true&w=majority')
db = client.bbalibaba

import hashlib
import jwt
import datetime

SECRET_KEY = 'BBalibaba'

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/signin_page')
def signin_page():
    return render_template('signin.html')

@app.route('/signin', methods=["POST"])
def api_login():
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    print(id_receive,password_receive)

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    if result is not None:

        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
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

@app.route('/mypage')
def my_page():
    return render_template('mypage.html')

@app.route('/product_post')
def product_post_page():
    return render_template('product_post.html')

@app.route("/products", methods=["POST"])
def post_product():
    category_receive = request.form['category_give']
    productName_receive = request.form['productName_give']
    productDesc_receive = request.form['productDesc_give']
    startPrice_receive = request.form['startPrice_give']
    productImg_receive = request.form['productImg_give']
    userId_receive = request.form['userId_give']
    userName_receive = request.form['userName_give']
    userPhone_receive = request.form['userPhone_give']

    doc = {
        'category': category_receive,
        'product_name': productName_receive,
        'product_desc': productDesc_receive,
        'start_price': startPrice_receive,
        'price_status': startPrice_receive,
        'product_image': productImg_receive,
        'user_id': userId_receive,
        'user_name': userName_receive,
        'user_phone': userPhone_receive
    }
    db.products.insert_one(doc)
    return jsonify({'msg': '상품이 등록되었습니다.'})

@app.route("/products", methods=["GET"])
def product_get():
    product_list = list(db.products.find({}, {'_id': False}))

    return jsonify({'products': product_list})

@app.route('/product_modify')
def product_modify_page():
    return render_template('product_modify.html')

@app.route('/detail')
def detail_page():
    return render_template('detail.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
