"use client";

import Example from "@/components/input-box";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import Image from "next/image";
import TabViewComponent from "../../_components/tab-view";

const MainScreen = () => {
  return (
    <SidebarInset className="w-full flex flex-col">
      <header className="flex h-16 shrink-0 items-center gap-2 border-b px-4">
        <SidebarTrigger className="-ml-1" />
        <Separator
          orientation="vertical"
          className="mr-2 data-[orientation=vertical]:h-4"
        />
        <Breadcrumb>
          <BreadcrumbList>
            <BreadcrumbItem className="hidden md:block">
              <BreadcrumbLink href="/">Home</BreadcrumbLink>
            </BreadcrumbItem>
            <BreadcrumbSeparator className="hidden md:block" />
            <BreadcrumbItem>
              <BreadcrumbPage>Financial Reseacher</BreadcrumbPage>
            </BreadcrumbItem>
          </BreadcrumbList>
        </Breadcrumb>
      </header>
      <TabViewComponent />
      {/* <div className="p-10 w-full flex flex-col gap-10 justify-center items-center">
        <Image
          src={"/crew/financial-researcher.svg"}
          alt="financial researcher"
          height={700}
          width={800}
        />
        <div className="w-1/2">
          <Example />
        </div>
      </div> */}
    </SidebarInset>
  );
};

export default MainScreen;
