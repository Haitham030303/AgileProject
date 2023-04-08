window.onload = () => {
    $(document).ready(function() { //close button alert
        $('.close').click(function() {
            $(this).parent().fadeOut(120);
        });
    });
    
    
    // remove button
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
    
    // add button
    const addBtn = document.querySelector('.add_leader_btn');
    if (addBtn) {
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
            input.setAttribute('placeholder', 'Project Leader Email');
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

    }
    
    //   show more option
    const showMoreBtn = document.querySelector('.show-more-btn');
    const projectCards = document.querySelectorAll('.project-card');
    
    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', () => {
            projectCards.forEach(card => {
                card.classList.remove('hidden');
            });
            showMoreBtn.style.display = 'none';
            showLessBtn.style.display = 'block';
        });
    }
    
    //   show less option
    const projectCardHidden = document.querySelectorAll('.project-card-hidden');
    const showLessBtn = document.querySelector('.show-less-btn');
    if (showLessBtn && projectCardHidden) {
        showLessBtn.addEventListener('click', () => {
            projectCardHidden.forEach(card => {
                card.classList.add('hidden');
            });
            showLessBtn.style.display = 'none';
            showMoreBtn.style.display = 'block';
        });
    }
        
    //   show more option collab
    const showMoreBtnCollab = document.querySelector('.show-more-btn-collab');
    const collabCards = document.querySelectorAll('.collab-card');
    
    if (showMoreBtnCollab) {
        showMoreBtnCollab.addEventListener('click', () => {
            collabCards.forEach(card => {
                card.classList.remove('hidden');
            });
            showMoreBtnCollab.style.display = 'none';
            showLessBtnCollab.style.display = 'block';
        });
    }
    
    //   show less option collab
    const showLessBtnCollab = document.querySelector('.show-less-btn-collab');
    const collabCardHidden = document.querySelectorAll('.collab-card-hidden');
    
    if (showLessBtnCollab) {
        showLessBtnCollab.addEventListener('click', () => {
            collabCardHidden.forEach(card => {
                card.classList.add('hidden');
            });
            showLessBtnCollab.style.display = 'none';
            showMoreBtnCollab.style.display = 'block';
        });
    }

    function editFields() {
        // Enable all form fields
        document.querySelectorAll('input').forEach(input => input.disabled = false);
        
        // Show the Save button
        // document.getElementById('saveButton').style.display = 'block';
    }
};
