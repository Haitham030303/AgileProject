$(document).ready(function() {   //close button alert
  $('.close').click(function() {
    $(this).parent().fadeOut(120);
  });
});


// Find all "remove" buttons and add a click event listener to each one
const removeBtns = document.querySelectorAll('.remove_leader_btn');
if (removeBtns.length === 1) {
  removeBtns[0].setAttribute("disabled", true);
}
removeBtns.forEach((btn) => {
  btn.addEventListener('click', (e) => {
    e.preventDefault();
    const inputContainer = e.target.parentNode;
    inputContainer.parentNode.removeChild(inputContainer);
  });
});

// Find the "add" button and add a click event listener
const addBtn = document.querySelector('.add_leader_btn');
addBtn.addEventListener('click', (e) => {
  e.preventDefault();
  const inputContainer = document.createElement('div');
  inputContainer.classList.add('project_leader_inputs');
  const input = document.createElement('input');
  input.setAttribute('autocomplete', 'off');
  input.setAttribute('class', 'form-control');
  input.setAttribute('type', 'text');
  input.setAttribute('minlength', '5');
  input.setAttribute('maxlength', '255');
  input.setAttribute('name', 'project_leader[]');
  input.setAttribute('placeholder', 'Leaders\'s name');
  const removeBtn = document.createElement('button');
  removeBtn.classList.add('leader_btn', 'remove_leader_btn');
  removeBtn.setAttribute('type', 'button');
  removeBtn.innerHTML = '<i class="far fa-times-circle"></i>';
  removeBtn.addEventListener('click', (e) => {
    e.preventDefault();
    inputContainer.parentNode.removeChild(inputContainer);
  });
  inputContainer.appendChild(input);
  inputContainer.appendChild(removeBtn);
  addBtn.parentNode.insertBefore(inputContainer, addBtn);
});


