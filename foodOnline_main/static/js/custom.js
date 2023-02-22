

$(document).ready(function () {
    // Add to cart
    $('.add_to_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                } else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);

                    // Subtotal, tac and grand totl
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })
    })

    // Decrease Cart
    $('.decrese_cart').on('click', function (e) {
        e.preventDefault();

        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        cart_id = $(this).attr('id');
        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function (response) {
                console.log(response)
                if (response.status == 'login_required') {
                    swal(response.message, '', 'info').then(function () {
                        window.location = '/login';
                    })
                } else if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                }
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    $('#qty-' + food_id).html(response.qty);
                    if (window.location.pathname == '/cart/') {
                        removeCartItem(response.qty, cart_id)
                        checkEmptyCart()
                        // Subtotal, tac and grand totl
                        applyCartAmount(
                            response.cart_amount['subtotal'],
                            response.cart_amount['tax'],
                            response.cart_amount['grand_total']
                        )
                    }
                }
            }
        })
    })


    //  Place the cart item quantity on load

    $('.item_qty').each(function () {
        let the_id = $(this).attr('id')
        let qty = $(this).attr('data-qty')
        // console.log(qty);
        $('#' + the_id).html(qty)
    })


    // Delete Cart Item

    $('.delete_cart').on('click', function (e) {
        e.preventDefault();


        cart_id = $(this).attr('data-id');
        url = $(this).attr('data-url');

        $.ajax({
            type: 'GET',
            url: url,
            // data: data,
            success: function (response) {
                console.log(response)
                if (response.status == 'Failed') {
                    swal(response.message, '', 'error')
                }
                else {
                    $('#cart_counter').html(response.cart_counter['cart_count']);
                    swal(response.status, response.message, 'success')
                    removeCartItem(0, cart_id)
                    checkEmptyCart()
                    // Subtotal, tac and grand totl
                    applyCartAmount(
                        response.cart_amount['subtotal'],
                        response.cart_amount['tax'],
                        response.cart_amount['grand_total']
                    )
                }
            }
        })
    })

    // delete cart element from page after clicking delete button
    function removeCartItem(cartItemQty, cart_id) {
        if (cartItemQty <= 0) {
            //  remove element
            document.getElementById('cart-item-' + cart_id).remove()
        }
    }

    //  Check if the cart is empty
    function checkEmptyCart() {
        let cart_counter = document.getElementById('cart_counter').innerHTML;
        if (cart_counter == 0) {
            document.getElementById('empty-cart').style.display = 'block'
        }
    }

    //  Apply Cart Amount
    function applyCartAmount(subtotal, tax, grand_total) {
        if (window.location.pathname == '/cart/') {
            $('#subtotal').html(subtotal)
            $('#tax').html(tax)
            $('#total').html(grand_total)
        }
    }

})

