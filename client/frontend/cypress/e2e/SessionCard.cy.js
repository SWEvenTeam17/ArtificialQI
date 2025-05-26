describe("SessionCardActions", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [
        {
          id: 1,
          title: "Sessione di prova",
          description: "Descrizione di prova",
        },
      ],
    }).as("getSessions");

    cy.visit("http://localhost:3000/");

    cy.wait("@getSessions");
  });

  it("mostra i bottoni Modifica e Cancella quando non in modifica", () => {
    cy.get('[data-cy="edit-button"]').should("be.visible").click();

    cy.get('[data-cy="save-button"]').should("be.visible");
    cy.get('[data-cy="cancel-button"]').should("be.visible");
  });

  it("permette di modificare e salvare la sessione", () => {
    cy.get('[data-cy="edit-button"]').click();

    cy.get('input[placeholder="Nome"]')
      .should("be.visible")
      .clear()
      .type("Titolo aggiornato");
    cy.get('[data-cy="description-input"]')
      .click()
      .clear()
      .type("Descrizione aggiornata");

    cy.intercept("PUT", "**/session_list/1/", {
      statusCode: 200,
      body: {},
    }).as("updateSession");

    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [
        {
          id: 1,
          title: "Titolo aggiornato",
          description: "Descrizione aggiornata",
        },
      ],
    }).as("getSessionsAfterUpdate");

    cy.get('[data-cy="save-button"]').click({ multiple: true });

    cy.wait("@updateSession");
    cy.wait("@getSessionsAfterUpdate");
    cy.get('[data-cy="session-card"]').within(() => {
      cy.contains("Titolo aggiornato").should("be.visible");
      cy.contains("Descrizione aggiornata").should("be.visible");
    });
  });

  it("permette di annullare la modifica", () => {
    cy.get('[data-cy="edit-button"]').click();
    cy.get('input[placeholder="Nome"]').clear().type("Qualcosa di sbagliato");
    cy.get('[data-cy="cancel-button"]').click();
    cy.get('[data-cy="session-title')
      .contains("Sessione di prova")
      .should("be.visible");
    cy.contains("Qualcosa di sbagliato").should("not.exist");
  });

  it("permette di cancellare la sessione", () => {
    cy.intercept("DELETE", "**/session_list/1/", {
      statusCode: 204,
      body: {},
    }).as("deleteSession");

    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [],
    }).as("getSessionsAfterDelete");

    cy.get('[data-cy="delete-button"]').click();

    cy.wait("@deleteSession");
    cy.wait("@getSessionsAfterDelete");

    cy.contains("Sessione di prova").should("not.exist");
  });
});
