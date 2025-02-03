'use client'
import delteIcon from '/public/images/icon.png';
import Image from 'next/image';

const LLMCard = ({ id, llm, fetchLLMData, setSessionData }) => {

    const deleteLLM = async (llmId) => {
        const response = await fetch(`http://localhost:8000/llm_delete/${id}/${llmId}`, {
            method: 'DELETE',
        });
        if (!response.ok) {
            throw new Error(response.statusText);
        }
        if (response.status !== 204) {
            await response.json();
        }
        setSessionData((prevSessionData) => ({
            ...prevSessionData,
            llm: prevSessionData.llm.filter((llm) => llm.id !== llmId),
        }));
        fetchLLMData();

    };

    return (
        <div className="card shadow border-light rounded-5">
            <div className="card-body">
                <h5 className="card-title text-primary">{llm.name}</h5>
                <p className="card-text text-muted">Numero di Parametri: {llm.n_parameters}</p>
                <button
                    className="btn btn-danger"
                    onClick={() => deleteLLM(llm.id)}
                >
                    <Image width={32} height={32} alt='Elimina llm' src={delteIcon} />
                </button>
            </div>
        </div>
    );
}
export default LLMCard;