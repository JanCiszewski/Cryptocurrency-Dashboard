import { loadView } from "./views.js";

document.querySelectorAll("[data-view]").forEach(link => {

    link.addEventListener("click", (e) => {

        e.preventDefault();

        const view = link.dataset.view;

        loadView(view);

    });

});

const token = localStorage.getItem("token");

if (token) {
    loadView("dashboard");
} else {
    loadView("account");
}