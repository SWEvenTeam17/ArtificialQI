import React from "react";
import { BlocksContextProvider } from "../../contexts/BlocksContext";
import SessionLLMPanelContainer from "../../containers/sessions/SessionLLMPanelContainer";
import TestForm from "../../question-blocks/TestForm";

export default function SessionContentPresentational({sessionData}) {
  if (sessionData === null) {
    return (
      <div
        className="d-flex justify-content-center align-items-center"
        style={{ height: "100vh", backgroundColor: "#f8f9fa" }}
      >
        <div
          className="spinner-grow text-secondary"
          style={{ width: "6rem", height: "6rem" }}
          role="status"
        >
          <span className="visually-hidden">Loading...</span>
        </div>
      </div>
    );
  }

  return (
    <div className="container-fluid">
      <h1 className="text-center mt-3">
        Benvenuto alla sessione
        <span className="text-primary">{" " + sessionData.title}</span>
      </h1>

      <div className="row g-0 p-0 m-0">
        <div className="col-12">
          <div className="card border-0 h-100">
            <SessionLLMPanelContainer/>
          </div>
        </div>
        <BlocksContextProvider>
          <div className="col-12">
            <div className="row row-cols-1">
              <div className="col">
                <TestForm sessionData={sessionData} />
              </div>
            </div>
          </div>
        </BlocksContextProvider>
      </div>
    </div>
  );
}
