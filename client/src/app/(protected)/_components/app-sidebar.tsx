"use client";

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from "@/components/ui/sidebar";
import Link from "next/link";
import Image from "next/image";
import { BookOpenIcon, DollarSignIcon, Speech, ToolCase } from "lucide-react";
import { usePathname } from "next/navigation";
import UserButton from "./user-button";

// This is sample data.
const data = {
  navMain: [
    {
      title: "Prebuilt Crew",
      url: "#",
      items: [
        {
          title: "Financial Researcher",
          url: "/financial-researcher",
          icon: <DollarSignIcon className="size-4" />,
        },
        {
          title: "Debater",
          url: "/debater",
          icon: <Speech className="size-4" />,
        },
        {
          title: "Book Researcher",
          url: "/book-researcher",
          icon: <BookOpenIcon className="size-4" />,
        },
        {
          title: "Engineering Team",
          url: "/engineering-team",
          icon: <ToolCase className="size-4" />,
        },
      ],
    },
  ],
};

const AppSidebar = ({ ...props }: React.ComponentProps<typeof Sidebar>) => {
  const pathname = usePathname();

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <Link href="/" className="flex items-center gap-2 p-2">
          <Image src={"/logo.png"} alt="logo" height={60} width={60} />
          <span className="text-xl font-semibold pt-1">Agents</span>
        </Link>
      </SidebarHeader>
      <SidebarContent>
        {/* We create a SidebarGroup for each parent. */}
        {data.navMain.map((item) => (
          <SidebarGroup key={item.title}>
            <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {item.items.map((item) => (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      isActive={pathname.includes(item.url)}
                      asChild
                    >
                      <Link href={item.url} className="flex gap-2">
                        {item.icon}
                        {item.title}
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                ))}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarRail />
      <SidebarFooter>
        <UserButton />
      </SidebarFooter>
    </Sidebar>
  );
};

export default AppSidebar;
