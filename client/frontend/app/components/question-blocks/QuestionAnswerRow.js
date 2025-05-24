export function QuestionAnswerRow({ pair, index, inputRefs, onChange, onRemove, canRemove }) {
  return (
    <>
      <div className="row g-3 align-items-center">
        <div className={`${canRemove ? "col-md-5" : "col-md-6"} col-12`}>
          <div className="form-floating">
            <input
              ref={(el) => (inputRefs.current[`question-${index}`] = el)}
              type="text"
              className="form-control rounded-5"
              id={`question-${index}`}
              name="question"
              placeholder={`Domanda numero ${index + 1}`}
              value={pair.question}
              onChange={(e) => onChange(index, e)}
            />
            <label htmlFor={`question-${index}`}>{`Domanda numero ${index + 1}`}</label>
          </div>
        </div>
        <div className={`${canRemove ? "col-md-5" : "col-md-6"} col-12`}>
          <div className="form-floating">
            <input
              ref={(el) => (inputRefs.current[`answer-${index}`] = el)}
              type="text"
              className="form-control rounded-5"
              id={`answer-${index}`}
              name="answer"
              placeholder={`Risposta attesa numero ${index + 1}`}
              value={pair.answer}
              onChange={(e) => onChange(index, e)}
            />
            <label htmlFor={`answer-${index}`}>{`Risposta attesa numero ${index + 1}`}</label>
          </div>
        </div>
        {canRemove && (
          <div className="col-12 col-md-2">
            <button
              className="btn btn-danger rounded-5 w-100"
              onClick={(e) => {
                e.preventDefault();
                onRemove(index);
              }}
            >
              X
            </button>
          </div>
        )}
      </div>
      <hr />
    </>
  );
}
