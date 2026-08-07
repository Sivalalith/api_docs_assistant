import { useRef, useState } from "react";
import { uploadDocuments } from "../services/uploadService";
import LoadingSpinner from "./LoadingSpinner";

function FileUpload({ fetchDocuments }) {
  const fileInputRef = useRef(null);

  const [selectedFiles, setSelectedFiles] = useState([]);
  const [dragActive, setDragActive] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleBrowseClick = () => {
    fileInputRef.current.click();
  };

  const handleFileChange = (event) => {
    const newFiles = Array.from(event.target.files);

    setSelectedFiles((prev) => {
      const merged = [...prev, ...newFiles];

      return merged.filter(
        (file, index, self) =>
          index === self.findIndex((f) => f.name === file.name),
      );
    });
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setDragActive(false);

    const newFiles = Array.from(event.dataTransfer.files);

    setSelectedFiles((prev) => {
      const merged = [...prev, ...newFiles];

      return merged.filter(
        (file, index, self) =>
          index === self.findIndex((f) => f.name === file.name),
      );
    });
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const handleDragEnter = () => {
    setDragActive(true);
  };

  const handleDragLeave = () => {
    setDragActive(false);
  };

  const removeSelectedFile = (fileName) => {
    setSelectedFiles((prev) => prev.filter((file) => file.name !== fileName));
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    try {
      setLoading(true);

      const response = await uploadDocuments(selectedFiles);

      console.log("BE Response:", response);

      setSelectedFiles([]);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }

      await fetchDocuments();
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <h3 className="text-2xl font-semibold text-slate-800 mb-6">
        Upload Documents
      </h3>

      <div
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        className={`
          bg-blue-50
          border-2
          border-dashed
          border-blue-300
          rounded-xl
          py-14
          px-6
          flex
          flex-col
          items-center
          justify-center
          text-center
        
          ${dragActive ? "border-blue-600 bg-blue-100" : "border-blue-300"}`}
      >
        <div className="text-6xl mb-4">📤</div>

        <h4 className="text-xl font-semibold text-slate-800">
          Drag & drop your files here
        </h4>

        <p className="text-slate-500 mt-4 mb-4">or</p>

        <button
          onClick={handleBrowseClick}
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
          📂 Browse Files
        </button>
        <input
          ref={fileInputRef}
          type="file"
          multiple
          hidden
          accept=".pdf,.yaml,.yml,.json"
          onChange={handleFileChange}
        />
      </div>

      <p className="mt-4 text-sm text-slate-500">
        Supported: PDF, OpenAPI (.yaml / .json), Postman Collections
      </p>
      {selectedFiles.length > 0 && (
        <section className="mt-6 bg-slate-50 rounded-xl p-4">
          <h4 className="font-semibold text-slate-800 mb-3">Selected Files</h4>

          <div className="space-y-2">
            {selectedFiles.map((file) => (
              <div
                key={file.name}
                className="flex justify-between items-center border rounded-lg px-4 py-3 bg-white"
              >
                <div>
                  <p className="font-medium text-slate-800">📄 {file.name}</p>

                  <p className="text-sm text-slate-500 mt-1">
                    {(file.size / 1024).toFixed(1)} KB
                  </p>
                </div>

                <button
                  onClick={() => removeSelectedFile(file.name)}
                  className="text-red-600 hover:text-red-700 text-xl transition"
                  title="Remove file"
                >
                  🗑️
                </button>
              </div>
            ))}
          </div>
          <div className="mt-6 flex justify-end">
            <button
              onClick={handleUpload}
              disabled={loading}
              className="
              min-w-[140px]
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
              {loading ? (
                <LoadingSpinner text="Uploading..." />
              ) : (
                `⬆ Upload ${selectedFiles.length} File${selectedFiles.length > 1 ? "s" : ""}`
              )}
            </button>
          </div>
        </section>
      )}
    </section>
  );
}

export default FileUpload;
