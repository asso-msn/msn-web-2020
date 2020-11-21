window.onload = (event) => {
  var grid_items = document.querySelector('.grid');
  var msnry = new Masonry(grid_items, {
    itemSelector: '.grid-item',
    // percentPosition: true
  });
};
