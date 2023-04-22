import strawberry

name: str = "jisu"


@strawberry.type
class Query:
    @strawberry.field
    def ping(self) -> str:
        return "pong"


schema = strawberry.Schema(query=Query)
