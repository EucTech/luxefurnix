$(document).ready(function () {
    $('.carty').unbind().click(function (event) {
        event.preventDefault(); // Prevent the default form submission

        let productId = $(this).data('product-id');
        let formData = {
            product_id: productId,
        };

        // console.log('Constructed URL:', `/shopping-cart/${productId}`);
        // Make a request to the database using ajax
        $.ajax({
            type: 'POST',
            url: `/add-to-cart/${productId}`,
            data: formData,
            success: function (response) {
                // Update the cart count in the UI
                $('#cart-count').text(response.count_cart);
                console.log(response.message);
            },
            error: function (error) {
                console.error('Error:', error)
            },
        });
    });
}); 
