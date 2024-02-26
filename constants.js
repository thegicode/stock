const REAL_DOMAIN = "https://openapi.koreainvestment.com:9443";
const MOCK_DOMAIN = "https://openapivts.koreainvestment.com:29443";

const URL = {
    // OAuth인증
    ACCESS_TOKEN: "/oauth2/tokenP",
    REVOKE_ACCESS_TOKEN: "/oauth2/revokeP",

    // 국내주식시세
    INQUIRE_PRICE: "/uapi/domestic-stock/v1/quotations/inquire-price", // 주식현재가 시세
};

module.exports = {
    DOMAIN: MOCK_DOMAIN,
    REAL_DOMAIN,
    MOCK_DOMAIN,
    URL,
};
