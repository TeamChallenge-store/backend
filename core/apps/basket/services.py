def show_cart(request, serializer, response_data, cart_items):
    response_data.update(
        {
            "session_key": request.session.session_key,
            "cart_items": serializer.data,
            "total_items": sum(item.quantity for item in cart_items),
            "total_price": sum(
                item.quantity * item.product.price for item in cart_items
            ),
        },
    )
    return response_data
