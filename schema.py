from flask_marshmallow import Marshmallow
from models import User,Contact,db
from marshmallow_sqlalchemy import fields

ma = Marshmallow()



class ContactSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Contact
        load_instance = True
        sqla_session = db.session
        include_fk = True


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session
        include_relationships = True

    contacts = fields.Nested(ContactSchema, many=True)


contact_schema = ContactSchema()
contacts_schema = ContactSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)