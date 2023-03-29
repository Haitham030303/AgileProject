$(document).ready(function() {   //close button alert
  $('.close').click(function() {
    $(this).parent().fadeOut(120);
  });
});


const addBtn = document.querySelector('#add-btn');
const inputBox = document.querySelector('#input-box');

addBtn.addEventListener('click', function() {
  inputBox.style.display = inputBox.style.display === 'none' ? 'block' : 'none';
});


