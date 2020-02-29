from marshmallow import Schema, fields


class UserSchema(Schema):
    # Just for loading not for dumping
    class Meta:
        load_only = ("password",)
        dump_only = ("id",)

    id = fields.Int()
    username = fields.Str(required=True)
    password = fields.Str(required=True)
