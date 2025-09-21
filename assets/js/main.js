// Minimal site JS for mil.gxe scaffold
(function(){
  // Simple carousel auto-scroll
  var c = document.getElementById('carousel');
  if(c){
    var i = 0;
    setInterval(function(){
      i = (i+1) % c.children.length;
      c.style.transform = 'translateX(' + (-i * 272) + 'px)';
      c.style.transition = 'transform .6s ease';
    },4000);
  }

  // Inject overlay menu and backdrop if not present (with ARIA + focus management)
  function ensureMenu(){
    if(document.querySelector('.menu-overlay')) return;
    var overlay = document.createElement('div');
    overlay.className = 'menu-overlay';
    overlay.setAttribute('role','dialog');
    overlay.setAttribute('aria-modal','true');
    overlay.setAttribute('aria-hidden','true');
    overlay.innerHTML = '<button class="close" aria-label="Close menu">✕</button>'+
      '<nav aria-label="Main navigation"><ul>'+
      '<li><a href="/index.html">Home</a></li>'+
      '<li><a href="/about.html">About</a></li>'+
      '<li><a href="/branches/index.html">Branches</a></li>'+
      '<li><a href="/tech/index.html">Tech</a></li>'+
      '<li><a href="/history/index.html">History</a></li>'+
      '<li><a href="/media/index.html">Media</a></li>'+
      '<li><a href="/contact/index.html">Contact</a></li>'+
      '</ul></nav>';
    document.body.appendChild(overlay);

    var backdrop = document.createElement('div');
    backdrop.className = 'overlay-backdrop';
    backdrop.setAttribute('aria-hidden','true');
    document.body.appendChild(backdrop);

    overlay.querySelector('.close').addEventListener('click',function(){toggleMenu(false)});
    backdrop.addEventListener('click',function(){toggleMenu(false)});

    // store focusable nodes for focus trap
    overlay._focusable = Array.prototype.slice.call(overlay.querySelectorAll('a,button'));
    overlay._firstFocusable = overlay._focusable[0] || null;
    overlay._lastFocusable = overlay._focusable[overlay._focusable.length-1] || null;
  }

  function toggleMenu(open){
    var overlay = document.querySelector('.menu-overlay');
    var backdrop = document.querySelector('.overlay-backdrop');
    if(!overlay || !backdrop) return;
    if(typeof open === 'undefined') open = !overlay.classList.contains('open');
    overlay.classList.toggle('open', !!open);
    backdrop.classList.toggle('open', !!open);
    overlay.setAttribute('aria-hidden', !!open ? 'false' : 'true');
    backdrop.setAttribute('aria-hidden', !!open ? 'false' : 'true');

    // when opening, move focus into overlay and trap
    if(open){
      overlay._lastFocused = document.activeElement;
      try{ (overlay._firstFocusable || overlay).focus(); }catch(e){}
      document.body.classList.add('overlay-open');
      // focus trap
      document.addEventListener('keydown', _trapTab);
    } else {
      // restore
      if(overlay._lastFocused && typeof overlay._lastFocused.focus === 'function') overlay._lastFocused.focus();
      document.body.classList.remove('overlay-open');
      document.removeEventListener('keydown', _trapTab);
    }
  }

  function _trapTab(e){
    if(e.key !== 'Tab') return;
    var overlay = document.querySelector('.menu-overlay');
    if(!overlay || !overlay.classList.contains('open')) return;
    var first = overlay._firstFocusable;
    var last = overlay._lastFocusable;
    if(!first || !last) return;
    if(e.shiftKey && document.activeElement === first){
      e.preventDefault(); last.focus();
    } else if(!e.shiftKey && document.activeElement === last){
      e.preventDefault(); first.focus();
    }
  }

  // Attach menu toggle to any element with .menu-toggle
  function initMenuToggle(){
    ensureMenu();
    var btns = document.getElementsByClassName('menu-toggle');
    for(var i=0;i<btns.length;i++){
      (function(b){
        b.setAttribute('aria-expanded','false');
        b.addEventListener('click',function(e){
          e.preventDefault(); toggleMenu();
          // sync aria-expanded after a tiny delay to let class toggle
          setTimeout(function(){
            var overlay = document.querySelector('.menu-overlay');
            b.setAttribute('aria-expanded', overlay && overlay.classList.contains('open') ? 'true' : 'false');
          },50);
        });
      })(btns[i]);
    }
    // close on Escape
    window.addEventListener('keydown',function(e){ if(e.key === 'Escape'){ toggleMenu(false); } });
  }

  // Placeholder for modal open/close and map interactions
  window.milgxe = {
    openModal: function(id){console.log('open modal',id)}
  };

  // Simple newsletter client-side handler for Netlify forms
  function initSignupForm(){
    var form = document.querySelector('form[name="newsletter"]');
    if(!form) return;
    form.addEventListener('submit',function(e){
      e.preventDefault();
      var data = new FormData(form);
      fetch(form.action || '/', { method: 'POST', body: data }).then(function(){
        var msg = form.querySelector('.signup-success');
        if(msg){ msg.textContent = 'Thanks — we\'ll be in touch!'; msg.style.display = 'block'; }
        form.reset();
      }).catch(function(){
        var msg = form.querySelector('.signup-success');
        if(msg){ msg.textContent = 'Submission failed — please try again.'; msg.style.display = 'block'; }
      });
    });
  }

  // init on DOM ready
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initMenuToggle); else initMenuToggle();
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initSignupForm); else initSignupForm();

})();