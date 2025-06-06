describe("LLMManager", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/llm_list/", {
      statusCode: 200,
      body: [],
    }).as("initialLLMs");

    cy.visit("http://localhost:3000/manage-llm");
    cy.wait("@initialLLMs");
  });

  it("crea, elimina e carica modelli da Ollama", () => {
    cy.intercept("POST", "**/llm_list/", (req) => {
      expect(req.body).to.deep.equal({
        name: "GPT Test",
        n_parameters: "123456",
      });
      req.reply({
        statusCode: 201,
        body: { id: 1, name: "GPT Test", n_parameters: "123456" },
      });
    }).as("createLLM");

    cy.intercept("GET", "**/llm_list/", {
      statusCode: 200,
      body: [{ id: 1, name: "GPT Test", n_parameters: "123456" }],
    }).as("refetchLLMs");

    cy.get('input[name="name"]').type("GPT Test");
    cy.get('input[name="nparameters"]').type("123456");
    cy.get('[data-cy="create-llm"]').click();

    cy.wait("@createLLM");
    cy.wait("@refetchLLMs");

    cy.contains("GPT Test").should("be.visible");

    cy.intercept("DELETE", "**/llm_list/1/", {
      statusCode: 204,
    }).as("deleteLLM");

    cy.intercept("GET", "**/llm_list/", {
      statusCode: 200,
      body: [],
    }).as("refetchAfterDelete");

    cy.get("button.btn-danger").click();

    cy.wait("@deleteLLM");
    cy.wait("@refetchAfterDelete");

    cy.contains("GPT Test").should("not.exist");
    cy.contains("Nessun LLM disponibile").should("be.visible");

    cy.intercept("POST", "**/llm_list/load_ollama/", {
      statusCode: 200,
      body: [
        { name: "mistral", n_parameters: "7000000000" },
        { name: "llama3", n_parameters: "13000000000" },
      ],
    }).as("loadOllama");

    cy.get('[data-cy="load-ollama-models"]').click();
    cy.wait("@loadOllama");
  });

  it("gestisce errore nel caricamento modelli da Ollama", () => {
    cy.intercept("POST", "**/llm_list/load_ollama/", {
      statusCode: 500,
      body: { error: "Errore interno" },
    }).as("ollamaFail");

    cy.get('[data-cy="load-ollama-models"]').click();
    cy.wait("@ollamaFail");

    cy.contains("Connessione con il server Ollama fallita.").should("exist");
  });
});
