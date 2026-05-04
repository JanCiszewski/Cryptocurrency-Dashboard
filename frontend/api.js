//Connection with API
export async function getCoins() {
    const response = await fetch("http://127.0.0.1:8000/coins/");
    const data = await response.json();
    return data;
}