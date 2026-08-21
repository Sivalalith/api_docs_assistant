import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function AnswerCard({ answer, setQuery, setIsSuggestionClicked }) {
  const [copiedCode, setCopiedCode] = useState(null);

  const handleCopy = async (code, index) => {
    await navigator.clipboard.writeText(code);
    setCopiedCode(index);

    setTimeout(() => {
      setCopiedCode(null);
    }, 1500);
  };

  // Modern Industry-Level "Bento Box" Empty State (Triggered when no answer exists)
  if (!answer) {
    return (
      <div className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-slate-900">Answer</h2>
        <div className="rounded-xl border border-slate-200/80 bg-white p-8 shadow-[0_8px_30px_rgb(0,0,0,0.02)]">
          <div className="text-center py-6">
            <div className="mx-auto w-12 h-12 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center text-xl mb-4 shadow-inner">
              ✨
            </div>
            <h3 className="text-base font-semibold text-slate-900">
              Ready to Analyze
            </h3>
            <p className="text-sm text-slate-500 max-w-sm mx-auto mt-1">
              Upload documents on the left and ask a question to generate code
              structures or documentation.
            </p>
          </div>

          {/* Render Suggestions only if setQuestion hook is provided from parent */}
          {setQuery && (
            <div className="mt-4 pt-6 border-t border-slate-100">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-3">
                ⚡ Quick Suggestions
              </h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => {
                    setQuery("How can a user log in?");
                    setIsSuggestionClicked(true);
                  }}
                  className="text-left text-xs p-3.5 rounded-xl border border-slate-100 bg-slate-50/60 hover:bg-blue-50/40 hover:border-blue-200 text-slate-500 hover:text-blue-700 transition-all duration-200 hover:scale-[1.01] active:scale-[0.99]"
                >
                  <span className="font-semibold block mb-0.5 text-slate-800 hover:text-blue-800">
                    User Login API
                  </span>
                  "How can a user log in?..."
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setQuery("List all the possible status of pets");
                    setIsSuggestionClicked(true);
                  }}
                  className="text-left text-xs p-3.5 rounded-xl border border-slate-100 bg-slate-50/60 hover:bg-blue-50/40 hover:border-blue-200 text-slate-500 hover:text-blue-700 transition-all duration-200 hover:scale-[1.01] active:scale-[0.99]"
                >
                  <span className="font-semibold block mb-0.5 text-slate-800 hover:text-blue-800">
                    Pet Status
                  </span>
                  "List all the possible status of pets..."
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    );
  }

  // Active State (Triggered when an answer exists)
  return (
    <div className="mt-6">
      <h2 className="mb-3 text-xl font-semibold text-gray-900">Answer</h2>

      <div className="rounded-xl border border-blue-200 bg-blue-50 p-6 max-h-[550px] overflow-y-auto">
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
