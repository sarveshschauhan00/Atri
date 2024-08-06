document.addEventListener('DOMContentLoaded', function () {
    // Add event listeners for "Add to Cart" buttons
    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            addToCart(productId);
        });
    });

    // Add event listeners for "Remove from Cart" buttons
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
    removeFromCartButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const productId = this.dataset.productId;
            removeFromCart(productId);
        });
    });

    // Add event listener for the checkout form submission
    const checkoutForm = document.querySelector('#checkout-form');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', function (event) {
            event.preventDefault();
            handleCheckoutFormSubmission(this);
        });
    }
});

function addToCart(productId) {
    fetch(`/add_to_cart/${productId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product added to cart!');
            updateCartDisplay(data.cart);
        } else {
            alert('Error adding product to cart.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function removeFromCart(productId) {
    fetch(`/remove_from_cart/${productId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Product removed from cart!');
            updateCartDisplay(data.cart);
        } else {
            alert('Error removing product from cart.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function handleCheckoutFormSubmission(form) {
    const formData = new FormData(form);
    const formObject = {};
    formData.forEach((value, key) => {
        formObject[key] = value;
    });

    fetch('/checkout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(formObject),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Order placed successfully!');
            window.location.href = `/confirmation/${data.order_id}`;
        } else {
            alert('Error placing order.');
        }
    })
    .catch(error => console.error('Error:', error));
}

function updateCartDisplay(cart) {
    const cartItemsContainer = document.querySelector('#cart-items');
    const totalPriceContainer = document.querySelector('#total-price');

    if (cartItemsContainer && totalPriceContainer) {
        cartItemsContainer.innerHTML = '';
        let totalPrice = 0;

        cart.forEach(item => {
            const cartItem = document.createElement('div');
            cartItem.classList.add('cart-item');
            cartItem.innerHTML = `
                <p>${item.name} - ${item.quantity} x $${item.price}</p>
                <button class="remove-from-cart" data-product-id="${item.id}">Remove</button>
            `;
            cartItemsContainer.appendChild(cartItem);
            totalPrice += item.price * item.quantity;
        });

        totalPriceContainer.textContent = `Total: $${totalPrice.toFixed(2)}`;

        // Re-attach event listeners for the new "Remove from Cart" buttons
        const removeFromCartButtons = document.querySelectorAll('.remove-from-cart');
        removeFromCartButtons.forEach(button => {
            button.addEventListener('click', function (event) {
                event.preventDefault();
                const productId = this.dataset.productId;
                removeFromCart(productId);
            });
        });
    }
}
