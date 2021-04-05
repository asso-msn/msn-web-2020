window.onload = (event) => {
  var grid_items = document.querySelector('.grid');
  var msnry = new Masonry(grid_items, {
    itemSelector: '.grid-item',
    // percentPosition: true
  });
};

nav_links = document.querySelectorAll('#navbar section .section-name');
nav_links.forEach(e => {
  e.onclick = () => {
    let is_active = e.parentElement.classList.contains('active');
    nav_links.forEach(n =>{
      n.parentElement.classList.remove('active');
    });
    if (!is_active)
      e.parentElement.classList.add('active');
  };
});


// NAV BURGER
const click_overlay = document.getElementById('click-overlay');
navbar = document.getElementById('navbar')
document.getElementById('nav-toggle').onclick = () => {
    navbar.classList.toggle('open')
    if (navbar.classList.contains('open'))
        click_overlay.classList.add('active');
    else
        click_overlay.classList.remove('active');
};
click_overlay.onclick = () => {
    navbar.classList.remove('open');
    click_overlay.classList.remove('active');
};
