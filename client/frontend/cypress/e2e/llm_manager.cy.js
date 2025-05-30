describe('LLMManager', () => {
  beforeEach(() => {
    cy.intercept('GET', '**/llm_list/', {
      statusCode: 200,
      body: [],
    }).as('getEmptyLLMs');

    cy.visit('http://localhost:3000/components/llm-manager');
  });

  it('should render the LLM form and show empty message if no LLMs exist', () => {
    cy.contains('Gestisci LLM').should('exist');
    cy.wait('@getEmptyLLMs');
    cy.contains('Nessun LLM disponibile').should('exist');
  });

  it('should allow creating a new LLM and show it in the list', () => {
    cy.intercept('POST', '**/llm_list/', {
      statusCode: 201,
      body: {
        id: 1,
        name: 'Test LLM',
        n_parameters: '7B',
      },
    }).as('createLLM');

    cy.intercept('GET', '**/llm_list/', {
      statusCode: 200,
      body: [
        {
          id: 1,
          name: 'Test LLM',
          n_parameters: '7B',
        },
      ],
    }).as('getLLMs');

    cy.get('input[name="name"]').type('Test LLM');
    cy.get('input[name="nparameters"]').type('7B');
    cy.get('[data-cy="create-llm-form"]').submit();

    cy.wait('@createLLM');
    cy.wait('@getLLMs');

    cy.contains('Test LLM').should('exist');
    cy.contains('7B').should('exist');
  });
});
