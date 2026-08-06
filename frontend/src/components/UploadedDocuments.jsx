import { useEffect, useState } from "react";
import { getDocuments, deleteDocument } from "../services/documentService";

function UploadedDocuments() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    const data = await getDocuments();
    setDocuments(data);
  };

  const handleDelete = async (id) => {
    await deleteDocument(id);
    fetchDocuments();
  };

  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h3 className="text-2xl font-semibold text-slate-800">
          Uploaded Documents
        </h3>

        <span className="text-sm text-slate-500">{documents.length} Files</span>
      </div>

      <div className="">
        {documents.map((doc) => (
          <div
            key={doc.id}
            className="
              flex
              items-center
              justify-between
              p-4
              border
              border-slate-200
              rounded-md
              hover:shadow-md
              transition
            "
          >
            <div className="flex items-center gap-4">
              <div className="text-3xl">📁</div>

              <div>
                <h4 className="font-semibold text-slate-800">{doc.name}</h4>

                <p className="text-sm text-slate-500">
                  {doc.type} • {doc.size}
                </p>
              </div>
            </div>

            <button
              onClick={() => handleDelete(doc.id)}
              className="
                bg-red-50
                text-red-600
                hover:bg-red-200
                px-4
                py-2
                rounded-lg
                font-medium
                transition
              "
            >
              🗑️ Delete
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}

export default UploadedDocuments;
