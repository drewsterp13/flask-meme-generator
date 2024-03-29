from flask import Blueprint, render_template, jsonify, request
from helpers import token_required
from models import Photo, Meme, photo_schema, all_photo_schemas, meme_schema, all_meme_schemas, db, User

api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/data")
def data():
    return jsonify({"Minecraft": "is great"})

@api.route("/photos", methods = ["POST"])
@token_required
def addphoto(your_token):
    name = request.json["name"]
    link = request.json["link"]
    user_token = your_token.token

    print(f"BIG TESTER: {your_token}")

    photo = Photo(name, link, user_token = user_token)
    
    db.session.add(photo)
    db.session.commit()

    response = photo_schema.dump(photo)
    return jsonify(response)

@api.route("/photos", methods = ["GET"])
@token_required
def displayallphotos(your_token):
    owner = your_token.token
    photos = Photo.query.filter_by(user_token = owner).all()
    response = all_photo_schemas.dump(photos)
    return jsonify(response)

@api.route("/photos/<id>", methods = ["GET"])
@token_required
def displayphotos(your_token, id):
    owner = your_token.token
    if owner == your_token.token:
        photo = Photo.query.get(id)
        response = photo_schema.dump(photo)
        return jsonify(response)
    else:
        return jsonify({"ERROR": "Sorry, valid token required"}), 401

@api.route("/photos/<id>", methods = ["PUT", "POST"])
@token_required
def updatephoto(your_token, id):
    photo = Photo.query.get(id)
    photo.name = request.json["name"]
    photo.link = request.json["link"]
    photo.user_token = your_token.token

    db.session.commit()
    response = photo_schema.dump(photo)
    return jsonify(response)

@api.route("/photos/<id>", methods = ["DELETE"])
@token_required
def deletephoto(your_token, id):
    photo = Photo.query.get(id)
    db.session.delete(photo)
    db.session.commit()
    response = photo_schema.dump(photo)
    return jsonify(response)

@api.route("/memes", methods = ["POST"])
@token_required
def creatememe(your_token):
    title = request.json["title"]
    caption = request.json["caption"]
    photo_id = request.json["photo_id"]
    user_token = your_token.token

    meme = Meme(title, caption, photo_id, user_token = user_token)

    db.session.init(meme)
    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route("/memes", methods = ["GET"])
@token_required
def viewallmemes(your_token):
    owner = your_token.token
    memes = Meme.query.filter_by(user_token = owner).all()
    response = all_meme_schemas.dump(memes)
    return jsonify(response)

@api.route("/memes/<id>", methods = ["GET"])
@token_required
def viewmeme(your_token, id):
    owner = your_token.token

    if owner == your_token.token:
        memes = Meme.query.get(id)
        response = meme_schema.dump(memes)
        return jsonify(response)
    else:
        return jsonify({"ERROR": "Sorry, valid token required"}), 41

@api.route("/memes/<id>", methods = ["PUT", "POST"])
@token_required
def editmeme(your_token, id):
    meme = Meme.query.get(id)

    meme.title = request.json["title"]
    meme.caption = request.json["caption"]
    meme.photo_id = request.json["photo_id"]
    meme.user_token = your_token.token

    db.session.commit()

    response = meme_schema.dump(meme)
    return jsonify(response)

@api.route("/memes/<id>", methods = ["DELETE"])
@token_required
def deletememe(your_token, id):
    meme = Meme.query.get(id)
    db.session.delete(meme)
    db.session.commit()
    response = meme_schema.dump(meme)
    return jsonify(response)

