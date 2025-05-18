"use client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function TestResults({ testResults }) {
  return (
    <div className="mt-5">
      {testResults.results.map((block, index) => (
        <div key={index} className="mb-5">
          <h3 className="text-center text-primary">{block.block_name}</h3>

          <h5 className="mt-4 mb-3">Risposte dettagliate</h5>
          <div className="row row-cols-1 row-cols-md-2 g-4">
            {block.results.map((res, i) => (
              <div className="col" key={i}>
                <div className="card h-100 shadow-sm">
                  <div className="card-body">
                    <h5 className="card-title text-primary">{res.llm_name}</h5>
                    <p className="mb-1">
                      <strong>Domanda:</strong><br />
                      {res.question}
                    </p>
                    <p className="mb-1">
                      <strong>Risposta:</strong><br />
                      <span className="text-dark">{res.answer}</span>
                    </p>
                    <p className="mb-1">
                      <strong>Risposta attesa:</strong><br />
                      {res.expected_answer}
                    </p>
                    <p className="mb-1">
                      <strong>Valutazione semantica:</strong>{" "}
                      <span className="badge text-dark">{res.semantic_evaluation}</span>
                    </p>
                    <p className="mb-0">
                      <strong>Valutazione esterna:</strong>{" "}
                      <span className="badge text-dark">{res.external_evaluation}</span>
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <h5 className="mt-5">Media valutazioni per LLM</h5>
          <ResponsiveContainer width="100%" height={300} margin={{ top: 0, right: 0, left: 20, bottom: 0 }}>
            <BarChart
              layout="vertical"
              data={Object.entries(block.averages_by_llm).map(
                ([llm, scores]) => ({
                  name: llm,
                  semantic: scores.avg_semantic_scores,
                  external: scores.avg_external_scores,
                })
              )}
              margin={{ top: 5, right: 30, left: 
                30, bottom: 5 }}
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
