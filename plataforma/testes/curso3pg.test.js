"use strict";

const assert = require("node:assert/strict");
const { test } = require("node:test");
const data = require("../dados_min.json");
const { run } = require("../modelo3pg.js");
const { MODULES, checkStage, validateInitial } = require("../curso3pg.js");

const site = data.sitios.IND;
const material = data.materiais.A1;
const aswMax = site.asw_local;
const initial = { WF0: material.WF0, WR0: material.WR0, WS0: material.WS0, stems_n: 10000 / 9, asw_i: aswMax };
const engineSite = { lat: site.lat, asw_max: aswMax, asw_i: initial.asw_i, from: material.inicio, to: "2023-01" };
const species = { planted: "2015-01", fertility: material.FR_ref, stems_n: initial.stems_n, WS0: initial.WS0, WR0: initial.WR0, WF0: initial.WF0 };
const climateStartIndex = site.clima.year.findIndex((year, index) =>
  year === Number(material.inicio.slice(0, 4)) && site.clima.month[index] === Number(material.inicio.slice(5, 7)));
const execute = stage => run(engineSite, species, site.clima, material.params, {}, {}, stage);
const scenarioHash = "a".repeat(64);

test("missing stage preserves the explicit D6 output", () => {
  assert.deepEqual(run(engineSite, species, site.clima, material.params, {}, {}), execute("D6"));
});

test("each learning stage passes its registered invariants", () => {
  for (const { id } of MODULES) {
    const output = execute(id);
    const repeatOutput = id === "D6" ? execute("D6") : null;
    const checks = checkStage(id, output, {
      initial, aswMax, climate: site.clima, climateStartIndex, y: material.params.y,
      repeatOutput, scenarioHash
    });
    assert.equal(checks.pass, true, `${id}: ${checks.checks.filter(check => !check.pass).map(check => check.name).join(", ")}`);
  }
});

test("canopy checks align climate months to the selected material start", () => {
  const secondMaterial = data.materiais.C5;
  const start = secondMaterial.inicio.split("-").map(Number);
  const startIndex = site.clima.year.findIndex((year, index) => year === start[0] && site.clima.month[index] === start[1]);
  const output = run(
    { lat: site.lat, asw_max: aswMax, asw_i: aswMax, from: secondMaterial.inicio, to: "2023-01" },
    { planted: "2015-01", fertility: secondMaterial.FR_ref, stems_n: 10000 / 9,
      WS0: secondMaterial.WS0, WR0: secondMaterial.WR0, WF0: secondMaterial.WF0 },
    site.clima, secondMaterial.params, {}, {}, "D1"
  );
  const checks = checkStage("D1", output, { climate: site.clima, climateStartIndex: startIndex });
  assert.equal(startIndex, 3);
  assert.equal(checks.pass, true, checks.checks.filter(check => !check.pass).map(check => check.name).join(", "));
});

test("damage extensions are rejected before D6", () => {
  assert.throws(() => run(engineSite, species, site.clima, material.params, { "2017-01": 0.5 }, {}, "D5"), /só podem ser executadas/);
  assert.notDeepEqual(
    run(engineSite, species, site.clima, material.params, { "2017-01": 0.5 }, {}, "D6"),
    execute("D6")
  );
});

test("initial water state must fit the selected scenario capacity", () => {
  assert.deepEqual(validateInitial({ ...initial, asw_i: aswMax + 0.1 }, aswMax), [
    "ASW inicial deve estar entre 0 e ASWmax."
  ]);
});
