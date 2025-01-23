'use client'
import { useState } from "react";
import EditLLMForm from "../components/LLM/EditLLMForm";

export default function ManageLLM() {
    const [LLMList, setLLMList] = useState(null);

    const fetchLLMList = async () => {
        fetch(`http://localhost:8000/llm_list`, {
          method: 'GET',
        })
          .then((response) => response.json())
          .then((data) => setLLMList(data))
          .catch((error) => {
            console.error("Error fetching LLM list:", error);
            setLLMList(null);
        });
    };

    return (
        <div className="container">
            <EditLLMForm LLMList={LLMList} fetchLLMList={fetchLLMList} />
        </div>
    );
}