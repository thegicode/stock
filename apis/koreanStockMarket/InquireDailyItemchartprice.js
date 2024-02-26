const { DOMAIN } = require("../../constants");
const { appkey, appsecret } = require("../../config");
const { getAccessToken } = require("../../server/handleToken");

// 국내주식기간별시세(일/주/월/년)[v1_국내주식-016]
async function inquireDailyItemchartprice() {
    const accessToken = await getAccessToken();

    const searchParams = new URLSearchParams({
        fid_cond_mrkt_div_code: "J", // J : 주식, ETF, ETN
        fid_input_iscd: "005930", // 종목번호 (6자리)
        fid_input_date_1: "20220101", // 조회 시작일자
        fid_input_date_2: "20220809", // 조회 시작일자
        fid_period_div_code: "M", // D:일봉, W:주봉, M:월봉, Y:년봉
        fid_org_adj_prc: "1", // 0:수정주가 1:원주가
    });

    const url = `${DOMAIN}/uapi/domestic-stock/v1/quotations/inquire-daily-itemchartprice?${searchParams}`;
    const options = {
        method: "GET",
        headers: {
            "content-type": "application/json",
            authorization: `Bearer ${accessToken}`,
            appkey,
            appsecret,
            tr_id: "FHKST03010100",
        },
        redirect: "follow",
    };

    try {
        const response = await fetch(url, options);
        if (!response.ok) throw new Error(`Error: ${response.statusText}`);
        const data = await response.json();

        console.log("InquireDailyItemchartprice: ", data);

        if (data.rt_cd === "0")
            return {
                output1: data.output1,
                output2: data.output2,
            };
        else console.log(`실패: ${data.msg_cd}, ${data.msg1}`);
    } catch (error) {
        console.error("Error fetching inquire price:", error);
        throw error;
    }
}

inquireDailyItemchartprice();
