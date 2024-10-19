from dotenv import load_dotenv
import os
from mongoengine import (
    connect,
    Document,
    StringField,
    ListField,
    ReferenceField
)


load_dotenv()

connect(
    db="max4",
    host=f"mongodb+srv://gladkovnissan:{os.getenv('MONGO_DB_PASSWORD')}@cluster0.v0zgt.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
)
    

class Author(Document):
    author = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()


class Quote(Document):
    keywords = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField(required=True)