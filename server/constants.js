const path = require("path");

const URL = {
    ACCESS_TOKEN: "/oauth2/tokenP",
    REVOKE_ACCESS_TOKEN: "/oauth2/revokeP",
};

module.exports = {
    REAL_DOMAIN: "https://openapi.koreainvestment.com:9443",
    MOCK_DOMAIN: "https://openapivts.koreainvestment.com:29443",
    URL,
};
