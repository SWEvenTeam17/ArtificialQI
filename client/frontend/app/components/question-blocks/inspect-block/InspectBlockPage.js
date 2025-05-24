import React from "react";
import { useInspectBlockHook } from "@/app/components/hooks/QuestionBlocks/InspectBlockHook";
import TestResultsContainer from "../../containers/sessions/TestResults";
import BlockHeader from "./BlockHeader";
import PromptList from "./PromptList";

export default function InspectBlockPage({ id }) {
  const {
    blockData,
    testResults,
    uniqueId,
    loading,
    error,
    deletePrompt,
    handleView,
  } = useInspectBlockHook(id);

  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border text-primary" role="status" />
        <p className="mt-3">Caricamento in corso...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="alert alert-danger text-center mt-4" role="alert">
        {error}
      </div>
    );
  }

  return (
    <div className="container py-4">
      <BlockHeader name={blockData.name} promptCount={blockData.prompt?.length || 0} />

      <PromptList
        prompts={blockData.prompt}
        onDelete={deletePrompt}
        onView={handleView}
      />

      {testResults && (
        <TestResultsContainer key={uniqueId} testResults={testResults} />
      )}
    </div>
  );
}
