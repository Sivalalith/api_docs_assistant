import { useState } from "react";
import { deleteDocument } from "../services/documentService";

import LoadingSpinner from "./LoadingSpinner";

function UploadedDocuments({ documents, fetchDocuments }) {
  const [loadingId, setLoadingId] = useState(null);

  const handleDelete = async (id) => {
    try {
      setLoadingId(id);

      await deleteDocument(id);

      await fetchDocuments();
    } catch (error) {
      console.error(error);
    } finally {
      setLoadingId(null);
    }
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
        {documents.length === 0 ? (
          <p className="text-center text-slate-500 py-8">
            No documents uploaded yet.
          </p>
        ) : (
          documents.map((doc) => (
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
                disabled={loadingId === doc.id}
                className="
                min-w-[140px]
                bg-red-50
                text-red-600
                hover:bg-red-200
                px-4
                py-2
                rounded-lg
                font-medium
                transition
                disabled:bg-red-200
                disabled:cursor-not-allowed
              "
              >
                {loadingId === doc.id ? (
                  <LoadingSpinner text="Deleting..." />
                ) : (
                  "🗑️ Delete"
                )}
              </button>
            </div>
          ))
        )}
      </div>
    </section>
  );
}

export default UploadedDocuments;
