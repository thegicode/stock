const fs = require("fs");
const path = require("path");

const { DOMAIN, URL } = require("../constants");
const { appkey, appsecret } = require("../config");

const TOKEN_PATH = path.resolve("./config/accessToken.json");

async function createAccessToken() {
    const requestURL = `${DOMAIN}${URL.ACCESS_TOKEN}`;
    const options = {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
            grant_type: "client_credentials",
            appkey,
            appsecret,
        }),
    };

    try {
        const response = await fetch(requestURL, options);
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching access token:", error);
        throw error;
    }
}

async function revokeAccessToken(token) {
    console.log("revokeAccessToken");

    const requestURL = `${DOMAIN}${URL.REVOKE_ACCESS_TOKEN}`;
    const options = {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
            appkey,
            appsecret,
            token,
        }),
    };

    try {
        const response = await fetch(requestURL, options);
        if (!response.ok) throw new Error(`Error: ${response.status}`);
        await saveAccessToken("{}");
        return await response.json();
    } catch (error) {
        console.error("Error revokeing access token:", error);
        throw error;
    }
}

async function saveAccessToken(token) {
    try {
        if (!token.access_token) return;
        await fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
    } catch (error) {
        console.error("Error saving token to file:", error);
        throw error;
    }
}

async function readAccessToken() {
    try {
        const data = await fs.readFileSync(TOKEN_PATH, "utf-8");
        if (!data) return null;

        const token = JSON.parse(data);

        console.log("readAccessToken", token);

        if (!token.access_token) return;
        return token;
    } catch (error) {
        console.error("Error reading token from file:", error);
        throw error;
    }
}

async function getAccessToken() {
    try {
        const token = await readAccessToken();

        console.log("getAccessToken token", token);

        if (token) {
            if (new Date(token.access_token_token_expired) > new Date()) {
                return token.access_token;
            }
        }

        const createdToken = await createAccessToken();

        await saveAccessToken(createdToken);

        return createdToken.access_token;

        // if (token && new Date(token.access_token_token_expired) > new Date()) {
        //     return token.access_token;
        // } else {
        //     if (token) revokeAccessToken(token);
        //     const createdToken = await createAccessToken();
        //     console.log("createdToken", createdToken.access_token);
        //     await saveAccessToken(createdToken);
        //     return createdToken.access_token;
        // }
    } catch (error) {
        console.error("Error getting access token:", error);
        throw error;
    }
}

// async function useAccessToken() {
//     try {
//         const accessToken = await getAccessToken();
//         console.log("Access Token:", accessToken);
//     } catch (error) {
//         console.error("Error using access token:", error);
//     }
// }
// useAccessToken();

module.exports = {
    createAccessToken,
    revokeAccessToken,
    saveAccessToken,
    readAccessToken,
    getAccessToken,
};
