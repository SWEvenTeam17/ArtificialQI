"use client";
import { TestContextProvider } from "@/app/components/contexts/TestContext";
import SessionContentContainer from "@/app/components/containers/sessions/SessionContentContainer";
import { use } from "react";



export default function SessionPage({ params }) {
  const {id} = use(params);

  return (
    <TestContextProvider sessionId={id}>
      <SessionContentContainer id={id} />
    </TestContextProvider>
  );
}
