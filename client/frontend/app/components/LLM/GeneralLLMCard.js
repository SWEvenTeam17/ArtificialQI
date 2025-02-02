'use client'

const GeneralLLMCard = ({ llm, fetchLLMList }) => {


    const deleteLLM = async (id) => {
        let data ={
            id: id
        };
        const JSONData = JSON.stringify(data);
        try{
            await fetch(`http://localhost:8000/llm_list/${id}/`,{
                method: 'DELETE',
                headers: {"Content-type": "application/json"},
                body: JSONData
            });
            fetchLLMList();
        } catch(error)
        {
            console.error(error);
        }
    };

    return (
        <div className="card shadow-sm border-light rounded-lg">
            <div className="card-body">
                <h5 className="card-title text-primary">{llm.name}</h5>
                <p className="card-text text-muted">Numero di Parametri: {llm.n_parameters}</p>
                <button
                    className="btn btn-danger"
                    onClick={() => deleteLLM(llm.id)}
                >
                    Rimuovi
                </button>
            </div>
        </div>
    );
}
export default GeneralLLMCard;