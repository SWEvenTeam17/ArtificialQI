import { QuestionBlockProvider } from "../components/contexts/question-blocks/QuestionBlockContext";

export default function Layout({ children }) {
  return <QuestionBlockProvider>{children}</QuestionBlockProvider>;
}
