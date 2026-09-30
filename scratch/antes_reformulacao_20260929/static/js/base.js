/**
 * JavaScript Base — Instituto Mente em Foco
 * Utilitários essenciais e acessibilidade (Vanilla JS nativo).
 */
document.addEventListener('DOMContentLoaded', () => {
  // Acessibilidade: Garante que o Skip Link passe o foco real para o <main>
  const skipLink = document.querySelector('.skip-link');
  const mainContent = document.querySelector('#conteudo-principal');

  if (skipLink && mainContent) {
    skipLink.addEventListener('click', () => {
      mainContent.setAttribute('tabindex', '-1');
      mainContent.focus();
    });
  }
});
