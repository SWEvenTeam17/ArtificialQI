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
            <div className="card shadow border-light rounded-5 mt-3">
                <div className="card-body">
                    <h2 className="card-title text-center">
                        Gestisci LLM
                    </h2>
                    <div className="ms-5 me-5 mb-5 row justify-content-center">
                        <div className="col-12 col-md-7">
                            <CreateLLMForm fetchLLMList={fetchLLMList}/>
                        </div>
                    </div>
                    <h2 className="card-title text-center mb-4">
                        LLM collegati ad ArtificialQI
                    </h2>
                    <div className="row row-cols-lg-3 g-2 row-cols-1">
                        {LLMList.length > 0 ? (
                            LLMList.map((llm) => (
                                <div className="col" key={llm.id}>
                                    <GeneralLLMCard llm={llm} fetchLLMList={fetchLLMList} />
                                </div>
                            ))
                        ) : (
                            <p>Nessun LLM disponibile</p>
                        )}
                    </div>
                </div>

            </div>


        </div>
    );
}
