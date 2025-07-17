import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import Image from "next/image";

type Props = {
  overview: React.ReactNode;
  tryOut?: React.ReactNode;
  code: React.ReactNode;
  isTry?: boolean;
};

const TabViewComponent = ({ overview, code, isTry }: Props) => {
  return (
    <div className="flex w-full min-h-screen flex-col gap-6 p-5">
      <Tabs defaultValue="overview">
        <div className="w-full flex justify-center items-center">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            {isTry && <TabsTrigger value="try">Try Out</TabsTrigger>}
            <TabsTrigger value="code">Code</TabsTrigger>
          </TabsList>
        </div>
        <TabsContent value="overview">{overview}</TabsContent>
        {/* <TabsContent value="try">
          <div className="w-full px-20 py-10">
            <Example />
            <ReasoningBlock company="Google" />
          </div>
        </TabsContent> */}
        <TabsContent value="code">
          <div className="p-5  min-h-screen">{code}</div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default TabViewComponent;
