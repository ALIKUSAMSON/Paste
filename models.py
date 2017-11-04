class User(db.Model):
    __tablename__ = "users"
    uid = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(54))
