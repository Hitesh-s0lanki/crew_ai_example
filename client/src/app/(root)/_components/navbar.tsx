"use client";

import { Button } from "@/components/ui/button";
import { SignInButton, useAuth, UserButton } from "@clerk/nextjs";
import Image from "next/image";
import Link from "next/link";

const Navbar = () => {
  const { isLoaded, isSignedIn } = useAuth();
  return (
    <nav className="relative flex items-center justify-between p-4 md:px-16 lg:px-24 xl:px-32 md:py-6 w-full ">
      <div className=" flex gap-2 items-center">
        <Image src={"/logo.png"} alt="logo" height={40} width={40} />
        <h1 className="text-xl font-semibold">Crewai</h1>
      </div>
      <div className="md:ml-auto md:justify-end justify-between flex items-center gap-x-2">
        {isLoaded && !isSignedIn && (
          <SignInButton mode="modal">
            <Button className=" rounded-full">Get Started</Button>
          </SignInButton>
        )}

        {isLoaded && isSignedIn && (
          <>
            <Button
              variant="outline"
              size="sm"
              className=" bg-transparent"
              asChild>
              <Link href="/home">Get Started</Link>
            </Button>
            <UserButton />
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
