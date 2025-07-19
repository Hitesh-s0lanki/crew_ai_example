import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import { crewData } from "./data";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function getCrewById(id: string) {
  for (const crew of crewData) {
    if (crew.id === id) {
      return crew;
    }
  }

  return null;
}
