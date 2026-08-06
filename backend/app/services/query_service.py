class QueryService:

    @staticmethod
    def query(question: str):

        print(question)

        return {
            "endpoint": "POST /login",
            "headers": "Authorization: Bearer <token>",
            "description": "Dummy AI response.",
            "code": """{
  "email": "user@example.com",
  "password": "password123"
}""",
        }