import { crewData } from "@/lib/data";
import Image from "next/image";
import React from "react";

const OurCreation = () => (
  <section className="py-20 px-4">
    <h1 className="text-3xl font-semibold text-center mx-auto">
      Our Latest Creations
    </h1>
    <p className="text-sm text-slate-500 text-center mt-2 max-w-lg mx-auto">
      A visual collection of our most recent works — each piece crafted with
      intention, emotion, and style.
    </p>

    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 mt-8 px-5 md:px-20 lg:px-40">
      {crewData.map(({ image, name, description }, idx) => (
        <div key={idx} className="relative group rounded-lg overflow-hidden">
          <Image
            src={image}
            alt={name}
            height={150}
            width={250}
            className="w-full object-cover object-top"
          />
          <div className="absolute inset-0 flex flex-col gap-2 justify-end p-4 text-white bg-black/50 opacity-0 group-hover:opacity-100 transition-all duration-300">
            <h2 className="text-sm font-medium">{name}</h2>
            <p className="text-xs">{description}</p>
          </div>
        </div>
      ))}
    </div>
  </section>
);

export default OurCreation;
