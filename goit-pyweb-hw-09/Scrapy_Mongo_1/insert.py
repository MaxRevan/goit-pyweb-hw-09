import json
from models import Author, Quote


with open("authors.json", "r", encoding="utf-8") as f:
    authors_data = json.load(f)

for author_data in authors_data:
    author = Author(
        author=author_data["author"],
        born_date=author_data.get("born_date"),
        born_location=author_data.get("born_location"),
        description=author_data.get("description")
    )
    author.save()


with open("qoutes.json", "r", encoding="utf-8") as f:
    qoutes_data = json.load(f)

for qoute_data in qoutes_data:
    author = Author.objects(author=qoute_data["author"]).first()
    if author:
        quote = Quote(
            keywords=qoute_data["keywords"],
            author=author,
            quote=qoute_data["quote"]
        )
        quote.save()
