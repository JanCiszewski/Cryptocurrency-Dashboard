export function renderCoins(coins) {
    const container = document.getElementById("coins");

    container.innerHTML = "";

    coins.forEach(coin => {
        const div = document.createElement("div");
        div.textContent = `${coin.name} - ${coin.price}`;
        container.appendChild(div);
    });
}