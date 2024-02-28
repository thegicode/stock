const { dartkey } = require("../config");

// 단일회사 전체 재무제표
async function fnlttSinglAcntAll(corpCode, yearCode, reprtCode, fsDivCode) {
    const url = "https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
        bsns_year: yearCode,
        reprt_code: reprtCode,
        fs_div: fsDivCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = fnlttSinglAcntAll;
