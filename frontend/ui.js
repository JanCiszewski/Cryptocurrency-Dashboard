function createCoinCard(coin) {
    const card = document.createElement("div");
    card.classList.add("card");

    card.innerHTML = `
        <h3>${coin.name}</h3>
        <p>${coin.symbol}</p>
        <p>$${coin.price.toLocaleString()}</p>
    `
    return card;

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