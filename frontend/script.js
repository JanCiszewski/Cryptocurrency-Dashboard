import { getCoins } from "./api.js";
import { renderCoins } from "./ui.js";

async function init() {
    const coins = await getCoins();
    renderCoins(coins);
}

init();