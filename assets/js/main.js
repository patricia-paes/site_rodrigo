/* Rodrigo Victor — interações do site */
(function () {
  'use strict';

  var WHATSAPP = '5521996160489';

  /* ---------- ano do rodapé ---------- */
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();

  /* ---------- topo fixo ---------- */
  var topo = document.querySelector('.topo');
  var fixar = function () {
    topo.classList.toggle('is-fixo', window.scrollY > 40);
  };
  fixar();
  window.addEventListener('scroll', fixar, { passive: true });

  /* ---------- menu mobile ---------- */
  var botao = document.getElementById('menu');
  var nav = document.getElementById('nav');

  function fecharMenu() {
    nav.classList.remove('is-aberto');
    botao.setAttribute('aria-expanded', 'false');
    botao.setAttribute('aria-label', 'Abrir menu');
  }

  botao.addEventListener('click', function () {
    var aberto = nav.classList.toggle('is-aberto');
    botao.setAttribute('aria-expanded', String(aberto));
    botao.setAttribute('aria-label', aberto ? 'Fechar menu' : 'Abrir menu');
  });

  nav.addEventListener('click', function (e) {
    if (e.target.closest('a')) fecharMenu();
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && nav.classList.contains('is-aberto')) {
      fecharMenu();
      botao.focus();
    }
  });

  /* ---------- link ativo conforme a seção visível ---------- */
  var links = Array.prototype.slice.call(nav.querySelectorAll('a[href^="#"]'));
  var alvos = links
    .map(function (a) { return document.querySelector(a.getAttribute('href')); })
    .filter(Boolean);

  if ('IntersectionObserver' in window && alvos.length) {
    var obs = new IntersectionObserver(function (entradas) {
      entradas.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          a.classList.toggle('is-ativo', a.getAttribute('href') === '#' + en.target.id);
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    alvos.forEach(function (s) { obs.observe(s); });
  }

  /* ---------- máscara de telefone ---------- */
  var tel = document.getElementById('f-tel');
  if (tel) {
    tel.addEventListener('input', function () {
      var d = tel.value.replace(/\D/g, '').slice(0, 11);
      var out = d;
      if (d.length > 2) out = '(' + d.slice(0, 2) + ') ' + d.slice(2);
      if (d.length > 6) {
        var corte = d.length > 10 ? 7 : 6;
        out = '(' + d.slice(0, 2) + ') ' + d.slice(2, corte) + '-' + d.slice(corte);
      }
      tel.value = out;
    });
  }

  /* ---------- formulário: abre o WhatsApp já preenchido ---------- */
  var form = document.getElementById('form');
  if (!form) return;

  var erro = document.getElementById('form-erro');

  function mostrarErro(msg, campo) {
    erro.textContent = msg;
    erro.hidden = false;
    if (campo) campo.focus();
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    erro.hidden = true;

    var nome = form.nome.value.trim();
    var fone = form.telefone.value.replace(/\D/g, '');
    var mod = form.modalidade.value;
    var msg = form.mensagem.value.trim();

    if (nome.length < 2) return mostrarErro('Informe seu nome para continuar.', form.nome);
    if (fone.length < 10) return mostrarErro('Informe um WhatsApp com DDD, com 10 ou 11 dígitos.', form.telefone);
    if (!form.consentimento.checked) return mostrarErro('Marque a autorização de contato para enviar.', form.consentimento);

    var texto =
      'Olá, Rodrigo! Vim pelo site.\n\n' +
      'Nome: ' + nome + '\n' +
      'WhatsApp: ' + form.telefone.value + '\n' +
      'Modalidade: ' + mod +
      (msg ? '\nObjetivo: ' + msg : '') +
      '\n\nGostaria de agendar uma avaliação.';

    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
  });
})();
