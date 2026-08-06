// ===========================
// Imports
// ===========================
import { api } from "./api.js";
import { formatDate } from "./utils.js";

// ===========================
// Variables
// ===========================
const API_URL = "/api";
const APP_NAME = "Builder";
let currentTheme = "light";

// ===========================
// Object
// ===========================
const config = {
    apiUrl: API_URL,
    timeout: 5000,
    retry: 3,
};

// ===========================
// Array
// ===========================
const roles = ["admin", "editor", "viewer"];

// ===========================
// Function
// ===========================
function showToast(message) {
    console.log(message);
}

// ===========================
// Arrow Function
// ===========================
const formatPrice = (price) => {
    return `$${price}`;
};

// ===========================
// Class
// ===========================
class UserService {
    login() {
        console.log("User logged in");
    }

    logout() {
        console.log("User logged out");
    }
}

// ===========================
// Call Expression
// ===========================
showToast("Application Started");

// ===========================
// If
// ===========================
if (currentTheme === "light") {
    console.log("Using Light Theme");
}

// ===========================
// For
// ===========================
for (let i = 0; i < roles.length; i++) {
    console.log(roles[i]);
}

// ===========================
// While
// ===========================
let counter = 0;

while (counter < 3) {
    counter++;
}

// ===========================
// Try Catch
// ===========================
try {
    api.connect();
} catch (error) {
    console.error(error);
}

// ===========================
// Switch
// ===========================
switch (currentTheme) {
    case "light":
        console.log("Light");
        break;

    case "dark":
        console.log("Dark");
        break;

    default:
        console.log("Unknown");
}

// ===========================
// Event Listener
// ===========================
document.addEventListener("click", showToast);

// ===========================
// Export
// ===========================
export {
    showToast,
    formatPrice,
    UserService,
};