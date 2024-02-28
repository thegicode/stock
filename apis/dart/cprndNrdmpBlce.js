const { dartkey } = require("../../config");

// 회사채 미상환 잔액
async function cprndNrdmpBlce(corpCode, yearCode, reprtCode) {
    const url = "https://opendart.fss.or.kr/api/cprndNrdmpBlce.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
        bsns_year: yearCode,
        reprt_code: reprtCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = cprndNrdmpBlce;
