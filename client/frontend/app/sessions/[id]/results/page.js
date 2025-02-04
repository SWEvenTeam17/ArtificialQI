'use client'
import { useResponse } from "@/app/components/contexts/ResponseContext";
import ResponseCard from "@/app/components/responses/ResponseCard";

export default function ResultsPage() {
    const { responseData } = useResponse();

    return (
        <div className="container">
            <h1 className="text-center mb-5">Results</h1>
            <div className="row row-cols-auto g-4 mb-5 p-5">
                {responseData && responseData.length > 0 ? (
                    responseData.map((response, index) => (
                        <div className="col" key={index}>
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
