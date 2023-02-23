let autocomplete;

function initAutoComplete() {
    autocomplete = new google.maps.places.Autocomplete(
        document.getElementById('id_address'),
        {
            types: ['geocode', 'establishment'],
            //default in this app is "IN" - add your country code
            componentRestrictions: { 'country': ['ca'] },
        })
    // function to specify what should happen when the prediction is clicked
    autocomplete.addListener('place_changed', onPlaceChanged);
}

function onPlaceChanged() {
    var place = autocomplete.getPlace();

    // User did not select the prediction. Reset the input field or alert()
    if (!place.geometry) {
        document.getElementById('id_address').placeholder = "Start typing...";

    }
    else {
        // console.log('place name=>', place.name)
    }
    // get the address components and assign them to the fields
    console.log(place)
    let geocoder = new google.maps.Geocoder()
    let address = document.getElementById('id_address').value
    geocoder.geocode({ 'address': address }, function (results, status) {
        console.log(geocoder);
        //  If the Status get Okay then find Lat and Long
        if (status == google.maps.GeocoderStatus.OK) {
            let latitude = results[0].geometry.location.lat()
            let longitude = results[0].geometry.location.lng()

            //  Display Lat and Long on UI at the same time when we click on showing address.. By Jquery
            $('#id_latitude').val(latitude);
            $('#id_longitude').val(longitude);

            $('#id_address').val(address);

        }

    });

    //  Looping on address object for getting city, provienc, country and pin.

    for (let i = 0; i < place.address_components.length; i++) {

        for (let j = 0; j < place.address_components[i].types.length; j++) {
            // get Country
            if (place.address_components[i].types[j] == 'country') {
                $('#id_country').val(place.address_components[i].long_name)
            }
            // get City
            if (place.address_components[i].types[j] == "locality") {
                $('#id_city').val(place.address_components[i].long_name)
            }
            // get Postal Code
            if (place.address_components[i].types[j] == 'postal_code') {
                $('#id_pin_code').val(place.address_components[i].long_name)
            }
            // get Provienc
            if (place.address_components[i].types[j] == 'administrative_area_level_1') {
                $('#id_province').val(place.address_components[i].long_name)
            }

        }
    }

}





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

