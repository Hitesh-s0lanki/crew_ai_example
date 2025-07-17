import Example from "@/components/input-box";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Image from "next/image";
import NotebookViewer, { Notebook } from "./notebook-view";
import rawNotebook from "./sample.json";

type Props = {};

const TabViewComponent = ({}: Props) => {
  const notebook: Notebook = rawNotebook;
  return (
    <div className="flex w-full min-h-screen flex-col gap-6 p-5">
      <Tabs defaultValue="overview">
        <div className="w-full flex justify-center items-center">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="try">Try Out</TabsTrigger>
            <TabsTrigger value="code">Code</TabsTrigger>
          </TabsList>
        </div>
        <TabsContent value="overview">
          <div className="w-full flex flex-col justify-center items-center px-20">
            <div className="w-full rounded-2xl ">
              <div className="flex flex-col items-center justify-center text-center py-5 rounded-[15px]">
                {/* Title */}
                <h2 className="text-2xl font-medium mt-2">
                  Meet the <br />
                  <span className="bg-gradient-to-r from-primary to-red-400 bg-clip-text text-transparent text-4xl">
                    Financial Researcher Crew
                  </span>
                </h2>

                {/* Description */}
                <p className="text-slate-500 mt-2 max-w-full md:text-lg px-10">
                  Our Crew combines a Senior Financial Researcher—digging deep
                  into company health, history, news and trends—with a Market
                  Analyst who transforms those insights into clear, actionable
                  reports.
                </p>

                <Image
                  src={"/crew/financial-researcher.svg"}
                  alt="financial researcher"
                  height={700}
                  width={800}
                  className="mt-5"
                />
              </div>
            </div>
          </div>
        </TabsContent>
        <TabsContent value="try">
          <div className="w-full px-20 py-10">
            <Example />
          </div>
        </TabsContent>
        <TabsContent value="code">
          <div className="p-6  min-h-screen">
            <NotebookViewer notebook={notebook} />
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TabViewComponent;
