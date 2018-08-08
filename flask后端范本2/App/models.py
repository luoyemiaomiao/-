from App.exts import db

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),unique=True)
    passwd = db.Column(db.String(32))

    def to_dict(self):
        return {'id':self.id,'name':self.name,'passwd':self.passwd}