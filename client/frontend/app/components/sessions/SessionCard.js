"use client";
import { SessionCardProvider } from "@/app/components/contexts/session/SessionCardContext";
import SessionCardBody from "./SessionCardBody";
import SessionCardActions from "./SessionCardActions";

export default function SessionCard({ session }) {
  return (
    <SessionCardProvider session={session}>
      <div data-cy="session-card" className="card text-center rounded-5 border-light shadow hover-grow p-3 mb-2 w-100">
        <div className="card-body">
          <SessionCardBody />
        </div>
        <SessionCardActions />
      </div>
    </SessionCardProvider>
  );
}
