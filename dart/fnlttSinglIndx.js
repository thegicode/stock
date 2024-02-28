const { dartkey } = require("../config");

// 단일회사 주요 재무지표
async function fnlttSinglIndx(corpCode, yearCode, reprtCode, idxClCode) {
    const url = "https://opendart.fss.or.kr/api/fnlttSinglIndx.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: corpCode,
        bsns_year: yearCode,
        reprt_code: reprtCode,
        idx_cl_code: idxClCode,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = fnlttSinglIndx;
