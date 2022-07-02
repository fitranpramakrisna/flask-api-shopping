from functools import wraps
from config import app, db, api
from flask import request, make_response, jsonify
from flask_restful import Resource
from models import User, Shopping
from passlib.hash import sha256_crypt

import jwt
import datetime

app.config["SECRET_KEY"] = "INIRAHASIA"


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return make_response(jsonify({"msg": "Token is invalid!"}), 401)
        try:
            jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except:
            return make_response(jsonify({"msg": "Token is invalid!"}), 401)
        return f(*args, **kwargs)
    return decorator


class RegisterUser(Resource):
    def post(self):
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')
        city = request.form.get('city')
        country = request.form.get('country')
        name = request.form.get('name')
        postcode = request.form.get('postcode')

        user = User.query.filter(User.email == email, User.username==username).all()

        if not user:
            password_hashed = sha256_crypt.encrypt(password)
            modelData = User(
            username=username, password=password_hashed,
            email=email, phone = phone,
            address = address, city = city,
            country = country, name = name, postcode = postcode)
                
            db.session.add(modelData)
            db.session.commit()

            return make_response(jsonify({"msg": "Registrasi berhasil!", "email":email, "username":username}), 201)
        else:
            return make_response(jsonify(
                {"msg": "Username atau email yang anda masukan sudah terdaftar!"}), 404)


class LoginUser(Resource):
    def post(self):
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user is None:
            return make_response(jsonify({"msg": "Login gagal! Silahkan cek kembali Email dan Password"}), 404)
        
        check = sha256_crypt.verify(password, user.password)
        if user and check:
            token = jwt.encode(
                {
                    "email": email, "exp": datetime.datetime.now() + datetime.timedelta(minutes=10)
                }, app.config['SECRET_KEY'],  algorithm="HS256"
            )
            return make_response(jsonify({"msg": "Login Sukses", "token": token.decode()}), 200)
        else:
            return make_response(jsonify({"msg": "Login gagal! Silahkan cek kembali Email dan Password"}), 404)
            


class GetAllUsers(Resource):
    @token_required
    def get(self):
        user = User.query.all()
        if user:
            output = [
                {"id": data.id,
                 "name": data.name,
                 "city": data.city,
                 "country":data.country,
                 "postcode":data.postcode,
                 "address":data.address
                 }
                for data in user
            ]
            return make_response(jsonify({"msg":"Successful!", "data":output}), 200)
        
        return make_response(jsonify({"msg": "Data masih kosong!"}), 404)
    
    
class CreateShopping(Resource):
    @token_required
    def post(self):
        name = request.form.get('name')
        
        modelData = Shopping(name=name)
        db.session.add(modelData)
        db.session.commit()
        return make_response(jsonify({"msg": "Shopping baru berhasil ditambahkan!"}), 201)
    
    
class GetAllShopping(Resource):
    @token_required
    def get(self):
        shopping = Shopping.query.all()
        if shopping:
            output = [
                {"id": data.id,
                 "name": data.name,
                 "created_date": data.created_date,
                 }
                for data in shopping
            ]
            return make_response(jsonify({"msg":"Successful!", "data":output}), 200)
        
        return make_response(jsonify({"msg": "Data masih kosong!"}), 404)
    
    
class GetShoppingById(Resource):
    @token_required
    def get(self, shopping_id):
        shoppingModel = Shopping.query.filter_by(id=shopping_id).first()
        if shoppingModel:
            dataOutput = [
                {"id": shoppingModel.id,
                 "name": shoppingModel.name,
                 "created_date": shoppingModel.created_date,
                 }
            ]
            return make_response(jsonify({"msg": "Successful!", "data": dataOutput}), 200)
        return make_response(jsonify({"msg": "Shopping id tidak ditemukan!"}), 404)
     
     
class EditShopping(Resource):
    @token_required
    def put(self, shopping_id):
        name = request.form.get('name')
        shoppingModel = Shopping.query.filter_by(id=shopping_id).first()
        if shoppingModel:
            shoppingModel.name = name
            db.session.commit()
            return make_response(jsonify({"msg": "Shopping berhasil diubah!"}), 200)
        else:
            return make_response(jsonify({"msg": "Shopping id tidak ditemukan!"}), 404)


class DeleteShopping(Resource):
    @token_required
    def delete(self, shopping_id):
        shoppingModel = Shopping.query.filter_by(id=shopping_id).first()
        if shoppingModel:
            db.session.delete(shoppingModel)
            db.session.commit()
            return make_response(jsonify({"msg": "Shopping berhasil dihapus!"}), 200)
        else:
            return make_response(jsonify({"msg": "Shopping id tidak ditemukan!"}), 404)
        


# setup resource endpoint
api.add_resource(RegisterUser, "/api/signup", methods=["POST"])
api.add_resource(LoginUser, "/api/signin", methods=["POST"])
api.add_resource(GetAllUsers, "/api/users", methods=["GET"])
api.add_resource(GetAllShopping, "/api/shopping", methods=["GET"])
api.add_resource(CreateShopping, "/api/shopping", methods=["POST"])
api.add_resource(GetShoppingById, "/api/shopping/<shopping_id>", methods=["GET"])
api.add_resource(EditShopping, "/api/shopping/<shopping_id>", methods=["PUT"])
api.add_resource(DeleteShopping, "/api/shopping/<shopping_id>", methods=["DELETE"])


if __name__ == "__main__":
    app.run(debug=True, port=5005)
