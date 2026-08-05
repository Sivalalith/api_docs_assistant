function AnswerCard() {
  const response = {
    endpoint: "POST /login",
    headers: "Authorization: Bearer <token>",
    description: "Authenticates the user and returns an access token.",
    code: `{
  "email": "user@example.com",
  "password": "password123"
}`,
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(response.code);
  };

  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <h3 className="text-2xl font-semibold text-slate-800 mb-6">Answer</h3>

      <div className="bg-blue-50 border border-blue-100 rounded-xl p-6">
        <p className="mb-3 text-slate-700">
          <span className="font-semibold text-blue-600">Endpoint:</span>{" "}
          {response.endpoint}
        </p>

        <p className="mb-3 text-slate-700">
          <span className="font-semibold text-blue-600">Headers:</span>{" "}
          {response.headers}
        </p>

        <p className="mb-5 text-slate-700">
          <span className="font-semibold text-blue-600">Description:</span>{" "}
          {response.description}
        </p>

        <div className="relative">
          <button
            onClick={handleCopy}
            className="absolute top-3 right-3 text-slate-500 hover:text-blue-600 transition"
            title="Copy"
          >
            📋
          </button>

          <pre className="bg-white border border-slate-200 rounded-lg p-5 overflow-x-auto text-sm">
            <code>{response.code}</code>
          </pre>
        </div>
      </div>
    </section>
  );
}

export default AnswerCard;
