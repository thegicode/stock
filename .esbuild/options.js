const { minifyTemplates, writeFiles } = require("esbuild-minify-templates");

const entryPoints = [
    "./app/src/scripts/pages/aPage/index.ts",
    "./app/src/scripts/pages/bPage/index.ts",
];

module.exports = {
    entryPoints,
    outbase: "./app/src/scripts/pages/",
    outdir: "./app/static/js/",
    entryNames: "[dir]/[name]",
    plugins: [minifyTemplates(), writeFiles()],
    target: "es6",
    minify: false,
    bundle: true,
    write: true,
    sourcemap: true,
};
