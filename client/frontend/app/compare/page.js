"use client";
import { useContext, useEffect, useState } from "react";
import TestComparator from "@/app/components/comparators/TestComparator";
import QuestionComparator from "@/app/components/comparators/QuestionComparator";
import { SessionContext } from "../components/contexts/SessionContext";

export default function Compare() {
  const { sessions } = useContext(SessionContext);
  return (
    <div className="container-fluid">
      <TestComparator sessions={sessions} />
    </div>
  );
}
