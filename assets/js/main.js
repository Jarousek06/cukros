/* ==========================================================================
   CUKROŠ — interakce webu
   ========================================================================== */
(function () {
  'use strict';

  /* ---------- Hlavička: pevný stav po odscrollování ---------- */
  var header = document.querySelector('.header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-stuck', window.scrollY > 24);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ---------- Mobilní menu ---------- */
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    var setMenu = function (open) {
      menu.classList.toggle('is-open', open);
      document.body.classList.toggle('is-locked', open);
      burger.setAttribute('aria-expanded', String(open));
      menu.setAttribute('aria-hidden', String(!open));
    };
    burger.addEventListener('click', function () {
      setMenu(!menu.classList.contains('is-open'));
    });
    menu.addEventListener('click', function (e) {
      if (e.target.closest('a')) setMenu(false);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) setMenu(false);
    });
    setMenu(false);
  }

  /* ---------- Odhalování obsahu při scrollu ---------- */
  var revealables = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && revealables.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-in');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    revealables.forEach(function (el) { io.observe(el); });
  } else {
    revealables.forEach(function (el) { el.classList.add('is-in'); });
  }

  /* ---------- Běžící pás: zdvojení pro plynulou smyčku ---------- */
  var track = document.querySelector('.marquee__track');
  if (track) {
    track.innerHTML += track.innerHTML;
  }

  /* ---------- Otevírací doba: dnešek + stav otevřeno/zavřeno ----------
     Po–So 7:30–18:00, Ne 8:30–18:00                                     */
  var HOURS = [
    { open: 8 * 60 + 30, close: 18 * 60 },  // 0 = neděle
    { open: 7 * 60 + 30, close: 18 * 60 },  // 1 = pondělí
    { open: 7 * 60 + 30, close: 18 * 60 },
    { open: 7 * 60 + 30, close: 18 * 60 },
    { open: 7 * 60 + 30, close: 18 * 60 },
    { open: 7 * 60 + 30, close: 18 * 60 },
    { open: 7 * 60 + 30, close: 18 * 60 }   // 6 = sobota
  ];
  /* celá předložková vazba — čeština má „ve středu“ a „ve čtvrtek“, ne „v“ */
  var DAY_NAMES = ['v neděli', 'v pondělí', 'v úterý', 've středu',
                   've čtvrtek', 'v pátek', 'v sobotu'];

  var pad = function (n) { return (n < 10 ? '0' : '') + n; };
  var hhmm = function (mins) { return Math.floor(mins / 60) + ':' + pad(mins % 60); };

  var now = new Date();
  var day = now.getDay();
  var minutes = now.getHours() * 60 + now.getMinutes();
  var today = HOURS[day];
  var isOpen = minutes >= today.open && minutes < today.close;

  document.querySelectorAll('[data-status]').forEach(function (el) {
    var label;
    if (isOpen) {
      label = 'Otevřeno · zavíráme v ' + hhmm(today.close);
    } else if (minutes < today.open) {
      label = 'Zavřeno · otevíráme v ' + hhmm(today.open);
    } else {
      var next = HOURS[(day + 1) % 7];
      label = 'Zavřeno · ' + DAY_NAMES[(day + 1) % 7] + ' otevíráme v ' + hhmm(next.open);
    }
    el.innerHTML = '<span class="dot' + (isOpen ? '' : ' is-closed') + '"></span>' + label;
  });

  /* zvýraznění dnešního dne v rozpisu */
  document.querySelectorAll('.hours [data-days]').forEach(function (row) {
    var days = row.getAttribute('data-days').split(',');
    if (days.indexOf(String(day)) !== -1) row.classList.add('is-today');
  });

  /* ---------- Rok v patičce ---------- */
  document.querySelectorAll('[data-year]').forEach(function (el) {
    el.textContent = String(now.getFullYear());
  });
})();

/* ==========================================================================
   Carousel — vodorovný pás fotek se šipkami, tečkami a automatickým posunem
   ========================================================================== */
