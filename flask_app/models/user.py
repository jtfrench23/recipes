from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re
from flask import flash, session
from flask_bcrypt import Bcrypt
from datetime import date
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
bcrypt= Bcrypt(app)




class User:
    db = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name=data['first_name']
        self.last_name= data['last_name']
        self.email= data['email']
        self.password=data['password']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']

#CREATE
    @classmethod
    def save(cls, data):
        if not cls.validate_user(data):
            return False
        else:
            data = cls.parse_user_data(data)
        query = "INSERT INTO users ( first_name , last_name , email, password) VALUES ( %(first_name)s , %(last_name)s , %(email)s, %(password)s);"
        user_id=connectToMySQL(cls.db).query_db( query, data )
        session['user_id']=user_id
        return user_id



#READ
    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        result= connectToMySQL(cls.db).query_db(query)
        users=[]
        for user in result:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, id):
        print(id)
        data={'id': id}
        query = """
        SELECT * from users
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        user= cls(result[0])
        return user

    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def login_user(cls, data):
        user = cls.get_user_by_email(data['email'])
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                return True
        flash('Your login information is incorrect',"login")
        return False
    
    @classmethod
    def lastIndex(cls):
        query="SELECT * FROM users WHERE id=(SELECT max(id) FROM users);"
        user=connectToMySQL(cls.db).query_db(query)
        return user


#UPDATE
    @classmethod
    def update(cls, data):
        query = """
        UPDATE users 
        SET email = %(email)s, 
        first_name=%(fname)s, 
        last_name=%(lname)s 
        WHERE id = %(id)s;"""
        return connectToMySQL(cls.db).query_db( query, data )



#DELETE
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM users WHERE id = (%(id)s);"
        return connectToMySQL(cls.db).query_db(query, data)


#static
    @staticmethod
    def validate_user( user ):
        is_valid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!","register")
            is_valid = False
        for email in User.get_all():
            if user['email']== email.email:
                flash("This email is taken","register")
                is_valid= False
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.","register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("last name must be at least 2 characters.","register")
            is_valid = False
        if len(user['password']) < 8:
            flash("password must be at least 8 characters.","register")
            is_valid = False
        if user['password']!= user['confirm']:
            flash("passwords don't match","register")
            is_valid=False
        if   re.search('[A-Z]',user['password']) is None:
            flash("Password must contain at least one capital letter and one number.","register")
            is_valid=False
        elif re.search('[0-9]',user['password']) is None:
            flash("Password must contain at least one capital letter and one number.","register")
            is_valid=False 
        elif re.search('[a-z]',user['password']) is None: 
            flash("Password must contain at least one capital letter and one number.","register")
            is_valid=False          
        # print(user['birthday'])
        # birthday=datetime.strptime(user['birthday'],"%Y-%m-%d")
        # print(birthday.year)
        # age=calculate_age(birthday)
        # print (age)
        # if age<16:
        #     flash("you are too young to use this site")
        #     is_valid=False
        return is_valid
    @staticmethod
    def parse_user_data(data):
        parsed_data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data
def calculate_age(born):
    today = date.today()
    age=today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    print(age)
    return age