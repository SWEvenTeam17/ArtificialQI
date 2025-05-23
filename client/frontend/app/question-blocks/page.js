"use client";
import Link from "next/link";
import QuestionBlockCard from "../components/question-blocks/QuestionBlockCard";
import BlockListHook from "../components/hooks/QuestionBlocks/BlockListHook";

export default function QuestionBlocks() {
  const { questionBlocks } = BlockListHook();

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
        {questionBlocks.map((block) => (
          <div className="col" key={block.id}>
            <QuestionBlockCard
              block={block}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
