const JSZip = require("jszip");
const xml2js = require("xml2js");
const fs = require("fs");
const path = require("path");

const { dartkey } = require("../config");

await function saveCorpCode() {
    const url = "https://opendart.fss.or.kr/api/corpCode.xml";
    const params = new URLSearchParams({ crtfc_key: dartkey });

    // Make an HTTP GET request
    fetch(`${url}?${params}`, { method: "GET" })
        .then((res) => res.arrayBuffer())
        .then(async (buffer) => {
            const zip = new JSZip();
            // Load ZIP file from the response buffer
            await zip.loadAsync(buffer);
            // Assuming the XML file has a known name, 'CORPCODE.xml'
            const xmlContent = await zip.file("CORPCODE.xml").async("string");

            // Save the XML content to a file
            const outputPath = path.join(__dirname, "../data/CORPCODE.xml");
            fs.writeFileSync(outputPath, xmlContent, "utf8");

            console.log(`File saved to ${outputPath}`);

            // Optionally, parse the XML content
            xml2js.parseString(xmlContent, (err, result) => {
                if (err) {
                    throw err;
                }
                // Process the XML content as needed
                // Example: Logging the first entry
                const lists = result.result.list;
                console.log(lists[0].corp_code[0]);
                console.log(lists[0].corp_name[0]);
                console.log(lists[0].stock_code[0]);
                console.log(lists[0].modify_date[0]);
            });
        })
        .catch((error) => {
            console.error(error);
        });
};

module.exports = saveCorpCode;
