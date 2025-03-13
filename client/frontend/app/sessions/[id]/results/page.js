"use client";
import { useResponse } from "@/app/components/contexts/ResponseContext";
import ResponseCard from "@/app/components/responses/ResponseCard";

export default function ResultsPage() {
  const { responseData } = useResponse();
  console.log("risposta=", responseData);
  const sortedResponseData = responseData
    ? responseData.sort((a, b) => a.llm_name.localeCompare(b.llm_name))
    : [];

  return (
    <div className="container">
      <h2 className="text-center mb-1 mt-5">Risultati</h2>
      <div className="row row-cols-1 justify-content-center g-4 mb-5 p-5">
        {sortedResponseData && sortedResponseData.length > 0 ? (
          sortedResponseData.map((response, index) => (
            <div className="col-12" key={index}>
              <ResponseCard response={response} />
            </div>
          ))
        ) : (
          <p>No results available</p>
        )}
      </div>
    </div>
  );
}
