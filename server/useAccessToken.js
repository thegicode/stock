const { getAccessToken, revokeAccessToken } = require("./handleToken");

async function getToken() {
    try {
        const token = await getAccessToken();
        console.log("Access Token:", token);
    } catch (error) {
        console.error("Failed to get access token:", error);
    }
}
getToken();

async function revokeToken() {
    try {
        const token = "";
        const revoked = await revokeAccessToken(token);
        console.log("revoked", revoked);
    } catch (error) {
        console.error("Failed to get access token:", error);
    }
}

// revokeToken();
