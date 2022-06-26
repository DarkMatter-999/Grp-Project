const hamburger = document.querySelector('.hamburger');
const hmenu = document.querySelector('.hmenu');

hamburger.addEventListener("click", function() {
   this.classList.toggle("is-active");
   hmenu.classList.toggle("is-active");
});