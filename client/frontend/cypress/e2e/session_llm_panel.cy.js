describe("SessionLLMPanel", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/session_list/42", {
      statusCode: 200,
      body: {
        id: 42,
        title: "Sessione di benchmark",
        description: "Sessione per il test dei LLM",
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        llm: [],
      },
    }).as("getSession");

    cy.intercept("GET", "**/llm_remaining/42", {
      statusCode: 200,
      body: [
        { id: 1, name: "LLM 1", n_parameters: "7B" },
        { id: 2, name: "LLM 2", n_parameters: "13B" },
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

    cy.intercept("GET", "**/llm_list/", {
      statusCode: 200,
      body: [
        { id: 1, name: "LLM 1", n_parameters: "7B" },
        { id: 2, name: "LLM 2", n_parameters: "13B" },
      ],
    }).as("getLLMs");

    cy.intercept("POST", "**/llm_add/**", {
      statusCode: 200,
      body: { id: 1, name: "LLM 1", n_parameters: "7B" },
    }).as("addLLM");

    cy.intercept("DELETE", "**/llm_delete/**/**", {
      statusCode: 204,
    }).as("deleteLLM");

    cy.visit("http://localhost:3000/sessions/42");
  });

  it("should show message when no LLM is selected", () => {
    cy.contains(
      "Nessun LLM selezionato, aggiungi un LLM per cominciare.",
    ).should("exist");
  });

  it("should allow selecting and adding an LLM", () => {
    cy.get('select[name="selectllm"]').select("LLM 1");
    cy.get('[data-cy="add-llm-button"]').click();

    cy.contains("LLM 1").should("exist");
    cy.contains("Numero di Parametri: 7B").should("exist");
  });
  it("should allow removing an LLM from the session", () => {
    cy.get('select[name="selectllm"]').select("LLM 1");
    cy.get('[data-cy="add-llm-button"]').click();
    cy.contains("LLM 1").should("exist");
    cy.get(".row-cols-md-4 > .col > .card > .card-body").should("exist");
    cy.get('[data-cy="delete-llm-button"]').click();
    cy.get(".row-cols-md-4 > .col > .card > .card-body").should("not.exist");
  });
});
