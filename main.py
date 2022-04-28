from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


def to_dict(cafe):
    return {val.name: getattr(cafe, val.name) for val in cafe.__table__.columns}

# HTTP GET - Read Record


@app.route("/all")
def all():
    cafes = Cafe.query.all()
    return jsonify([to_dict(cafe) for cafe in cafes])


@app.route("/random")
def rndm():
    cafes = Cafe.query.all()
    cafe = random.choice(cafes)
    return jsonify(to_dict(cafe))


@app.route("/search", methods=["GET"])
def srch():
    loc = request.args.get("loc")
    cafes = Cafe.query.filter_by(location=loc).all()
    lst = [to_dict(cafe) for cafe in cafes]
    if len(lst) == 0:
        return jsonify({"error": {"Not found": "Sorry,we dont have a cafe at that location"}})
    else:
        return jsonify(lst)

# HTTP POST - Create Record


@app.route("/add", methods=["POST"])
def add():
    add_cf = Cafe(name=request.form.get("name"),
                  map_url=request.form.get("map_url"),
                  img_url=request.form.get("img_url"),
                  location=request.form.get("loc"),
                  has_sockets=bool(request.form.get("sockets")),
                  has_toilet=bool(request.form.get("toilet")),
                  has_wifi=bool(request.form.get("wifi")),
                  can_take_calls=bool(request.form.get("calls")),
                  seats=request.form.get("seats"),
                  coffee_price=request.form.get("coffee_price"))
    db.session.add(add_cf)
    db.session.commit()
    return jsonify(response={"success": "added new cafe"})

# HTTP PUT/PATCH - Update Record


@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def update(cafe_id):
    cf = Cafe.query.filter_by(id=cafe_id).first()
    if cf:
        cf.coffee_price = request.args.get("new_price")
        db.session.commit()
        return jsonify(response={"sucess": "added"}), 200
    else:
        return jsonify(response={"Error": "Cafe not found"}), 404

# HTTP DELETE - Delete Record


@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def dlt(cafe_id):
    if request.args.get("api_key") == "LO#*&TL#ER6dbahdaf63712":
        cafe = Cafe.query.filter_by(id=cafe_id).first()
        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"Success": "Deleted"}), 200
        else:
            return jsonify(error={"Not found": "Cafe was not found"}), 404
    else:
        return jsonify({"error": "Sorry api key is invalid"}), 403


if __name__ == '__main__':
    app.run(debug=True)
