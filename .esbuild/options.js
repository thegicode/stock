const { minifyTemplates, writeFiles } = require("esbuild-minify-templates");

const entryPoints = ["./src/script/pages/index.js"];

module.exports = {
    outbase: "./src/",
    entryPoints,
    outdir: "./static/",
    entryNames: "[dir]/[name]",
    plugins: [minifyTemplates(), writeFiles()],
    target: "es6",
    minify: false,
    bundle: true,
    write: true,
    sourcemap: true,
};
