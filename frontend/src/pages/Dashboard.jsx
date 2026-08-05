import Header from "../components/Header";
import Hero from "../components/Hero";
import FileUpload from "../components/FileUpload";
import UploadedDocuments from "../components/UploadedDocuments";
import QueryForm from "../components/QueryForm";
import AnswerCard from "../components/AnswerCard";

function Dashboard() {
  return (
    <div className="min-h-screen bg-slate-100">
      <Header />

      <main className="max-w-5xl mx-auto px-6 py-10">
        <Hero />

        <div className="mt-10 space-y-8">
          <FileUpload />
          <UploadedDocuments />
          <QueryForm />
          <AnswerCard />
        </div>
      </main>
    </div>
  );
}

export default Dashboard;
