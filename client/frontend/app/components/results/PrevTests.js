"use client";

import { getCSRFToken } from "@/app/helpers/csrf";
import { useTestFormContext } from "../contexts/session/test-form/TestFormContext";

function formatTimestamp(ts) {
  const date = new Date(ts);
  return date.toLocaleString("it-IT", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
}

export default function PrevTests() {
  const { prevTests, setPrevTests, handlePrevTestClick } = useTestFormContext();
  const handleDelete = async (testId) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/previous_tests/${testId}/`,
      {
        method: "DELETE",
        headers: {
          "Content-type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      },
    );
    if (response.ok) {
      setPrevTests(prevTests.filter((test) => test.id !== testId));
    }
  };

  return (
    <div className="container p-5">
      <h3 className="text-center text-primary">Test precedenti</h3>
      {prevTests.length === 0 ? (
        <p className="fs-5 text-center p-5">Nessun test precedente trovato.</p>
      ) : (
        <div className="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-3 mt-2">
          {prevTests.map((test) => (
            <div className="col" key={test.id}>
              <div
                className="card h-100 shadow-sm"
                style={{ cursor: "pointer", userSelect: "none" }}
                onClick={() => handlePrevTestClick && handlePrevTestClick(test)}
                onMouseDown={(e) => e.preventDefault()}
              >
                <div className="card-body">
                  <h5 className="card-title text-primary">Test #{test.id}</h5>
                  <p className="mb-1">
                    <strong>Insieme di domande:</strong>
                    <br />
                    <span className="text-dark">{test.block.name}</span>
                  </p>
                  <p className="mb-1">
                    <strong>Data e ora:</strong>
                    <br />
                    <span className="text-dark">
                      {formatTimestamp(test.timestamp)}
                    </span>
                  </p>
                </div>
                <div className="card-footer text-end">
                  <button
                    className="btn btn-outline-danger btn-sm"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDelete(test.id);
                    }}
                  >
                    Elimina
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
