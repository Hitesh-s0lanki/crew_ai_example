"use client";

import { Button } from "@/components/ui/button";
import { SignInButton, useAuth } from "@clerk/nextjs";
import { ChevronRight } from "lucide-react";
import React from "react";
import TrustedBrands from "./trusted-brands";
import Link from "next/link";

const Hero = () => {
  const { isLoaded, isSignedIn } = useAuth();
  return (
    <section className="pt-40 md:pt-32 text-center px-4">
      {/* Headline */}
      <h1 className="text-4xl md:text-6xl font-semibold max-w-[800px] mx-auto mt-8">
        Meet Crewai Agents
      </h1>
      <p className="text-lg mx-auto max-w-2xl mt-4">
        Crewai Agents are AI-powered assistants that can automate tasks,
        streamline workflows, and integrate seamlessly into your existing
        systems.
      </p>

      {/* CTAs */}
      <div className="mx-auto w-full flex flex-col md:flex-row items-center justify-center gap-4 mt-10">
        {isLoaded && !isSignedIn && (
          <>
            <SignInButton mode="modal">
              <Button>Get Started</Button>
            </SignInButton>
            <SignInButton mode="modal">
              <Button variant={"outline"}>
                Learn More
                <ChevronRight className="ml-2 size-4" />
              </Button>
            </SignInButton>
          </>
        )}

        {isLoaded && isSignedIn && (
          <Button asChild>
            <Link href="/home">Get Started</Link>
          </Button>
        )}
      </div>
      <TrustedBrands />
    </section>
  );
};

export default Hero;
