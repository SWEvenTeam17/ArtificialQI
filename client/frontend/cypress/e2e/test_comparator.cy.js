describe("TestComparator", () => {
  beforeEach(() => {
    cy.intercept('GET', '**/sessions/', {
      statusCode: 200,
      body: [
        { id: 1, title: 'Sessione 1' },
        { id: 2, title: 'Sessione 2' }
      ]
    }).as('getSessions');

    cy.intercept('GET', '**/llm_comparison/**', {
      statusCode: 200,
      body: {
        comparison: [
          { llm: 'GPT-4', score: 85 },
          { llm: 'Claude', score: 67 }
        ]
      }
    }).as('getComparison');

    cy.visit("http://localhost:3000/test-comparator");
  });

  it("mostra il selettore di sessione", () => {
    cy.contains("Seleziona una sessione").should("exist");
  });

  it("inizialmente non visualizza il selettore o il grafico LLM", () => {
    cy.get('[data-cy="llm-selector"]').should("not.exist");
    cy.get('[data-cy="comparison-chart"]').should("not.exist");
  });

  it("visualizza LLMSelector e LLMComparisonChart quando si seleziona la sessione e gli LLM", () => {
    cy.get('[data-cy="session-select"]').select("Sessione 1");
    cy.get('[data-cy="first-llm-select"]').select("GPT-4");
    cy.get('[data-cy="second-llm-select"]').select("Claude");

    cy.get('[data-cy="llm-selector"]').should("exist");
    cy.get('[data-cy="comparison-chart"]').should("exist");
    cy.contains("GPT-4").should("exist");
    cy.contains("Claude").should("exist");
  });

  it("gestisce errore quando la chiamata al confronto fallisce", () => {
    cy.intercept('GET', '**/llm_comparison/**', {
      statusCode: 500,
      body: { message: 'Errore confronto' }
    }).as('failComparison');

    cy.get('[data-cy="session-select"]').select("Sessione 1");
    cy.get('[data-cy="first-llm-select"]').select("GPT-4");
    cy.get('[data-cy="second-llm-select"]').select("Claude");

    cy.get('.toast-error').should('contain.text', 'Errore confronto');
  });

  it("mostra messaggio se i due LLM selezionati sono uguali", () => {
    cy.get('[data-cy="session-select"]').select("Sessione 1");
    cy.get('[data-cy="first-llm-select"]').select("GPT-4");
    cy.get('[data-cy="second-llm-select"]').select("GPT-4");

    cy.contains('Seleziona due LLM differenti').should('exist');
    cy.get('[data-cy="comparison-chart"]').should('not.exist');
  });
});
