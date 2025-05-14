import { useState, useEffect, useCallback } from "react";
import { useBlocksContext } from "../contexts/BlocksContext";
import { getCSRFToken } from "@/app/helpers/csrf";
const TestForm = ({ sessionData }) => {
  const [questionBlocks, setQuestionBlocks] = useState([]);
  const { selectedBlocks, setSelectedBlocks, addBlock, removeBlock } =
    useBlocksContext();

  const fetchQuestionBlocks = useCallback(async () => {
    let response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/question_blocks/`
    );
    let data = await response.json();
    console.log(data);

    const filteredData = data.filter(
      (block) => Array.isArray(block.prompt) && block.prompt.length > 0
    );

    setQuestionBlocks(filteredData);
  }, []);

  useEffect(() => {
    fetchQuestionBlocks();
  }, []);

  const isSelected = (questionId) => {
    return selectedBlocks.some((q) => q.id === questionId);
  };

  const submitToBackend = async () => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BACKEND_URL}/runtest`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          sessionId: sessionData.id,
          blocks: selectedBlocks,
        }),
      }
    );
    const data = await response.json();
    console.log(data);
  };
  return questionBlocks.length > 0 ? (
    <div className="card border-0">
      <div className="card-body">
        <h5 className="card-title text-center text-primary fw-bold">
          Blocchi di domande disponibili
        </h5>
        <ul
          className="list-group list-group-flush"
          style={{ maxHeight: "300px", overflowY: "auto" }}
        >
          {questionBlocks.map((block, index) => (
            <li
              key={index}
              className="list-group-item list-group-item-action rounded-3"
            >
              <div className="row">
                <div className="col-9">
                  <p className="fw-bold mb-1">Nome</p>
                  <p>{block.name}</p>
                </div>
                <div className="col-md-3 col-12">
                  {isSelected(block.id) ? (
                    <button
                      className="btn btn-outline-success rounded-5 w-100 mb-2"
                      onClick={(e) => {
                        e.preventDefault();
                        removeBlock(block.id);
                      }}
                    >
                      Rimuovi
                    </button>
                  ) : (
                    <button
                      className="btn btn-success rounded-5 w-100 mb-2"
                      onClick={(e) => {
                        e.preventDefault();
                        addBlock(block.id);
                      }}
                    >
                      Seleziona
                    </button>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
      <div className="row row-cols-1 mt-5 justify-content-center text-center">
        <div className="col-md-6 col-12">
          <button
            onClick={(e) => {
              e.preventDefault();
              submitToBackend();
            }}
            className="btn btn-outline-primary w-100 rounded-5"
          >
            Inizia il test
          </button>
        </div>
      </div>
    </div>
  ) : null;
};

export default TestForm;
