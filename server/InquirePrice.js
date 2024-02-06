const { MOCK_DOMAIN } = require("./constants");
const { appkey, appsecret } = require("./config");
const { getAccessToken } = require("./handleToken");

// 주식 현재가 시세
async function inquirePrice() {
    const accessToken = await getAccessToken();

    const searchParams = new URLSearchParams({
        fid_cond_mrkt_div_code: "J",
        fid_input_iscd: "005930",
    });
    const url = `${MOCK_DOMAIN}/uapi/domestic-stock/v1/quotations/inquire-price?${searchParams}`;

    const options = {
        method: "GET",
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${accessToken}`,
            appkey,
            appsecret,
            tr_id: "FHKST01010100",
        },
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        const data = await response.json();

        console.log("InquirePrice: ", data);

        if (data.rt_cd === "0") return data.output;
        else console.log(`실패: ${data.msg_cd}, ${data.msg1}`);
    } catch (error) {
        console.error("Error fetching inquire price:", error);
        throw error;
    }
}

inquirePrice();
