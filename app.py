import os
from datetime import datetime
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# подключение через переменные окружения
DB_USER = os.environ["POSTGRES_USER"]
DB_PASS = os.environ["POSTGRES_PASSWORD"]
DB_HOST = os.environ["POSTGRES_HOST"]
DB_PORT = os.environ.get("POSTGRES_PORT", "5432")
DB_NAME = os.environ["POSTGRES_DB"]

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

db = SQLAlchemy(app)


class Visit(db.Model):
    __tablename__ = "visits"
    id = db.Column(db.Integer, primary_key=True)
    visited_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=False)


# на старте создаем таблицу
with app.app_context():
    db.create_all()


@app.route("/hello", methods=["GET"])
def hello():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    visit = Visit(visited_at=datetime.utcnow(), ip_address=ip)
    db.session.add(visit)
    db.session.commit()
    return "Hello", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)