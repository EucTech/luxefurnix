$(document).ready(function () {
    // DELETE FROM CART USING AJAX
    $(document).on('click', '.delete-from-cart', function () {
        let productId = $(this).data('product-id');
    
         // Make a request to the database using ajax
        $.ajax({
            type: 'DELETE',
            url:   `/shopping-cart/${productId}`,
            success: function (response) {
                $('#cart-count').text(response.count_cart);
                console.log(response.message);
            },
            error: function (error) {
                console.error('Error:', error)
            }
        });
    });


    $(document).on('input', '.quantity', function () {
        let productId = $(this).data('product-id');
        let quantity = $(this).val();

        let formData = {
            product_id: productId,
            quantity: quantity
        };

        $.ajax({
            type: 'POST',
            url:  `/shopping-cart/${productId}`,
            data: formData,
            success: function (response) {
                console.log(response.message);
                $(this).closest('.list').find('.total').text(`Total: $${response.total}`);
            },
            error: function (error) {
                console.error('Error:', error);
            }  
        });
    });
});