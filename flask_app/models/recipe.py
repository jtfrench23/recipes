from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
from flask import flash, session
from datetime import date

class Recipe:
    db = 'recipe_schema'
    def __init__(self, data):
        self.id = data['id']
        self.name=data['name']
        self.description=data['description']
        self.under_thirty=data['under_thirty']
        self.instructions=data['instructions']
        self.date_made=data['date_made']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']
        self.users_id=data['users_id']

#CREATE MODEL
    @classmethod
    def create_recipe(cls, data):
        if Recipe.validate_recipe(data):
            query = """INSERT INTO recipes ( name , description , under_thirty, instructions, date_made, users_id) 
            VALUES ( %(name)s , %(description)s , %(under_thirty)s, %(instructions)s, %(date_made)s, %(users_id)s);"""
            return connectToMySQL(cls.db).query_db( query, data )
        else:
            return False

#READ
    @classmethod
    def get_all_recipes_by_user(cls, id):
        data={'id':id}
        query="""
        SELECT * FROM recipes
        WHERE users_id = %(id)s
        ;"""
        result=connectToMySQL(cls.db).query_db(query, data)
        recipes=[]
        for recipe in result:
            recipes.append(cls(recipe))
        return recipes
    @classmethod
    def get_one_by_id(cls, id):
        data={'id':id}
        query="""
        SELECT * FROM recipes
        WHERE id=%(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return cls(result[0])

#UPDATE
    @classmethod
    def update_recipe_by_id(cls, data):
        if Recipe.validate_recipe(data):
            query="""
            UPDATE recipes
            SET name=%(name)s,
            description=%(description)s,
            under_thirty=%(under_thirty)s,
            instructions=%(instructions)s,
            date_made=%(date_made)s
            WHERE id=%(id)s
            ;"""
            connectToMySQL(cls.db).query_db( query, data )
            return True
        else:
            return False
#DELETE MODEL
    @classmethod
    def delete_recipe(cls,id):
        data={'id':id}
        if cls.validate_delete(data):
            query="DELETE FROM recipes WHERE id = (%(id)s);"
            return connectToMySQL(cls.db).query_db(query, data)
        else:
            return

    @staticmethod
    def validate_delete(data):
        is_valid = True
        recipe=Recipe.get_one_by_id(data['id'])
        if recipe.users_id == session['user_id']:
            return is_valid
        else:
            is_valid=False
            return is_valid
    @staticmethod
    def validate_recipe(data):
        is_valid=True
        if len(data['name'])<3:
            is_valid=False
            flash("Name must be at least 3 characters long","recipe")
        if len(data['description'])<3:
            is_valid=False
            flash("description must be at least 3 characters long","recipe")
        if len(data['instructions'])<3:
            is_valid=False
            flash("instuctions must be at least 3 characters long","recipe")
        if not data['date_made']:
            is_valid=False
            flash("must put a date","recipe")
        return is_valid