const fs = require("fs");

const { MOCK_DOMAIN, TOKEN_PATH } = require("./constants");
const { appkey, appsecret } = require("./config");

async function createAccessToken() {
    const url = `${MOCK_DOMAIN}/oauth2/tokenP`;
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
        const response = await fetch(url, options);
        console.log("createAccessToken", response.json());

        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error("Error fetching access token:", error);
        throw error;
    }
}

async function revokeAccessToken(token) {
    console.log("revokeAccessToken");

    const url = `${MOCK_DOMAIN}/oauth2/revokeP`;
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
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        return await response.json();
    } catch (error) {
        console.error("Error revokeing access token:", error);
        throw error;
    }
}

async function saveTokenToFile(token) {
    try {
        if (!token.access_token) return;
        await fs.writeFileSync(TOKEN_PATH, JSON.stringify(token, null, 2));
    } catch (error) {
        console.error("Error saving token to file:", error);
        throw error;
    }
}

async function readTokenFromFile() {
    try {
        const data = await fs.readFileSync(TOKEN_PATH, "utf-8");
        if (!data) return null;

        const token = JSON.parse(data);
        if (!token.access_token) return;
        return token;
    } catch (error) {
        console.error("Error reading token from file:", error);
        throw error;
    }
}

async function getAccessToken() {
    try {
        const token = await readTokenFromFile();
        if (token && new Date(token.access_token_token_expired) > new Date()) {
            return token.access_token;
        } else {
            const createdToken = await createAccessToken();
            await saveTokenToFile(createdToken);
            return createdToken.access_token;
        }
    } catch (error) {
        console.error("Error getting access token:", error);
        throw error;
    }
}

async function useAccessToken() {
    try {
        const accessToken = await getAccessToken();
        console.log("Access Token:", accessToken);
    } catch (error) {
        console.error("Error using access token:", error);
    }
}
useAccessToken();

module.exports = {
    createAccessToken,
    revokeAccessToken,
    saveTokenToFile,
    readTokenFromFile,
    getAccessToken,
};
