// AREX — Ev ağındaki Mac'te çalışan Ollama'ya (http://192.168.x.x:11434) bağlanabilmek için ağ güvenliği yapılandırması.
// Şifresiz (http) trafik YALNIZ yerel ağ adreslerine izinli; internetteki her şey https zorunlu kalır.
const { withAndroidManifest, withDangerousMod } = require("@expo/config-plugins");
const fs = require("fs");
const path = require("path");

function xml() {
  const alanlar = ["localhost", "127.0.0.1"];
  for (const ag of ["192.168.0", "192.168.1", "192.168.2", "10.0.0"]) for (let i = 1; i < 255; i++) alanlar.push(`${ag}.${i}`);
  return `<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
  <base-config cleartextTrafficPermitted="false" />
  <domain-config cleartextTrafficPermitted="true">
${alanlar.map((a) => `    <domain includeSubdomains="false">${a}</domain>`).join("\n")}
  </domain-config>
</network-security-config>
`;
}

module.exports = function evAgi(config) {
  config = withAndroidManifest(config, (c) => {
    c.modResults.manifest.application[0].$["android:networkSecurityConfig"] = "@xml/arex_ag";
    return c;
  });
  return withDangerousMod(config, ["android", async (c) => {
    const klasor = path.join(c.modRequest.platformProjectRoot, "app", "src", "main", "res", "xml");
    fs.mkdirSync(klasor, { recursive: true });
    fs.writeFileSync(path.join(klasor, "arex_ag.xml"), xml());
    return c;
  }]);
};
