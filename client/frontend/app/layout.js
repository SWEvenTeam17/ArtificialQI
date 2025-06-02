"use client";
import Script from "next/script";
import "./bootstrap.css";
import { SessionContextProvider } from "./components/contexts/session/SessionContext";
import Navbar from "@/app/components/layout/navbar/Navbar";
export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <header>
          <Script src="/scripts/bootstrap.bundle.js"></Script>
          <title>ArtificialQI</title>
        </header>
        <main>
          <SessionContextProvider>
            <Navbar />
            {children}
          </SessionContextProvider>
        </main>
      </body>
    </html>
  );
}
