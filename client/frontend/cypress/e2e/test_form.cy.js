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
});
