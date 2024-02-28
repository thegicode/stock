// 단일회사 전체 재무제표 개발가이드

const https = require("https");
const fs = require("fs");
const path = require("path");
const unzipper = require("unzipper");

// const { createWriteStream, createReadStream } = require("fs");
// const { pipeline } = require("stream");
// const { promisify } = require("util");

const { dartkey } = require("../../config");
const DOWNLOAD_PATH = path.join(__dirname, "./corpCode.zip");

function downloadAndExtractZip() {
    const url = "https://opendart.fss.or.kr/api/corpCode.xml";
    const params = new URLSearchParams({ crtfc_key: dartkey });

    https
        .get(`${url}?${params}`, (response) => {
            if (response.statusCode === 302 && response.headers.location) {
                console.log("Redirecting to:", response.headers.location);
                https.get(response.headers.location, (redirectResponse) => {
                    processResponse(redirectResponse);
                });
            } else {
                processResponse(response);
            }
        })
        .on("error", (error) => {
            console.error("Error downloading the file:", error);
        });
}

function processResponse(response) {
    if (response.statusCode !== 200) {
        console.error(
            `Failed to download file: Status Code ${response.statusCode}`
        );
        return;
    }

    const fileStream = fs.createWriteStream(DOWNLOAD_PATH);
    response.pipe(fileStream);

    fileStream.on("finish", () => {
        fileStream.close();
        console.log("File downloaded!");

        // Extract the ZIP file
        fs.createReadStream(DOWNLOAD_PATH)
            .pipe(unzipper.Extract({ path: __dirname }))
            .on("close", () => console.log("Extraction complete."));
    });
}

downloadAndExtractZip();

async function fnlttSinglAcntAll() {
    const requestURL = `https://opendart.fss.or.kr/api/fnlttSinglAcntAll.json?crtfc_key=${dartkey}&corp_code=00126380&bsns_year=2018&reprt_code=11011&fs_div=OFS`;
    const response = await fetch(requestURL);
    const data = await response.json();
}
// fnlttSinglAcntAll();

/* const downloadCorpCodeZip = () => {
    const fileStream = fs.createWriteStream(DOWNLOAD_PATH);
    https
        .get(requestURL, (response) => {
            // 응답 스트림을 파일 스트림에 파이프 연결
            response.pipe(fileStream);

            fileStream.on("finish", () => {
                fileStream.close();
                console.log("Download Completed: corpCode.zip");
            });
        })
        .on("error", (err) => {
            fs.unlinkSync(DOWNLOAD_PATH); // 다운로드 실패 시 파일 삭제
            console.error("Error downloading the file:", err.message);
        });
};

downloadCorpCodeZip();
 */
