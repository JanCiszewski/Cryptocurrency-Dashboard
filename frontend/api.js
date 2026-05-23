export async function getCoins() {
    const response = await fetch("http://127.0.0.1:8000/coins/");
    const data = await response.json();
    return data;
}

export async function getCoin(id) {

    const response = await fetch(
        `http://127.0.0.1:8000/coins/${id}`
    );

    const data = await response.json();

    return data;
}

export async function getMe() {

    const token = localStorage.getItem("token");

    const response = await fetch(
        "http://127.0.0.1:8000/auth/me",
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("Failed to fetch user");
    }

    return await response.json();
}