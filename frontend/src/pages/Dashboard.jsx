import { useEffect, useState } from "react";

import Header from "../components/Header";
import Hero from "../components/Hero";
import FileUpload from "../components/FileUpload";
import UploadedDocuments from "../components/UploadedDocuments";
import QueryForm from "../components/QueryForm";
import AnswerCard from "../components/AnswerCard";

import { getDocuments } from "../services/documentService";

function Dashboard() {
  const [documents, setDocuments] = useState([]);
  const [query, setQuery] = useState("");
  const [isSuggestionClicked, setIsSuggestionClicked] = useState(false);

  const [answer, setAnswer] = useState(""); // 1. Create state for the answer

  const fetchDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />

      {/* Hero — stays narrow and centered */}
      <div className="max-w-3xl mx-auto px-6 pt-8 pb-4">
        <Hero />
      </div>

      {/* Main content — much wider */}
      <main className="max-w-7xl mx-auto px-6 pb-12">
        <div className="mt-10 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left column — Documents */}
          <div className="space-y-6 lg:col-span-5 bg-white p-6 rounded-xl border border-slate-200/80 shadow-sm">
            <div>
              <FileUpload fetchDocuments={fetchDocuments} />
            </div>
            <div className="border-t border-slate-100 pt-6">
              <UploadedDocuments
                documents={documents}
                fetchDocuments={fetchDocuments}
              />
            </div>
          </div>
          {/* Right column — Query & Answer */}
          <div className="space-y-6 lg:col-span-7">
            <QueryForm
              query={query}
              setQuery={setQuery}
              setAnswer={setAnswer}
              isSuggestionClicked={isSuggestionClicked}
              setIsSuggestionClicked={setIsSuggestionClicked}
            />
            <AnswerCard
              setQuery={setQuery}
              setIsSuggestionClicked={setIsSuggestionClicked}
              answer={answer}
            />
          </div>
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
