describe("TestForm", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/test-form");
  });

  it("Compila il modulo e invialo", () => {
    cy.get('[data-cy="question-input"]').type("Qual è la capitale della Francia?");
    cy.get('[data-cy="llm-select"]').select("GPT-4");
    cy.get('[data-cy="submit-button"]').click();
    cy.contains("Test inviato con successo").should("exist"); 
  });

  it("Mostra errore se i campi sono vuoti", () => {
    cy.get('[data-cy="submit-button"]').click();
    cy.get('.error-message').should('contain.text', 'Campo obbligatorio');
  });

  it("Mostra errore del server se la richiesta fallisce", () => {
    cy.intercept('POST', '**/run_test/', {
      statusCode: 500,
      body: { message: 'Errore del server' },
    }).as('failSubmit');

    cy.get('[data-cy="question-input"]').type("Quanto fa 2+2?");
    cy.get('[data-cy="llm-select"]').select("GPT-4");
    cy.get('[data-cy="submit-button"]').click();

  });

  it("Mostra il loader durante l'invio", () => {
    cy.intercept('POST', '**/run_test/', (req) => {
      return new Promise((resolve) => {
        setTimeout(() => resolve({ statusCode: 200, body: {} }), 1000);
      });
    }).as('delayedSubmit');

    cy.get('[data-cy="question-input"]').type("Qual è la radice quadrata di 9?");
    cy.get('[data-cy="llm-select"]').select("GPT-4");
    cy.get('[data-cy="submit-button"]').click();

    cy.get('[data-cy="loader"]').should('be.visible');
    cy.get('[data-cy="loader"]').should('not.exist');
  });

  it("Previene invio con selezione di LLM non valida", () => {
    cy.get('[data-cy="question-input"]').type("Test senza selezione valida");
    cy.get('[data-cy="llm-select"]').select('---');
    cy.get('[data-cy="submit-button"]').click();
    cy.get('.error-message').should('contain.text', 'Seleziona un LLM valido');
  });
});
