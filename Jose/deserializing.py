from marshmallow import Schema, fields, INCLUDE, EXCLUDE


class BookSchema(Schema):
    title = fields.Str(required=True)
    author = fields.Str()


incoming_book_data = {
    "title": "Clean Code",
    "author": "Bob Martin",
    "description": "A book about writing cleaner code, with examples in Java",
}

book_schema = BookSchema(unknown=EXCLUDE)
book = book_schema.load(incoming_book_data)

print(book)
