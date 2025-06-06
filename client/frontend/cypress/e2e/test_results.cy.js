describe("TestResults", () => {
  beforeEach(() => {
    cy.intercept("DELETE", /\/prompt_runs/, { statusCode: 200 }).as("deleteRun");
    cy.visit("http://localhost:3000/test-results");
  });

  it("mostrare i risultati", () => {
    cy.contains("Risposte dettagliate").should("exist");
    cy.contains("Domanda:").should("exist");
    cy.contains("Risposta attesa:").should("exist");
  });

  it("Elimina run", () => {
    cy.get("button").contains("Elimina run").first().click();
    cy.wait("@deleteRun");
    cy.contains("Risposta attesa:").should("not.exist");
  });
});
