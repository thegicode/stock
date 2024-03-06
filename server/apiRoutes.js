const { cndlCaplScritsNrdmpBlce, fnlttSinglAcntAll } = require("../apis");

async function handleCndlCaplScritsNrdmpBlce(req, res) {
    const data = await cndlCaplScritsNrdmpBlce("00266961", "2023", "11014");
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(data));
}

// 다른 API 처리 함수들을 여기에 추가...

module.exports = {
    "/cndlCaplScritsNrdmpBlce": handleCndlCaplScritsNrdmpBlce,
};
