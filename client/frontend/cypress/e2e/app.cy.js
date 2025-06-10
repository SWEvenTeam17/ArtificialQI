describe("Home Page - Visualizzazione delle sessioni", () => {
  beforeEach(() => {
    cy.intercept("GET", "**/session_list/", {
      statusCode: 200,
      body: [
        {
          id: 1,
          title: "Benchmark GPT vs Claude",
          description: "Sessione per confrontare GPT-4 e Claude 3",
          created_at: "2024-05-25T12:00:00Z",
          updated_at: "2024-05-26T12:00:00Z",
          llm: [
            {
              id: 1,
              name: "GPT-4",
              n_parameters: "175B",
            },
            {
              id: 2,
              name: "Claude 3",
              n_parameters: "Unknown",
            },
          ],
        },
        {
          id: 2,
          title: "Test LLM open-source",
          description: "Sessione per valutare LLaMA e Mistral",
          created_at: "2024-05-24T12:00:00Z",
          updated_at: "2024-05-26T13:00:00Z",
          llm: [
            {
              id: 3,
              name: "LLaMA 3",
              n_parameters: "65B",
            },
            {
              id: 4,
              name: "Mistral 7B",
              n_parameters: "7B",
            },
          ],
        },
      ],
    }).as("getSessions");

    cy.visit("http://localhost:3000/");
  });

  it("visualizza il titolo della pagina e la lista delle sessioni", () => {
    cy.wait("@getSessions");
    cy.get(".container").within(() => {
      cy.contains("h1", "ArtificialQI").should("be.visible");
      cy.contains("Per cominciare, seleziona una sessione:").should(
        "be.visible",
      );
      cy.contains("Benchmark GPT vs Claude").should("be.visible");
      cy.contains("Test LLM open-source").should("be.visible");
    });
  });

  it("verifica che ogni sessione abbia un titolo e i LLM associati", () => {
    cy.wait("@getSessions");
    cy.get(".container").within(() => {
      cy.contains("Benchmark GPT vs Claude")
        .parents(".col")
        .within(() => {
          cy.contains("Sessione per confrontare GPT-4 e Claude 3").should(
            "exist",
          );
        });

      cy.contains("Test LLM open-source")
        .parents(".col")
        .within(() => {
          cy.contains("Sessione per valutare LLaMA e Mistral").should("exist");
        });
    });
  });
});
