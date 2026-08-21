// function AnswerCard() {
//   const response = {
//     endpoint: "POST /login",
//     headers: "Authorization: Bearer <token>",
//     description: "Authenticates the user and returns an access token.",
//     code: `{
//   "email": "user@example.com",
//   "password": "password123"
// }`,
//   };

//   const handleCopy = async () => {
//     await navigator.clipboard.writeText(response.code);
//   };

//   return (
//     <section className="bg-white rounded-2xl shadow-md p-6">
//       <h3 className="text-2xl font-semibold text-slate-800 mb-6">Answer</h3>

//       <div className="bg-blue-50 border border-blue-100 rounded-xl p-6">
//         <p className="mb-3 text-slate-700">
//           <span className="font-semibold text-blue-600">Endpoint:</span>{" "}
//           {response.endpoint}
//         </p>

//         <p className="mb-3 text-slate-700">
//           <span className="font-semibold text-blue-600">Headers:</span>{" "}
//           {response.headers}
//         </p>

//         <p className="mb-5 text-slate-700">
//           <span className="font-semibold text-blue-600">Description:</span>{" "}
//           {response.description}
//         </p>

//         <div className="relative">
//           <button
//             onClick={handleCopy}
//             className="absolute top-3 right-3 text-slate-500 hover:text-blue-600 transition"
//             title="Copy"
//           >
//             📋
//           </button>

//           <pre className="bg-white border border-slate-200 rounded-lg p-5 overflow-x-auto text-sm">
//             <code>{response.code}</code>
//           </pre>
//         </div>
//       </div>
//     </section>
//   );
// }

// export default AnswerCard;

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function AnswerCard({ answer }) {
  const [copiedCode, setCopiedCode] = useState(null);

  const handleCopy = async (code, index) => {
    await navigator.clipboard.writeText(code);
    setCopiedCode(index);

    setTimeout(() => {
      setCopiedCode(null);
    }, 1500);
  };

  return (
    <div className="mt-6">
      <h2 className="mb-3 text-xl font-semibold text-gray-900">Answer</h2>

      <div className="rounded-xl border border-blue-200 bg-blue-50 p-6">
        <div className="prose max-w-none prose-gray">
          <ReactMarkdown
            remarkPlugins={[remarkGfm]}
            components={{
              h1: ({ children }) => (
                <h1 className="mb-4 mt-2 text-2xl font-bold text-gray-900">
                  {children}
                </h1>
              ),

              h2: ({ children }) => (
                <h2 className="mb-3 mt-6 text-xl font-semibold text-gray-900">
                  {children}
                </h2>
              ),

              h3: ({ children }) => (
                <h3 className="mb-2 mt-5 text-lg font-semibold text-gray-900">
                  {children}
                </h3>
              ),

              p: ({ children }) => (
                <p className="mb-4 leading-7 text-gray-700">{children}</p>
              ),

              ul: ({ children }) => (
                <ul className="mb-4 list-disc space-y-1 pl-6 text-gray-700">
                  {children}
                </ul>
              ),

              ol: ({ children }) => (
                <ol className="mb-4 list-decimal space-y-1 pl-6 text-gray-700">
                  {children}
                </ol>
              ),

              li: ({ children }) => <li className="leading-6">{children}</li>,

              blockquote: ({ children }) => (
                <blockquote className="my-4 border-l-4 border-blue-300 pl-4 italic text-gray-600">
                  {children}
                </blockquote>
              ),

              table: ({ children }) => (
                <div className="my-5 overflow-x-auto rounded-lg border border-gray-200 bg-white">
                  <table className="min-w-full border-collapse text-sm">
                    {children}
                  </table>
                </div>
              ),

              th: ({ children }) => (
                <th className="border-b border-gray-200 bg-gray-100 px-4 py-3 text-left font-semibold text-gray-800">
                  {children}
                </th>
              ),

              td: ({ children }) => (
                <td className="border-b border-gray-100 px-4 py-3 text-gray-700">
                  {children}
                </td>
              ),

              code: ({ className, children, node }) => {
                const code = String(children).replace(/\n$/, "");
                const language = className?.replace("language-", "");
                const isInline = !className && !code.includes("\n");

                if (isInline) {
                  return (
                    <code className="rounded bg-gray-200 px-1.5 py-0.5 font-mono text-sm text-gray-800">
                      {children}
                    </code>
                  );
                }

                const codeIndex = code;

                return (
                  <div className="my-5 overflow-hidden rounded-lg border border-gray-200 bg-white">
                    <div className="flex items-center justify-between border-b border-gray-200 px-4 py-2">
                      <span className="text-xs font-medium uppercase text-gray-500">
                        {language || "code"}
                      </span>

                      <button
                        type="button"
                        onClick={() => handleCopy(codeIndex, codeIndex)}
                        className="text-xs font-medium text-blue-600 hover:text-blue-800"
                      >
                        {copiedCode === codeIndex ? "Copied!" : "Copy"}
                      </button>
                    </div>

                    <pre className="overflow-x-auto p-4 text-sm">
                      <code>{code}</code>
                    </pre>
                  </div>
                );
              },

              hr: () => <hr className="my-6 border-gray-200" />,
            }}
          >
            {answer}
          </ReactMarkdown>
        </div>
      </div>
    </div>
  );
}

export default AnswerCard;
