function openSearch() {
    document.getElementById("myOverlay").style.display = "block";
    document.getElementById("bgFade").style.display = "none";    
  }
  
  function closeSearch() {
    document.getElementById("myOverlay").style.display = "none";
    document.getElementById("bgFade").style.display = "block";
  }
// menu
function openMenu() {
  document.getElementById("menuBars").style.display = "none";
  document.getElementById("closeCross").style.display = "block";
  document.getElementById("menus").style.display = "block";    
}

function closeMenu() {
  document.getElementById("menuBars").style.display = "block";
  document.getElementById("closeCross").style.display = "none";
  document.getElementById("menus").style.display = "none"; 
}
// button
var btn = $('#button');

$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});

