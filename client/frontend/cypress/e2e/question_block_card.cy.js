describe('QuestionBlockCard', () => {
  const sampleBlock = {
    id: 42,
    name: 'Blocco di esempio',
    prompt: [
      {
        prompt_text: 'Che ore sono?',
        expected_answer: 'Sono le tre.',
      },
      {
        prompt_text: 'Che giorno è oggi?',
        expected_answer: 'È giovedì.',
      },
    ],
  };

  const blockWithoutPrompts = {
    id: 99,
    name: 'Blocco vuoto',
    prompt: [],
  };

  beforeEach(() => {
    cy.visit('http://localhost:3000/components/question-blocks'); 
  });

  it('should render the block name and prompts', () => {
    cy.contains('Blocco di esempio').should('exist');
    cy.contains('Domanda: Che ore sono?').should('exist');
    cy.contains('Risposta attesa: Sono le tre.').should('exist');
  });

  it('should render fallback if no questions exist', () => {
    cy.contains('Blocco vuoto').should('exist');
    cy.contains('Nessuna domanda disponibile.').should('exist');
  });

  it('should call onDelete when clicking delete', () => {
    cy.window().then((win) => {
      cy.spy(win.console, 'log').as('consoleLog');
    });

    cy.get('[data-cy="delete-btn-42"]').click();
    cy.get('@consoleLog').should('have.been.calledWith', 'Deleted block', 42);
  });

  it('should handle error gracefully if delete fails', () => {
    cy.intercept('DELETE', '**/question_blocks/42', {
      statusCode: 500,
      body: { message: 'Errore di eliminazione' },
    }).as('deleteFail');

    cy.get('[data-cy="delete-btn-42"]').click();
    cy.get('.toast-error').should('contain.text', 'Errore di eliminazione');
  });

  it('should show all question-answer pairs', () => {
    cy.get('[data-cy="question-pair"]').should('have.length', 2);
  });

  it('should be accessible with keyboard', () => {
    cy.get('[data-cy="delete-btn-42"]').focus().type('{enter}');
    cy.get('@consoleLog').should('have.been.called');
  });
});
