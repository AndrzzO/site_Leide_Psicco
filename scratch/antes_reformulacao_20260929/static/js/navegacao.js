/**
 * NAVEGAÇÃO E CONTROLE DO MENU MOBILE — INSTITUTO MENTE EM FOCO
 * JavaScript vanilla defensivo para gerenciamento de acessibilidade,
 * controle de foco, suporte a teclado (Escape) e redimensionamento responsivo.
 */

(function () {
  'use strict';

  // Seleção defensiva de elementos
  const toggleBtn = document.querySelector('[data-menu-toggle]');
  const panel = document.querySelector('[data-menu-panel]');
  const backdrop = document.querySelector('[data-menu-backdrop]');

  if (!toggleBtn || !panel) {
    return;
  }

  let menuAberto = false;

  function abrirMenu() {
    menuAberto = true;
    panel.removeAttribute('hidden');
    if (backdrop) backdrop.removeAttribute('hidden');

    // Pequeno timeout para engatilhar transição CSS suave
    requestAnimationFrame(() => {
      toggleBtn.setAttribute('aria-expanded', 'true');
      toggleBtn.setAttribute('aria-label', 'Fechar menu de navegação');
      panel.classList.add('menu-aberto');
      if (backdrop) backdrop.classList.add('ativo');
      document.body.classList.add('menu-travado');
    });

    // Foco no primeiro link acessível do menu
    const primeiroLink = panel.querySelector('a');
    if (primeiroLink) {
      primeiroLink.focus();
    }
  }

  function fecharMenu(restaurarFoco = true) {
    if (!menuAberto) return;

    menuAberto = false;
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.setAttribute('aria-label', 'Abrir menu de navegação');
    panel.classList.remove('menu-aberto');
    if (backdrop) backdrop.classList.remove('ativo');
    document.body.classList.remove('menu-travado');

    // Aguarda o fim da animação/transição antes de ocultar
    setTimeout(() => {
      if (!menuAberto) {
        panel.setAttribute('hidden', '');
        if (backdrop) backdrop.setAttribute('hidden', '');
      }
    }, 250);

    if (restaurarFoco) {
      toggleBtn.focus();
    }
  }

  // Alternância pelo botão de toggle
  toggleBtn.addEventListener('click', function (evento) {
    evento.stopPropagation();
    if (menuAberto) {
      fecharMenu(true);
    } else {
      abrirMenu();
    }
  });

  // Fechamento pelo clique no backdrop (clique fora)
  if (backdrop) {
    backdrop.addEventListener('click', function () {
      fecharMenu(true);
    });
  }

  // Fechamento ao clicar em qualquer link interno do menu
  panel.addEventListener('click', function (evento) {
    const link = evento.target.closest('a');
    if (link) {
      fecharMenu(false);
    }
  });

  // Suporte a teclado: Tecla Escape e Focus Trap / Loop acessível
  document.addEventListener('keydown', function (evento) {
    if (!menuAberto) return;

    if (evento.key === 'Escape' || evento.key === 'Esc') {
      evento.preventDefault();
      fecharMenu(true);
      return;
    }

    if (evento.key === 'Tab') {
      const elementosFocaveis = Array.from(
        panel.querySelectorAll('a[href], button:not([disabled]), [tabindex]:not([tabindex="-1"])')
      );
      // Inclui o botão de alternância no ciclo para permitir fechamento direto
      elementosFocaveis.unshift(toggleBtn);

      if (elementosFocaveis.length === 0) return;

      const primeiro = elementosFocaveis[0];
      const ultimo = elementosFocaveis[elementosFocaveis.length - 1];

      if (evento.shiftKey) {
        if (document.activeElement === primeiro) {
          evento.preventDefault();
          ultimo.focus();
        }
      } else {
        if (document.activeElement === ultimo) {
          evento.preventDefault();
          primeiro.focus();
        }
      }
    }
  });

  // Monitora redimensionamento de janela (Breakpoint Desktop 1080px)
  const mediaQueryDesktop = window.matchMedia('(min-width: 1080px)');
  function verificarLargura(e) {
    if (e.matches && menuAberto) {
      fecharMenu(false);
    }
  }

  if (mediaQueryDesktop.addEventListener) {
    mediaQueryDesktop.addEventListener('change', verificarLargura);
  } else if (mediaQueryDesktop.addListener) {
    mediaQueryDesktop.addListener(verificarLargura);
  }
})();
