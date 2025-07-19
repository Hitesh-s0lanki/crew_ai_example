import { Notebook } from "@/lib/data";
import React from "react";
import SyntaxHighlighter from "react-syntax-highlighter";
import { docco } from "react-syntax-highlighter/dist/esm/styles/hljs";

interface NotebookViewerProps {
  notebook: Notebook;
}

const NotebookViewer: React.FC<NotebookViewerProps> = ({ notebook }) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {notebook.cells.map((cell, idx) => (
        <div
          key={cell.id || idx}
          className="bg-white rounded-lg shadow overflow-hidden"
        >
          {/* Header */}
          <div className="px-4 py-2 bg-gray-50 border-b border-gray-200 flex justify-between items-center">
            <span className="text-xs font-medium text-gray-600 uppercase">
              {cell.cell_type} cell
            </span>
            {cell.cell_type === "code" && (
              <span className="text-xs text-gray-500">
                Exec Count: {cell.execution_count ?? "–"}
              </span>
            )}
          </div>

          {/* Content */}
          {cell.cell_type === "code" ? (
            <SyntaxHighlighter
              language="python"
              style={docco}
              className="p-4 overflow-auto"
            >
              {cell.source.join("")}
            </SyntaxHighlighter>
          ) : (
            <div className="p-4 prose prose-sm">
              {cell.source.map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default NotebookViewer;
