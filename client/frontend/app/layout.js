"use client";
import Script from "next/script";
import "./bootstrap.css";
import { SessionContextProvider } from "./components/contexts/SessionContext";
import NavbarContainer from "./components/containers/layout/navbar/NavbarContainer";

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
            <NavbarContainer></NavbarContainer>
            {children}
          </SessionContextProvider>
        </main>
      </body>
    </html>
  );
}
