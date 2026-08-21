from app.ai.pipeline import Pipeline

class QueryService:

    @staticmethod
    async def query(user_query: str):

        pipeline = Pipeline()

        results = pipeline.answer_query(user_query)

        return {
             "answer": results
        }