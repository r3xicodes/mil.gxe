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

  // Inject overlay menu and backdrop if not present
  function ensureMenu(){
    if(document.querySelector('.menu-overlay')) return;
    var overlay = document.createElement('div');
    overlay.className = 'menu-overlay';
    overlay.innerHTML = '<button class="close" aria-label="Close menu">✕</button>'+
      '<nav><ul>'+
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
    document.body.appendChild(backdrop);

    overlay.querySelector('.close').addEventListener('click',function(){toggleMenu(false)});
    backdrop.addEventListener('click',function(){toggleMenu(false)});
  }

  function toggleMenu(open){
    var overlay = document.querySelector('.menu-overlay');
    var backdrop = document.querySelector('.overlay-backdrop');
    if(!overlay || !backdrop) return;
    if(typeof open === 'undefined') open = !overlay.classList.contains('open');
    overlay.classList.toggle('open', !!open);
    backdrop.classList.toggle('open', !!open);
  }

  // Attach menu toggle to any element with .menu-toggle
  function initMenuToggle(){
    ensureMenu();
    var btns = document.getElementsByClassName('menu-toggle');
    for(var i=0;i<btns.length;i++){
      btns[i].addEventListener('click',function(e){
        e.preventDefault(); toggleMenu();
      });
    }
    // close on Escape
    window.addEventListener('keydown',function(e){ if(e.key === 'Escape'){ toggleMenu(false); } });
  }

  // Placeholder for modal open/close and map interactions
  window.milgxe = {
    openModal: function(id){console.log('open modal',id)}
  };

  // init on DOM ready
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initMenuToggle); else initMenuToggle();

})();