const { dartkey } = require("../config");

// 조건부 자본증권 미상환 잔액
async function cndlCaplScritsNrdmpBlce(corpCode, year, partCode) {
    const url = "https://opendart.fss.or.kr/api/cndlCaplScritsNrdmpBlce.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
        bsns_year: year,
        reprt_code: partCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = cndlCaplScritsNrdmpBlce;
