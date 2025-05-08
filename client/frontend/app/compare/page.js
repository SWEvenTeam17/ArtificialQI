"use client";
import { useState } from "react";
import LLMComparator from "@/app/components/comparators/LLMComparator";
import QuestionComparator from "@/app/components/comparators/QuestionComparator";

export default function Compare() {
  const [selectedComparison, setSelectedComparison] = useState("LLM");
  return (
    <div className="container py-4">
      <p className="text-center fs-3 fw-semibold">
        Seleziona un metodo di confronto:
      </p>
      <div className="row row-cols-2 g-3 mt-3 justify-content-center">
        <div className="col d-grid">
          <button
            onClick={(e) => {
              setSelectedComparison("LLM");
            }}
            className={
              selectedComparison === "LLM"
                ? `btn btn-primary btn-lg`
                : `btn btn-outline-primary btn-lg`
            }
          >
            Confronto tra LLM
          </button>
        </div>
        <div className="col d-grid">
          <button
            onClick={(e) => {
              setSelectedComparison("Question");
            }}
            className={
              selectedComparison === "Question"
                ? `btn btn-primary btn-lg`
                : `btn btn-outline-primary btn-lg`
            }
          >
            Confronto tra Domande
          </button>
        </div>
      </div>
      {selectedComparison === "LLM" ? (
        <LLMComparator />
      ) : (
        <QuestionComparator />
      )}
    </div>
  );
}
