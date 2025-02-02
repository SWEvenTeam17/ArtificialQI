'use client'
import { useEffect, useState } from "react";
import GeneralLLMCard from "../components/LLM/GeneralLLMCard";
import CreateLLMForm from "../components/LLM/CreateLLMForm";

export default function ManageLLM() {
    const [LLMList, setLLMList] = useState([]);

    useEffect(() => {
        fetchLLMList();
    }, []);

    const fetchLLMList = async () => {
        try {
            const response = await fetch(`http://localhost:8000/llm_list/`);
            const data = await response.json();
            setLLMList(data);
        } catch (error) {
            console.error("Error fetching LLM list:", error);
        }
    };

    return (
        <div className="container">
            <div className="row">
                <CreateLLMForm fetchLLMList={fetchLLMList} />
            </div>
            <div className="row row-cols-lg-4 row-cols-2">
                {LLMList.length > 0 ? (
                    LLMList.map((llm, index) => (
                        <div className="col" key={index}>
                            <GeneralLLMCard llm={llm} fetchLLMList={fetchLLMList} />
                        </div>
                    ))
                ) : (
                    <p>Nessun LLM disponibile</p>
                )}
            </div>
        </div>
    );
}
