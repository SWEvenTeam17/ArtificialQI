"use client";
import { TestFormContextProvider } from "@/app/components/contexts/TestFormContext";
import InspectBlockPage from "@/app/components/question-blocks/inspect-block/InspectBlockPage";
import { use } from "react";

export default function QuestionBlockInspect({ params }) {
  const { id } = use(params);

  return <TestFormContextProvider><InspectBlockPage id={id} /></TestFormContextProvider>;
}
