describe("PrevTests Component", () => {
  beforeEach(() => {
    cy.intercept("DELETE", /\/previous_tests\/\d+\//, { statusCode: 200 }).as("deleteTest");
    cy.visit('http://localhost:3000/prev-test');
  });

  it("i test precedenti", () => {
    cy.contains("Test #1").should("exist");
    cy.contains("Test #2").should("exist");
    cy.contains("Blocco A").should("exist");
    cy.contains("Blocco B").should("exist");
  });

  it("Elimina un test facendo clic su Elimina", () => {
    cy.contains("Test #1").parent().find("button").click();
    cy.wait("@deleteTest");
    cy.contains("Test #1").should("not.exist");
  });
});
