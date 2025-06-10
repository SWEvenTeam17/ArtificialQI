describe("PrevTests - pagina reale", () => {
  const sessionId = 42;

  beforeEach(() => {
    cy.intercept("GET", "**/session_list/42", {
      statusCode: 200,
      body: {
        id: 42,
        title: "Sessione di benchmark",
        description: "Sessione per il test dei LLM",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        llm: [
          { id: 1, name: "GPT-4", n_parameters: "175B" },
          { id: 2, name: "Claude 3", n_parameters: "52B" },
        ],
      },
    }).as("getSession");

    cy.intercept("GET", "**/llm_remaining/42", {
      statusCode: 200,
      body: [
        { id: 3, name: "Mistral 7B", n_parameters: "7B" },
        { id: 4, name: "LLaMA 3", n_parameters: "65B" },
      ],
    }).as("getRemainingLLMs");

    cy.intercept("GET", "**/question_blocks/", {
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
          ],
        },
        {
          id: 2,
          name: "Blocco B",
          prompt: [],
        },
      ],
    }).as("getQuestionBlocks");

    cy.visit("http://localhost:3000/sessions/42");
  });

  it("mostra i blocchi di domande non vuoti", () => {
    cy.wait("@getQuestionBlocks");
    cy.contains("Blocco A").should("exist");
    cy.contains("Blocco B").should("not.exist");
  });

  it("visualizza i test precedenti e li elimina", () => {
    cy.intercept("GET", "**/previous_tests/**", {
      statusCode: 200,
      body: [
        {
          id: 1001,
          block: { name: "Blocco A" },
          timestamp: new Date().toISOString(),
        },
      ],
    }).as("getPreviousTests");

    cy.intercept("DELETE", "**/previous_tests/1001", {
      statusCode: 204,
    }).as("deleteTest");

    cy.contains("Visualizza test precedenti").click();
    cy.wait("@getPreviousTests");

    cy.contains("Blocco A").should("exist");
    cy.contains("Elimina").click();
    cy.wait("@deleteTest");
  });

  it("mostra un messaggio se non ci sono test precedenti", () => {
    cy.intercept("GET", "**/previous_tests/**", {
      statusCode: 200,
      body: [],
    }).as("getNoTests");

    cy.contains("Visualizza test precedenti").click();
    cy.wait("@getNoTests");

    cy.contains("Nessun test precedente trovato").should("exist");
  });
});
