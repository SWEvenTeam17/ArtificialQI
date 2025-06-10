describe("TestComparator", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [
        {
          id: 1,
          title: "Sessione 1",
          llm: [
            { id: 1, name: "GPT-4", n_parameters: "175B" },
            { id: 2, name: "Claude 3", n_parameters: "52B" },
          ],
        },
        {
          id: 2,
          title: "Sessione 2",
          llm: [
            { id: 1, name: "GPT-4", n_parameters: "175B" },
            { id: 2, name: "Claude 3", n_parameters: "52B" },
          ],
        },
      ],
    }).as("getSessions");

    cy.intercept("GET", "**/session_list/1", {
      statusCode: 200,
      body: {
        id: 1,
        title: "Sessione 1",
        llm: [
          { id: 1, name: "GPT-4", n_parameters: "175B" },
          { id: 2, name: "Claude 3", n_parameters: "52B" },
        ],
      },
    }).as("getSessionById");

    cy.intercept("GET", "**/question_blocks/compare/**", {
      statusCode: 200,
      body: {
        common_blocks: [
          {
            block_name: "Blocco A",
            llms: {
              1: { semantic_avg: 0.8, external_avg: 0.7 },
              2: { semantic_avg: 0.6, external_avg: 0.5 },
            },
          },
          {
            block_name: "Blocco B",
            llms: {
              1: { semantic_avg: 0.9, external_avg: 0.85 },
              2: { semantic_avg: 0.65, external_avg: 0.6 },
            },
          },
        ],
      },
    }).as("getComparison");

    cy.visit("http://localhost:3000/compare");
  });

  it("mostra il selettore di sessione", () => {
    cy.contains("Seleziona una sessione").should("exist");
  });

  it("inizialmente non visualizza i selettori LLM o il grafico", () => {
    cy.get('[data-cy="llm-selector"]').should("not.exist");
    cy.get('[data-cy="comparison-chart"]').should("not.exist");
  });

  it("visualizza LLMSelector e LLMComparisonChart dopo selezione sessione e LLM", () => {
    cy.get('[data-cy="session-select"]').select("Sessione 1");
    cy.get('[data-cy="first-llm-select"]').select("GPT-4");
    cy.get('[data-cy="second-llm-select"]').select("Claude 3");
    cy.wait("@getComparison");

    cy.get('[data-cy="llm-selector"]').should("exist");
    cy.get('[data-cy="comparison-chart"]').should("exist");
    cy.contains("GPT-4 - Semantica").should("exist");
    cy.contains("Claude 3 - Esterna").should("exist");
  });
});
