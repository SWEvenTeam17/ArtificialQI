describe("InspectBlockPage", () => {
  beforeEach(() => {
    cy.visit("http://localhost:3000/test-inspect-block"); 
  });

  it("mostra il nome del blocco e le sue domande", () => {
    cy.contains("Blocco A").should("exist");
    cy.contains("Domanda 1").should("exist");
  });

  it("consente di tornare indietro o navigare", () => {
    cy.get('[data-cy="back-button"]').click();
    cy.url().should("include", "/blocks"); 
  });
});
