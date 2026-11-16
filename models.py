from db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255))

class Budget(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    month = db.Column(
        db.Integer,
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    @property
    def month_name(self):

        months = {
            1: "Styczeń",
            2: "Luty",
            3: "Marzec",
            4: "Kwiecień",
            5: "Maj",
            6: "Czerwiec",
            7: "Lipiec",
            8: "Sierpień",
            9: "Wrzesień",
            10: "Październik",
            11: "Listopad",
            12: "Grudzień"
        }

        return months.get(self.month)

    def __repr__(self):
        return f'<Budget {self.category}>'

class Transaction(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer,db.ForeignKey("user.id"))

    name = db.Column(db.String(100))

    amount = db.Column(db.Float)

    type = db.Column(db.String(20))
    # income / expense

    category = db.Column(db.String(50))

    date = db.Column(db.Date)

