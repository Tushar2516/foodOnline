

$(document).ready(function(){
    $('.add_to_cart').on('click', function(e){
        e.preventDefault();
        
        food_id = $(this).attr('data-id');
        url = $(this).attr('data-url');
        data = {
            food_id : food_id,
        }
        $.ajax({
            type :'GET',
            url :url,
            data : data,
            success : function(response){
                 
            }
        })
    })

    //  Place the cart item quantity on load

    $('.item_qty').each(function(){
        var the_id = $(this).attr('id')
        var qty = $(this).attr('data-qty')
        // console.log(qty);
        $('#'+the_id).html(qty)
    })

})