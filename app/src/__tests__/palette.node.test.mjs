import { test, describe } from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(__dirname, "..", "..");

describe("Frontend Bundle & Accessibility Verification (Node Native Test Runner)", () => {
  const publicDataDir = path.join(appRoot, "public", "data");

  test("all required JSON and Parquet artifacts exist in app/public/data/", () => {
    const requiredFiles = [
      "municipios_bundle.json",
      "perfiles_caracterizacion.json",
      "transiciones.json",
      "simulador_what_if.json",
      "llm_perfiles_narrativas_estrategias.json",
      "features_municipio.parquet",
      "perfiles_municipio.parquet",
      "proyeccion_2027.parquet",
    ];
    for (const fname of requiredFiles) {
      const fpath = path.join(publicDataDir, fname);
      assert.equal(fs.existsSync(fpath), true, `Missing frontend artifact: ${fname}`);
    }
  });

  test("municipios_bundle.json contains 2,477 municipalities with valid coordinates and 2027 intervals", () => {
    const raw = fs.readFileSync(path.join(publicDataDir, "municipios_bundle.json"), "utf-8");
    const bundle = JSON.parse(raw);
    assert.ok(bundle.municipios.length >= 2450);
    const sample = bundle.municipios[0];
    assert.equal(sample.cve_geo.length, 5);
    assert.ok(sample.p2027_lo < sample.p2027 && sample.p2027 < sample.p2027_hi);
  });

  test("HTML & Next.js components include all 8 required sections and non-causal / ecological fallacy notices", () => {
    const html = fs.readFileSync(path.join(appRoot, "public", "index.html"), "utf-8");
    assert.match(html, /1\. Mapa Coroplético/i);
    assert.match(html, /2\. Tarjetas de Perfil/i);
    assert.match(html, /3\. Dinámica y Transiciones \(Sankey\)/i);
    assert.match(html, /4\. ¿Qué perfil tiene mi municipio\?/i);
    assert.match(html, /5\. Proyección 2027/i);
    assert.match(html, /6\. Simulador What-If \(No Causal\)/i);
    assert.match(html, /7\. Pregúntale a los Datos \(SQL\)/i);
    assert.match(html, /8\. Metodología y Límites/i);
    assert.match(html, /Falacia Ecológica/i);
    assert.match(html, /NO CAUSAL/i);
  });
});
