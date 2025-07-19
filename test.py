import json
import requests

def save_sse_events_to_json(company: str, output_file: str = "output.json"):
    """
    Connects to the SSE endpoint for a company, collects all events,
    and saves them to a JSON file.
    """
    url = f"http://localhost:8000/stream/financial-researcher?company={company}"
    headers = {
        "Accept": "text/event-stream"
    }

    events = []

    with requests.get(url, headers=headers, stream=True) as response:
        if response.status_code != 200:
            raise Exception(f"Failed to connect: {response.status_code} - {response.text}")

        print(f"📡 Connected to SSE stream for company '{company}'...")

        for line in response.iter_lines(decode_unicode=True):
            if line.startswith("data: "):
                try:
                    payload = json.loads(line.replace("data: ", ""))
                    events.append(payload)
                    print(f"✅ Event received: {payload['title']}")
                    if payload.get("title") == "Crew Output":
                        break
                except json.JSONDecodeError:
                    print(f"⚠️ Failed to parse line: {line}")

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(events, f, indent=2, ensure_ascii=False)

    print(f"💾 All {len(events)} events saved to {output_file}")


# Example usage
if __name__ == "__main__":
    save_sse_events_to_json("26ideas", "26ideas_events.json")
