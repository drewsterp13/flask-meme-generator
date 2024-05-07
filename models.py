from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import secrets
import uuid

login_manager = LoginManager()
db = SQLAlchemy()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(25), nullable = True)
    last_name = db.Column(db.String(25), nullable = True)
    username = db.Column(db.String(25), nullable = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String, default = " ")
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = " ", unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.now)

    def __init__(self, first_name, last_name, username, email, password = " ", g_auth_verify = False, token = " "):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)
        self.g_auth_verify = g_auth_verify
        self.token = self.set_token()
    
    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, enter_password):
        self.hash_password = generate_password_hash(enter_password)
        return self.hash_password
    
    def set_token(self):
        return secrets.token_hex(24)
    
    def __repr__(self):
        return f"LOG: {self.first_name} {self.last_name} ({self.username}) Successfully created a new account"
    
class Photo(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(200))
    link = db.Column(db.String)
    user_token = db.Column(db.String, db.ForeignKey("user.token"))
    
    def __init__(self, name, link, user_token, id = " "):
        self.id = self.set_id()
        self.name = name
        self.link = link
        self.user_token = user_token
    
    def set_id(self):
        return str(secrets.token_urlsafe())
    
    def __repr__(self):
        return f"LOG: Successfully added a new picture"

class Meme(db.Model):
    id = db.Column(db.String, primary_key = True)
    title = db.Column(db.String(200), nullable = True)
    caption = db.Column(db.String(1000), nullable = True)
    photo_id = db.Column(db.String, db.ForeignKey("photo.id"))
    user_token = db.Column(db.String, db.ForeignKey("user.token"))

    def __init__(self, title, caption, photo_id, user_token, id = " "):
        self.id = self.set_id()
        self.title = title
        self.caption = caption
        self.photo_id = photo_id
        self.user_token = user_token
    
    def set_id(self):
        return str(secrets.token_urlsafe())
    
    def __repr__(self):
        return f"LOG: Successfully added a new meme :)"

class PhotoSchema(ma.Schema):
    class Meta:
        fields = ["id", "name", "link", "user_token"]

class MemeSchema(ma.Schema):
    class Meta:
        fields = ["id", "title", "caption", "photo_id", "user_token"]

photo_schema = PhotoSchema()
all_photo_schemas = PhotoSchema(many = True)
meme_schema = MemeSchema()
all_meme_schemas = MemeSchema(many = True)
