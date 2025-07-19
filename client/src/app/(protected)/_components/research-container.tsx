// components/ResearchContainer.tsx
import { useState, useRef, useEffect } from "react";
import EventPlayer, { EventItem } from "./event-player";
import InputBox from "@/components/input-box";
import { Crew } from "@/lib/data";
import { toast } from "sonner";

type Props = {
  crew: Crew;
};

const ResearchContainer = ({ crew }: Props) => {
  const [companyInput, setCompanyInput] = useState("");
  const [events, setEvents] = useState<EventItem[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [streaming, setStreaming] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  const handleSubmit = () => {
    const company = companyInput.trim();
    if (!company) return;

    // reset
    setEvents([]);
    setCurrentIndex(0);
    setStreaming(true);

    // open SSE once
    const es = new EventSource(
      `http://localhost:8000/stream/${crew.id}?input=${encodeURIComponent(
        company
      )}`
    );
    esRef.current = es;

    es.onmessage = (e) => {
      const payload: EventItem = JSON.parse(e.data);
      setEvents((prev) => [...prev, payload]);

      // close on final event
      if (payload.title === "Crew Output") {
        es.close();
      }
    };

    es.onerror = (err) => {
      console.error("SSE error", err);
      toast.error("Streaming error. Please try again.");
      setStreaming(false);
      es.close();
    };
  };

  // advance slide every 2s when there's a “next” event
  useEffect(() => {
    if (!streaming) return;
    if (currentIndex < events.length - 1) {
      const timer = setTimeout(() => setCurrentIndex((i) => i + 1), 2000);
      return () => clearTimeout(timer);
    }
  }, [events.length, currentIndex, streaming]);

  return (
    <div className="w-full px-5 md:px-20 lg:px-20 py-10 flex flex-col items-center gap-10">
      <InputBox
        text={companyInput}
        label={crew.input_type[0].label}
        placeholder={crew.input_type[0].placeholder}
        setText={setCompanyInput}
        status={streaming ? "streaming" : "ready"}
        setStatus={() => {}}
        onSubmit={handleSubmit}
      />

      <div className="px-5 md:px-20 lg:px-20 flex flex-col items-start justify-start w-full gap-4">
        {streaming && (
          <EventPlayer events={events} currentIndex={currentIndex} />
        )}
      </div>
    </div>
  );
};

export default ResearchContainer;
