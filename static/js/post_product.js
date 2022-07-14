function post_product() {
    const product_name = $('#product-name').val();
    const category = $('#category').val();
    const product_desc = $('#product-desc').val();
    const start_price = $('#product-start-price').val();
    const product_img = $('#product-img').val();
    const user_id = $('#user-id').val();
    const user_name = $('#user-name').val();
    const user_phone = $('#user-phone').val();

    $.ajax({
        type: 'POST',
        url: '/products',
        data: {
            productName_give: product_name,
            category_give: category,
            productDesc_give: product_desc,
            startPrice_give: start_price,
            productImg_give: product_img,
            userId_give: user_id,
            userName_give: user_name,
            userPhone_give: user_phone
        },
        success: function (response) {
            alert(response['msg'])
            window.location.href= '/';
        }
    });
}