const {
    company,
    cndlCaplScritsNrdmpBlce,
    cprndNrdmpBlce,
    fnlttSinglIndx,
    fnlttSinglAcntAll,
    fnlttXbrl,
    list,
    saveCorpCode,
} = require("./index");

// NAVER
const corpCode = "00266961";
const reprtCode = {
    part1: "11013", // 1분기보고서
    part2: "11012", // 반기보고서
    part3: "11014", // 3분기보고서
    part4: "11011", // 사업보고서
};
const fsDivCode = {
    part1: "OFS",
    part2: "CFS",
};

const idxClCode = {
    part1: "M210000", // 수익성지표
    part2: "M220000", //안정성지표
    part3: "M230000", // 성장성지표
    part4: "M240000", //활동성지표
};

const pblntfTy = {
    a: "A", // 정기공시
    b: "B", // 주요사항보고
    c: "C", // 발행공시
    d: "D", // 지분공시
    e: "E", // 기타공시
    f: "F", // 외부감사관련
    g: "G", // 펀드공시
    h: "H", // 자산유동화
    i: "I", // 거래소공시
    j: "J", // 공정위공시
};

// 고유번호
saveCorpCode();

// 기업개황
async function getCompany() {
    console.log("기업개황 : company", await company(corpCode));
}
// getCompany();

// 조건부 자본증권 미상환 잔액
async function getCndlCaplScritsNrdmpBlce() {
    console.log(
        "조건부 자본증권 미상환 잔액 : cndlCaplScritsNrdmpBlce",
        await cndlCaplScritsNrdmpBlce(corpCode, "2023", reprtCode.part3)
    );
}
// getCndlCaplScritsNrdmpBlce();

// 회사채 미상환 잔액
async function getCprndNrdmpBlce() {
    console.log(
        " 회사채 미상환 잔액 : cprndNrdmpBlce",
        await cprndNrdmpBlce(corpCode, "2023", reprtCode.part3)
    );
}
// getCprndNrdmpBlce();

// 단일회사 전체 재무제표
async function getFnlttSinglAcntAll() {
    console.log(
        "단일회사 전체 재무제표 : fnlttSinglAcntAll",
        await fnlttSinglAcntAll(
            corpCode,
            "2023",
            reprtCode.part2,
            fsDivCode.part1
        )
    );
}
// getFnlttSinglAcntAll();

// 단일회사 주요 재무지표
async function getCprndNrdmpBlce() {
    console.log(
        " 회사채 미상환 잔액 : cprndNrdmpBlce",
        await fnlttSinglIndx(corpCode, "2023", reprtCode.part3, idxClCode.part1)
    );
}
// getCprndNrdmpBlce();

// 공시검색
async function getList() {
    const params = {
        corpCode,
        startDate: "20220101",
        endDate: "20220130",
        lastReprtAt: "Y",
        pblntfTy: pblntfTy.a,
        // pblntf_detail_ty,
        sort: "date", // default, 회사명 : crp, 보고서명 : rpt,
        sort_mth: "asc", // 오름차순, 내림차순 : desc
        page_no: "1", // 기본값
        page_count: "10", // 페이지당 건수(1~100) 기본값 : 10, 최대값 : 100
    };
    console.log("공시검색 : list", await list(params));
}
// getList();

// 재무제표 원본파일(XBRL) -- TODO
async function getFnlttXbrl() {
    console.log(
        " 재무제표 원본파일 : fnlttXbrl",
        await fnlttXbrl(corpCode, "2023", "20220127800045", reprtCode.part1)
    );
}
// getFnlttXbrl();
