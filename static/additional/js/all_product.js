    //Adding Item to Cart
        function addToCart(event) {
            event.preventDefault();

            var quantity = parseInt(event.target.elements.quantity.value);
            var image = event.target.elements.image.value;
            var name = event.target.elements.name.value;
            var price = parseFloat(event.target.elements.price.value);
            var total = price * quantity;

            var item = {
                quantity: quantity,
                image: image,
                name: name,
                price: price,
                total: total
            };

            var cartItems = JSON.parse(localStorage.getItem('cartItems')) || [];
            cartItems.push(item);
            localStorage.setItem('cartItems', JSON.stringify(cartItems));
            $('#OpenModal').modal('show');
        }

        //Deleting Comment
        $(document).ready(function() {
            $('.delete-comment-form').on('submit', function(e) {
                e.preventDefault(); 
        
                var commentId = $(this).data('comment-id'); 
        
                $.ajax({
                    url: '/delete_comment/' + commentId + '/',
                    type: 'POST',
                    data: {
                        'csrfmiddlewaretoken': '{{ csrf_token }}'
                    },
                    success: function(response) {
                        $('.delete-comment-form[data-comment-id="' + commentId + '"]').closest('.row').remove();
                    },
                    error: function(xhr, status, error) {
                        alert('An error occurred while deleting the comment.');
                    }
                });
            });
        });

        //Adding Stars
        const stars = document.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.addEventListener('click', () => {
                stars.forEach((s, i) => {
                if (i <= index) {
                    s.innerHTML = '<i class="fas fa-star"></i>';
                } else {
                    s.innerHTML = '<i class="far fa-star"></i>';
                }
                });
                const ratingInput = document.getElementById('ratingInput');
                ratingInput.value = index + 1;
            });
        });

        // Counting Review
        document.addEventListener('DOMContentLoaded', function() {
            const reviewCountElement = document.getElementById('review-count');
            const reviewCountElement2 = document.getElementById('top-review-count');
            const mediaElements = document.querySelectorAll('div.media.mb-4');
            reviewCountElement.textContent = mediaElements.length.toString();
            reviewCountElement2.textContent = mediaElements.length.toString();
        });


        // Calculate the number of filled stars
        function calculateFilledStars(value) {
            const starElements = document.querySelectorAll('.text-primary small');
            const roundedValue = Math.round(value * 2) / 2; 

            for (let i = 0; i < starElements.length; i++) {
                if (i < roundedValue) {
                    starElements[i].classList.add('fas');
                    starElements[i].classList.remove('far');
                } else {
                    starElements[i].classList.add('far');
                    starElements[i].classList.remove('fas', 'fa-star-half-alt');
                }
            }

            if (roundedValue % 1 !== 0) {
            starElements[Math.floor(roundedValue)].classList.add('fas', 'fa-star-half-alt');
            starElements[Math.floor(roundedValue)].classList.remove('far');
            }
        }

        const mediaElements = document.querySelectorAll('.media.mb-4');
        const mediaCount = mediaElements.length;
        const starElements2 = document.querySelectorAll('.media .text-primary .fas.fa-star');
        const uniqueStarCount = new Set(starElements2).size;
        const ratingValue = uniqueStarCount / mediaCount;
        calculateFilledStars(ratingValue);
        