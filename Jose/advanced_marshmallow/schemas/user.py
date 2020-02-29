# from marshmallow import Schema , fields class UserSchema(Schema):
from ma import ma
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    # Just for loading not for dumping
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)

    # With flask-marshmallow initialization
    # it knows it has to go to the model
    # id = fields.Int()
    # username = fields.Str(required=True)
    # password = fields.Str(required=True)
