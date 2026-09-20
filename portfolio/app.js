/**
 * demonOS Developer Portfolio Client Script
 * Target: Emmanuel Twumasi
 */

(function () {
  'use strict';

  // =========================================================================
  // 1. Theme Toggle & Persistence
  // =========================================================================
  const themeToggle = document.getElementById('themeToggle');
  const htmlEl = document.documentElement;

  function initTheme() {
    const savedTheme = localStorage.getItem('demon_theme');
    if (savedTheme) {
      htmlEl.setAttribute('data-theme', savedTheme);
    } else {
      const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
      htmlEl.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
    }
  }

  function toggleTheme() {
    const currentTheme = htmlEl.getAttribute('data-theme') || 'dark';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    htmlEl.setAttribute('data-theme', nextTheme);
    localStorage.setItem('demon_theme', nextTheme);
    showToast(`Theme switched to ${nextTheme} mode`, 'success');
  }

  if (themeToggle) {
    themeToggle.addEventListener('click', toggleTheme);
  }

  // =========================================================================
  // 2. Typewriter Effect
  // =========================================================================
  const typewriterEl = document.getElementById('typewriter');
  const phrases = [
    'Autonomous Agent Systems',
    'Full-Stack Web Architecture',
    'Distributed Cloud Backends',
    'Self-Healing Test Gauntlets'
  ];

  let phraseIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typeSpeed = 80;

  function handleTypewriter() {
    if (!typewriterEl) return;
    const currentPhrase = phrases[phraseIndex];

    if (isDeleting) {
      typewriterEl.textContent = currentPhrase.substring(0, charIndex - 1);
      charIndex--;
      typeSpeed = 40;
    } else {
      typewriterEl.textContent = currentPhrase.substring(0, charIndex + 1);
      charIndex++;
      typeSpeed = 80;
    }

    if (!isDeleting && charIndex === currentPhrase.length) {
      isDeleting = true;
      typeSpeed = 1800; // Pause at end of phrase
    } else if (isDeleting && charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typeSpeed = 400; // Pause before typing new phrase
    }

    setTimeout(handleTypewriter, typeSpeed);
  }

  // =========================================================================
  // 3. Mobile Navigation Drawer
  // =========================================================================
  const mobileMenuBtn = document.getElementById('mobileMenuBtn');
  const navMenu = document.getElementById('navMenu');

  if (mobileMenuBtn && navMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = navMenu.classList.toggle('open');
      mobileMenuBtn.setAttribute('aria-expanded', isOpen);
    });

    // Close on nav-link click
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });

    // Close on outside click
    document.addEventListener('click', (e) => {
      if (!navMenu.contains(e.target) && !mobileMenuBtn.contains(e.target)) {
        navMenu.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // =========================================================================
  // 4. Project Category Filtering
  // =========================================================================
  const filterBtns = document.querySelectorAll('.filter-btn');
  const projectCards = document.querySelectorAll('.project-card');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => {
        b.classList.remove('active');
        b.setAttribute('aria-selected', 'false');
      });
      btn.classList.add('active');
      btn.setAttribute('aria-selected', 'true');

      const filter = btn.getAttribute('data-filter');

      projectCards.forEach(card => {
        const category = card.getAttribute('data-category');
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
          }, 10);
        } else {
          card.style.opacity = '0';
          card.style.transform = 'translateY(10px)';
          setTimeout(() => {
            card.style.display = 'none';
          }, 200);
        }
      });
    });
  });

  // =========================================================================
  // 5. Copy Email Utilities
  // =========================================================================
  const emailToCopy = 'protwumasi@gmail.com';

  function copyEmailToClipboard() {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(emailToCopy).then(() => {
        showToast(`Copied ${emailToCopy} to clipboard!`, 'success');
      }).catch(() => {
        fallbackCopy(emailToCopy);
      });
    } else {
      fallbackCopy(emailToCopy);
    }
  }

  function fallbackCopy(text) {
    const tempInput = document.createElement('input');
    tempInput.value = text;
    document.body.appendChild(tempInput);
    tempInput.select();
    try {
      document.execCommand('copy');
      showToast(`Copied ${text} to clipboard!`, 'success');
    } catch (err) {
      showToast('Could not copy email automatically.', 'error');
    }
    document.body.removeChild(tempInput);
  }

  const copyEmailBtn = document.getElementById('copyEmailBtn');
  const copyEmailQuickBtn = document.getElementById('copyEmailQuickBtn');
  if (copyEmailBtn) copyEmailBtn.addEventListener('click', copyEmailToClipboard);
  if (copyEmailQuickBtn) copyEmailQuickBtn.addEventListener('click', copyEmailToClipboard);

  // =========================================================================
  // 6. Contact Form Validation & Submission
  // =========================================================================
  const contactForm = document.getElementById('contactForm');
  const nameInput = document.getElementById('contactName');
  const emailInput = document.getElementById('contactEmail');
  const messageInput = document.getElementById('contactMessage');
  const nameError = document.getElementById('nameError');
  const emailError = document.getElementById('emailError');
  const messageError = document.getElementById('messageError');

  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  }

  if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
      e.preventDefault();
      let isValid = true;

      // Clear errors
      nameError.textContent = '';
      emailError.textContent = '';
      messageError.textContent = '';

      if (!nameInput.value.trim() || nameInput.value.trim().length < 2) {
        nameError.textContent = 'Please enter your name (at least 2 characters).';
        isValid = false;
      }

      if (!emailInput.value.trim() || !validateEmail(emailInput.value.trim())) {
        emailError.textContent = 'Please enter a valid email address.';
        isValid = false;
      }

      if (!messageInput.value.trim() || messageInput.value.trim().length < 8) {
        messageError.textContent = 'Please enter a message (at least 8 characters).';
        isValid = false;
      }

      if (isValid) {
        const submitBtn = document.getElementById('submitBtn');
        const originalText = submitBtn.innerHTML;
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span>Sending...</span>';

        setTimeout(() => {
          showToast('Thank you, Emmanuel! Your message was submitted successfully.', 'success');
          contactForm.reset();
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalText;
        }, 600);
      }
    });
  }

  // =========================================================================
  // 7. Toast Notification Dispatcher
  // =========================================================================
  function showToast(message, type = 'success') {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    const icon = type === 'success' ? '✅' : '⚠️';
    toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;

    container.appendChild(toast);

    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transform = 'translateY(10px)';
      toast.style.transition = 'all 0.3s ease';
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  }

  // =========================================================================
  // 8. Active Nav Link on Scroll (Intersection Observer)
  // =========================================================================
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav-link');

  if ('IntersectionObserver' in window && sections.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach(link => {
            if (link.getAttribute('href') === `#${id}`) {
              link.classList.add('active');
            } else {
              link.classList.remove('active');
            }
          });
        }
      });
    }, { threshold: 0.3 });

    sections.forEach(sec => observer.observe(sec));
  }

  // Initialize
  initTheme();
  handleTypewriter();

})();
