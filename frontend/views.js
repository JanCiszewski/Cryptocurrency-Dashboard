import { getCoins } from "./api.js";
import { renderCoins } from "./ui.js";

const content = document.getElementById("main-content");

export async function loadView(view) {

    if (view === "dashboard") {

        content.innerHTML = `
        
            <div class="dashboard-top">

                <div class="balance-card">
                    <p class="balance-label">TOTAL BALANCE</p>

                    <h2>$167,312<span>.92</span></h2>

                    <div class="stats">

                        <div class="stat">
                            <p>Today</p>
                            <span class="negative">-2.5%</span>
                        </div>

                        <div class="stat">
                            <p>7 Days</p>
                            <span class="positive">+4.25%</span>
                        </div>

                        <div class="stat">
                            <p>30 Days</p>
                            <span class="positive">+11.5%</span>
                        </div>

                    </div>
                </div>

            </div>

            <div class="dashboard-grid">

                <section class="market-section">

                    <div class="section-title">
                        <h3>Market Overview</h3>
                    </div>

                    <div class="cards" id="coins"></div>

                </section>

                <section class="portfolio-section">

                    <div class="section-title">
                        <h3>My Portfolio</h3>
                    </div>

                    <div class="portfolio-list">

                        <div class="portfolio-item">
                            <span>Bitcoin</span>
                            <span>37%</span>
                        </div>

                        <div class="portfolio-item">
                            <span>Ethereum</span>
                            <span>20%</span>
                        </div>

                        <div class="portfolio-item">
                            <span>Solana</span>
                            <span>18%</span>
                        </div>

                        <div class="portfolio-item">
                            <span>XRP</span>
                            <span>12%</span>
                        </div>

                    </div>

                </section>

            </div>
        `;

        const coins = await getCoins();

        renderCoins(coins);

    }

    if (view === "coins") {

        content.innerHTML = `
        
            <section class="market-section">

                <div class="section-title">
                    <h3>All Coins</h3>
                </div>

                <div class="cards" id="coins"></div>

            </section>
        `;

        const coins = await getCoins();

        renderCoins(coins, true);

    }

        if (view === "wallet") {

        content.innerHTML = `

            <section class="wallet-section">

                <div class="section-title">
                    <h3>My Wallet</h3>
                </div>

                <div class="wallet-grid">

                    <div class="wallet-card">

                        <h4>Total Assets</h4>

                        <p class="wallet-balance">$167,312</p>

                    </div>

                    <div class="wallet-card">

                        <h4>Top Holding</h4>

                        <p class="wallet-coin">Bitcoin</p>

                    </div>

                    <div class="wallet-card">

                        <h4>24h Profit</h4>

                        <p class="wallet-profit">+$2,430</p>

                    </div>

                </div>

                <div class="wallet-coins">

                    <div class="section-title">
                        <h3>Owned Coins</h3>
                    </div>

                    <div class="cards" id="coins"></div>

                </div>

            </section>
        `;

        const coins = await getCoins();

        renderCoins(coins);

    }
}