describe('Create Block Form', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/question-blocks/create');
  });

  it('should allow user to fill and submit the form with two questions', () => {
    cy.intercept('POST', '**/question_blocks/', {
      statusCode: 201,
      body: {
        id: 1,
        name: 'Blocco di test'
      },
    }).as('createBlock');

    cy.get('[data-cy="block-name-input"]')
      .should('exist')
      .type('Blocco di test')
      .should('have.value', 'Blocco di test');

    cy.contains('Aggiungi una domanda').click();

    cy.get('input[name^="question"]').eq(0).type('Qual è la capitale dell\'Italia?');
    cy.get('input[name^="answer"]').eq(0).type('Roma');

    cy.get('input[name^="question"]').eq(1).type('Quanto fa 2+2?');
    cy.get('input[name^="answer"]').eq(1).type('4');

    cy.get('[data-cy="create-block-form"]').submit();

    cy.wait('@createBlock');

    cy.get('.toast')
      .should('exist')
      .and('contain.text', 'creato con successo');
  });
});
