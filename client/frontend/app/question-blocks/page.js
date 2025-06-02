"use client";
import QuestionBlockCard from "../components/question-blocks/QuestionBlockCard";
import { useQuestionBlockContext } from "../components/contexts/question-blocks/QuestionBlockContext";
import Link from "next/link";

export default function QuestionBlocks() {
  const { questionBlocks, deleteQuestionBlock } = useQuestionBlockContext();

  return (
    <div className="container-fluid">
      <p className="fs-1 text-center">Blocchi di domande</p>
      <div className="row justify-content-center text-center">
        <Link
          className="btn btn-outline-primary rounded-5 w-25 mb-5"
          href="/question-blocks/create"
        >
          Crea nuovo blocco
        </Link>
      </div>
      <div className="row row-cols-md-2 row-cols-1">
        {questionBlocks.map((block, index) => (
          <div className="col" key={index}>
            <QuestionBlockCard block={block} onDelete={deleteQuestionBlock} />
          </div>
        ))}
      </div>
    </div>
  );
}
