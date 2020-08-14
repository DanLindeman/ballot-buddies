import random
from quart import redirect, request, render_template, url_for, session
from sqlalchemy.orm import sessionmaker

from . import api
from app import app, db
from app.models import User

db.create_all()


@app.route("/")
async def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        our_user = db.session.query(User).filter_by(**form).first()
        if not our_user:
            u = User(
                first_name=form["first_name"],
                last_name=form["last_name"],
                birth_date=form["birth_date"],
                zip_code=form["zip_code"],
            )
            db.session.add(u)
            db.session.commit()

        our_user = db.session.query(User).filter_by(**form).first()
        session["user_id"] = our_user.id

        return redirect(url_for("friends", user_id=our_user.id))

    return await render_template("login.html", voter=request.args)


@app.route("/<user_id>/friends", methods=["GET"])
async def friends(user_id: int):
    u = User.query.get(session["user_id"])
    status = await api.get_status(**u.form())
    return await render_template("friends.html", status=status, session_data=u)
