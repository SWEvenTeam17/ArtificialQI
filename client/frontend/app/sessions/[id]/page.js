"use client";
import { SessionPageContextProvider } from "@/app/components/contexts/SessionPageContext";
import SessionContentContainer from "@/app/components/containers/sessions/SessionContentContainer";
import { use } from "react";



export default function SessionPage({ params }) {
  const {id} = use(params);

  return (
    <SessionPageContextProvider sessionId={id}>
      <SessionContentContainer id={id} />
    </SessionPageContextProvider>
  );
}
