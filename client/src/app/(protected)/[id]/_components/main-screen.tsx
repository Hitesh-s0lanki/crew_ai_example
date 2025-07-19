"use client";

import { SidebarInset } from "@/components/ui/sidebar";
import TabViewComponent from "../../_components/tab-view";
import Header from "../../_components/header";
import Overview from "../../_components/overview";
import NotebookViewer from "../../_components/notebook-view";
import ResearchContainer from "../../_components/research-container";
import { getCrewById } from "@/lib/utils";

type Props = {
  id: string;
};

const MainScreen = ({ id }: Props) => {
  const crew = getCrewById(id);

  if (!crew) {
    return (
      <div className="p-4 flex justify-center items-center">Crew not found</div>
    );
  }

  return (
    <SidebarInset className="w-full flex flex-col">
      <Header title={crew.name} />
      <TabViewComponent
        overview={
          <Overview
            title={crew.name}
            description={crew.description}
            image={crew.image}
          />
        }
        isTry={true}
        tryOut={<ResearchContainer crew={crew} />}
        code={<NotebookViewer notebook={crew.code} />}
      />
    </SidebarInset>
  );
};

export default MainScreen;
