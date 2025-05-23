import React from "react";
import SessionContentPresentational from "../../presentations/sessions/SessionContentPresentational";
import { useTestContext } from "../../contexts/SessionPageContext";

export default function SessionContentContainer({id}) {
  const { sessionData, setSessionData, remainingLLMs, fetchRemainingLLMs } =
    useTestContext();
  return <SessionContentPresentational id={id} sessionData={sessionData} setSessionData={setSessionData} remainingLLMs={remainingLLMs} fetchRemainingLLMs={fetchRemainingLLMs} />;
}
