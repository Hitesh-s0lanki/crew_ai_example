import FinancialResearcher from "./financial_researcher.json";
import Debater from "./debater.json";
import BookResearcher from "./book_researcher.json";
import EngineeringTeam from "./engineering_team.json";

export interface NotebookCell {
  id: string;
  cell_type: "code" | "markdown" | string;
  execution_count: number | null;
  source: string[];
}

export interface Notebook {
  cells: NotebookCell[];
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  metadata: Record<string, any>;
}

export type Crew = {
  id: string;
  name: string;
  description: string;
  image: string;
  code: Notebook;
  input_type: InputType[];
};

export type InputType = {
  type: "textarea" | "input";
  label: string;
  placeholder?: string;
  input: string;
};

export const crewData: Crew[] = [
  {
    id: "financial-researcher",
    name: "Financial Researcher Crew",
    description:
      "Our Crew combines a Senior Financial Researcher—digging deep into company health, history, news and trends—with a Market Analyst who transforms those insights into clear, actionable reports",
    image: "/crew/financial-researcher.svg",
    code: FinancialResearcher,
    input_type: [
      {
        type: "textarea",
        label: "Write the name of the Company.",
        placeholder: "Google",
        input: "motion",
      },
    ],
  },
  {
    id: "debater",
    name: "Debater Crew",
    description:
      "Our Crew combines a Senior Debater—crafting compelling arguments and counterpoints—with a Market Analyst who transforms those insights into clear, actionable reports",
    image: "/crew/debater.svg",
    code: Debater,
    input_type: [
      {
        type: "textarea",
        label: "Tell us about the motion.",
        placeholder: "There needs to be strict laws to regulate LLMs",
        input: "motion",
      },
    ],
  },
  {
    id: "book-researcher",
    name: "Book Researcher Crew",
    description:
      "Our Crew combines a Senior Book Researcher—digging deep into book trends, genres, and author insights—with a Market Analyst who transforms those insights into clear, actionable reports",
    image: "/crew/book_researcher.svg",
    code: BookResearcher,
    input_type: [
      {
        type: "textarea",
        label: "What genre of book are you interested in?",
        placeholder: "Fantasy",
        input: "genre",
      },
    ],
  },
  {
    id: "engineering-team",
    name: "Engineering Team Crew",
    description:
      "Our Crew combines a Senior Engineer—designing and implementing robust software solutions—with a Frontend Developer who crafts intuitive user interfaces, ensuring a seamless user experience gradio interface",
    image: "/crew/engineering_team.svg",
    code: EngineeringTeam,
    input_type: [
      {
        type: "textarea",
        label: "What is the project requirements with specifications module?",
        placeholder: `A simple account management system for a trading simulation platform. The system should allow users to create an account, deposit funds, and withdraw funds. The system should allow users to record that they have bought or sold shares, providing a quantity. The system should calculate the total value of the user's portfolio, and the profit or loss from the initial deposit. The system should be able to report the holdings of the user at any point in time. The system should be able to report the profit or loss of the user at any point in time. The system should be able to list the transactions that the user has made over time. The system should prevent the user from withdrawing funds that would leave them with a negative balance, or from buying more shares than they can afford, or selling shares that they don't have. The system has access to a function get_share_price(symbol) which returns the current price of a share, and includes a test implementation that returns fixed prices for AAPL, TSLA, GOOGL.`,
        input: "requirements",
      },
      {
        type: "input",
        label: "What is the module name?",
        placeholder:
          "A simple account management system for a trading simulation platform.",
        input: "module_name",
      },
    ],
  },
];
