const ResponseCard = ({ response }) => {
    return (
        <div className="card text-center rounded-4 shadow-lg p-4 mb-4 w-100 transition-transform transform hover:scale-105">
            <div className="card-body">
                <h5 className="card-title text-primary font-weight-bold">{response.llm_name}</h5>
                <p className="card-text text-muted" style={{ fontSize: '1.1rem' }}>{response.answer}</p>
                <p className="card-text text-primary" style={{ fontSize: '1.2rem', fontWeight: '500' }}>
                    Valutazione semantica: <span className="font-weight-bold">{response.semantic_evaluation}%</span>
                </p>
            </div>
        </div>
    );
}

export default ResponseCard;