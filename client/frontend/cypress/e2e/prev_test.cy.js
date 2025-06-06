describe("PrevTests Component", () => {
  beforeEach(() => {
    cy.intercept("DELETE", /\/previous_tests\/\d+\//, { statusCode: 200 }).as("deleteTest");
    cy.intercept("GET", '**/previous_tests/', {
      statusCode: 200,
      body: [
        {
          id: 1,
          block: { name: "Blocco A" },
          timestamp: new Date().toISOString()
        },
        {
          id: 2,
          block: { name: "Blocco B" },
          timestamp: new Date().toISOString()
        }
      ]
    }).as("getPrevTests");

    cy.visit('http://localhost:3000/prev-test');
  });

  it("mostra i test precedenti", () => {
    cy.contains("Test #1").should("exist");
    cy.contains("Test #2").should("exist");
    cy.contains("Blocco A").should("exist");
    cy.contains("Blocco B").should("exist");
  });

  it("elimina un test facendo clic su Elimina", () => {
    cy.get('[data-cy="delete-button-1"]').click();
    cy.contains("Test #1").should("not.exist");
  });

  it("gestisce errore del server durante l'eliminazione", () => {
    cy.intercept("DELETE", /\/previous_tests\/\d+\//, {
      statusCode: 500,
      body: { message: 'Errore del server' },
    }).as("deleteTestFail");

    cy.get('[data-cy="delete-button-2"]').click();
  });

  it("mostra un messaggio se non ci sono test precedenti", () => {
    cy.intercept("GET", '**/previous_tests/', {
      statusCode: 200,
      body: [],
    }).as("getNoTests");

    cy.visit('http://localhost:3000/prev-test');
    cy.contains("Nessun test precedente trovato").should("exist");
  });

  it("verifica che ogni test mostri titolo e blocchi associati", () => {
    cy.get('[data-cy^="test-card-"]').each(($el) => {
      cy.wrap($el).within(() => {
        cy.get('[data-cy^="test-title-"]').should('exist');
        cy.get('[data-cy^="block-name-"]').should('exist');
      });
    });
  });
});
