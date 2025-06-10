describe("QuestionBlocksSelector - esecuzione test", () => {
  beforeEach(() => {
    // Mock delle chiamate iniziali
    cy.intercept("GET", "**/session_list/**", {
      statusCode: 200,
      body: [{
        id: 42,
        title: "Sessione di benchmark",
        llm: [{ id: 1, name: "GPT-4", n_parameters: "175B" }],
      }],
    }).as("getSession");

    cy.intercept("GET", "**/session_list/42", {
      statusCode: 200,
      body: {
        id: 42,
        title: "Sessione di benchmark",
        llm: [{ id: 1, name: "GPT-4", n_parameters: "175B" }],
      },
    }).as("getSessionById");

    cy.intercept("GET", "**/llm_remaining/42", {
      statusCode: 200,
      body: [
        { id: 3, name: "Mistral 7B", n_parameters: "7B" },
        { id: 4, name: "LLaMA 3", n_parameters: "65B" },
      ],
    }).as("getRemainingLLMs");

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
          ],
        },
        {
          id: 2,
          name: "Blocco Vuoto",
          prompt: [],
        },
      ],
    }).as("getQuestionBlocks");

    // Mock POST runtest per simulare esecuzione test
    cy.intercept("POST", "**/runtest/", (req) => {
      req.reply({
        statusCode: 200,
        body: {
          results: [
            {
              block_id: 1,
              block_name: "Blocco A",
              results: [
                {
                  run_id: 123,
                  llm_name: "GPT-4",
                  question: "Qual è la capitale della Francia?",
                  expected_answer: "Parigi",
                  answer: "Parigi",
                  semantic_evaluation: 1.0,
                  external_evaluation: 0.95,
                },
              ],
              averages_by_llm: {
                "GPT-4": {
                  avg_semantic_scores: 1.0,
                  avg_external_scores: 0.95,
                },
              },
            },
          ],
        },
      });
    }).as("postRunTest");

    cy.visit("http://localhost:3000/sessions/42");
    cy.wait("@getQuestionBlocks");
  });

  it("Esegue il test e mostra i risultati", () => {
    cy.get('[data-cy="block-select-button"]').click();
    cy.get('[data-cy="run-test-button"]').click();
    cy.wait("@postRunTest").its("request.body").should("have.property", "blocks");
    cy.contains("Risposte dettagliate").should("exist");
    cy.contains("Qual è la capitale della Francia?").should("exist");
    cy.contains("Parigi").should("exist");
    cy.contains("GPT-4").should("exist");
    cy.contains("Valutazione semantica").should("exist");
    cy.contains("Valutazione esterna").should("exist");
    cy.contains("1").should("exist");
    cy.contains("0.95").should("exist");
  });
});
