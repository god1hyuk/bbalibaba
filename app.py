from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://god1hyuk:gkdgo11wh@bbalibaba.pcvsk.mongodb.net/?retryWrites=true&w=majority')
db = client.bbalibaba

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/signin')
def signin_page():
    return render_template('signin.html')

@app.route('/signup')
def signup_page():
    return render_template('signup.html')

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
