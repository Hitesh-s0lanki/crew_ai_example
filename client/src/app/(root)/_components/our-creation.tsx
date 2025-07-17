import Image from "next/image";
import React from "react";

const galleryItems = [
  {
    src: "/financial_researcher_crew.png",
    alt: "Financial Researcher Crew",
    title: "Financial Researcher Crew",
    description: "Research the company and prepare Financial report Out of it.",
  },
];

const OurCreation = () => (
  <section className="py-20 px-4">
    <h1 className="text-3xl font-semibold text-center mx-auto">
      Our Latest Creations
    </h1>
    <p className="text-sm text-slate-500 text-center mt-2 max-w-lg mx-auto">
      A visual collection of our most recent works — each piece crafted with
      intention, emotion, and style.
    </p>

    <div className="flex flex-wrap items-center justify-center mt-12 gap-4 max-w-5xl mx-auto">
      {galleryItems.map(({ src, alt, title, description }, idx) => (
        <div key={idx} className="relative group rounded-lg overflow-hidden">
          <Image
            src={src}
            alt={alt}
            height={150}
            width={150}
            className="size-64 object-cover object-top"
          />
          <div className="absolute inset-0 flex flex-col gap-2 justify-end p-4 text-white bg-black/50 opacity-0 group-hover:opacity-100 transition-all duration-300">
            <h2 className="text-sm font-medium">{title}</h2>
            <p className="text-xs">{description}</p>
          </div>
        </div>
      ))}
    </div>
  </section>
);

export default OurCreation;
