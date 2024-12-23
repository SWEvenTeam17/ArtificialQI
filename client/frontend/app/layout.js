
import Link from 'next/link'
import Script from 'next/script'
import './bootstrap.css'

export default function RootLayout({ children }) {
  return (
    <html lang="en" data-bs-theme="dark">
      <body>
        <header>
          <Script src="/scripts/bootstrap.bundle.js"></Script>
        </header>
        <main>
        <nav className="navbar navbar-expand-lg bg-body-tertiary">
            <div className="container-fluid">
              <Link className="navbar-brand" href="/">ArtificialQi</Link>
              <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                <span className="navbar-toggler-icon"></span>
              </button>
              <div className="collapse navbar-collapse" id="navbarSupportedContent">
                <ul className="navbar-nav me-auto mb-2 mb-lg-0">
                  <li className="nav-item">
                    <Link className="nav-link active" aria-current="page" href="/">Home</Link>
                  </li>
                </ul>
              </div>
            </div>
          </nav>
          {children}
        </main>
      </body>
    </html>
  );
}
