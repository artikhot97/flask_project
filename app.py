from flask import request, render_template, make_response,Flask,jsonify,Response
from flask_restful import Resource, Api, reqparse
from application.models import *
from flaskext.mysql import MySQL
import mysql.connector
from flask_jwt_extended import JWTManager ,create_access_token # for Authentication
from datetime import timedelta
import datetime
from flask_jwt_extended import jwt_required
import jwt
import re
import json
from werkzeug.security import generate_password_hash, check_password_hash #hashing function
import uuid
from functools import wraps



app = Flask(__name__)


app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root@123'
app.config['MYSQL_DATABASE_DB'] = 'flask_db'

# app.config.from_envvar('ENV_FILE_LOCATION')

mysql = MySQL(app)

conn = mysql.connect()
cursor = conn.cursor()

app.config['SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'




ACCESS = {
    'admin': 1,
    'user': 2,
}

class User():
    def __init__(self, name, email, password, access=ACCESS['user']):
        self.name = name
        self.email = email
        self.password = password
        self.access = access

    def is_admin(self):
        return self.access == ACCESS['admin']

    def allowed(self, access_level):
        return self.access >= access_level


''' Email Validation '''

regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
def email_validate(email):
    if (re.search(regex, email)):
        return True
        # print("Valid Email")  
    else:
        return False
        # print("Invalid Email")

''' Convert and Validate Password '''
def hash_password(data):
    return generate_password_hash(data)


def password_validation(password):
    flag = 0
    while True:
        if (len(password)<8): 
            flag = -1
            break
        elif not re.search("[a-z]", password): 
            flag = -1
            break
        elif not re.search("[A-Z]", password): 
            flag = -1
            break
        elif not re.search("[0-9]", password): 
            flag = -1
            break
        elif not re.search("[_@$]", password): 
            flag = -1
            break
        elif re.search("\s", password): 
            flag = -1
            break
        else:
            flag = 0
            break
    if flag == -1:
        print("Not a Valid Password") 
        return False
    else:
        return True

def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")


def dictify(a):
    return [dict(zip(("id","name"),vv)) for vv in a]


''' Decorator for validate Request with Token '''
def is_valid_token(f): 
    @wraps(f) 
    def decorator(*args, **kwargs): 
        token = None
        if 'x-access-token' in request.headers: # jwt is passed in the request header 
            token = request.headers['x-access-token']
        if not token:
            return make_response(f'Token Missing !!')
        try:
            # decoding the payload
            data = jwt.decode(token, app.config['SECRET_KEY'])
            print(data)
            cursor.execute('''SELECT * FROM user where public_id=%s''',(data['public_id']))
            current_user = cursor.fetchone()
        except:
            return make_response(f'Token Invalid !!')
        return  f(current_user) 
    return decorator


''' Display Movie List for all user '''
@app.route('/movie', methods=['GET','POST'])
def movie():
    if request.method == 'GET':
        cursor.execute('''SELECT * FROM movies''')
        results = cursor.fetchall()
        print(results)
    return jsonify(results)



""" Registration API where we can register user """

class UserSignUp(Resource):
    def __init__(self):
        pass
    def post(self, data = None):
        try:
            resi_data = request.json
            name = resi_data.get('name',None)
            email = resi_data.get('email', None)
            admin = resi_data.get('admin', None)
            passwrd = resi_data.get('password', None)
            public_id = str(uuid.uuid4())
            register_date = str(datetime.datetime.now())  # use str just to avoid JSON Seializer error while retrive user details
            print(register_date)
            if not email_validate(email):
                return make_response(
                        f'Please Enter valid Email . '
                    )
            if not password_validation(passwrd):
                return make_response(
                        f'Please Enter Password contains Minimum 8 characters include at least 1 Upper Case Char,1 Digit and 1 Special Symbole . '
                    )
            if name and email and passwrd != None:
                cursor.execute('''SELECT * FROM user where name=%s and email=%s''',(name,email))
                existing_user = cursor.fetchall()
                hash_pass = hash_password(passwrd)
                if existing_user:
                    return make_response(
                        f'{name} ({email}) user already created!'
                    )
                # Adds new User record to database
                cursor.execute('''INSERT INTO user (name,email,admin,password,registered_on,public_id) VALUES(%s,%s,%s,%s,%s,%s)''',(name, email, admin, hash_pass,register_date,public_id))
                conn.commit()  # Commits all changes
                return make_response(f"Name : {name} , Email : {email} ,Admin:{admin} Cretaed Sucessfully ...!!")
            return make_response({'Wrong credentials'})
        except Exception as e:
            return make_response(f"{e}")

''' Get User List with Token Please Provide Token'''
class UserList(Resource):
    @is_valid_token
    def get(self):
        try:
            if request.method == 'GET':
                cursor.execute('''SELECT * FROM user''')
                results = cursor.fetchall()
                rows = []
                print(json.dumps(results, sort_keys=False, default=datetime_handler ,indent=4, separators=(',', ': ')))
                return jsonify(results)
            return jsonify('Wrong Request..!!')
        except Exception as e:
            return make_response(f"{e}")


''' Login API '''
class LoginApi(Resource):
    def post(self):
        body = request.json
        email = body.get('email',None)
        password = body.get('password')
        cursor.execute('''SELECT * FROM user WHERE email=%s''',(email))
        data = cursor.fetchall()
        if data:
            for item in data:
                if not item[2]:
                    return make_response(jsonify({'message': 'You are Not Authorized to view User List..!'}))
                if check_password_hash(item[4], body.get('password')): 
                    # generates the JWT Token 
                    token = jwt.encode({ 
                        'public_id': item[6], 
                        'exp' : datetime.datetime.utcnow() + timedelta(minutes = 60) 
                    }, app.config['SECRET_KEY']) 
                    return make_response(jsonify({'token': token.decode('UTF-8'),'messgae':f'Logged in as {email}'}), 201)
        else:
            return make_response(jsonify({'message': 'Wrong credentials'}))

''' Get Movie List '''
class MovieCURD(Resource):
    def get(self):
        try:
            if request.method == 'GET':
                cursor.execute('''SELECT * FROM movies''')
                results = cursor.fetchall()
                return jsonify(results)
            return jsonify('Wrong Request..!!')
        except:
            return 'Someting Went Wrong'
    @is_valid_token
    def post(self):
        try:
            if request.method == 'POST':
                json_data = request.json
                if not json_data.is_admin():
                    return make_response(jsonify({'message': 'Not Authorized'}))
                for item in json_data:
                    popularity = json_data['99popularity']
                    director = json_data['director']
                    genre = json_data['genre']
                    imdb_score = json_data['imdb_score']
                    name = json_data['name']
                    cursor.execute('''INSERT INTO movies (99popularity,director,genre,imdb_score,name) VALUES(%s,%s,%s,%s,%s)''',(popularity, director, genre, imdb_score,name))
                    conn.commit()
                return jsonify('Movie added successfully!')
            return jsonify('Wrong Request..!!')
        except Exception as e:
            print(e)
            return 204

class SingleMovie(Resource):
    def get(self,moive_id):
        try:
            if request.method == 'GET':
                cursor.execute('''SELECT * FROM movies WHERE movie_id=%s''',(moive_id))
                data = cursor.fetchall()
            return jsonify(data)
        except:
            return 'Someting Went Wrong'
    @is_valid_token
    def put(self,movie_id):
        try:
            if request.method == 'PUT':
                json_data = request.json
                if not json_data.is_admin():
                    return make_response(jsonify({'message': 'Not Authorized'}))
                popularity = json_data.get('99popularity', 0)
                director = json_data.get('director', '-')
                genre = json_data.get('genre', [])
                imdb_score = json_data.get('imdb_score', 0)
                name = json_data.get('name', '-')
                id = json_data.get('id', 0)
                cursor.execute('''UPDATE movies SET 99popularity=%s, director=%s, genre=%s, imdb_score=%s, name=%s WHERE movie_id=%s''',(popularity, director, genre, imdb_score, name,id,))
                conn.commit()
                cursor.execute('''SELECT * FROM movies''')
                results = cursor.fetchall()
                return jsonify('Movie update successfully!')
            return jsonify('Wrong Request..!!')
        except Exception as e:
            print(e)
            return 204
    @jwt_required
    def delete(self, movie_id):
        try:
            if request.method == 'GET':
                cursor.execute("DELETE FROM movies WHERE id =%s", (movie_id))
                conn.commit()
                return jsonify('Movie deleted successfully!')
            return jsonify('Wrong Request..!!')
        except:
            return 'Someting Went Wrong'



apis = Api(app)

apis.add_resource(MovieCURD, '/api/movies_curd/',methods=['GET', 'POST'])
apis.add_resource(SingleMovie, '/single_movies/<int:moive_id>',methods=['GET'])
apis.add_resource(UserSignUp, '/api/register/', methods=['GET', 'POST'])
apis.add_resource(UserList, '/api/user_list/',methods=['GET'])
apis.add_resource(LoginApi, '/api/login_user/',methods=['GET','POST'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)




