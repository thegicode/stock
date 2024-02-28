const esbuild = require("esbuild");
const options = require("./options.js");
const http = require("node:http");
const portNumber = 3000;

async function server() {
    let esContext = await esbuild.context(options);

    const { host, port } = await esContext.serve({
        servedir: "./app/static",
        host: "localhost",
        port: portNumber,
        // fallback: 'www/404.html',
        onRequest: async (args) => {
            console.log("esContext:onRequest", JSON.stringify(args));
        },
    });

    http.createServer((req, res) => {
        const options = {
            hostname: host,
            port: port,
            path: req.url,
            method: req.method,
            headers: req.headers,
        };

        console.log("http:options", JSON.stringify(options));

        const proxyReq = http.request(options, (proxyRes) => {
            if (proxyRes.statusCode === 404) {
                res.writeHead(404, { "Content-Type": "text/html" });
                res.end("<h1>A custom 404 page</h1>");
                return;
            }

            res.writeHead(proxyRes.statusCode, proxyRes.headers);
            proxyRes.pipe(res, { end: true });
        });

        req.pipe(proxyReq, { end: true });
    }).listen(portNumber);
}

server();
