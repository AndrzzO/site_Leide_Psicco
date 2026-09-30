/**
 * home.js — Script modular para a Home do Instituto Mente em Foco.
 *
 * Módulo 1: Revelação suave de seções (IntersectionObserver)
 * Módulo 2: Carrossel 3D Elegante (Coverflow em Arco Tridimensional)
 *           - Disposição em arco/círculo tridimensional suave
 *           - Drag com mouse (clique, segure e arraste)
 *           - Rotação com a roda do mouse (scroll wheel)
 *           - Swipe com o dedo em dispositivos móveis (touch)
 *           - Clique direto nos cards laterais para centralizá-los
 *           - Botões laterais de navegação (anterior / próximo)
 *           - Indicadores dinâmicos (dots) com estado ativo
 *           - Loop infinito circular (módulo N)
 *           - Acessibilidade por teclado (setas esquerda/direita)
 *           - Respeito a prefers-reduced-motion
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        /* ================================================================
           MÓDULO 1 — Revelação suave de seções
           ================================================================ */
        var prefereReducaoMovimento = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!prefereReducaoMovimento && ('IntersectionObserver' in window)) {
            var secoes = document.querySelectorAll(
                '.secao-introducao, .secao-identificacao, .secao-areas, .secao-sobre,' +
                '.secao-processo, .secao-neuro, .secao-conteudos, .secao-faq, .secao-cta-final'
            );
            if (secoes.length) {
                var observer = new IntersectionObserver(function (entries, obs) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add('secao--visivel');
                            obs.unobserve(entry.target);
                        }
                    });
                }, { root: null, rootMargin: '0px 0px -50px 0px', threshold: 0.1 });
                secoes.forEach(function (s) {
                    s.classList.add('secao--animavel');
                    observer.observe(s);
                });
            }
        }

        /* ================================================================
           MÓDULO 2 — Carrossel 3D de Áreas de Atuação
           ================================================================ */
        var carrossel = document.getElementById('carrossel-areas');
        var palco = document.getElementById('carrossel-palco');
        var btnPrev = document.getElementById('carrossel-anterior');
        var btnNext = document.getElementById('carrossel-proximo');
        var indicadoresWrap = document.getElementById('carrossel-indicadores');

        if (!carrossel || !palco) return;

        var cards = Array.prototype.slice.call(
            palco.querySelectorAll('.carrossel-3d__card')
        );
        var totalCards = cards.length;
        if (totalCards === 0) return;

        var indiceAtivo = 0;
        var dotElements = [];
        var estaArrastando = false;
        var foiArrastado = false;
        var pointerStartX = 0;
        var wheelBloqueado = false;

        /* ----------------------------------------------------------------
           2.1 — Criação dos indicadores (dots)
           ---------------------------------------------------------------- */
        if (indicadoresWrap && totalCards > 1) {
            for (var d = 0; d < totalCards; d++) {
                var dot = document.createElement('button');
                dot.className = 'carrossel-3d__dot' + (d === 0 ? ' ativo' : '');
                dot.setAttribute('type', 'button');
                dot.setAttribute('aria-label', 'Ir para área clínica ' + (d + 1));
                (function (indice) {
                    dot.addEventListener('click', function () {
                        irParaIndice(indice);
                    });
                })(d);
                indicadoresWrap.appendChild(dot);
                dotElements.push(dot);
            }
        }

        /* ----------------------------------------------------------------
           2.2 — Cálculo de posições tridimensionais (Arco/Cilindro Suave)
           ---------------------------------------------------------------- */
        function renderizar3D() {
            var isMobile = window.innerWidth < 768;
            var reducao = prefereReducaoMovimento;

            // Espaçamento horizontal refinado
            var espacamento = isMobile ? 180 : 225;

            cards.forEach(function (card, i) {
                // Distância circular mais curta (para loop infinito contínuo)
                var diff = i - indiceAtivo;
                while (diff > totalCards / 2) diff -= totalCards;
                while (diff < -totalCards / 2) diff += totalCards;

                var absDiff = Math.abs(diff);

                if (reducao) {
                    var op = (diff === 0) ? 1 : 0.4;
                    card.style.transform = 'translateX(' + (diff * espacamento) + 'px)';
                    card.style.opacity = op;
                    card.style.zIndex = 10 - absDiff;
                    card.style.pointerEvents = (diff === 0) ? 'auto' : 'none';
                    return;
                }

                var tx = 0;
                var tz = 0;
                var ry = 0;
                var escala = 1;
                var opacidade = 1;
                var brilho = 1;
                var zIndex = 10;
                var shadow = '0 10px 25px rgba(44, 60, 48, 0.12)';

                if (diff === 0) {
                    // Card central (destaque em foco, plano para o usuário)
                    tx = 0;
                    tz = 60;
                    ry = 0;
                    escala = 1.05;
                    opacidade = 1.0;
                    brilho = 1.0;
                    zIndex = 12;
                    shadow = '0 24px 48px rgba(44, 60, 48, 0.28)';
                } else if (absDiff === 1) {
                    // Vizinhos imediatos (curva suave voltada para o centro)
                    var sinal1 = diff > 0 ? 1 : -1;
                    tx = sinal1 * espacamento;
                    tz = isMobile ? -30 : -10;
                    ry = -sinal1 * (isMobile ? 20 : 16);
                    escala = isMobile ? 0.85 : 0.92;
                    opacidade = isMobile ? 0.55 : 0.90;
                    brilho = 0.92;
                    zIndex = 9;
                    shadow = '0 14px 30px rgba(44, 60, 48, 0.18)';
                } else {
                    // Laterais externas (arco da roda)
                    var sinal2 = diff > 0 ? 1 : -1;
                    tx = sinal2 * (isMobile ? 320 : 420);
                    tz = isMobile ? -100 : -70;
                    ry = -sinal2 * (isMobile ? 35 : 28);
                    escala = isMobile ? 0.70 : 0.82;
                    opacidade = isMobile ? 0 : 0.72;
                    brilho = 0.82;
                    zIndex = 6;
                    shadow = '0 8px 20px rgba(44, 60, 48, 0.12)';
                }

                card.style.transform = 'translateX(' + tx + 'px) translateZ(' + tz + 'px) rotateY(' + ry + 'deg) scale(' + escala + ')';
                card.style.opacity = opacidade;
                card.style.filter = 'brightness(' + brilho + ')';
                card.style.zIndex = zIndex;
                card.style.boxShadow = shadow;
                card.style.pointerEvents = (isMobile && absDiff > 1) ? 'none' : 'auto';

                card.classList.toggle('carrossel-3d__card--ativo', diff === 0);
            });

            // Atualiza indicadores (dots)
            dotElements.forEach(function (dot, idx) {
                var ativo = idx === indiceAtivo;
                dot.classList.toggle('ativo', ativo);
                dot.setAttribute('aria-current', ativo ? 'true' : 'false');
            });
        }

        /* ----------------------------------------------------------------
           2.3 — Funções de navegação (próximo / anterior / específico)
           ---------------------------------------------------------------- */
        function proximo() {
            indiceAtivo = (indiceAtivo + 1) % totalCards;
            renderizar3D();
        }

        function anterior() {
            indiceAtivo = (indiceAtivo - 1 + totalCards) % totalCards;
            renderizar3D();
        }

        function irParaIndice(novoIndice) {
            indiceAtivo = (novoIndice % totalCards + totalCards) % totalCards;
            renderizar3D();
        }

        // Botões de navegação lateral
        if (btnNext) {
            btnNext.addEventListener('click', function () {
                proximo();
            });
        }
        if (btnPrev) {
            btnPrev.addEventListener('click', function () {
                anterior();
            });
        }

        /* ----------------------------------------------------------------
           2.4 — Clique em card lateral: centraliza o card
           ---------------------------------------------------------------- */
        palco.addEventListener('click', function (e) {
            if (foiArrastado) {
                e.preventDefault();
                e.stopPropagation();
                foiArrastado = false;
                return;
            }

            var cardClicado = e.target.closest('.carrossel-3d__card');
            if (!cardClicado) return;

            var indiceClicado = parseInt(cardClicado.getAttribute('data-indice'), 10);
            if (!isNaN(indiceClicado) && indiceClicado !== indiceAtivo) {
                // Se clicou em card lateral, não navega o link — apenas centraliza
                e.preventDefault();
                irParaIndice(indiceClicado);
            }
        });

        /* ----------------------------------------------------------------
           2.5 — Drag com o mouse (Desktop)
           ---------------------------------------------------------------- */
        palco.addEventListener('mousedown', function (e) {
            // Permite interação nativa com links caso não haja arrasto
            if (e.target.closest('button')) return;
            estaArrastando = true;
            foiArrastado = false;
            pointerStartX = e.clientX;
            palco.classList.add('is-dragging');
        });

        document.addEventListener('mousemove', function (e) {
            if (!estaArrastando) return;
            var deltaX = e.clientX - pointerStartX;
            if (Math.abs(deltaX) > 8) {
                foiArrastado = true;
            }
        });

        document.addEventListener('mouseup', function (e) {
            if (!estaArrastando) return;
            estaArrastando = false;
            palco.classList.remove('is-dragging');

            if (foiArrastado) {
                var deltaX = e.clientX - pointerStartX;
                if (deltaX > 40) {
                    anterior();
                } else if (deltaX < -40) {
                    proximo();
                }
            }
        });

        /* ----------------------------------------------------------------
           2.6 — Touch Swipe (Dispositivos móveis / touch)
           ---------------------------------------------------------------- */
        var touchStartX = 0;
        var touchStartY = 0;

        palco.addEventListener('touchstart', function (e) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
            foiArrastado = false;
        }, { passive: true });

        palco.addEventListener('touchmove', function (e) {
            var deltaX = e.touches[0].clientX - touchStartX;
            var deltaY = e.touches[0].clientY - touchStartY;
            // Se o movimento for mais horizontal do que vertical, trata como swipe
            if (Math.abs(deltaX) > Math.abs(deltaY) && Math.abs(deltaX) > 10) {
                foiArrastado = true;
            }
        }, { passive: true });

        palco.addEventListener('touchend', function (e) {
            if (foiArrastado) {
                var deltaX = e.changedTouches[0].clientX - touchStartX;
                if (deltaX > 35) {
                    anterior();
                } else if (deltaX < -35) {
                    proximo();
                }
            }
        });

        /* ----------------------------------------------------------------
           2.7 — Scroll Wheel do mouse (rolagem do mouse sobre o carrossel)
           ---------------------------------------------------------------- */
        carrossel.addEventListener('wheel', function (e) {
            // Determina a intensidade e direção do scroll
            var delta = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
            if (Math.abs(delta) < 15) return;

            e.preventDefault(); // Impede scroll vertical da página durante o gesto no carrossel

            if (wheelBloqueado) return;
            wheelBloqueado = true;

            if (delta > 0) {
                proximo();
            } else {
                anterior();
            }

            // Throttle de 420ms para permitir uma troca suave por cada gesto da roda
            setTimeout(function () {
                wheelBloqueado = false;
            }, 420);
        }, { passive: false });

        /* ----------------------------------------------------------------
           2.8 — Navegação por teclado (Acessibilidade)
           ---------------------------------------------------------------- */
        carrossel.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                anterior();
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                proximo();
            }
        });

        /* ----------------------------------------------------------------
           2.9 — Inicialização e responsividade (Resize)
           ---------------------------------------------------------------- */
        renderizar3D();

        var resizeTimer;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                renderizar3D();
            }, 100);
        });

    });

})();
