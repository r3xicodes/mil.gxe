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

  // Placeholder for modal open/close and map interactions
  window.milgxe = {
    openModal: function(id){console.log('open modal',id)}
  };
})();