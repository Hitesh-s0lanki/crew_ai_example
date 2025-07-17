"use client";

import {
  AIInput,
  AIInputButton,
  AIInputSubmit,
  AIInputTextarea,
  AIInputToolbar,
  AIInputTools,
} from "@/components/ui/kibo-ui/ai/input";
import { MicIcon, PlusIcon } from "lucide-react";
import { type FormEventHandler, useState } from "react";

const Example = () => {
  const [text, setText] = useState<string>("");
  const [status, setStatus] = useState<
    "submitted" | "streaming" | "ready" | "error"
  >("ready");
  const handleSubmit: FormEventHandler<HTMLFormElement> = (event) => {
    event.preventDefault();
    if (!text) {
      return;
    }
    setStatus("submitted");
    setTimeout(() => {
      setStatus("streaming");
    }, 200);
    setTimeout(() => {
      setStatus("ready");
    }, 2000);
  };
  return (
    <AIInput onSubmit={handleSubmit}>
      <AIInputTextarea
        onChange={(e) => setText(e.target.value)}
        value={text}
        placeholder="Write the name of the Company"
      />
      <AIInputToolbar>
        <AIInputTools>
          <AIInputButton>
            <PlusIcon size={16} />
          </AIInputButton>
          <AIInputButton>
            <MicIcon size={16} />
          </AIInputButton>
        </AIInputTools>
        <AIInputSubmit disabled={!text} status={status} />
      </AIInputToolbar>
    </AIInput>
  );
};
export default Example;
