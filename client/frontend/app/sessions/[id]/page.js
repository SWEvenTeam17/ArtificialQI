"use client";
import { TestContextProvider } from "@/app/components/contexts/TestContext";
import SessionContent from "@/app/components/sessions/session-content/SessionContent";
import { use } from "react";



export default function SessionPage({ params }) {
  const {id} = use(params);

  return (
    <TestContextProvider sessionId={id}>
      <SessionContent />
    </TestContextProvider>
  );
}
