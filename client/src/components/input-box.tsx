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
import { type FormEventHandler } from "react";

type Props = {
  text: string;
  label: string;
  placeholder?: string;
  setText: (text: string) => void;
  status: "submitted" | "streaming" | "ready" | "error" | "done";
  setStatus: (
    status: "submitted" | "streaming" | "ready" | "error" | "done"
  ) => void;
  onSubmit: FormEventHandler<HTMLFormElement>;
};

const InputBox = ({
  text,
  label,
  placeholder,
  setText,
  status,
  setStatus,
  onSubmit,
}: Props) => {
  const handleSubmit: FormEventHandler<HTMLFormElement> = (e) => {
    e.preventDefault();
    setStatus("done");
    onSubmit(e);
  };
  return (
    <div className="w-full md:w-1/2 lg:w-2/3 flex flex-col gap-6 justify-center items-center py-10">
      <h1 className=" text-xl text-center ">{label}</h1>
      <AIInput onSubmit={handleSubmit}>
        <AIInputTextarea
          onChange={(e) => setText(e.target.value)}
          value={text}
          placeholder={placeholder}
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
    </div>
  );
};
export default InputBox;
