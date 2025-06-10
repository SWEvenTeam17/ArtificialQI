describe("QuestionBlockCard", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/question_blocks/**", {
      statusCode: 200,
      body: [
        {
          id: 1,
          name: "Blocco A",
          prompt: [
            {
              id: 101,
              prompt_text: "Qual è la capitale della Francia?",
              expected_answer: "Parigi",
              timestamp: new Date().toISOString(),
              evaluation_set: [],
            },
            {
              id: 102,
              prompt_text: "Quanto fa 2 + 2?",
              expected_answer: "4",
              timestamp: new Date().toISOString(),
              evaluation_set: [],
            },
          ],
        },
        {
          id: 2,
          name: "Blocco B",
          prompt: [],
        },
      ],
    }).as("getBlocks");

    cy.visit("http://localhost:3000/question-blocks");
  });

  it("should render fallback if no questions exist", () => {
    cy.intercept("GET", "**/question_blocks/**", {
      statusCode: 200,
      body: [
        {
          id: 2,
          name: "Blocco vuoto",
          prompt: [],
        },
      ],
    }).as("getEmptyBlock");
    cy.visit("http://localhost:3000/question-blocks");
    cy.contains("Blocco vuoto").should("exist");
    cy.contains("Nessuna domanda disponibile.").should("exist");
  });

  it("should call onDelete when clicking delete", () => {
    cy.intercept("GET", "**/question_blocks/**", {
      statusCode: 200,
      body: [
        {
          id: 42,
          name: "Blocco da eliminare",
          prompt: [
            {
              id: 101,
              prompt_text: "Qual è la capitale della Francia?",
              expected_answer: "Parigi",
              timestamp: new Date().toISOString(),
              evaluation_set: [],
            },
          ],
        },
      ],
    }).as("getEmptyBlock");

    cy.intercept("DELETE", "**/question_blocks/**", {
      statusCode: 204,
      body: [],
    }).as("getEmptyBlock");

    cy.get('[data-cy="delete-btn-42"]').click();
  });
});
