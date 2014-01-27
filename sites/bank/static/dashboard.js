$(document).ready(function() {
  $('nav ul a').on('click', function() {
    $('nav ul a').removeClass('active');
    $(this).toggleClass('active');
  });
});