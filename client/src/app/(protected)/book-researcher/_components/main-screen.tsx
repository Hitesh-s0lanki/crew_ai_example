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
      <Header title="Book Reseacher" />
      <TabViewComponent
        overview={
          <Overview
            title="Book Researcher Crew"
            description="Our Crew combines a Senior Financial Researcher—digging deep
                  into company health, history, news and trends—with a Market
                  Analyst who transforms those insights into clear, actionable
                  reports."
            image="/crew/financial-researcher.svg"
          />
        }
        isTry={true}
        code={<NotebookViewer notebook={notebook} />}
      />
    </SidebarInset>
  );
};

export default MainScreen;
