"use client";

import {
  AIReasoning,
  AIReasoningContent,
  AIReasoningTrigger,
} from "@/components/ui/kibo-ui/ai/reasoning";
import { useEffect, useState } from "react";

interface Props {
  company: string;
}

const ReasoningBlock: React.FC<Props> = ({ company }) => {
  const [title, setTitle] = useState("Thinking");
  const [content, setContent] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);

  useEffect(() => {
    // kick off SSE when component mounts
    const es = new EventSource(
      `http://localhost:8000/stream/financial-researcher?company=${encodeURIComponent(
        company
      )}`
    );
    setIsStreaming(true);

    es.onmessage = (e) => {
      const { title, response } = JSON.parse(e.data) as {
        title: string;
        response: string;
      };

      // append each chunk
      setTitle(title);
      setContent(response);

      // once crew completes, stop streaming & close connection
      if (title === "Crew Completed") {
        setIsStreaming(false);
        es.close();
      }
    };

    es.onerror = () => {
      // on error, close and stop
      setIsStreaming(false);
      es.close();
    };

    return () => {
      es.close();
    };
  }, [company]);

  return (
    <div className="w-full p-4">
      <AIReasoning className="w-full" isStreaming={isStreaming}>
        <AIReasoningTrigger title={title} />
        <AIReasoningContent>{content}</AIReasoningContent>
      </AIReasoning>
    </div>
  );
};

export default ReasoningBlock;
