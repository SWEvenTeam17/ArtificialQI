import { useState, useEffect } from "react";
import { getCSRFToken } from "@/app/helpers/csrf";
import {
  ResponsiveContainer,
  BarChart,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Bar,
} from "recharts";
import { useInspectBlockContext } from "../../contexts/question-blocks/InspectBlockContext";

export default function PromptResults() {
  const { testResults } = useInspectBlockContext();
  const [results, setResults] = useState(testResults.results);

  const handleDeleteRun = async (runId) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_runs/?run_id=${runId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      },
    );
    if (response.ok) {
      setResults((prevResults) =>
        prevResults.map((block) => ({
          ...block,
          results: block.results.filter((res) => res.run_id !== runId),
        })),
      );
    }
  };

  const getAvg = (semantic, external) =>
    (parseFloat(semantic) + parseFloat(external)) / 2;

  const getCardBgClass = (semantic, external) => {
    const avg = getAvg(semantic, external);
    if (avg > 75) return "bg-success bg-opacity-25";
    if (avg >= 40) return "bg-warning bg-opacity-25";
    return "bg-danger bg-opacity-25";
  };

  const allResults = results.flatMap((block) =>
    block.results.map((res) => ({
      ...res,
      block_name: block.block_name,
      avg: getAvg(res.semantic_evaluation, res.external_evaluation),
    })),
  );

  const summaryResults = [
    {
      result:
        allResults.length > 0
          ? allResults.reduce(
              (best, curr) => (curr.avg > best.avg ? curr : best),
              allResults[0],
            )
          : null,
      label: "Risultato migliore",
    },
    {
      result:
        allResults.length > 0
          ? allResults.reduce(
              (worst, curr) => (curr.avg < worst.avg ? curr : worst),
              allResults[0],
            )
          : null,
      label: "Risultato peggiore",
    },
  ];

  if (!results.length) {
    return <p className="text-center">Nessun risultato disponibile.</p>;
  }

  return (
    <div className="mt-5">
      <div className="row mb-4">
        {summaryResults.map(
          ({ result, label }, idx) =>
            result && (
              <div className="col-md-6 mb-3" key={label}>
                <div className="card h-100 shadow-sm">
                  <div
                    className={`card-body d-flex flex-column ${getCardBgClass(result.semantic_evaluation, result.external_evaluation)}`}
                  >
                    <h5 className="card-title text-primary">{label}</h5>
                    <p className="mb-1">
                      <strong>Blocco:</strong>
                      <br />
                      {result.block_name}
                    </p>
                    <p className="mb-1">
                      <strong>LLM:</strong>
                      <br />
                      {result.llm_name}
                    </p>
                    <p className="mb-1">
                      <strong>Domanda:</strong>
                      <br />
                      {result.question}
                    </p>
                    <p className="mb-1">
                      <strong>Risposta:</strong>
                      <br />
                      <span className="text-dark">{result.answer}</span>
                    </p>
                    <p className="mb-1">
                      <strong>Risposta attesa:</strong>
                      <br />
                      {result.expected_answer}
                    </p>
                    <div className="row text-center g-0 pt-3 mt-2">
                      <div className="col-12 col-md-6 d-flex align-items-center justify-content-center">
                        <div className="w-100">
                          <strong>Valutazione semantica</strong>
                          <div className="mt-2">
                            <span className="badge text-dark fs-5">
                              {result.semantic_evaluation}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="col-12 col-md-6 d-flex align-items-center justify-content-center">
                        <div className="w-100">
                          <strong>Valutazione esterna</strong>
                          <div className="mt-2">
                            <span className="badge text-dark fs-5">
                              {result.external_evaluation}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ),
        )}
      </div>
      {results.map((block, index) => (
        <div key={index} className="mb-5">
          <h3 className="text-center text-primary">{block.block_name}</h3>

          <h5 className="mt-4 mb-3">Risposte dettagliate</h5>
          <div className="row row-cols-1 row-cols-md-2 g-4">
            {block.results.map((res, i) => (
              <div className="col" key={i}>
                <div className="card h-100 shadow-sm">
                  <div
                    className={`card-body d-flex flex-column ${getCardBgClass(res.semantic_evaluation, res.external_evaluation)}`}
                  >
                    <h5 className="card-title text-primary">{res.llm_name}</h5>
                    <p className="mb-1">
                      <strong>Domanda:</strong>
                      <br />
                      {res.question}
                    </p>
                    <p className="mb-1">
                      <strong>Risposta:</strong>
                      <br />
                      <span className="text-dark">{res.answer}</span>
                    </p>
                    <p className="mb-1">
                      <strong>Risposta attesa:</strong>
                      <br />
                      {res.expected_answer}
                    </p>
                    <div className="row text-center g-0 pt-3 mt-2">
                      <div className="col-12 col-md-6 d-flex align-items-center justify-content-center">
                        <div className="w-100">
                          <strong>Valutazione semantica</strong>
                          <div className="mt-2">
                            <span className="badge text-dark fs-5">
                              {res.semantic_evaluation}
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="col-12 col-md-6 d-flex align-items-center justify-content-center">
                        <div className="w-100">
                          <strong>Valutazione esterna</strong>
                          <div className="mt-2">
                            <span className="badge text-dark fs-5">
                              {res.external_evaluation}
                            </span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="card-footer text-end">
                    <button
                      className="btn btn-outline-danger btn-sm"
                      onClick={() => handleDeleteRun(res.run_id)}
                    >
                      Elimina run
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <h5 className="mt-5">Media valutazioni per LLM</h5>
          <ResponsiveContainer
            width="100%"
            height={300}
            margin={{ top: 0, right: 0, left: 20, bottom: 0 }}
          >
            <BarChart
              layout="vertical"
              data={Object.entries(block.averages_by_llm).map(
                ([llm, scores]) => ({
                  name: llm,
                  semantic: scores.avg_semantic_scores,
                  external: scores.avg_external_scores,
                }),
              )}
              margin={{ top: 5, right: 30, left: 30, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 1]} />
              <YAxis dataKey="name" type="category" />
              <Tooltip />
              <Legend />
              <Bar dataKey="semantic" fill="#8884d8" name="Semantica" />
              <Bar dataKey="external" fill="#82ca9d" name="Esterna" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      ))}
    </div>
  );
}
