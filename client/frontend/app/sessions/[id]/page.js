"use client";
import { SessionLLMContextProvider } from "@/app/components/contexts/session/SessionLLMContext";
import SessionContent from "@/app/components/sessions/session-content/SessionContent";
import { use } from "react";



export default function SessionPage({ params }) {
  const {id} = use(params);

  return (
    <SessionLLMContextProvider sessionId={id}>
      <SessionContent />
    </SessionLLMContextProvider>
  );
}
