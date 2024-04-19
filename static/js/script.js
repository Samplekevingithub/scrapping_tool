(function() {
    const ratingContainer = document.querySelector('.rating-container');
  
    ratingContainer.addEventListener('click', (event) => {
      if (event.target.classList.contains('rating')) {
        const ratingElements = ratingContainer.querySelectorAll('.rating');
  
        ratingElements.forEach((element) => {
          if (element.dataset.value <= event.target.dataset.value) {
            element.classList.add('selected');
          } else {
            element.classList.remove('selected');
          }
        });
  
        const ratingInput = document.getElementById('rating-input');
  
        if (ratingInput) {
          ratingInput.value = event.target.dataset.value;
        }
      }
    });
  })();
