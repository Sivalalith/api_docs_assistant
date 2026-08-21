import { useState, useEffect } from "react";
import { askQuery } from "../services/queryService";
import LoadingSpinner from "./LoadingSpinner";

function QueryForm({
  setAnswer,
  query,
  setQuery,
  isSuggestionClicked,
  setIsSuggestionClicked,
}) {
  const MAX_CHARACTERS = 1000;

  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    // If there is no query text yet, don't submit
    if (!query.trim()) return;
    try {
      setLoading(true);
      const response = await askQuery(query);

      setAnswer(response.answer || response);
    } catch (error) {
      console.error("Failed to fetch query response", error);
    } finally {
      setLoading(false);
    }
  };

  // Safe side-effect: Triggers submission when a suggestion changes the state
  useEffect(() => {
    if (isSuggestionClicked && query) {
      setIsSuggestionClicked(false); // Turn off the flag immediately to break the loop
      handleSubmit();
    }
  }, [isSuggestionClicked, query]); // Listens for click events and query value matches

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
          disabled={loading}
          className="
            bg-blue-600
            hover:bg-blue-700
            disabled:bg-blue-300
            text-white
            font-medium
            px-6
            py-3
            rounded-lg
            transition
            duration-200
          "
        >
          {" "}
          {loading ? <LoadingSpinner text="Querying..." /> : "💬 Ask Question"}
        </button>
      </div>
    </section>
  );
}

export default QueryForm;
