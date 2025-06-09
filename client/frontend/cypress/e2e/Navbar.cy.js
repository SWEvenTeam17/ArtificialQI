describe("Navbar", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [],
    }).as("getSessions");

    cy.visit("http://localhost:3000/");
    cy.wait("@getSessions");
  });

  it("crea una nuova sessione dalla navbar", () => {
    cy.get(".navbar-toggler").click();
    cy.get("#offcanvasNavbar").should("have.class", "show");
    cy.get("#title").clear().type("Titolo test");
    cy.get("#description").clear().type("Descrizione test");

    cy.intercept("POST", "**/session_list/", (req) => {
      expect(req.body).to.deep.equal({
        title: "Titolo test",
        description: "Descrizione test",
      });
      req.reply({ statusCode: 201 });
    }).as("createSession");

    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [
        {
          id: 999,
          title: "Titolo test",
          description: "Descrizione test",
        },
      ],
    }).as("getSessionsAfterCreate");

    cy.get('button[type="submit"]').click();

    cy.wait("@createSession");
    cy.wait("@getSessionsAfterCreate");

    cy.get(".list-group")
      .should("contain.text", "Titolo test")
  });

  it("naviga ai link della navbar", () => {
    cy.get(".navbar-nav").contains("Gestisci LLM").click();
    cy.url().should("include", "/manage-llm");

    cy.get(".navbar-nav").contains("Confronta risultati").click();
    cy.url().should("include", "/compare");

    cy.get(".navbar-nav").contains("Insiemi di domande").click();
    cy.url().should("include", "/question-blocks");
  });
});
