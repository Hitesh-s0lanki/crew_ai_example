import ReasoningBlock from "./reasoning-block";

export interface EventItem {
  title: string;
  type: string;
  response?: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  [key: string]: any;
}

interface EventPlayerProps {
  events: EventItem[];
  currentIndex: number;
}

function humanize(key: string) {
  // e.g. "top_novelists" → "Top Novelists"
  return key.replace(/_/g, " ").replace(/\b\w/g, (l) => l.toUpperCase());
}

const EventPlayer: React.FC<EventPlayerProps> = ({ events, currentIndex }) => {
  if (events.length === 0) return <div>Waiting for events…</div>;

  const current = events[currentIndex];

  // 2) decide what text to show
  let body: string;
  if (current.response) {
    body = current.response;
  } else {
    // gather all other fields except title/type
    const sections = Object.entries(current)
      .filter(([k]) => !["title", "type"].includes(k))
      .map(([k, v]) => `## ${humanize(k)}\n\n${String(v).trim()}`);
    body = sections.join("\n\n");
  }

  // 3) if it really is an error type, show inline… otherwise render reasoning
  if (current.type === "error") {
    return (
      <div className="p-4 bg-red-50 text-red-700 rounded">
        <strong>Error:</strong> {body}
      </div>
    );
  }

  return <ReasoningBlock title={current.title} reasoningSteps={body} />;
};

export default EventPlayer;
