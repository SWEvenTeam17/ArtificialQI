import React from 'react'
import TestResultsPresentational from '../../presentations/sessions/TestResultsPresentational'
export default function TestResultsContainer({testResults}) {
  return (
    <TestResultsPresentational testResults={testResults}/>
  )
}
