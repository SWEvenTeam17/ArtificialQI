import React from "react";
import QuestionBlockPresentational from "../../presentations/question-blocks/QuestionBlockPresentational";
export default function QuestionBlockContainer({ block, onDelete }) {
  return <QuestionBlockPresentational block={block} onDelete={onDelete} />;
}
