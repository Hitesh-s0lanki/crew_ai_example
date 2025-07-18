"use client";

import {
  AIReasoning,
  AIReasoningContent,
  AIReasoningTrigger,
} from "@/components/ui/kibo-ui/ai/reasoning";
import { useCallback, useEffect, useState } from "react";

type Props = {
  title?: string;
  reasoningSteps: string;
};

const ReasoningBlock = ({ title = "Thinking...", reasoningSteps }: Props) => {
  const [content, setContent] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentTokenIndex, setCurrentTokenIndex] = useState(0);
  const [tokens, setTokens] = useState<string[]>([]);

  // Function to chunk text into fake tokens of 3-4 characters
  const chunkIntoTokens = useCallback((text: string): string[] => {
    const tokens: string[] = [];
    let i = 0;
    while (i < text.length) {
      const chunkSize = Math.floor(Math.random() * 2) + 3; // Random size between 3-4
      tokens.push(text.slice(i, i + chunkSize));
      i += chunkSize;
    }
    return tokens;
  }, []);

  useEffect(() => {
    const tokenizedSteps = chunkIntoTokens(reasoningSteps);
    setTokens(tokenizedSteps);
    setContent("");
    setCurrentTokenIndex(0);
    setIsStreaming(true);
  }, [chunkIntoTokens, reasoningSteps]);

  useEffect(() => {
    if (!isStreaming || currentTokenIndex >= tokens.length) {
      if (isStreaming) {
        setIsStreaming(false);
      }
      return;
    }
    const timer = setTimeout(() => {
      setContent((prev) => prev + tokens[currentTokenIndex]);
      setCurrentTokenIndex((prev) => prev + 1);
    }, 25); // Faster interval since we're streaming smaller chunks
    return () => clearTimeout(timer);
  }, [isStreaming, currentTokenIndex, tokens]);

  return (
    <div className="w-full p-4">
      <AIReasoning title={title} className="w-full" isStreaming={isStreaming}>
        <AIReasoningTrigger />
        <AIReasoningContent>{content}</AIReasoningContent>
      </AIReasoning>
    </div>
  );
};
export default ReasoningBlock;
