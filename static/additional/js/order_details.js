// Calculate and update the total price
document.addEventListener("DOMContentLoaded", function() {
    var totalElement = document.getElementById("totalPrice");
    var total = 0;

    var priceElements = document.querySelectorAll(".it_price");
    priceElements.forEach(function(element) {
        var price = parseFloat(element.textContent.trim());
        total += price;
    });

    totalElement.textContent = total.toFixed(2) + "/-";
});


// Downloading Invoice Process
var downloadButton = document.getElementById('downloadButton');
downloadButton.addEventListener('click', function(event) {
event.preventDefault();
// Generate the PDF from the invoice details HTML
html2pdf()
    .from(document.body)
    .save('invoice.pdf');
});