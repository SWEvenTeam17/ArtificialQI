"use client";

import { TestComparatorContextProvider } from "../components/contexts/TestComparatorContext";

export default function Layout({ children }) {
  return (
      <TestComparatorContextProvider>
        {children}
      </TestComparatorContextProvider>
  );
}
