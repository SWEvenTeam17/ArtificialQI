import { useState, useEffect } from 'react';
import Form from 'next/form';

const AddLLMForm = ({ LLMData, sessionData, setSessionData, fetchLLMData }) => {
    // State to track if LLMData is empty
    const [isLLMDataEmpty, setIsLLMDataEmpty] = useState(!LLMData || LLMData.length === 0);

    // Update the state whenever LLMData changes
    useEffect(() => {
        setIsLLMDataEmpty(!LLMData || LLMData.length === 0);
    }, [LLMData]);

    const submitLLM = async (e) => {
        e.preventDefault();

        if (sessionData.llm.length >= 3) {
            alert("Solo fino a 3 LLM possono essere aggiunti!");
        } else {
            const formData = new FormData(e.target);
            const data = {
                sessionId: sessionData.id,
                llmId: formData.get('selectllm')
            };
            const JSONData = JSON.stringify(data);

            const response = await fetch("http://localhost:8000/llm_add/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSONData
            });
            const result = await response.json();
            setSessionData((prevSessionData) => ({
                ...prevSessionData,
                llm: [...prevSessionData.llm, result]
            }));
            fetchLLMData();
        }
    };

    return (
        <Form onSubmit={submitLLM}>
            <select
                className="form-select mt-4 mb-4 rounded-5 text-center"
                name="selectllm"
                id="selectllm"
                defaultValue={isLLMDataEmpty ? "no-llm" : ""}
                required
                disabled={isLLMDataEmpty}
            >
                <option value="">
                    {isLLMDataEmpty ? "Nessun LLM disponibile" : "Seleziona un LLM..."}
                </option>
                {!isLLMDataEmpty && LLMData.map((llm) => (
                    <option key={llm.id} value={llm.id}>{llm.name}</option>
                ))}
            </select>
            <button className="btn btn-primary rounded-5 w-100" type="submit" disabled={isLLMDataEmpty}>
                Aggiungi
            </button>
        </Form>
    );
};

export default AddLLMForm;
