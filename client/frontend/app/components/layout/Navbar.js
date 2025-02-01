'use client';
import Link from 'next/link';
import { useRouter } from 'next/navigation';

export default function Navbar({ sessions, onFormSubmit }) {

    return (
        <nav className="navbar bg-body-tertiary">
            <div className="container-fluid justify-content-start">
                <button className="navbar-toggler me-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <a className="navbar-brand" href="/">ArtificialQI</a>
                <ul className="navbar-nav flex-row me-auto mb-2 mb-lg-0">
                    <li className="nav-item me-3">
                        <a className="nav-link" href="/">Home</a>
                    </li>
                    <li className="nav-item me-3">
                        <a className="nav-link" href="/manage-llm">Gestisci LLM</a>
                    </li>
                </ul>
                <div className="offcanvas offcanvas-start" tabIndex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
                    <div className="offcanvas-header">
                        <h1 className="offcanvas-title" id="offcanvasNavbarLabel">ArtificialQI</h1>
                        <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                    </div>
                    <div className="offcanvas-body">
                        <AccordionForm onSubmit={onFormSubmit} />
                        <div className="mt-4">
                            <ul className="list-group">
                                {sessions.map((session, index) => (
                                    <NavbarSessionElement session={session} key={index}></NavbarSessionElement>
                                ))}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
}


function NavbarSessionElement({ session }) {
    const router = useRouter();
    return (

        <Link
            href={`/sessions/${session.id}`}
            onClick={() => router.push(`/sessions/${session.id}`)}
            data-bs-dismiss="offcanvas"
            className="btn w-100 mt-2 btn-light rounded-5 border"
        >
            {session.title}
        </Link>);
}

function AccordionForm({ onSubmit }) {
    return (
        <div className="accordion" id="formAccordion">
            <div className="accordion-item">
                <h2 className="accordion-header" id="headingForm">
                    <button className="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseForm" aria-expanded="true" aria-controls="collapseForm">
                        Crea nuova sessione
                    </button>
                </h2>
                <div id="collapseForm" className="accordion-collapse collapse show" aria-labelledby="headingForm" data-bs-parent="#formAccordion">
                    <div className="accordion-body">
                        <div className="container align-items-center">
                            <div className="mt-3">
                                <form onSubmit={onSubmit}>
                                    <div className="form-floating mb-3">
                                        <input type="text" className="form-control rounded-5" id="title" name="title" placeholder="Titolo" />
                                        <label htmlFor="title">Titolo</label>
                                    </div>
                                    <div className="form-floating mb-3">
                                        <input type="text" className="form-control rounded-5" id="description" name="description" placeholder="Descrizione" />
                                        <label htmlFor="description">Descrizione</label>
                                    </div>
                                    <div className="text-center align-items-center col-12">
                                        <button type="submit" className="btn btn-primary w-50 rounded-5">Crea</button>
                                    </div>
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
