'use client'
import { useContext, useEffect, useState } from 'react';
import { SessionContext } from './components/contexts/SessionContext';
import Link from 'next/link';
import Form from 'next/form'
import Script from 'next/script';
import './bootstrap.css';

export default function RootLayout({ children }) {


  const [sessions, setSessions] = useState([]);
  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/session_list");
      const data = await response.json();
      setSessions(data);
    } catch (error) {
      console.error("Error fetching sessions:", error);
    }
  };

  async function onSubmit(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const data = {
      title: formData.get('title'),
      description: formData.get('description'),
    };

    const JSONData = JSON.stringify(data);

    try {
      await fetch('http://localhost:8000/session_list/', {
        method: 'POST',
        headers: { "Content-type": "application/json" },
        body: JSONData,
      });

      fetchSessions();
      event.target.reset();
    } catch (error) {
      console.error("Error submitting form:", error);
    }
  }


  return (
    <html lang="en">
      <body>
        <header>
          <Script src="/scripts/bootstrap.bundle.js"></Script>
          <title>ArtificialQI</title>
        </header>
        <main>
          <nav className="navbar bg-body-tertiary">
            <div className="container-fluid justify-content-start">
              <button className="navbar-toggler me-2" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasNavbar" aria-controls="offcanvasNavbar" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
              <a className="navbar-brand" href="/#">ArtificialQI</a>
              <div className="offcanvas offcanvas-start" tabIndex="-1" id="offcanvasNavbar" aria-labelledby="offcanvasNavbarLabel">
                <div className="offcanvas-header">
                  <h1 className="offcanvas-title" id="offcanvasNavbarLabel">ArtificialQI</h1>
                  <button type="button" className="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
                </div>
                <div className="offcanvas-body">
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
                              <Form onSubmit={onSubmit}>
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
                              </Form>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="mt-4">
                    <ul className="list-group">
                      {sessions.map((session, index) => (
                        <a key={index} className='btn mt-2 btn-light rounded-5 border'>{session.title}</a>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </nav>
          <SessionContext.Provider value={sessions}>{children}</SessionContext.Provider>

        </main>
      </body>
    </html>
  );
}
