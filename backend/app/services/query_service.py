from app.ai.pipeline import Pipeline

class QueryService:

    @staticmethod
    async def query(user_query: str):

        pipeline = Pipeline()

        results = pipeline.answer_query(user_query)

        return {
            "results": [
                {
                    "score": result.score,
                    "text": result.payload.get("text"),
                    "metadata": {
                        key: value
                        for key, value in result.payload.items()
                        if key != "text"
                    },
                }
                for result in results
            ]
        }