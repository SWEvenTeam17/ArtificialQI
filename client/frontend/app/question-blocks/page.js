"use client";
import { useEffect, useState } from "react";
import QuestionBlockContainer from "../components/containers/question-blocks/QuestionBlockContainer";
import Link from "next/link";
import { getCSRFToken } from "../helpers/csrf";

export default function QuestionBlocks() {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const fetchQuestionBlocks = async () => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`,
      {
        method: "GET",
      },
    );
    let parsed = await response.json();
    setQuestionBlocks(parsed);
  };

  const deleteQuestionBlock = async (id) => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/${id}/`,
      {
        method: "DELETE",
        headers: {
          "X-CSRFToken": getCSRFToken(),
        },
      },
    );

    if (response.status === 204) {
      setQuestionBlocks(questionBlocks.filter((block) => block.id !== id));
    }
  };

  useEffect(() => {
    fetchQuestionBlocks();
  }, []);
  return (
    <div className="container-fluid">
      <p className="fs-1 text-center"> Blocchi di domande</p>
      <div className="row justify-content-center text-center">
        <Link
          className="btn btn-outline-primary rounded-5 w-25 mb-5"
          href="/question-blocks/create"
        >
          Crea nuovo blocco
        </Link>
      </div>
      <div className="row row-cols-md-2 row-cols-1">
        {questionBlocks.map((block, index) => {
          return (
            <div className="col" key={index}>
              <QuestionBlockContainer block={block} onDelete={deleteQuestionBlock} />
            </div>
          );
        })}
      </div>
    </div>
  );
}
