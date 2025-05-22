"use client";
import InspectBlockPageContainer from "@/app/components/containers/question-blocks/InspectBlockPageContainer";
import { use } from "react";

export default function QuestionBlockInspect({ params }) {
  const { id } = use(params);

  return <InspectBlockPageContainer id={id} />;
}
