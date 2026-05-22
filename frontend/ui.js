import { getCoin } from "./api.js";

function createCoinCard(coin) {
    const card = document.createElement("div");
    card.classList.add("card");

    card.innerHTML = `
        <h3>${coin.name}</h3>
        <p>${coin.symbol}</p>
        <p>$${coin.price.toLocaleString()}</p>
    `

     card.addEventListener("click", async () => {

        const coinDetails = await getCoin(coin.id);

        showCoinModal(coinDetails);

    });

    return card;

}

function showCoinModal(coin) {

    const oldModal = document.querySelector(".coin-modal");

    if (oldModal) {
        oldModal.remove();
    }

    const modal = document.createElement("div");

    modal.classList.add("coin-modal");

    modal.innerHTML = `

        <div class="coin-modal-content">

            <button class="close-modal">
                ✕
            </button>

            <h2>${coin.name}</h2>

            <p>
                Symbol: ${coin.symbol.toUpperCase()}
            </p>

            <p>
                Price: $${coin.price.toLocaleString()}
            </p>
            <button class="buy-button">
                 Buy Crypto
            </button>

            <p class="payment-message"></p>

        </div>
    `;

    document.body.appendChild(modal);

    const closeButton = modal.querySelector(".close-modal");

    closeButton.addEventListener("click", () => {
        modal.remove();
    });

    const buyButton = modal.querySelector(".buy-button");

    const paymentMessage = modal.querySelector(".payment-message");

    buyButton.addEventListener("click", async () => {

        try {

            const response = await fetch(
                `http://127.0.0.1:8000/payments/create?amount=${coin.price}`,
                {
                    method: "POST"
                }
            );

            const data = await response.json();

            setTimeout(() => {
                window.open(data.redirect_url, "_blank");
            }, 1500);

        } catch (error) {

            paymentMessage.innerHTML = `
                Payment failed
            `;

        }

    });

}

export function renderCoins(coins, showAll = false) {

    const container = document.getElementById("coins");

    container.innerHTML = "";

    let coinsToRender = coins;

    if (!showAll) {

        const featuredCoins = [
            "bitcoin",
            "ethereum",
            "solana",
            "ripple"
        ];

        coinsToRender = coins.filter(coin =>
            featuredCoins.includes(coin.id)
        );
    }

    coinsToRender.forEach(coin => {
        container.appendChild(createCoinCard(coin));
    });

}
