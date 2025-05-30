"use client";
import { InspectBlockProvider } from "@/app/components/contexts/question-blocks/InspectBlockContext";
import { TestFormContextProvider } from "@/app/components/contexts/session/test-form/TestFormContext";
import InspectBlockPage from "@/app/components/question-blocks/inspect-block/InspectBlockPage";
import { use } from "react";

export default function QuestionBlockInspect({ params }) {
  const { id } = use(params);

  return <InspectBlockProvider id={id}><InspectBlockPage /></InspectBlockProvider>;
}
