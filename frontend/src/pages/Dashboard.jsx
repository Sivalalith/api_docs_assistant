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
    <div className="min-h-screen bg-slate-100">
      <Header />

      <main className="max-w-5xl mx-auto px-6 py-10">
        <Hero />

        <div className="mt-10 space-y-8">
          <FileUpload fetchDocuments={fetchDocuments} />
          <UploadedDocuments
            documents={documents}
            fetchDocuments={fetchDocuments}
          />
          <QueryForm />
          <AnswerCard />
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
