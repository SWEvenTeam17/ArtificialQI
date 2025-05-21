import React from "react";
import PromptCardContainer from "../../containers/question-blocks/PromptCardContainer";

export default function InspectBlockPagePresentational({
  loading,
  error,
  blockData,
  setBlockdata,
}) {
  if (loading) {
    return (
      <div className="text-center mt-5">
        <div className="spinner-border text-primary" role="status"></div>
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
      <div className="text-center mb-4">
        <h1 className="text-primary">Blocco: {blockData.name}</h1>
        <h4 className="text-muted">
          Contiene {blockData.prompt?.length || 0} prompt
        </h4>
      </div>

      <div className="row row-cols-1 row-cols-md-2 g-4">
        {blockData.prompt?.map((prompt, index) => (
          <div className="col" key={index}>
            <PromptCardContainer
              blockData={blockData}
              setBlockData={setBlockdata}
              prompt={prompt}
            />
          </div>
        ))}
      </div>
    </div>
  );
}
