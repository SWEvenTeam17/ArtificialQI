"use client";
import React from "react";
import { TestComparatorContextProvider } from "../components/contexts/TestComparatorContext";

export default function Layout({ children }) {
  return (
      <TestComparatorContextProvider>
        {children}
      </TestComparatorContextProvider>
  );
}
