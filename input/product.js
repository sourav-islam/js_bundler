// ===========================
// Imports
// ===========================
import { api } from "./api.js";
import { formatPrice } from "./global.js";

// ===========================
// Variables
// ===========================
const API_URL = "/product-api";
const PRODUCT_LIMIT = 20;
let currentTheme = "light";

// ===========================
// Object
// ===========================
const config = {
    apiUrl: API_URL,
    timeout: 4000,
    cache: true,
};

// ===========================
// Array
// ===========================
const categories = [
    "Electronics",
    "Furniture",
    "Books",
];

// ===========================
// Function
// ===========================
function showToast(message) {
    console.log("Product:", message);
}

function loadProducts() {
    console.log("Loading Products");
}

// ===========================
// Arrow Function
// ===========================
const calculateDiscount = (price, discount) => {
    return price - discount;
};

// ===========================
// Class
// ===========================
class ProductService {

    fetchProducts() {
        console.log("Fetching Products");
    }

    deleteProduct(id) {
        console.log(id);
    }

}

// ===========================
// Call Expression
// ===========================
loadProducts();

// ===========================
// If Statement
// ===========================
if (PRODUCT_LIMIT > 10) {
    console.log("Large Catalog");
}

// ===========================
// For Loop
// ===========================
for (const category of categories) {
    console.log(category);
}

// ===========================
// While Loop
// ===========================
let page = 1;

while (page < 3) {
    page++;
}

// ===========================
// Try Catch
// ===========================
try {
    api.fetchProducts();
} catch (error) {
    console.error(error);
}

// ===========================
// Switch
// ===========================
switch (currentTheme) {

    case "light":
        console.log("Light Theme");
        break;

    default:
        console.log("Other Theme");

}

// ===========================
// Event Listener
// ===========================
document.addEventListener(
    "scroll",
    loadProducts
);

// ===========================
// Export
// ===========================
export {
    loadProducts,
    ProductService,
    calculateDiscount,
};