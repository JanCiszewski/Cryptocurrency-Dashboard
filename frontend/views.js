import { getCoins, getMe } from "./api.js";
import { renderCoins } from "./ui.js";

const content = document.getElementById("main-content");
const pageTitle = document.getElementById("page-title");
const menu = document.querySelector(".menu");
const appGrid = document.querySelector(".app-grid");

export async function loadView(view) {

    if (view === "dashboard") {

        pageTitle.innerHTML = "Dashboard";
        menu.style.display = "block";
        appGrid.classList.remove("auth-layout");

        content.innerHTML = `
        
            <div class="dashboard-top">

                <div class="balance-card">
                    <p class="balance-label">TOTAL BALANCE</p>

                    <h2 id="dashboard-balance">$0</h2>

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

                    <div class="portfolio-list" id="portfolio-list"></div>

                </section>

            </div>
        `;

        const coins = await getCoins();
        const user = await getMe();
        const balanceElement = document.getElementById("dashboard-balance");
        balanceElement.innerHTML = `$${user.balance.toLocaleString()}`;
        const portfolioList = document.getElementById("portfolio-list");
        portfolioList.innerHTML = "";
        user.coins.forEach((coin) => {
        portfolioList.innerHTML += `

            <div class="portfolio-item">

                <span>
                    ${coin.id}
                </span>

                <span>
                    ${coin.amount.toFixed(2)}
                </span>

            </div>

        `;

});
        renderCoins(coins, user);

    }

    if (view === "coins") {

        pageTitle.innerHTML = "Coins";
        menu.style.display = "block";
        appGrid.classList.remove("auth-layout");

        content.innerHTML = `
        
            <section class="market-section">

                <div class="section-title">
                    <h3>All Coins</h3>
                </div>

                <div class="cards" id="coins"></div>

            </section>
        `;

        const coins = await getCoins();
        const user = await getMe();
        renderCoins(coins,null,true);

    }

    if (view === "wallet") {

        pageTitle.innerHTML = "Wallet";
        menu.style.display = "block";
        appGrid.classList.remove("auth-layout");
        

        content.innerHTML = `

            <section class="wallet-section">

                <div class="section-title">
                    <h3>My Wallet</h3>
                </div>

                <div class="wallet-grid">

                    <div class="wallet-card">

                        <h4>Total Assets</h4>

                        <p class="wallet-balance" id="wallet-assets">$0</p>

                    </div>

                    <div class="wallet-card">

                        <h4>Top Holding</h4>

                        <p class="wallet-coin" id="top-coin">-</p>

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

            </section>`;

        const coins = await getCoins();
        const user = await getMe();
        const walletAssets =
        document.getElementById("wallet-assets");
        let totalAssets = 0;
        user.coins.forEach(userCoin => {
        const matchingCoin = coins.find(coin => coin.id === userCoin.id);

        if (matchingCoin) {
            totalAssets += matchingCoin.price * userCoin.amount;
        }

        });

        walletAssets.innerHTML =
            `$${totalAssets.toLocaleString(
                undefined,
                {
                    maximumFractionDigits: 2
                }
            )}`;

        const topCoin = document.getElementById("top-coin");
        if (user.coins.length > 0) {

            topCoin.innerHTML =
                user.coins[0].id;

        }

        renderCoins(coins, user);
    }

    if (view === "account") {

    const token = localStorage.getItem("token");
    if (token) {
        pageTitle.innerHTML = "Account";
        const user = await getMe();
        content.innerHTML = `

        <section class="account-section">

            <div class="account-card">

                <div class="account-header">

                    <h2>My Account</h2>

                    <p>
                        Manage your profile
                    </p>

                </div>

                <div class="account-info">

                    <div class="account-item">

                        <span>Username</span>

                        <strong>
                            ${user.username}
                        </strong>

                    </div>

                    <div class="account-item">
                        <span>Email</span>
                        <strong>
                            ${user.email}
                        </strong>
                    </div>

                    <div class="account-item">
                        <span>Available Balance</span>
                        <strong>
                            $${user.balance}
                        </strong>
                    </div>

                </div>

                <button id="edit-account-btn">Edit Profile</button>

            </div>

        </section>`;

        const editButton =
    document.getElementById(
        "edit-account-btn"
    );

editButton.addEventListener(
    "click",
    () => {

        const modal =
            document.createElement("div");

        modal.classList.add(
            "profile-modal"
        );

        modal.innerHTML = `

            <div class="profile-modal-content">

                <button class="close-modal">
                    ✕
                </button>

                <h2>Edit Profile</h2>
                <input type="text" id="edit-username" value="${user.username}" placeholder="Username">
                <input type="email" id="edit-email" value="${user.email}" placeholder="Email">
                <input type="password" id="edit-password" placeholder="New password">
                <button id="save-profile">Save Changes</button>
            </div>
        `;

        document.body.appendChild(modal);

        modal.querySelector(
            ".close-modal"
        ).addEventListener(
            "click",
            () => modal.remove()
        );

        modal.querySelector(
            "#save-profile"
        ).addEventListener(
            "click",
            async () => {

                const username =
                    document.getElementById(
                        "edit-username"
                    ).value;

                const email =
                    document.getElementById(
                        "edit-email"
                    ).value;
                const password =
                    document.getElementById(
                        "edit-password"
                    ).value;

                await fetch(
                    "http://127.0.0.1:8000/auth/update",
                    {
                        method: "PUT",

                        headers: {
                            "Content-Type":
                                "application/json",

                            "Authorization":
                                `Bearer ${token}`
                        },

                        body: JSON.stringify({
                            username,
                            email,
                            password
                        })
                    }
                );

                modal.remove();

                loadView("account");

            }
        );

    }
);

        return;
    }



    
    menu.style.display = "none";
    appGrid.classList.add("auth-layout");
    content.innerHTML = `

        <section class="auth-section">

            <div class="auth-card">

                <div class="auth-tabs">

                    <button
                        id="login-tab"
                        class="auth-tab active"
                    >
                        Login
                    </button>

                    <button
                        id="register-tab"
                        class="auth-tab"
                    >
                        Register
                    </button>

                </div>

                <h2 id="auth-title">
                    Login
                </h2>

                <form id="auth-form">

                    <input
                        type="text"
                        id="username"
                        placeholder="Username"
                        style="display: none;"
                    >

                    <input
                        type="email"
                        id="email"
                        placeholder="Email"
                        required
                    >

                    <input
                        type="password"
                        id="password"
                        placeholder="Password"
                        required
                    >

                    <button type="submit" id="auth-button">
                        Login
                    </button>

                </form>

                <p id="login-message"></p>

            </div>

        </section>
    `;

    let isRegisterMode = false;
    const loginTab = document.getElementById("login-tab");
    const registerTab = document.getElementById("register-tab");
    const usernameInput = document.getElementById("username");
    const authTitle = document.getElementById("auth-title");
    const authButton = document.getElementById("auth-button");

    loginTab.addEventListener("click", () => {

        isRegisterMode = false;
        usernameInput.style.display = "none";
        authTitle.innerHTML = "Login";
        authButton.innerHTML = "Login";
        loginTab.classList.add("active");
        registerTab.classList.remove("active");

    });

    registerTab.addEventListener("click", () => {

        isRegisterMode = true;
        usernameInput.style.display = "block";
        authTitle.innerHTML = "Register";
        authButton.innerHTML = "Register";
        registerTab.classList.add("active");
        loginTab.classList.remove("active");

    });

    const form = document.getElementById("auth-form");

    form.addEventListener("submit", async (e) => {

        e.preventDefault();

        const email =
            document.getElementById("email").value;

        const password =
            document.getElementById("password").value;

        const message =
            document.getElementById("login-message");

        try {

            if (isRegisterMode) {

                const username =
                    document.getElementById("username").value;

                const response = await fetch(
                    "http://127.0.0.1:8000/auth/register",
                    {
                        method: "POST",

                        headers: {
                            "Content-Type": "application/json"
                        },

                        body: JSON.stringify({
                            username,
                            email,
                            password
                        })
                    }
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.detail);
                }

                message.innerHTML =
                    "Account created successfully";

                return;
            }

            const response = await fetch(
                "http://127.0.0.1:8000/auth/login",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/x-www-form-urlencoded"
                    },

                    body: new URLSearchParams({
                        username: email,
                        password: password
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail);
            }

            localStorage.setItem(
                "token",
                data.access_token
            );

            message.innerHTML =
                "Logged in successfully";

            loadView("dashboard");

        } catch (error) {

            message.innerHTML = error.message;

        }

    });

}

  const logoutButton = document.querySelector('[data-view="logout"]');

    if (logoutButton) {
        logoutButton.addEventListener("click", (e) => {
                e.preventDefault();
                localStorage.removeItem("token");
                loadView("account");
            }
        );
    }
}