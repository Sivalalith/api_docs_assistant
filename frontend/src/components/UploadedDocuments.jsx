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
                /* Layout & Fluid Sizing */
    flex items-center justify-center gap-2
    w-auto sm:min-w-[110px]
    px-2 sm:px-4 py-2
    
    /* Styles & Colors */
    bg-red-50 text-red-600 hover:bg-red-100 rounded-lg font-medium transition
    
    /* Disabled States */
    disabled:bg-red-100 disabled:opacity-70 disabled:cursor-not-allowed
  "
                aria-label="Delete document"
              >
                {loadingId === doc.id ? (
                  <>
                    {/* On mobile, show just the spinner wheel icon. On desktop, show full component */}
                    <div className="sm:hidden">
                      <LoadingSpinner text="" />
                    </div>
                    <div className="hidden sm:block">
                      <LoadingSpinner text="Deleting..." />
                    </div>
                  </>
                ) : (
                  <>
                    <span>🗑️</span>
                    {/* Text hides on extra-small screens, reappears on small screens and up */}
                    <span className="hidden sm:inline">Delete</span>
                  </>
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
