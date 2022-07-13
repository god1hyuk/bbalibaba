from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.znoygno.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('detail.html')


@app.route("/products", methods=["POST"])
def web_detail_post():
    money_receive = request.form['money_give']

    doc = {
        'money': money_receive
    }

    db.미니프로젝트.insert_one(doc)

    return jsonify({'msg': '입찰가를 확인해주시기 바랍니다! 만약 아래 히스토리 표에서 자신의 입찰가가 보이지 않는다면, 현재입찰가 보다 낮은 금액을 제시하였기 때문입니다.'})


@app.route("/products", methods=["GET"])
def web_mars_get():
    order_list = list(db.미니프로젝트.find({}, {'_id': False}))
    return jsonify({'orders': order_list})

#<!-------------------------------------------------------------------->

# @app.route("/products", methods=["GET"])
# def web_dbdate_get():
#     dbdate_list = list(db.이름.find({}, {'_id': False}))
#     return jsonify({'dbdate':dbdate_list})


# @app.route("/products", methods=["GET"])
# 상세 페이지 구현 해야 할 기능
# X 1. 최초 입찰가 >  post 페이지에서 입력한 최초 입찰가 db에서 가져오기

# ● 2. 입찰가 현황 > 위에 order_list에서 가장 큰 값 가져오기?? >
#    const max = Math.max(db에서 order_list 목록);
#    console.log(max);

# X 3. 상품 설명 > post 페이지에서 상품 설명을 db에서 가져오기

# X 4. 회원 아이디 > 로그인을 한 유저의 아이디 db에서 가져오기 > ??

# ● 5. 입찰하기 버튼을 눌렀을 경우 기존의 입찰가 보다 금액이 작을 시 입력불가
#    existmoney 변수로 받아오기= db에서 최초입찰가 가져오기
#    input 부분을 newmoney로 받기
#    if (existmoney < newmoney){
#    console.log("입찰 완료");
#    } else (existmoney > newmoney){
#    console.log("기존의 입찰가보다 금액이 적어 입찰 할 수 없습니다.");

# ● 6. 히스토리 남겨지는 부분에 : order_list 금액이 가장 큰 부분을 위쪽으로 불러오기(액이 큰 순으로 정렬)금
#    const numbers = [db에서 order_list money 금액을 배열 형태로 ??];
#    numbers.sort((a, b) => b - a);
#    console.log.(numbers)

#<!-------------------------------------------------------------------->


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)