(function () {
  'use strict';

  var klidnyRezim = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  document.querySelectorAll('[data-carousel]').forEach(function (carousel) {
    var pas = carousel.querySelector('[data-track]');
    var slidy = Array.prototype.slice.call(pas.children);
    var tecky = carousel.querySelector('[data-dots]');
    var pocitadlo = carousel.querySelector('[data-count]');
    var vzad = carousel.querySelector('[data-prev]');
    var vpred = carousel.querySelector('[data-next]');
    if (!slidy.length) return;

    var casovac = null;
    var zastaveno = klidnyRezim;
    /* data-interval="0" = neposouvat sám (víc carouselů na jedné stránce) */
    var zadano = parseInt(carousel.getAttribute('data-interval'), 10);
    var interval = isNaN(zadano) ? 5000 : zadano;
    var index = 0;          // kde jsme — drženo zvlášť, ne dopočítáváno ze scrollu
    var posouvame = null;   // běží programový posun? (pak scroll index nepřepisuje)

    /* tečky */
    slidy.forEach(function (slide, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'carousel__dot';
      b.setAttribute('aria-label', 'Přejít na fotku ' + (i + 1));
      b.addEventListener('click', function () {
        zastav();
        posunNa(i);
      });
      tecky.appendChild(b);
    });
    var seznamTecek = Array.prototype.slice.call(tecky.children);

    function aktivni() {
      var stred = pas.scrollLeft + pas.clientWidth / 2;
      var nejlepsi = 0;
      var nejmensi = Infinity;
      slidy.forEach(function (s, i) {
        var d = Math.abs(s.offsetLeft + s.offsetWidth / 2 - stred);
        if (d < nejmensi) { nejmensi = d; nejlepsi = i; }
      });
      return nejlepsi;
    }

    function posunNa(i) {
      index = Math.max(0, Math.min(slidy.length - 1, i));
      clearTimeout(posouvame);
      posouvame = setTimeout(function () { posouvame = null; }, 700);
      pas.scrollTo({ left: slidy[index].offsetLeft, behavior: klidnyRezim ? 'auto' : 'smooth' });
      prekresli();
    }

    function prekresli() {
      slidy.forEach(function (sl, j) {
        sl.classList.toggle('is-active', j === index);
      });
      seznamTecek.forEach(function (d, j) {
        d.setAttribute('aria-current', j === index ? 'true' : 'false');
      });
      if (pocitadlo) {
        pocitadlo.textContent = ('0' + (index + 1)).slice(-2) + ' / ' + ('0' + slidy.length).slice(-2);
      }
      var naZacatku = pas.scrollLeft <= 2;
      var naKonci = pas.scrollLeft + pas.clientWidth >= pas.scrollWidth - 2;
      if (vzad) vzad.disabled = naZacatku;
      if (vpred) vpred.disabled = naKonci;
    }

    function dalsi() {
      var naKonci = pas.scrollLeft + pas.clientWidth >= pas.scrollWidth - 2;
      posunNa(naKonci ? 0 : index + 1);
    }

    function spust() {
      if (zastaveno || casovac || interval <= 0) return;
      casovac = setInterval(function () {
        if (!document.hidden) dalsi();
      }, interval);
    }

    function pauza() {
      clearInterval(casovac);
      casovac = null;
    }

    function zastav() {
      zastaveno = true;
      pauza();
    }

    if (vzad) vzad.addEventListener('click', function () { zastav(); posunNa(index - 1); });
    if (vpred) vpred.addEventListener('click', function () { zastav(); dalsi(); });

    /* posun prstem nebo kolečkem = uživatel to řídí sám */
    ['pointerdown', 'touchstart', 'wheel', 'keydown'].forEach(function (ev) {
      pas.addEventListener(ev, zastav, { passive: true });
    });
    carousel.addEventListener('mouseenter', pauza);
    carousel.addEventListener('mouseleave', spust);
    carousel.addEventListener('focusin', pauza);
    carousel.addEventListener('focusout', spust);

    var tiky;
    pas.addEventListener('scroll', function () {
      clearTimeout(tiky);
      tiky = setTimeout(function () {
        if (posouvame) return;   // posouváme si to sami, index už je správně
        index = aktivni();
        prekresli();
      }, 90);
    }, { passive: true });
    window.addEventListener('resize', prekresli);

    /* šipkami po klávesnici, když je pás zaostřený */
    pas.setAttribute('tabindex', '0');
    pas.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); posunNa(index + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); posunNa(index - 1); }
    });

    prekresli();
    spust();
  });
})();
