"use client";

import { SidebarInset } from "@/components/ui/sidebar";
import TabViewComponent from "../../_components/tab-view";
import Header from "../../_components/header";
import Overview from "../../_components/overview";
import rawNotebook from "./sample.json";
import NotebookViewer, { Notebook } from "../../_components/notebook-view";
import InputBox from "@/components/input-box";
import { FormEventHandler, useState } from "react";
import ReasoningBlock from "../../_components/reasoning-block";

const reasoningSteps = [
  "Let me think about this problem step by step.",
  "\n\nFirst, I need to understand what the user is asking for.",
  "\n\nThey want a reasoning component that opens automatically when streaming begins and closes when streaming finishes. The component should be composable and follow existing patterns in the codebase.",
  "\n\nThis seems like a collapsible component with state management would be the right approach.",
  "\n\nI should create a component that uses a controlled/uncontrolled pattern for flexibility. It needs to be aware of streaming state and handle auto-opening and closing based on that state. Most importantly, it should provide a smooth and intuitive user experience.",
  "\n\nThe component should be similar to how ChatGPT shows reasoning, with a clean and professional appearance that helps users understand the AI's thought process.",
].join("");

const MainScreen = () => {
  const notebook: Notebook = rawNotebook;

  const [text, setText] = useState<string>("");
  const [status, setStatus] = useState<
    "submitted" | "streaming" | "ready" | "error"
  >("ready");

  const onSubmit: FormEventHandler<HTMLFormElement> = (event) => {
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
    <SidebarInset className="w-full flex flex-col">
      <Header title="Financial Reseacher" />
      <TabViewComponent
        overview={
          <Overview
            title="Financial Researcher Crew"
            description="Our Crew combines a Senior Financial Researcher—digging deep
                  into company health, history, news and trends—with a Market
                  Analyst who transforms those insights into clear, actionable
                  reports."
            image="/crew/financial-researcher.svg"
          />
        }
        isTry={true}
        tryOut={
          <div className="w-full px-20 py-10 flex flex-col items-center gap-10">
            <InputBox
              text={text}
              setText={setText}
              status={status}
              setStatus={setStatus}
              onSubmit={onSubmit}
            />
            <div className="px-20 flex flex-col items-start justify-start w-full gap-4 ">
              <ReasoningBlock
                title="Financial Researcher Reasoning"
                reasoningSteps={reasoningSteps}
              />
            </div>
            {/* <ReasoningBlock company="Google" /> */}
          </div>
        }
        code={<NotebookViewer notebook={notebook} />}
      />
    </SidebarInset>
  );
};

export default MainScreen;
