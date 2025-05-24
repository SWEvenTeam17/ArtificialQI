"use client";
import InspectBlockPage from "@/app/components/question-blocks/inspect-block/InspectBlockPage";
import { use } from "react";

export default function QuestionBlockInspect({ params }) {
  const { id } = use(params);

  return <InspectBlockPage id={id} />;
}
