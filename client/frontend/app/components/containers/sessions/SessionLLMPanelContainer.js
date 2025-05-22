import React from 'react'
import SessionLLMPanelPresentational from '../../presentations/sessions/SessionLLMPanelPresentational'
import { useTestContext } from '../../contexts/TestContext'

export default function SessionLLMPanelContainer() {
  const {submitLLM, isLLMDataEmpty, remainingLLMs, sessionData, limit, deleteLLM } = useTestContext();
  return (
    <SessionLLMPanelPresentational submitLLM={submitLLM} limit={limit} deleteLLM={deleteLLM} isLLMDataEmpty={isLLMDataEmpty} remainingLLMs={remainingLLMs} sessionData={sessionData}/>
  )
}
