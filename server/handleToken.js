const { appkey, appsecret } = require("./config");

async function getAccessToken() {
    const url = "https://openapivts.koreainvestment.com:29443/oauth2/tokenP";
    const headers = {
        "content-type": "application/json",
    };
    const body = JSON.stringify({
        grant_type: "client_credentials",
        appkey: appkey,
        appsecret: appsecret,
    });

    try {
        const response = await fetch(url, {
            method: "POST",
            headers,
            body,
        });

        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching access token:", error);
        throw error;
    }
}

async function revokeAccessToken(token) {
    const url = "https://openapivts.koreainvestment.com:29443/oauth2/revokeP";
    const headers = {
        "content-type": "application/json",
    };
    const body = JSON.stringify({
        appkey: appkey,
        appsecret: appsecret,
        token,
    });

    try {
        const response = await fetch(url, {
            method: "POST",
            headers,
            body,
        });

        const data = await response.json();

        return data;
    } catch (error) {
        console.error("Error fetching access token:", error);
        throw error;
    }
}

module.exports = { getAccessToken, revokeAccessToken };
