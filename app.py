from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://god1hyuk:gkdgo11wh@bbalibaba.pcvsk.mongodb.net/?retryWrites=true&w=majority')
db = client.bbalibaba

from bson.json_util import ObjectId

import requests
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
    #로그인
    id_receive = request.form['id_give']
    password_receive = request.form['password_give']
    # 해시
    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'id': id_receive, 'password': pw_hash})

    # payload = {
    #     'id': id_receive,
    #     'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 30)
    # }
    # token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    #
    # print(token)
    # print(type(token))

    if result is not None:
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*30)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        decoded = jwt.decode(token, SECRET_KEY, algorithms="HS256")
        print(decoded)
        return jsonify({'result': 'success', 'token': token})
    # 못찾으면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/signup_page')
def signup_page():
    return render_template('signup.html')

@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"id": username_receive}))
    print(exists)
    return jsonify({'result': 'success', 'exists': exists})

#디비 유저랑 비교
@app.route("/sginupcmp", methods=["GET"])
def sginupcmp_get():
    user_list = list(db.users.find({}, {'_id': False}))
    return jsonify({'users':user_list})

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
        'user_post': [],
    }
    db.users.insert_one(doc)

    return jsonify({'msg': '가입이 완료되었습니다!'})

#페이로드 디코딩해서 뿌리는 거
@app.route('/login_info_road')
def login_info_road():
    token_receive = request.cookies.get('mytoken')
    payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
    user_info = db.users.find_one({"id": payload["id"]})

    print(user_info)
    return render_template('index.html', user_info=user_info)

@app.route('/mypage')
def my_page():
    return render_template('mypage.html')

@app.route('/product_post')
def product_post_page():
    return render_template('product_post.html')

@app.route('/products', methods=["POST"])
def post_product():
    productName_receive = request.form['productName_give']
    productDesc_receive = request.form['productDesc_give']
    startPrice_receive = request.form['startPrice_give']
    productImg_receive = request.form['productImg_give']
    userId_receive = request.form['userId_give']
    userName_receive = request.form['userName_give']
    userPhone_receive = request.form['userPhone_give']

    doc = {
        'is_open': 1,
        'product_name': productName_receive,
        'product_desc': productDesc_receive,
        'start_price': format(int(startPrice_receive), ','),
        'price_status': format(int(startPrice_receive), ','),
        'product_image': productImg_receive,
        'user_id': userId_receive,
        'user_name': userName_receive,
        'user_phone': userPhone_receive,
        'bid_list': []
    }
    db.products.insert_one(doc)
    return jsonify({'msg': '상품이 등록되었습니다.'})

@app.route('/products', methods=["GET"])
def get_products():
    product_list = list(db.products.find({}))
    for product in product_list:
        product["_id"] = str(product["_id"])

    return jsonify({'products': product_list})

@app.route('/products/delete', methods=["POST"])
def delete_product():
    _id_receive = request.form['_id_give']
    db.products.delete_one({'_id': ObjectId(_id_receive)})
    return jsonify({'msg': '상품이 삭제되었습니다.'})

@app.route('/product_modify')
def product_modify_page():
    return render_template('product_modify.html')

@app.route('/detail/<product_id>')
def detail_page(product_id):
    product = db.products.find_one({'_id': ObjectId(product_id)})
    return render_template('detail.html', product=product)

@app.route('/products/bidlist', methods=["POST"])
def add_bidlist():
    pathname_receive = request.form['pathname_give']
    price_receive = request.form['price_give']

    db.products.update_one(
        {'_id': ObjectId(pathname_receive)},
        {'$push': {'bid_list': {'user_id': 'god1hyuk', 'bid_price': format(int(price_receive), ','), 'choice': 0}}}
    )
    db.products.update_one({'_id': ObjectId(pathname_receive)}, {'$set': {'price_status': format(int(price_receive), ',')}})
    price_status = db.products.find_one({'_id': ObjectId(pathname_receive)})['price_status']

    print(price_status)
    return jsonify({'msg': '입찰 완료 되었습니다.', 'price_status': price_status})

@app.route('/products/bidlist/choice', methods=["POST"])
def choice_bid():
    _id_receive = request.form['_id_give']

    product_list = db.products.find_one({'_id': ObjectId(_id_receive)})
    bid_list = list(product_list['bid_list'])

    max_price = 0
    max_user = ''
    for bid in bid_list:
        bid_price = int(bid['bid_price'].replace(',', ''))
        if max_price < bid_price:
            max_price = bid_price
            max_user = bid['user_id']
    for bid in bid_list:
        bid_price = int(bid['bid_price'].replace(',', ''))
        if bid_price == max_price:
            bid['choice'] = 1

    product_list['bid_list'] = bid_list
    db.products.update_one({'_id': ObjectId(_id_receive)}, {'$set': product_list})

    db.products.update_one({'_id': ObjectId(_id_receive)}, {'$set': {'is_open': 0}})
    return jsonify({'msg': f'{max_user}님이 낙찰 확정 되었습니다.'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
