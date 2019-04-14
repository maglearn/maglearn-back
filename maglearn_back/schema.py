from graphene import ObjectType, String, Schema


class ExampleQuery(ObjectType):
    hello = String()

    def resolve_hello(self, info):
        return "Hello"


schema = Schema(query=ExampleQuery)
