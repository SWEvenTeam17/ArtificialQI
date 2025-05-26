import { QuestionBlockProvider } from "../components/contexts/QuestionBlockContext";

export default function Layout({ children }) {
  return <QuestionBlockProvider>{children}</QuestionBlockProvider>;
}
