import { uploadDocuments } from "../services/uploadService";

const handleUpload = async () => {
  const response = await uploadDocuments();

  console.log("BE response: ", response);
};

function FileUpload() {
  return (
    <section className="bg-white rounded-2xl shadow-md p-6">
      <h3 className="text-2xl font-semibold text-slate-800 mb-6">
        Upload Documents
      </h3>

      <div
        className="
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
        "
      >
        <div className="text-6xl mb-4">📤</div>

        <h4 className="text-xl font-semibold text-slate-800">
          Drag & drop your files here
        </h4>

        <p className="text-slate-500 mt-4 mb-4">or</p>

        <button
          onClick={handleUpload}
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
      </div>

      <p className="mt-4 text-sm text-slate-500">
        Supported: PDF, OpenAPI (.yaml / .json), Postman Collections
      </p>
    </section>
  );
}

export default FileUpload;
