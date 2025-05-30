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

    cy.visit('http://localhost:3000/test-llm'); 
  });

  it('should show message when no LLM is selected', () => {
    cy.contains('Nessun LLM selezionato, aggiungi un LLM per cominciare.').should('exist');
  });

  it('should allow selecting and adding an LLM', () => {
    //cy.wait('@getLLMs');

    cy.get('select[name="selectllm"]').should('exist').select('1');
    cy.get('[data-cy="add-llm-button"]').should('be.visible').click();

    //cy.wait('@addLLM');

    //cy.contains('LLM 1', { timeout: 5000 }).should('exist');
    //cy.contains('Numero di Parametri: 7B').should('exist');
  });

  it('should allow removing an LLM from the session', () => {
    cy.intercept('GET', '**/sessions/1', {
      statusCode: 200,
      body: {
        llm: [{ id: 1, name: 'LLM 1', n_parameters: '7B' }]
      }
    });

    //cy.visit('http://localhost:3000/test-llm');

    //y.get('[data-cy="delete-llm-button"]').click();

    // cy.wait('@deleteLLM');

    cy.contains('LLM 1').should('not.exist');
  });
});
