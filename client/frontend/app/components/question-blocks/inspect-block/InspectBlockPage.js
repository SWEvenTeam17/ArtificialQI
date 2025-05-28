import React from "react";
import { useInspectBlockHook } from "@/app/components/hooks/QuestionBlocks/InspectBlockHook";
import TestResults from "../../sessions/session-content/TestResults";
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
    handleEdit,
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
        onEdit={handleEdit}
      />

      {testResults && (
        <TestResults key={uniqueId} testResults={testResults} />
      )}
    </div>
  );
}
