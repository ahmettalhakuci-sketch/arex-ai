// AREX — sherpa-onnx (güçlü ses imzası) yerel Maven deposunu tüm Android projesine tanıtır
const { withProjectBuildGradle } = require("@expo/config-plugins");
const path = require("path");
module.exports = function sherpaDepo(config) {
  return withProjectBuildGradle(config, (c) => {
    const yol = path.join(__dirname, "..", "modules", "arex-erisim", "android", "maven").replace(/\\/g, "/");
    const satir = `    maven { url "${yol}" } // sherpa-onnx (AREX ses imzası)`;
    if (!c.modResults.contents.includes(yol))
      c.modResults.contents = c.modResults.contents.replace(/(maven \{ url 'https:\/\/www\.jitpack\.io' \})/, `$1\n${satir}`);
    return c;
  });
};
