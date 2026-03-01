from flask import Flask
import strawberry
from strawberry.flask.views import GraphQLView
from typing import List

app = Flask(__name__)

# Fake database
books = []

# -------------------
# Book Type. This is the GraphQL type that represents a book.
# -------------------
@strawberry.type
class Book:
    id: int
    title: str
    price: float

# -------------------
# Query. This defines the GraphQL queries that clients can execute. In this case, we have a query to get the list of books.
# -------------------
@strawberry.type
class Query:
    @strawberry.field
    def book_list(self) -> List[Book]:
        return books

# -------------------
# Mutation. This defines the GraphQL mutations that clients can execute. In this case, we have a mutation to add a new book.
# -------------------
@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_book(self, title: str, price: float) -> Book:
        new_book = Book(
            id=len(books) + 1,
            title=title,
            price=price
        )
        books.append(new_book)
        return new_book

schema = strawberry.Schema(query=Query, mutation=Mutation)

app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_view", schema=schema)
)

if __name__ == "__main__":
    app.run(debug=True)