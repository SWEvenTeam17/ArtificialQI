"use client";
import { SessionPageContextProvider } from "@/app/components/contexts/SessionPageContext";
import SessionContent from "@/app/components/sessions/session-content/SessionContent";
import { use } from "react";



export default function SessionPage({ params }) {
  const {id} = use(params);

  return (
    <SessionPageContextProvider sessionId={id}>
      <SessionContent />
    </SessionPageContextProvider>
  );
}
