describe("TestComparator", () => {
  beforeEach(() => {
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
  });
});
