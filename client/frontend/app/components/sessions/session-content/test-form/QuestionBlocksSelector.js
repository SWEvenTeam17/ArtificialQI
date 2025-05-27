export default function QuestionBlocksSelector({
  questionBlocks,
  isSelected,
  removeBlock,
  addBlock,
}) {
  return (
    <>
      <div className="card border-0 mb-5">
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
                        disabled={loading}
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