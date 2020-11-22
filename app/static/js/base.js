window.onload = (event) => {
  var grid_items = document.querySelector('.grid');
  var msnry = new Masonry(grid_items, {
    itemSelector: '.grid-item',
    // percentPosition: true
  });
};

/*
nav_links = document.querySelectorAll('#navbar section .section-name');
nav_links.forEach(e => {
  e.onclick = () => {
    nav_links.forEach(n =>{
      n.parentElement.classList.remove('active');
    });
    e.parentElement.classList.add('active');
  };
});
*/
