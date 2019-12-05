from app import db, admin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from flask_admin.contrib.sqla import ModelView


@login.user_loader
def load_user(uid):
    return User.query.get(int(uid))


def get_user(email, password):
    try:
        user = User.objects.get(email=email)
        if check_password_hash(user.password_hash, password):
            return user
        else:
            return None
    except Exception as err:
        return err


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(120), index=True)
    balance = db.Column(db.Float(5), index=True, default=0)
    invite = db.Column(db.Integer, index=True, default=0)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def get_user(self, email):
        try:
            user = self.query.filter(User.email == email).first()
            if not user:
                return False
            return user
        except Exception as err:
            print(err)
            return err

    def create_user(self, email, password):
        #проверка возможности регистрации согласно введеному инвайту
        user = User(email=email, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()

    def update_balance(self, email, balance):
        user = self.get_user(email)
        user.balance = user.balance + balance
        text = 'balance was changed on ' + str(balance)
        HistoryUser().write_history(user.id, text)
        db.session.commit()

    def login(self, email, password):
        user = self.get_user(email)
        if check_password_hash(user.password, password):
            return True
        return False

    def check_password(self, u_hash, password):
        return check_password_hash(u_hash, password)


class HistoryUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    act = db.Column(db.String(240))

    def __repr__(self):
        return '<Post {}>'.format(self.id)

    @classmethod
    def write_history(cls, uid, act):
        row = HistoryUser(uid=uid, act=act)
        db.session.add(row)
        db.session.commit()

    @classmethod
    def get_history(cls, uid):
        history = {}
        rows = cls.query.filter_by(uid=11)
        i = 0
        for row in rows:
            i += 1
            history[i] = row
        return history


class Objects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    inputPhone = db.Column(db.String(15))
    outputPhone = db.Column(db.String(15))
    price = db.Column(db.Float(5), default=0.0)
    name = db.Column(db.String(30))
    comment = db.Column(db.String(244))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    check = db.Column(db.Integer, default=0)

    def __repr__(self):
        return '<Object {} {} {} {}>'.format(self.id, self.inputPhone, self.outputPhone, self.price)

    def create_object(self, uid, inp, outp, name, comment):
        object = Objects(uid=uid, inputPhone=inp, outputPhone=outp, name=name, comment=comment)
        db.session.add(object)
        db.session.commit()


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(HistoryUser, db.session))
admin.add_view(ModelView(Objects, db.session))
