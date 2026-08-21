import { useState } from "react";
import { askQuery } from "../services/queryService";

function QueryForm({ setAnswer }) {
  const MAX_CHARACTERS = 1000;

  const [query, setQuery] = useState("");

  const handleSubmit = async () => {
    try {
      const response = await askQuery(query);

      setAnswer(response.answer || response);
    } catch (error) {
      console.error("Failed to fetch query response", error);
    }
  };

  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <h3 className="text-2xl font-semibold text-slate-800 mb-6">
        Ask a Question
      </h3>

      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        maxLength={MAX_CHARACTERS}
        placeholder="Example: How do I authenticate requests?"
        className="
          w-full
          min-h-[180px]
          border
          border-slate-300
          rounded-xl
          p-4
          resize-y
          focus:outline-none
          focus:ring-2
          focus:ring-blue-500
          focus:border-blue-500
        "
      />

      <div className="mt-3 flex justify-between items-center">
        <p className="text-sm text-slate-500">
          {query.length} / {MAX_CHARACTERS}
        </p>

        <button
          onClick={() => {
            handleSubmit(query);
          }}
          className="
            bg-blue-600
            hover:bg-blue-700
            text-white
            font-medium
            px-6
            py-3
            rounded-lg
            transition
            duration-200
          "
        >
          💬 Ask Question
        </button>
      </div>
    </section>
  );
}

export default QueryForm;
