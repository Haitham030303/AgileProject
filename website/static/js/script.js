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


    //   show more / show less options
    const showMoreBtn = document.querySelector('.show-more-btn');
    const showLessBtn = document.querySelector('.show-less-btn');
    const projectCards = document.querySelectorAll('.project-card-hidden');
    const originalNumVisibleCards = 1;

    if (showMoreBtn) {
        showMoreBtn.addEventListener('click', () => {
            projectCards.forEach(card => {
                card.classList.remove('hidden');
            });
            showMoreBtn.style.display = 'none';
            showLessBtn.style.display = 'block'; // uncomment to use 
        });
        // show less
        showLessBtn.addEventListener('click', () => {
            projectCards.forEach(card => {
                card.classList.add('hidden');
            });
            showMoreBtn.style.display = 'block';
            showLessBtn.style.display = 'none';
        });
    }
    // show more 

    //   show more / show less options collab
    const showMoreBtnCollab = document.querySelector('.show-more-btn-collab');
    const showLessBtnCollab = document.querySelector('.show-less-btn-collab');
    const collabCards = document.querySelectorAll('.collab-card-hidden');
    const CollaboriginalNumVisibleCards = 1;

    // show more 
    if (showMoreBtnCollab) {
        showMoreBtnCollab.addEventListener('click', () => {
            collabCards.forEach(card => {
                card.classList.remove('hidden-collab');
            });
            showMoreBtnCollab.style.display = 'none';
            showLessBtnCollab.style.display = 'block'; // uncomment to use 
        });

    }

    // show less
    if (showLessBtnCollab) {
        showLessBtnCollab.addEventListener('click', () => {
            collabCards.forEach(card => {
                card.classList.add('hidden-collab');
            });
            showMoreBtnCollab.style.display = 'block';
            showLessBtnCollab.style.display = 'none';
        });
    }

    // show less // if needed 
    //   showLessBtn.addEventListener('click', () => {
    //     projectCards.forEach((card, index) => {
    //         if (index > originalNumVisibleCards) {
    //             card.classList.add('hidden');
    //         }
    //     });
    //     showMoreBtn.style.display = 'block';
    //     showLessBtn.style.display = 'none';
    // });


    const addBtn = document.querySelector('.add_leader_btn');
    // add button
    if (addBtn) {

        addBtn.addEventListener('click', (e) => {
            e.preventDefault();
            const inputContainer = document.createElement('div');
            inputContainer.classList.add('project_leader_inputs');
            const input = document.createElement('input');
            input.setAttribute('autocomplete', 'off');
            input.setAttribute('class', 'form-control');
            input.setAttribute('type', 'email');
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



};