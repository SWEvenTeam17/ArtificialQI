import { useTestFormContext } from "@/app/components/contexts/session/test-form/TestFormContext";

export default function QuestionBlocksSelector() {
  const { questionBlocks, isSelected, removeBlock, addBlock, loading } =
    useTestFormContext();
  return (
    <>
      <div className="card border-0 mb-5">
        <div className="card-body">
          <h5 className="card-title text-center text-primary fw-bold">
            Insiemi di domande disponibili
          </h5>
          <ul
            className="list-group list-group-flush"
            style={{ maxHeight: "300px", overflowY: "auto" }}
          >
            {questionBlocks.map((block, index) => (
              <li
                key={index}
                data-cy={`block-${block.id}`}
                className={`list-group-item list-group-item-action rounded-3 ${isSelected(block.id) ? "selected" : ""}`}
                {...(isSelected(block.id)
                  ? { "data-cy-selected": "true" }
                  : {})}
              >
                <div className="row">
                  <div className="col-9">
                    <p className="fw-bold mb-1">Nome</p>
                    <p data-cy={`block-${block.id}-name`}>{block.name}</p>
                  </div>
                  <div className="col-md-3 col-12">
                    {isSelected(block.id) ? (
                      <button
                        className="btn btn-outline-success rounded-5 w-100 mb-2"
                        onClick={(e) => {
                          e.preventDefault();
                          removeBlock(block.id);
                        }}
                        disabled={loading}
                        data-cy="block-deselect-button"
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
                        disabled={loading}
                        data-cy="block-select-button"
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
      </div>
    </>
  );
}
