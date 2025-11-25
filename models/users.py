import marshmallow as ma 
import uuid
from sqlalchemy.dialects.postgresql import UUID 

from db import db

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = db.Column(db.String(), nullable=False, unique=True)   
    password = db.Column(db.String(), nullable=False)
    role=db.Column(db.String(),nullable=False, default='user')

   
    auth = db.relationship("AuthTokens",back_populates="user")


    def __init__(self, email, password,role='user'):
        self.email = email
        self.password = password
        self.role = role


    def new_user_obj():
        return Users('','','user')
    

class UsersSchema(ma.Schema):
    class Meta:
        fields = ['user_id','email','role']


    user_id = ma.fields.UUID()
    email= ma.fields.String(required=True)
    role = ma.fields.String(required=True, dump_default='user')

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)