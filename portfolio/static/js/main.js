/* Khushbu Patidar - Portfolio interactions (no libraries needed) */
(() => {
  'use strict';

  const $ = (sel, ctx = document) => ctx.querySelector(sel);
  const $$ = (sel, ctx = document) => Array.from(ctx.querySelectorAll(sel));
  const root = document.documentElement;
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const finePointer = matchMedia('(hover: hover) and (pointer: fine)').matches;

  /* ---------- Toast ---------- */
  const toastEl = $('#toast');
  let toastTimer;
  function toast(message) {
    if (!toastEl) return;
    toastEl.textContent = message;
    toastEl.classList.add('is-show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toastEl.classList.remove('is-show'), 2800);
  }

  /* ---------- Theme toggle ---------- */
  $('#themeToggle')?.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    root.dataset.theme = next;
    try { localStorage.setItem('theme', next); } catch (e) { /* ignore */ }
  });

  /* ---------- Nav: mobile menu, scrolled state, active link ---------- */
  const nav = $('#nav');
  const navToggle = $('#navToggle');
  navToggle?.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    navToggle.setAttribute('aria-expanded', String(open));
  });
  $$('#navLinks a').forEach(a => a.addEventListener('click', () => {
    nav.classList.remove('is-open');
    navToggle?.setAttribute('aria-expanded', 'false');
  }));

  const links = $$('#navLinks a');
  const sections = links.map(a => $(a.getAttribute('href'))).filter(Boolean);
  const homeSection = $('#home');
  if (homeSection) sections.push(homeSection); // hero par koi link active nahi hona chahiye
  if ('IntersectionObserver' in window && sections.length) {
    const spy = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        links.forEach(a => a.classList.toggle('is-active', a.getAttribute('href') === '#' + entry.target.id));
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    sections.forEach(s => spy.observe(s));
  }

  /* ---------- Scroll progress + nav state ---------- */
  const bar = $('#progressBar');
  let ticking = false;
  function onScroll() {
    const max = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.style.transform = `scaleX(${max > 0 ? Math.min(scrollY / max, 1) : 0})`;
    nav?.classList.toggle('is-scrolled', scrollY > 24);
    ticking = false;
  }
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  /* ---------- Reveal on scroll (content halka halka aake settle hota hai) ---------- */
  $$('[data-stagger]').forEach(group => {
    $$(':scope > [data-reveal]', group).forEach((el, i) => el.style.setProperty('--d', `${i * 110}ms`));
  });
  $$('[data-delay]').forEach(el => el.style.setProperty('--d', `${el.dataset.delay}ms`));

  const revealEls = $$('[data-reveal]');
  const countEls = $$('[data-count]');

  function countUp(el) {
    const target = parseInt(el.dataset.count, 10) || 0;
    if (reduceMotion || target === 0) { el.textContent = target; return; }
    const duration = 1300;
    const start = performance.now();
    (function step(now) {
      const t = Math.min((now - start) / duration, 1);
      el.textContent = Math.round(target * (1 - Math.pow(1 - t, 3)));
      if (t < 1) requestAnimationFrame(step);
    })(start);
  }

  if (!('IntersectionObserver' in window) || reduceMotion) {
    revealEls.forEach(el => el.classList.add('is-in'));
    countEls.forEach(el => { el.textContent = el.dataset.count; });
  } else {
    countEls.forEach(el => { el.textContent = '0'; });
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        const el = entry.target;
        io.unobserve(el);
        el.classList.add('is-in');
        const delay = parseFloat(el.style.getPropertyValue('--d')) || 0;
        // Animation khatam hone ke baad reveal hata do, taaki hover effects normal chalein.
        setTimeout(() => {
          el.removeAttribute('data-reveal');
          el.style.removeProperty('--d');
        }, delay + 1300);
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -6% 0px' });
    revealEls.forEach(el => io.observe(el));

    const counterIO = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        counterIO.unobserve(entry.target);
        countUp(entry.target);
      });
    }, { threshold: 0.6 });
    countEls.forEach(el => counterIO.observe(el));
  }

  /* ---------- Typing effect ---------- */
  const typedEl = $('.typed');
  if (typedEl && !reduceMotion) {
    const words = (typedEl.dataset.words || '').split(',').map(s => s.trim()).filter(Boolean);
    if (words.length) {
      let w = 0, c = 0, deleting = false;
      typedEl.textContent = '';
      const tick = () => {
        const word = words[w];
        if (!deleting) {
          c++;
          typedEl.textContent = word.slice(0, c);
          if (c === word.length) { deleting = true; return setTimeout(tick, 1600); }
          return setTimeout(tick, 85);
        }
        c--;
        typedEl.textContent = word.slice(0, c);
        if (c === 0) { deleting = false; w = (w + 1) % words.length; return setTimeout(tick, 350); }
        setTimeout(tick, 40);
      };
      setTimeout(tick, 1200);
    }
  }


  /* ---------- Project cover: tap to open on touch devices ---------- */
  $$('.project__cover').forEach(cover => {
    cover.addEventListener('click', () => cover.classList.toggle('is-open'));
    cover.addEventListener('keydown', e => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cover.classList.toggle('is-open'); }
    });
  });

  /* ---------- Resume modal ---------- */
  const dialog = $('#resumeDialog');
  if (dialog) {
    const frame = $('iframe', dialog);
    $$('[data-open-resume]').forEach(btn => btn.addEventListener('click', () => {
      if (!frame.getAttribute('src')) frame.setAttribute('src', frame.dataset.src);
      dialog.showModal();
      document.body.style.overflow = 'hidden';
    }));
    $$('[data-close]', dialog).forEach(btn => btn.addEventListener('click', () => dialog.close()));
    dialog.addEventListener('click', e => { if (e.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { document.body.style.overflow = ''; });
  }

  /* ---------- Copy email / phone ---------- */
  $$('[data-copy]').forEach(btn => btn.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(btn.dataset.copy);
      toast('Copied: ' + btn.dataset.copy);
    } catch (e) {
      toast('Could not copy. Please select the text manually.');
    }
  }));

  /* ---------- Contact form ---------- */
  const form = $('#contactForm');
  form?.addEventListener('submit', async e => {
    e.preventDefault();
    const submit = $('button[type="submit"]', form);
    const label = $('span', submit);
    const original = label.textContent;

    $$('.field', form).forEach(f => f.classList.remove('has-error'));
    $$('.field__error', form).forEach(p => { p.textContent = ''; });

    submit.disabled = true;
    label.textContent = 'Sending...';
    try {
      const res = await fetch(form.action, {
        method: 'POST',
        body: new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });
      const data = await res.json();
      if (res.ok && data.ok) {
        form.reset();
        toast(data.message);
      } else if (data.errors) {
        Object.entries(data.errors).forEach(([field, msgs]) => {
          const p = $(`[data-error-for="${field}"]`, form);
          if (p) { p.textContent = msgs.join(' '); p.closest('.field')?.classList.add('has-error'); }
        });
        $('.has-error input, .has-error textarea', form)?.focus();
      } else {
        toast('Something went wrong. Please try again.');
      }
    } catch (err) {
      toast('Network problem. Please check your connection and try again.');
    } finally {
      submit.disabled = false;
      label.textContent = original;
    }
  });
})();
