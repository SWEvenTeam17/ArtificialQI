"use client";
import { useResponse } from "@/app/components/contexts/ResponseContext";
import ResponseCard from "@/app/components/responses/ResponseCard";
import {
  BarChart,
  Bar,
  CartesianGrid,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

export default function ResultsPage() {
  const { responseData } = useResponse();

  const avgData = responseData.averages_by_llm
    ? Object.entries(responseData.averages_by_llm).map(([llmName, scores]) => ({
        llm_name: llmName,
        media_semantica: scores.avg_semantic_scores,
        media_esterna: scores.avg_external_scores,
      }))
    : [];

  return (
    <div className="container">
      <h2 className="text-center mb-1 mt-5">Risultati</h2>
      <div className="row row-cols-1 justify-content-center g-4 mb-5 p-5">
        {avgData && avgData.length > 0 ? (
          <>
            <div className="row row-cols-1 row-cols-lg-2 mb-5">
              <div className="col">
                <p className="text-center">Valutazione risultati semantici</p>
                <BarChart
                  layout="vertical"
                  width={600}
                  height={300}
                  data={avgData}
                  margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" domain={[0, 100]} />
                  <YAxis dataKey="llm_name" type="category" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="media_semantica" fill="#8884d8" name="Media Semantica" />
                </BarChart>
              </div>
              <div className="col">
                <p className="text-center">Valutazione risultati LLM Esterno</p>
                <BarChart
                  layout="vertical"
                  width={600}
                  height={300}
                  data={avgData}
                  margin={{ top: 20, right: 30, left: 100, bottom: 5 }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" domain={[0, 100]} />
                  <YAxis dataKey="llm_name" type="category" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="media_esterna" fill="#82ca9d" name="Media Esterna" />
                </BarChart>
              </div>
            </div>

            {responseData.results.map((response, index) => (
              <div className="col-12" key={index}>
                <ResponseCard response={response} />
              </div>
            ))}
          </>
        ) : (
          <p>No results available</p>
        )}
      </div>
    </div>
  );
}
