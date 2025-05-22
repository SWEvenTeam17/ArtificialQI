import React from 'react'
import { useState } from 'react';
import TestResultsPresentational from '../../presentations/sessions/TestResultsPresentational'
import { getCSRFToken } from '@/app/helpers/csrf';
export default function TestResultsContainer({testResults}) {
  const [results, setResults] = useState(testResults.results);
  
    const handleDeleteRun = async (runId) => {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/prompt_runs?run_id=${runId}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken(),
          },
        }
      );
      if (response.ok) {
        setResults((prevResults) =>
          prevResults.map((block) => ({
            ...block,
            results: block.results.filter((res) => res.run_id !== runId),
          }))
        );
      }
    };
  return (
    <TestResultsPresentational results={results} handleDeleteRun={handleDeleteRun} testResults={testResults}/>
  )
}
