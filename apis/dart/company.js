const { dartkey } = require("../../config");

// 기업개황
async function company(corpCode) {
    const url = "https://opendart.fss.or.kr/api/company.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = company;
