<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pharmacy App</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .inventory, .cart {
            margin-bottom: 20px;
        }
        .inventory-table, .cart-table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            border: 1px solid #ccc;
        }
        button {
            padding: 8px 12px;
            margin: 5px;
            cursor: pointer;
        }
        .total {
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>

<h1>Pharmacy App</h1>

<div class="inventory">
    <h3>Inventory</h3>
    <table class="inventory-table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Stock</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody id="inventory-list">
            <!-- Inventory items will be populated here -->
        </tbody>
    </table>
</div>

<div class="cart">
    <h3>Your Cart</h3>
    <table class="cart-table">
        <thead>
            <tr>
                <th>Product</th>
                <th>Price</th>
                <th>Quantity</th>
                <th>Total</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody id="cart-list">
            <!-- Cart items will be populated here -->
        </tbody>
    </table>
    <p class="total">Total: $<span id="cart-total">0.00</span></p>
    <button id="sell-button">Sell</button>
</div>

<script>
// Fetch and display inventory
async function fetchInventory() {
    const response = await fetch('/api/inventory');
    const data = await response.json();
    const inventoryList = document.getElementById('inventory-list');
    inventoryList.innerHTML = '';
    data.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>$${item.price}</td>
            <td>${item.stock}</td>
            <td><button onclick="addToCart(${item.id})">Add to Cart</button></td>
        `;
        inventoryList.appendChild(row);
    });
}

// Cart functionality
const cart = [];

// Add product to cart
function addToCart(id) {
    fetch('/api/inventory', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id: id })
    }).then(response => response.json()).then(data => {
        if (data.success) {
            cart.push(data.product);
            updateCart();
        } else {
            alert('Product not added to cart');
        }
    });
}

// Update the cart
function updateCart() {
    const cartList = document.getElementById('cart-list');
    cartList.innerHTML = '';
    let total = 0;
    cart.forEach(item => {
        total += item.price;
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.name}</td>
            <td>$${item.price}</td>
            <td>1</td>
            <td>$${item.price}</td>
            <td><button onclick="removeFromCart(${item.id})">Remove</button></td>
        `;
        cartList.appendChild(row);
    });
    document.getElementById('cart-total').textContent = total.toFixed(2);
}

// Remove item from cart
function removeFromCart(id) {
    const index = cart.findIndex(item => item.id === id);
    if (index > -1) {
        cart.splice(index, 1);
        updateCart();
    }
}

// Sell items in the cart
document.getElementById('sell-button').addEventListener('click', () => {
    cart.forEach(item => {
        fetch('/api/sell', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id: item.id, quantity: 1 })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                alert(`Sale successful! Total: $${data.total}`);
            } else {
                alert('Error selling product');
            }
        });
    });
});

// Fetch inventory when page loads
fetchInventory();
</script>

</body>
</html>
