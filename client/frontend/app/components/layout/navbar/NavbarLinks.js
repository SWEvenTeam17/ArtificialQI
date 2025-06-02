import Link from "next/link";

export default function NavbarLinks() {
  return (
    <ul className="navbar-nav flex-row me-auto mb-2 mb-lg-0">
      <li className="nav-item me-3">
        <Link className="nav-link" href="/">
          Home
        </Link>
      </li>
      <li className="nav-item me-3">
        <Link className="nav-link" href="/manage-llm">
          Gestisci LLM
        </Link>
      </li>
      <li className="nav-item me-3">
        <Link className="nav-link" href="/compare">
          Confronta risultati
        </Link>
      </li>
      <li className="nav-item me-3">
        <Link className="nav-link" href="/question-blocks">
          Blocchi di domande
        </Link>
      </li>
    </ul>
  );
}
