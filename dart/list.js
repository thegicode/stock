const { dartkey } = require("../config");

// 공시검색
async function list(args) {
    const url = "https://opendart.fss.or.kr/api/list.json";
    const params = new URLSearchParams({
        crtfc_key: dartkey,
        corp_code: args.corpCode,
        bgn_de: args.startDate,
        end_de: args.endDate,
        last_reprt_at: args.lastReprtAt,
        // pblntf_ty: args.pblntfTy,
        sort: args.sort,
        sort_mth: args.sort_mth,
        page_no: args.page_no,
        page_count: args.page_count,
    });
    const response = await fetch(`${url}?${params}`, { method: "GET" });
    return await response.json();
}

module.exports = list;
