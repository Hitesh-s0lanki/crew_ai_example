"use client";

import { SidebarInset } from "@/components/ui/sidebar";
import TabViewComponent from "../../_components/tab-view";
import Header from "../../_components/header";
import Overview from "../../_components/overview";
import rawNotebook from "./sample.json";
import NotebookViewer, { Notebook } from "../../_components/notebook-view";

const MainScreen = () => {
  const notebook: Notebook = rawNotebook;
  return (
    <SidebarInset className="w-full flex flex-col">
      <Header title="Debater Crew" />
      <TabViewComponent
        overview={
          <Overview
            title="Debater Crew"
            description="Debate crew with a Debater agent that crafts concise, persuasive pro and con arguments on any motion and a Judge agent that objectively chooses the more convincing side."
            image="/crew/debater.svg"
          />
        }
        code={<NotebookViewer notebook={notebook} />}
      />
    </SidebarInset>
  );
};

export default MainScreen;
