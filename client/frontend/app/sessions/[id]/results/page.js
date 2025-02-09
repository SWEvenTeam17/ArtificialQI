'use client'
import { useResponse } from "@/app/components/contexts/ResponseContext";
import ResponseCard from "@/app/components/responses/ResponseCard";

export default function ResultsPage() {
    const { responseData } = useResponse();
    console.log(responseData);
    return (
        <div className="container">
            <h2 className="text-center mb-3 mt-3">{responseData.question}</h2>
            <p className="text-center mb-1">Risultati</p>
            <div className="row row-cols-1 justify-content-center g-4 mb-5 p-5">
                {responseData.results && responseData.results.length > 0 ? (
                    responseData.results.map((response, index) => (
                        <div className="col-12 col-md-6" key={index}>
                            <ResponseCard response={response}/>
                        </div>
                    ))
                ) : (
                    <p>No results available</p>
                )}
            </div>
        </div>
    );
}
