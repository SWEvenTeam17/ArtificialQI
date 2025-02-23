const ResponseCard = ({ response }) => {
  return (
    <div className="card text-center rounded-4 shadow-lg p-4 mb-4 w-100 transition-transform transform hover:scale-105">
      <div className="card-body">
        <h5 className="card-title text-primary font-weight-bold">
          {response.llm_name}
        </h5>
        <p className="card-text">
          <span className="text-primary">Domanda:</span> {response.question}
        </p>
        <p className="card-text">
          <span className="text-primary">Risposta attesa:</span>{" "}
          {response.expected_answer}
        </p>
        <p className="card-text">
          <span className="text-primary">Risposta data:</span> {response.answer}
        </p>
        <p className="card-text">
          <span className="text-primary">Valutazione semantica:</span>{" "}
          <span className="font-weight-bold">
            {response.semantic_evaluation}%
          </span>
        </p>
        <p className="card-text">
          <span className="text-primary">Valutazione LLM esterno:</span>{" "}
          <span className="font-weight-bold">
            {response.external_evaluation}%
          </span>
        </p>
      </div>
    </div>
  );
};

export default ResponseCard;
