"use client";
import { useSessionContext } from "../components/contexts/SessionContext";
import TestComparatorContainer from "../components/containers/compare/TestComparatorContainer";

export default function Compare() {
  const { sessions } = useSessionContext();
  return (
    <div className="container-fluid">
      <TestComparatorContainer sessions={sessions} />
    </div>
  );
}
