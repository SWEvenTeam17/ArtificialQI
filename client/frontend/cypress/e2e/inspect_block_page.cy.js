describe("InspectBlockPage", () => {
  beforeEach(() => {
    cy.intercept('GET', '**/question_blocks/123', {
      statusCode: 200,
      body: {
        name: 'Blocco A',
        prompt: [
          { id: 1, prompt_text: 'Domanda 1', expected_answer: 'Risposta 1' },
          { id: 2, prompt_text: 'Domanda 2', expected_answer: 'Risposta 2' }
        ]
      }
    }).as('getBlock');

    cy.visit("http://localhost:3000/question-blocks/123");
  });

  it("mostra il nome del blocco e le sue domande", () => {
    cy.contains("Blocco A").should("exist");
    cy.contains("Domanda 1").should("exist");
    cy.contains("Risposta 1").should("exist");
    cy.contains("Domanda 2").should("exist");
    cy.contains("Risposta 2").should("exist");
  });

  it("mostra un messaggio di errore se il blocco non esiste", () => {
    cy.intercept('GET', '**/question_blocks/999', {
      statusCode: 404,
      body: { message: 'Blocco non trovato' }
    }).as('getMissingBlock');

    cy.visit("http://localhost:3000/question-blocks/999");

    cy.get('.alert-danger').should('contain.text', "Errore nel recupero dell'insieme di domande.");
  });

  it("valida che la visualizzazione sia responsive su schermi piccoli", () => {
    cy.contains("Blocco A").should("be.visible");
  });
});
