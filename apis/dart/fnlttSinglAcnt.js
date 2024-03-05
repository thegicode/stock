const { dartkey } = require("../../config");

// 단일회사 주요계정
async function fnlttSinglAcnt(corpCode, yearCode, reprtCode) {
    const url = "https://opendart.fss.or.kr/api/fnlttSinglAcnt.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
        bsns_year: yearCode,
        reprt_code: reprtCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = fnlttSinglAcnt;

// 유동자산, 유동부채
