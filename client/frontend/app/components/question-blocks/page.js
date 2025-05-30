//New
"use client";

import QuestionBlockCard from "../question-blocks/QuestionBlockCard";

export default function Page() {
  const block = {
    id: 42,
    name: "Blocco di esempio",
    prompt: [
      { prompt_text: "Che ore sono?", expected_answer: "Sono le tre." },
      { prompt_text: "Che giorno è oggi?", expected_answer: "È giovedì." },
    ],
  };

  const emptyBlock = {
    id: 99,
    name: "Blocco vuoto",
    prompt: [],
  };

  const handleDelete = (id) => {
    console.log("Deleted block", id);
  };

  return (
    <div className="container mt-4">
      <QuestionBlockCard block={block} onDelete={handleDelete} />
      <QuestionBlockCard block={emptyBlock} onDelete={handleDelete} />
    </div>
  );
}
