const { appkey, appsecret } = require("../../config");
const { DOMAIN, URL } = require("../../constants");
const { getAccessToken } = require("../../server/accessTokenManager");

// 주식 현재가 시세
async function inquirePrice() {
    const accessToken = await getAccessToken();

    const searchParams = new URLSearchParams({
        FID_COND_MRKT_DIV_CODE: "J", // J : (주식, ETF, ETN) W: ELW
        FID_INPUT_ISCD: "005930", // 종목번호 (6자리), ETN의 경우, Q로 시작 (EX. Q500001), 삼성전자
    });
    const apiURL = `${DOMAIN}${URL.INQUIRE_PRICE}?${searchParams}`;

    const options = {
        method: "GET",
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${accessToken}`,
            appkey,
            appsecret,
            tr_id: "FHKST01010100", // 주식현재가 시세
            // custtype: P, // 개인
        },
    };

    try {
        const response = await fetch(apiURL, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        const data = await response.json();

        console.log("InquirePrice: ", data);

        if (data.rt_cd === "0") return data;
        else console.log(`실패: ${data.msg_cd}, ${data.msg1}`);
    } catch (error) {
        console.error("Error fetching inquire price:", error);
        throw error;
    }
}

inquirePrice();
