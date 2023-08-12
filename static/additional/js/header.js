var counter = JSON.parse(localStorage.getItem('cartItems')) || [];
var all_items = counter.length; // Count the number of items
document.getElementById('total').textContent =  all_items;