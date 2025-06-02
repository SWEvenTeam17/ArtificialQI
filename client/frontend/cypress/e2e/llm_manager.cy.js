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

    cy.contains('Test LLM').should('exist');
    cy.contains('7B').should('exist');
  });

  it('should show validation error if form is submitted with empty fields', () => {
    cy.get('[data-cy="create-llm-form"]').submit();
    cy.get('.error-message').should('contain.text', 'Il nome è obbligatorio');
  });

  it('should show server error message if LLM creation fails', () => {
    cy.intercept('POST', '**/llm_list/', {
      statusCode: 500,
      body: { message: 'Errore del server' },
    }).as('failLLM');

    cy.get('input[name="name"]').type('Errore LLM');
    cy.get('input[name="nparameters"]').type('13B');
    cy.get('[data-cy="create-llm-form"]').submit();

    cy.get('.toast-error').should('contain.text', 'Errore del server');
  });

  it('should allow deleting an existing LLM and update the list', () => {
    cy.intercept('GET', '**/llm_list/', {
      statusCode: 200,
      body: [{ id: 2, name: 'LLM da cancellare', n_parameters: '13B' }],
    }).as('getLLMsToDelete');

    cy.intercept('DELETE', '**/llm_list/2', {
      statusCode: 204,
    }).as('deleteLLM');

    cy.reload();

    cy.contains('LLM da cancellare').should('exist');
    cy.get(`[data-cy="delete-llm-2"]`).click();
    cy.contains('LLM da cancellare').should('not.exist');
  });
});
