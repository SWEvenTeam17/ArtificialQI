describe('SessionLLMPanel', () => {
  beforeEach(() => {
    cy.intercept('GET', '**/llm_list/', {
      statusCode: 200,
      body: [
        { id: 1, name: 'LLM 1', n_parameters: '7B' },
        { id: 2, name: 'LLM 2', n_parameters: '13B' }
      ]
    }).as('getLLMs');

    cy.intercept('POST', '**/add_llm/', { 
      statusCode: 200, 
      body: {} 
    }).as('addLLM');

    cy.intercept('DELETE', '**/remove_llm/1', {
      statusCode: 200,
    }).as('deleteLLM');

    cy.visit('http://localhost:3000/test-llm'); 
  });

  it('should show message when no LLM is selected', () => {
    cy.contains('Nessun LLM selezionato, aggiungi un LLM per cominciare.').should('exist');
  });

  it('should allow selecting and adding an LLM', () => {
    cy.get('select[name="selectllm"]').select('LLM 1');
    cy.get('[data-cy="add-llm-button"]').click();

    cy.contains('LLM 1').should('exist');
    cy.contains('Numero di Parametri: 7B').should('exist');
  });

  it('should handle error when adding an LLM fails', () => {
    cy.intercept('POST', '**/add_llm/', {
      statusCode: 500,
      body: { message: 'Errore durante l\'aggiunta' }
    }).as('failAdd');

    cy.get('select[name="selectllm"]').select('LLM 2');
    cy.get('[data-cy="add-llm-button"]').click();

    cy.get('.toast-error').should('contain.text', 'Errore durante l\'aggiunta');
  });

  it('should allow removing an LLM from the session', () => {
    cy.intercept('GET', '**/sessions/1', {
      statusCode: 200,
      body: {
        llm: [{ id: 1, name: 'LLM 1', n_parameters: '7B' }]
      }
    }).as('getSession');

    cy.reload();

    cy.get('[data-cy="delete-llm-button-1"]').click();

    cy.contains('LLM 1').should('not.exist');
  });

  it('should handle error when removing an LLM fails', () => {
    cy.intercept('DELETE', '**/remove_llm/2', {
      statusCode: 500,
      body: { message: 'Errore durante la rimozione' }
    }).as('failDelete');

    // Simulazione di LLM già presente
    cy.get('select[name="selectllm"]').select('LLM 2');
    cy.get('[data-cy="add-llm-button"]').click();

    cy.get('[data-cy="delete-llm-button-2"]').click();
    cy.get('.toast-error').should('contain.text', 'Errore durante la rimozione');
  });
});
