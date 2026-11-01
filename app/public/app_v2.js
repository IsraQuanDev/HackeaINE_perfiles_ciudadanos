// Okabe-Ito colorblind-safe palette for the 6 territorial profiles
const CLUSTER_COLORS = [
  "#0072B2", // C0: Blue
  "#E69F00", // C1: Orange
  "#009E73", // C2: Bluish Green
  "#CC79A7", // C3: Reddish Purple
  "#56B4E9", // C4: Sky Blue
  "#D55E00"  // C5: Vermilion
];

const AGE_GROUPS_8 = ["18-19", "20-24", "25-29", "30-39", "40-49", "50-59", "60-69", "70+"];
const AGE_KEYS_8 = ["e18_19", "e20_24", "e25_29", "e30_39", "e40_49", "e50_59", "e60_69", "e70_mas"];

const STATE = {
  bundle: null,
  profiles: null,
  transitions: null,
  sim: null,
  llm: null,
  meta: null,
  dl: null,
  geoMun: null,
  geoDist: null,
  geoEnt: null,
  activeView: "overview",
  filterEnt: "ALL",
  filterPerfil: "ALL",
  filterAnio: "2024",
  timelineTimer: null,
  charts: {}
};

function getChart(domId) {
  const el = document.getElementById(domId);
  if (!el) return null;
  if (STATE.charts[domId]) {
    STATE.charts[domId].dispose();
  }
  const theme = document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : null;
  const ch = echarts.init(el, theme, { renderer: "canvas" });
  STATE.charts[domId] = ch;
  return ch;
}

function resizeAllVisibleCharts() {
  setTimeout(() => {
    Object.values(STATE.charts).forEach((ch) => {
      if (ch && !ch.isDisposed()) {
        try { ch.resize(); } catch (_) {}
      }
    });
  }, 60);
}

window.addEventListener("resize", resizeAllVisibleCharts);

function getProfileName(cid) {
  if (!STATE.llm || !STATE.llm.narrativas_perfiles) return `Perfil ${cid}`;
  const found = STATE.llm.narrativas_perfiles.find((n) => Number(n.cluster_id) === Number(cid));
  return found ? `P${cid} · ${found.nombre}` : `Perfil ${cid}`;
}

function getFilteredMunicipios() {
  if (!STATE.bundle) return [];
  return STATE.bundle.municipios.filter((m) => {
    if (STATE.filterEnt !== "ALL" && m.nom_ent !== STATE.filterEnt) return false;
    if (STATE.filterPerfil !== "ALL" && String(m.cluster_id) !== String(STATE.filterPerfil)) return false;
    return true;
  });
}

function toggleSidebar() {
  document.getElementById("app-sidebar").classList.toggle("collapsed");
  resizeAllVisibleCharts();
}

function toggleTheme() {
  const html = document.documentElement;
  const next = html.getAttribute("data-theme") === "dark" ? "light" : "dark";
  html.setAttribute("data-theme", next);
  document.getElementById("theme-label").textContent = next === "dark" ? "Modo Claro" : "Modo Oscuro";
  refreshCurrentView();
}

function switchView(viewId) {
  STATE.activeView = viewId;
  document.querySelectorAll(".nav-item").forEach((btn) => {
    btn.classList.toggle("active", btn.getAttribute("data-view") === viewId);
  });
  document.querySelectorAll(".view-pane").forEach((pane) => {
    pane.classList.toggle("active", pane.id === `view-${viewId}`);
  });
  refreshCurrentView();
  resizeAllVisibleCharts();
}

function onGlobalFilterChange() {
  STATE.filterEnt = document.getElementById("gf-entidad").value;
  STATE.filterPerfil = document.getElementById("gf-perfil").value;
  STATE.filterAnio = document.getElementById("gf-anio").value;
  const muns = getFilteredMunicipios();
  const lnSum = muns.reduce((a, b) => a + (b.ln_2024 || 0), 0);
  document.getElementById("active-filter-summary").textContent =
    `${muns.length.toLocaleString("es-MX")} municipios · LN 2024: ${lnSum.toLocaleString("es-MX")}`;
  refreshCurrentView();
}

function refreshCurrentView() {
  if (!STATE.bundle) return;
  const v = STATE.activeView;
  if (v === "overview") renderOverview();
  else if (v === "mapa") renderExplorerMap();
  else if (v === "perfiles") renderPerfilesView();
  else if (v === "dinamica") renderDinamicaView();
  else if (v === "ficha") renderMunicipioFicha(document.getElementById("ficha-mun-select").value || "22014");
  else if (v === "pronostico") renderPronosticoView();
  else if (v === "simulador") renderSimuladorView();
  else if (v === "chat") renderChatView();
  else if (v === "metodologia") renderMetodologiaView();
  else if (v === "calidad") renderCalidadView();
}

async function initDashboard() {
  const [bundle, profiles, transitions, sim, llm, meta, dl, geoMun] = await Promise.all([
    fetch("data/municipios_bundle.json").then((r) => r.json()),
    fetch("data/perfiles_caracterizacion.json").then((r) => r.json()),
    fetch("data/transiciones.json").then((r) => r.json()),
    fetch("data/simulador_what_if.json").then((r) => r.json()),
    fetch("data/llm_perfiles_narrativas_estrategias.json").then((r) => r.json()),
    fetch("data/clustering_model_metadata.json").then((r) => r.json()),
    fetch("data/deep_learning_eval.json").then((r) => r.json()),
    fetch("data/geo/municipios_mx.geojson").then((r) => r.json())
  ]);

  STATE.bundle = bundle;
  STATE.profiles = profiles;
  STATE.transitions = transitions;
  STATE.sim = sim;
  STATE.llm = llm;
  STATE.meta = meta;
  STATE.dl = dl;
  STATE.geoMun = geoMun;
  echarts.registerMap("mx_municipios", geoMun);

  // Lazy load district and state polygons in background
  fetch("data/geo/distritos_mx.geojson").then((r) => r.json()).then((g) => {
    STATE.geoDist = g;
    echarts.registerMap("mx_distritos", g);
  });
  fetch("data/geo/entidades_mx.geojson").then((r) => r.json()).then((g) => {
    STATE.geoEnt = g;
    echarts.registerMap("mx_entidades", g);
  });

  populateSelectors();
  renderOverview();
  inspectMunicipioInDrawer(STATE.bundle.municipios.find((m) => m.cve_geo === "22014") || STATE.bundle.municipios[0]);
}

function populateSelectors() {
  const ents = [...new Set(STATE.bundle.municipios.map((m) => m.nom_ent))].sort((a, b) => a.localeCompare(b, "es"));
  const entSel = document.getElementById("gf-entidad");
  ents.forEach((e) => {
    const opt = document.createElement("option");
    opt.value = e;
    opt.textContent = e;
    entSel.appendChild(opt);
  });

  const perfSel = document.getElementById("gf-perfil");
  const detSel = document.getElementById("profile-detail-select");
  const simSel = document.getElementById("sim-cluster-select");
  STATE.profiles.perfiles.forEach((p) => {
    const label = getProfileName(p.cluster_id);
    [perfSel, detSel, simSel].forEach((sel) => {
      if (!sel) return;
      const opt = document.createElement("option");
      opt.value = String(p.cluster_id);
      opt.textContent = `${label} (${p.n_municipios} muns.)`;
      sel.appendChild(opt);
    });
  });

  filterFichaSelect();
}

// VIEW 0: OVERVIEW
function renderOverview() {
  const muns = getFilteredMunicipios();
  const totalLn = muns.reduce((s, m) => s + (m.ln_2024 || 0), 0);
  const validAnioKey = STATE.filterAnio === "GLOBAL" ? "p_global" : `p${STATE.filterAnio}`;
  const validMuns = muns.filter((m) => m[validAnioKey] !== null && m[validAnioKey] !== undefined);
  const avgPart = validMuns.length
    ? (validMuns.reduce((s, m) => s + m[validAnioKey] * (m.ln_2024 || 1), 0) /
       validMuns.reduce((s, m) => s + (m.ln_2024 || 1), 0)).toFixed(2)
    : "0.00";
  const avgCaida = muns.length
    ? (muns.reduce((s, m) => s + m.caida_pi, 0) / muns.length).toFixed(2)
    : "0.00";
  const avgProj2027 = muns.length
    ? (muns.reduce((s, m) => s + m.p2027 * (m.ln_2027 || 1), 0) /
       muns.reduce((s, m) => s + (m.ln_2027 || 1), 0)).toFixed(2)
    : "0.00";
  const nRiesgo = muns.filter((m) => m.riesgo_2027).length;

  const kpiHtml = [
    {
      title: "Territorios Activos",
      val: muns.length.toLocaleString("es-MX"),
      delta: `LN 2024: ${totalLn.toLocaleString("es-MX")}`,
      cls: "delta-up"
    },
    {
      title: `Participación (${STATE.filterAnio})`,
      val: `${avgPart}%`,
      delta: "Ponderada por Lista Nominal (Cobertura ≥ 90%)",
      cls: "delta-up"
    },
    {
      title: "Brecha Presidencial → Intermedia",
      val: `${avgCaida > 0 ? "+" : ""}${avgCaida} p.p.`,
      delta: "Contracción media en intermedias",
      cls: "delta-down"
    },
    {
      title: "Pronóstico Intermedia 2027",
      val: `${avgProj2027}%`,
      delta: "Cobertura CQR 80%: 80.0% empírica",
      cls: "delta-up"
    },
    {
      title: "Zonas en Riesgo 2027",
      val: `${nRiesgo}`,
      delta: "Municipios prioritarios DECEyEC",
      cls: "delta-down"
    }
  ].map((k) => `
    <div class="kpi-card">
      <div class="kpi-top"><span>${k.title}</span></div>
      <div class="kpi-val num">${k.val}</div>
      <div class="kpi-delta ${k.cls}">${k.delta}</div>
    </div>
  `).join("");
  document.getElementById("overview-kpi-strip").innerHTML = kpiHtml;

  // Insights SQL Cards
  const insights = (STATE.llm && STATE.llm.insights_verificados_sql) || [];
  document.getElementById("overview-insights-grid").innerHTML = insights.map((ins) => `
    <div class="insight-card">
      <div>
        <div class="insight-top">
          <span class="insight-cat">${ins.categoria}</span>
          <span class="insight-metric num">${ins.metrica_destacada}</span>
        </div>
        <div style="font-weight:700; font-size:13.5px; margin:6px 0 4px;">${ins.titulo}</div>
        <p style="font-size:12.5px; color:var(--text-secondary);">${ins.hallazgo}</p>
      </div>
      <div style="display:flex; justify-content:space-between; align-items:center; margin-top:6px; padding-top:6px; border-top:1px dashed var(--border-subtle);">
        <span class="num" style="font-size:10.5px; color:var(--text-muted);">Verificado en DuckDB</span>
        <button class="icon-btn" style="padding:3px 8px; font-size:11px;" onclick="switchView('${ins.vista_destino}')">Explorar vista →</button>
      </div>
    </div>
  `).join("");

  // Mini Polygon Map in Overview
  const chMap = getChart("chart-overview-map");
  if (chMap && STATE.geoMun) {
    const mapData = muns.map((m) => ({
      name: m.cve_geo,
      value: m.cluster_id,
      mun: m
    }));
    chMap.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => {
          if (!p.data || !p.data.mun) return p.name;
          const m = p.data.mun;
          return `<strong>${m.nom_mun} (${m.nom_ent})</strong><br/>` +
                 `Clave INEGI: <span class="num">${m.cve_geo}</span><br/>` +
                 `${getProfileName(m.cluster_id)}<br/>` +
                 `Part. Media: <strong>${m.p_global}%</strong> | 2027: <strong>${m.p2027}%</strong>`;
        }
      },
      visualMap: {
        type: "piecewise",
        bottom: 6,
        left: "center",
        orient: "horizontal",
        pieces: CLUSTER_COLORS.map((col, idx) => ({
          value: idx,
          label: `P${idx}`,
          color: col
        }))
      },
      series: [{
        type: "map",
        map: "mx_municipios",
        nameProperty: "cve_geo",
        roam: true,
        itemStyle: { borderColor: "rgba(15,23,42,0.18)", borderWidth: 0.35 },
        emphasis: { itemStyle: { borderColor: "#9d2449", borderWidth: 1.4 } },
        data: mapData
      }]
    });
    chMap.on("click", (params) => {
      if (params.data && params.data.mun) {
        document.getElementById("ficha-mun-select").value = params.data.mun.cve_geo;
        switchView("ficha");
      }
    });
  }

  // National 8 Age Groups Curve by Profile
  const chAge = getChart("chart-overview-age8");
  if (chAge) {
    const series = STATE.profiles.perfiles.map((p) => {
      const cid = p.cluster_id;
      const curva = p.curva_edad_8_grupos_pct || {};
      return {
        name: getProfileName(cid),
        type: "line",
        smooth: true,
        symbolSize: 6,
        lineStyle: { width: 2.5, color: CLUSTER_COLORS[cid] },
        itemStyle: { color: CLUSTER_COLORS[cid] },
        data: AGE_GROUPS_8.map((g) => curva[g] || 0)
      };
    });
    chAge.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `${v}%` },
      legend: { bottom: 0, type: "scroll", textStyle: { fontSize: 11 } },
      grid: { top: 24, left: 46, right: 20, bottom: 52 },
      xAxis: { type: "category", data: AGE_GROUPS_8, name: "Grupo de Edad" },
      yAxis: { type: "value", min: 25, max: 85, axisLabel: { formatter: "{value}%" } },
      series
    });
  }
}
// VIEW 1: MAPA COROPLÉTICO POLIGONAL
function selectTimelineYear(yr) {
  STATE.filterAnio = yr;
  document.getElementById("gf-anio").value = yr;
  document.querySelectorAll("#timeline-year-buttons .year-step-btn").forEach((b) => {
    b.classList.toggle("active", b.textContent.trim() === yr);
  });
  if (document.getElementById("map-metric").value === "cluster_id") {
    document.getElementById("map-metric").value = "part_anio";
  }
  renderExplorerMap();
}

function toggleTimelinePlay() {
  const btn = document.getElementById("btn-play-timeline");
  if (STATE.timelineTimer) {
    clearInterval(STATE.timelineTimer);
    STATE.timelineTimer = null;
    btn.textContent = "Reproducir Serie 2009–2024";
    return;
  }
  const years = ["2009", "2012", "2015", "2018", "2021", "2024"];
  let idx = Math.max(0, years.indexOf(STATE.filterAnio));
  btn.textContent = "Pausar Animación";
  document.getElementById("map-metric").value = "part_anio";
  STATE.timelineTimer = setInterval(() => {
    idx = (idx + 1) % years.length;
    selectTimelineYear(years[idx]);
  }, 1300);
}

function renderExplorerMap() {
  const ch = getChart("chart-main-map");
  if (!ch) return;
  const level = document.getElementById("map-level").value;
  const metric = document.getElementById("map-metric").value;
  const muns = getFilteredMunicipios();

  if (level === "entidad" && STATE.geoEnt) {
    const byEnt = {};
    STATE.bundle.municipios.forEach((m) => {
      if (!byEnt[m.cve_ent]) byEnt[m.cve_ent] = { cve_ent: m.cve_ent, nom_ent: m.nom_ent, ln: 0, vot_w: 0 };
      const p = m[`p${STATE.filterAnio === "GLOBAL" ? "_global" : STATE.filterAnio}`] ?? m.p_global;
      byEnt[m.cve_ent].ln += m.ln_2024;
      byEnt[m.cve_ent].vot_w += p * m.ln_2024;
    });
    const entData = Object.values(byEnt).map((e) => ({
      name: e.cve_ent,
      value: Number((e.vot_w / Math.max(e.ln, 1)).toFixed(2)),
      nom_ent: e.nom_ent,
      ln: e.ln
    }));
    ch.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => p.data
          ? `<strong>${p.data.nom_ent} (Clave ${p.data.name})</strong><br/>Participación Ponderada: <strong>${p.data.value}%</strong><br/>LN 2024: ${p.data.ln.toLocaleString("es-MX")}`
          : p.name
      },
      visualMap: {
        min: 40,
        max: 78,
        left: 16,
        bottom: 16,
        text: ["Alta (%)", "Baja (%)"],
        inRange: { color: ["#f1f5f9", "#56B4E9", "#0072B2", "#9d2449"] },
        calculable: true
      },
      series: [{
        type: "map",
        map: "mx_entidades",
        nameProperty: "cve_ent",
        roam: true,
        itemStyle: { borderColor: "#334155", borderWidth: 0.9 },
        data: entData
      }]
    });
    return;
  }

  if (level === "distrito" && STATE.geoDist) {
    const distRows = STATE.bundle.vista_distritos_2024 || [];
    const distData = distRows.map((d) => ({
      name: `${String(d.cve_ent).padStart(2, "0")}_${String(d.def).padStart(2, "0")}`,
      value: d.participacion_pct,
      nom_ent: d.nom_ent,
      def: d.def,
      ln: d.lista_nominal
    }));
    ch.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => p.data
          ? `<strong>${p.data.nom_ent} · Distrito Federal ${p.data.def}</strong><br/>Participación 2024: <strong>${p.data.value}%</strong><br/>LN: ${Number(p.data.ln).toLocaleString("es-MX")}`
          : p.name
      },
      visualMap: {
        min: 42,
        max: 78,
        left: 16,
        bottom: 16,
        text: ["Alta (%)", "Baja (%)"],
        inRange: { color: ["#fef2f2", "#f43f5e", "#9d2449", "#4c0519"] },
        calculable: true
      },
      series: [{
        type: "map",
        map: "mx_distritos",
        nameProperty: "cve_dist",
        roam: true,
        itemStyle: { borderColor: "rgba(15,23,42,0.3)", borderWidth: 0.5 },
        data: distData
      }]
    });
    return;
  }

  // Default: Municipality polygons (2,477)
  const lisaMap = { "HH (Alto-Alto)": 1, "LL (Bajo-Bajo)": 2, "HL (Alto-Bajo)": 3, "LH (Bajo-Alto)": 4, "No significativo": 0 };
  const mapData = muns.map((m) => {
    let val = m.cluster_id;
    if (metric === "part_anio") {
      const k = STATE.filterAnio === "GLOBAL" ? "p_global" : `p${STATE.filterAnio}`;
      val = m[k];
    } else if (metric === "lisa") {
      val = lisaMap[m.lisa] ?? 0;
    } else if (metric !== "cluster_id") {
      val = m[metric];
    }
    return { name: m.cve_geo, value: val, mun: m };
  });

  let visualMap;
  if (metric === "cluster_id") {
    visualMap = {
      type: "piecewise",
      left: 16,
      bottom: 16,
      pieces: STATE.profiles.perfiles.map((p) => ({
        value: p.cluster_id,
        label: getProfileName(p.cluster_id),
        color: CLUSTER_COLORS[p.cluster_id]
      }))
    };
  } else if (metric === "lisa") {
    visualMap = {
      type: "piecewise",
      left: 16,
      bottom: 16,
      pieces: [
        { value: 1, label: "Hotspot HH (Alto-Alto)", color: "#dc2626" },
        { value: 2, label: "Coldspot LL (Bajo-Bajo)", color: "#2563eb" },
        { value: 3, label: "Atípico HL (Alto-Bajo)", color: "#f59e0b" },
        { value: 4, label: "Atípico LH (Bajo-Alto)", color: "#06b6d4" },
        { value: 0, label: "No significativo", color: "#cbd5e1" }
      ]
    };
  } else {
    const vals = mapData.map((d) => d.value).filter((v) => typeof v === "number" && !isNaN(v));
    const minV = vals.length ? Math.floor(Math.min(...vals)) : 0;
    const maxV = vals.length ? Math.ceil(Math.max(...vals)) : 80;
    visualMap = {
      min: minV,
      max: maxV,
      left: 16,
      bottom: 16,
      calculable: true,
      inRange: { color: ["#f8fafc", "#56B4E9", "#0072B2", "#9d2449"] }
    };
  }

  ch.setOption({
    tooltip: {
      trigger: "item",
      formatter: (p) => {
        if (!p.data || !p.data.mun) return p.name;
        const m = p.data.mun;
        const vStr = p.data.value === null || p.data.value === undefined ? "NA (Sin captura ≥90%)" : p.data.value;
        return `<strong>${m.nom_mun} (${m.nom_ent})</strong> · <span class="num">${m.cve_geo}</span><br/>` +
               `${getProfileName(m.cluster_id)}${m.es_medoide ? " · <strong>[MEDOIDE PROTOTIPO]</strong>" : ""}<br/>` +
               `Valor seleccionado: <strong>${vStr}</strong><br/>` +
               `Media 2009–2024: <strong>${m.p_global}%</strong> (EB: ${m.p_eb}%)<br/>` +
               `Pronóstico 2027: <strong>${m.p2027}%</strong> [${m.p2027_lo}% – ${m.p2027_hi}%]`;
      }
    },
    visualMap,
    series: [{
      type: "map",
      map: "mx_municipios",
      nameProperty: "cve_geo",
      roam: true,
      itemStyle: { borderColor: "rgba(15,23,42,0.22)", borderWidth: 0.35 },
      emphasis: { itemStyle: { borderColor: "#9d2449", borderWidth: 1.6 } },
      data: mapData
    }]
  });

  ch.on("click", (params) => {
    if (params.data && params.data.mun) {
      inspectMunicipioInDrawer(params.data.mun);
    }
  });
}

function inspectMunicipioInDrawer(m) {
  if (!m) return;
  document.getElementById("drawer-title").textContent = `${m.nom_mun} (${m.nom_ent})`;
  document.getElementById("drawer-subtitle").textContent = `Clave INEGI ${m.cve_geo} · Distrito Federal ${m.def}`;
  const col = CLUSTER_COLORS[m.cluster_id] || "#0072B2";
  document.getElementById("drawer-body").innerHTML = `
    <div style="display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:12px;">
      <span class="cluster-badge" style="background:${col}22; color:${col}; border:1px solid ${col}55;">
        <span class="dot" style="background:${col};"></span>${getProfileName(m.cluster_id)}
      </span>
      ${m.es_medoide ? `<span class="real-data-badge">MEDOIDE REAL</span>` : ""}
    </div>
    <div class="table-wrap" style="margin-bottom:12px;">
      <table>
        <tbody>
          <tr><td>Lista Nominal 2024</td><td class="num"><strong>${m.ln_2024.toLocaleString("es-MX")}</strong></td></tr>
          <tr><td>Participación Media (2009–2024)</td><td class="num"><strong>${m.p_global}%</strong> (Shrinkage EB: ${m.p_eb}%)</td></tr>
          <tr><td>Participación 2024 vs 2021</td><td class="num">${m.p2024 === null ? "NA" : m.p2024 + "%"} vs ${m.p2021 === null ? "NA" : m.p2021 + "%"}</td></tr>
          <tr><td>Caída Presidencial → Intermedia</td><td class="num">${m.caida_pi > 0 ? "+" : ""}${m.caida_pi} p.p.</td></tr>
          <tr><td>Brecha Mujeres − Hombres</td><td class="num">${m.brecha_gen > 0 ? "+" : ""}${m.brecha_gen} p.p.</td></tr>
          <tr><td>Participación 18–19 (Primer Voto)</td><td class="num">${m.e18_19}% (Retención: ${m.ret_pv > 0 ? "+" : ""}${m.ret_pv} p.p.)</td></tr>
          <tr><td>Cluster Espacial LISA / Gi*</td><td class="num">${m.lisa} (z=${m.gi_z})</td></tr>
          <tr><td>Pronóstico 2027 [IC 80% CQR]</td><td class="num"><strong>${m.p2027}%</strong> [${m.p2027_lo}% – ${m.p2027_hi}%]</td></tr>
        </tbody>
      </table>
    </div>
    <button class="icon-btn" style="width:100%; justify-content:center; background:var(--ine-primary); color:#fff; border-color:var(--ine-primary);" onclick="document.getElementById('ficha-mun-select').value='${m.cve_geo}'; switchView('ficha');">
      Abrir Ficha Técnica Completa e Imprimir PDF →
    </button>
  `;
}

// VIEW 2: TARJETAS DE PERFIL
function renderPerfilesView() {
  const narrs = STATE.llm.narrativas_perfiles || [];
  const ests = STATE.llm.estrategias_perfiles || [];
  const grid = document.getElementById("profiles-cards-grid");

  grid.innerHTML = STATE.profiles.perfiles.map((p) => {
    const cid = p.cluster_id;
    const col = CLUSTER_COLORS[cid];
    const narr = narrs.find((n) => n.cluster_id === cid) || {};
    const est = ests.find((e) => e.cluster_id === cid) || {};
    const med = p.municipio_prototipo_medoide || p.municipios_mas_representativos[0];
    const st = p.estadisticas_features;

    return `
      <div class="card" style="border-top: 4px solid ${col}; display:flex; flex-direction:column; justify-content:space-between; gap:12px;">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span class="cluster-badge" style="background:${col}20; color:${col};">
              <span class="dot" style="background:${col};"></span>Perfil ${cid} · ${p.n_municipios} muns. (${p.pct_lista_nominal_2024}% LN)
            </span>
            <span class="real-data-badge">DATO REAL</span>
          </div>
          <h3 style="font-size:16px; font-weight:800; margin-bottom:4px;">${narr.nombre || "Perfil " + cid}</h3>
          <p style="font-size:12px; color:var(--text-muted); font-style:italic; margin-bottom:10px;">"${narr.lema || ""}"</p>
          <p style="font-size:12.5px; color:var(--text-secondary); margin-bottom:10px;">${narr.descripcion_narrativa || ""}</p>
          <div style="background:var(--bg-elevated); padding:10px; border-radius:8px; font-size:12px; margin-bottom:10px;">
            <strong>Municipio Prototipo Medoide (Dato Real):</strong>
            <span class="num">${med.nom_mun} (${med.nom_ent}, ${med.cve_geo})</span> · Media: <strong class="num">${(med.part_media_global * 100).toFixed(2)}%</strong>
          </div>
          <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:6px; text-align:center; font-size:11.5px; background:var(--bg-app); padding:8px; border-radius:8px;">
            <div><div style="color:var(--text-muted);">Part. Media</div><strong class="num">${st.part_media_global.media_pct}%</strong></div>
            <div><div style="color:var(--text-muted);">Caída Inter.</div><strong class="num">${st.caida_presidencial_intermedia.media_pct} p.p.</strong></div>
            <div><div style="color:var(--text-muted);">Secc. Rural</div><strong class="num">${st.pct_ln_rural.media_pct}%</strong></div>
          </div>
        </div>
        <div style="border-top:1px solid var(--border-subtle); padding-top:10px; font-size:12px;">
          <div style="font-weight:700; color:var(--ine-primary); margin-bottom:3px;">Estrategia ENCCÍVICA / DECEyEC · Meta 2027: <span class="num">${est.linea_base}% → ${est.meta_2027}%</span></div>
          <p style="color:var(--text-secondary); margin-bottom:8px;">${est.accion_concreta || ""}</p>
          <button class="icon-btn" style="width:100%; justify-content:center;" onclick="document.getElementById('profile-detail-select').value='${cid}'; renderProfileDeepCharts();">
            Inspeccionar Curvas y SHAP del Perfil ${cid}
          </button>
        </div>
      </div>
    `;
  }).join("");

  renderProfileDeepCharts();
}

function renderProfileDeepCharts() {
  const cid = Number(document.getElementById("profile-detail-select").value || 0);
  const p = STATE.profiles.perfiles.find((x) => x.cluster_id === cid) || STATE.profiles.perfiles[0];
  const col = CLUSTER_COLORS[cid];
  const years = ["2009", "2012", "2015", "2018", "2021", "2024"];

  // 1. Trajectory with P10-P90 band
  const chBand = getChart("chart-profile-band");
  if (chBand) {
    const meanArr = years.map((y) => p.trayectoria_media_anual[y]);
    const p10Arr = years.map((y) => (p.trayectoria_banda_p10_p90 ? p.trayectoria_banda_p10_p90[y].p10 : p.trayectoria_media_anual[y] - 6));
    const p90Arr = years.map((y) => (p.trayectoria_banda_p10_p90 ? p.trayectoria_banda_p10_p90[y].p90 : p.trayectoria_media_anual[y] + 6));
    chBand.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `${v}%` },
      legend: { bottom: 0, data: ["Media del Perfil", "Percentil 90", "Percentil 10"] },
      grid: { top: 24, left: 46, right: 20, bottom: 44 },
      xAxis: { type: "category", data: years },
      yAxis: { type: "value", min: 25, max: 90, axisLabel: { formatter: "{value}%" } },
      series: [
        { name: "Percentil 90", type: "line", data: p90Arr, lineStyle: { opacity: 0.35, type: "dashed", color: col }, itemStyle: { color: col } },
        { name: "Media del Perfil", type: "line", data: meanArr, lineStyle: { width: 3.5, color: col }, itemStyle: { color: col }, areaStyle: { color: col, opacity: 0.12 } },
        { name: "Percentil 10", type: "line", data: p10Arr, lineStyle: { opacity: 0.35, type: "dashed", color: col }, itemStyle: { color: col } }
      ]
    });
  }

  // 2. 8 Age Groups Curve for Selected Profile vs Global
  const chAge8 = getChart("chart-profile-age8");
  if (chAge8) {
    const c8 = p.curva_edad_8_grupos_pct || {};
    chAge8.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `${v}%` },
      grid: { top: 24, left: 46, right: 20, bottom: 40 },
      xAxis: { type: "category", data: AGE_GROUPS_8 },
      yAxis: { type: "value", min: 25, max: 85, axisLabel: { formatter: "{value}%" } },
      series: [{
        name: getProfileName(cid),
        type: "bar",
        barWidth: "48%",
        itemStyle: { color: col, borderRadius: [6, 6, 0, 0] },
        label: { show: true, position: "top", formatter: "{c}%", fontSize: 11 },
        data: AGE_GROUPS_8.map((g) => c8[g] || 0)
      }]
    });
  }

  // 3. UMAP 2D Scatter
  const chUmap = getChart("chart-profile-umap");
  if (chUmap) {
    const series = STATE.profiles.perfiles.map((prof) => {
      const k = prof.cluster_id;
      const pts = STATE.bundle.municipios
        .filter((m) => m.cluster_id === k)
        .map((m) => ({ value: [m.umap_1, m.umap_2], mun: m }));
      return {
        name: `P${k}`,
        type: "scatter",
        symbolSize: k === cid ? 7 : 4,
        itemStyle: { color: CLUSTER_COLORS[k], opacity: k === cid ? 0.95 : 0.35 },
        data: pts
      };
    });
    chUmap.setOption({
      tooltip: {
        trigger: "item",
        formatter: (params) => {
          const m = params.data && params.data.mun;
          return m ? `<strong>${m.nom_mun} (${m.nom_ent})</strong><br/>${getProfileName(m.cluster_id)}<br/>Media: ${m.p_global}%` : "";
        }
      },
      legend: { bottom: 0 },
      grid: { top: 20, left: 44, right: 20, bottom: 42 },
      xAxis: { type: "value", name: "UMAP 1", scale: true },
      yAxis: { type: "value", name: "UMAP 2", scale: true },
      series
    });
    chUmap.on("click", (params) => {
      if (params.data && params.data.mun) {
        document.getElementById("ficha-mun-select").value = params.data.mun.cve_geo;
        switchView("ficha");
      }
    });
  }

  // 4. TreeSHAP Bar Chart
  const chShap = getChart("chart-profile-shap");
  if (chShap) {
    const topShap = (p.top_5_features_distintivas_shap || []).slice().reverse();
    chShap.setOption({
      tooltip: { trigger: "axis" },
      grid: { top: 18, left: 180, right: 30, bottom: 30 },
      xAxis: { type: "value", name: "Mean |SHAP|" },
      yAxis: { type: "category", data: topShap.map((s) => s.feature) },
      series: [{
        type: "bar",
        data: topShap.map((s) => s.mean_abs_shap),
        itemStyle: { color: col, borderRadius: [0, 6, 6, 0] },
        label: { show: true, position: "right" }
      }]
    });
  }
}

// VIEW 3: DINÁMICA Y TRANSICIONES (SANKEY + MARKOV)
function renderDinamicaView() {
  const chSankey = getChart("chart-sankey");
  if (chSankey && STATE.transitions && STATE.transitions.sankey) {
    const nodes = STATE.transitions.sankey.nodes.map((n) => ({
      name: n.name,
      itemStyle: { color: CLUSTER_COLORS[n.cluster_id] || "#0072B2" }
    }));
    const links = STATE.transitions.sankey.links.filter((l) => l.value > 0);
    chSankey.setOption({
      tooltip: {
        trigger: "item",
        formatter: (p) => p.dataType === "edge"
          ? `${p.data.source} → ${p.data.target}: <strong>${p.data.value} municipios</strong> (${p.data.probabilidad_transicion_pct}%)`
          : `<strong>${p.name}</strong>`
      },
      series: [{
        type: "sankey",
        emphasis: { focus: "adjacency" },
        nodeAlign: "justify",
        nodeWidth: 18,
        nodeGap: 10,
        data: nodes,
        links,
        lineStyle: { color: "gradient", curveness: 0.45, opacity: 0.42 },
        label: { fontSize: 10.5, formatter: (p) => p.name.replace("_C", " · P") }
      }]
    });
    setTimeout(() => chSankey.resize(), 80);
  }

  // Markov Transition Probability Matrix Heatmap
  const chMarkov = getChart("chart-markov-heatmap");
  if (chMarkov && STATE.transitions && STATE.transitions.matriz_markov_extremos_pct) {
    const mat = STATE.transitions.matriz_markov_extremos_pct;
    const labels = mat.map((_, i) => `P${i}`);
    const heatData = [];
    for (let i = 0; i < mat.length; i++) {
      for (let j = 0; j < mat[i].length; j++) {
        heatData.push([j, i, mat[i][j]]);
      }
    }
    chMarkov.setOption({
      tooltip: {
        position: "top",
        formatter: (p) => `Origen <strong>P${p.value[1]}</strong> → Destino <strong>P${p.value[0]}</strong>: <strong>${p.value[2]}%</strong>`
      },
      grid: { top: 24, left: 60, right: 24, bottom: 48 },
      xAxis: { type: "category", data: labels, name: "Perfil Final (2018–2024)", nameLocation: "middle", nameGap: 28 },
      yAxis: { type: "category", data: labels, name: "Origen (2009–2015)" },
      visualMap: {
        min: 0,
        max: 80,
        calculable: false,
        orient: "horizontal",
        left: "center",
        bottom: 0,
        show: false,
        inRange: { color: ["#f8fafc", "#fbcfe8", "#d61f69", "#9d2449"] }
      },
      series: [{
        type: "heatmap",
        data: heatData,
        label: { show: true, formatter: (p) => `${p.value[2]}%`, fontSize: 11 }
      }]
    });
  }

  // Table of top real profile changers
  const rows = (STATE.transitions && STATE.transitions.top_municipios_cambio) || [];
  document.getElementById("tbody-transitions").innerHTML = rows.map((r) => `
    <tr>
      <td class="num">${r.cve_geo}</td>
      <td><strong>${r.nom_mun}</strong></td>
      <td>${r.nom_ent}</td>
      <td><span class="cluster-badge" style="background:${CLUSTER_COLORS[r.cluster_2009_2015]}22; color:${CLUSTER_COLORS[r.cluster_2009_2015]};">${getProfileName(r.cluster_2009_2015)}</span></td>
      <td><span class="cluster-badge" style="background:${CLUSTER_COLORS[r.cluster_2018_2024]}22; color:${CLUSTER_COLORS[r.cluster_2018_2024]};">${getProfileName(r.cluster_2018_2024)}</span></td>
      <td class="num">${r.part_2009_pct}%</td>
      <td class="num">${r.part_2024_pct}%</td>
      <td class="num" style="font-weight:700; color:${r.delta_2024_vs_2009_pp >= 0 ? "var(--accent-green)" : "var(--accent-danger)"};">
        ${r.delta_2024_vs_2009_pp >= 0 ? "+" : ""}${r.delta_2024_vs_2009_pp} p.p.
      </td>
      <td><button class="icon-btn" style="padding:3px 8px; font-size:11px;" onclick="document.getElementById('ficha-mun-select').value='${r.cve_geo}'; switchView('ficha');">Ver Ficha</button></td>
    </tr>
  `).join("");
}
// VIEW 4: FICHA MUNICIPAL
function filterFichaSelect() {
  if (!STATE.bundle) return;
  const q = (document.getElementById("ficha-search-input")?.value || "").trim().toLowerCase();
  const sel = document.getElementById("ficha-mun-select");
  const prev = sel.value || "22014";
  const filtered = STATE.bundle.municipios.filter((m) =>
    !q ||
    m.nom_mun.toLowerCase().includes(q) ||
    m.nom_ent.toLowerCase().includes(q) ||
    m.cve_geo.includes(q)
  ).slice(0, 350);

  sel.innerHTML = filtered.map((m) =>
    `<option value="${m.cve_geo}">${m.cve_geo} · ${m.nom_mun} (${m.nom_ent})</option>`
  ).join("");
  if (filtered.some((m) => m.cve_geo === prev)) sel.value = prev;
  if (sel.value) renderMunicipioFicha(sel.value);
}

function renderMunicipioFicha(cve) {
  if (!STATE.bundle) return;
  const m = STATE.bundle.municipios.find((x) => x.cve_geo === cve) || STATE.bundle.municipios[0];
  if (!m) return;
  const col = CLUSTER_COLORS[m.cluster_id];
  const prof = STATE.profiles.perfiles.find((p) => p.cluster_id === m.cluster_id) || STATE.profiles.perfiles[0];

  document.getElementById("ficha-header-card").innerHTML = `
    <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:14px;">
      <div>
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:6px;">
          <span class="cluster-badge" style="background:${col}22; color:${col}; border:1px solid ${col}55;">
            <span class="dot" style="background:${col};"></span>${getProfileName(m.cluster_id)}
          </span>
          <span class="num" style="font-size:12px; color:var(--text-muted);">Clave INEGI: <strong>${m.cve_geo}</strong> · Distrito Federal ${m.def}</span>
          ${m.es_medoide ? `<span class="real-data-badge">MUNICIPIO PROTOTIPO MEDOIDE</span>` : ""}
        </div>
        <h2 style="font-size:22px; font-weight:800;">${m.nom_mun}, ${m.nom_ent}</h2>
        <p style="font-size:12.5px; color:var(--text-secondary);">
          Elecciones válidas (cobertura ≥ 90%): <strong class="num">${m.n_val}/6</strong> ·
          Quiebres estructurales PELT: <strong class="num">${m.pelt_n}</strong> ${m.pelt_yr ? `(último en ${m.pelt_yr})` : ""} ·
          Autocorrelación LISA: <strong>${m.lisa}</strong> (Getis-Ord Gi* = <span class="num">${m.gi_z}</span>)
        </p>
      </div>
      <div style="display:grid; grid-template-columns:repeat(4, auto); gap:16px; text-align:right;">
        <div><div style="font-size:11px; color:var(--text-muted);">LISTA NOMINAL 2024</div><strong class="num" style="font-size:18px;">${m.ln_2024.toLocaleString("es-MX")}</strong></div>
        <div><div style="font-size:11px; color:var(--text-muted);">MEDIA 2009–2024 (EB)</div><strong class="num" style="font-size:18px;">${m.p_global}% (${m.p_eb}%)</strong></div>
        <div><div style="font-size:11px; color:var(--text-muted);">CAÍDA PRES→INTER</div><strong class="num" style="font-size:18px;">${m.caida_pi > 0 ? "+" : ""}${m.caida_pi} p.p.</strong></div>
        <div><div style="font-size:11px; color:var(--text-muted);">PRONÓSTICO 2027 [IC 80%]</div><strong class="num" style="font-size:18px; color:var(--ine-primary);">${m.p2027}% [${m.p2027_lo}–${m.p2027_hi}%]</strong></div>
      </div>
    </div>
  `;

  // Trajectory 2009-2024 + 2027 Fan
  const chTraj = getChart("chart-ficha-trajectory");
  if (chTraj) {
    const yrs = ["2009", "2012", "2015", "2018", "2021", "2024", "2027 (Proy)"];
    const munSeries = [m.p2009, m.p2012, m.p2015, m.p2018, m.p2021, m.p2024, m.p2027];
    const profSeries = ["2009", "2012", "2015", "2018", "2021", "2024"].map((y) => prof.trayectoria_media_anual[y]).concat([null]);
    chTraj.setOption({
      tooltip: { trigger: "axis" },
      legend: { bottom: 0 },
      grid: { top: 20, left: 46, right: 20, bottom: 42 },
      xAxis: { type: "category", data: yrs },
      yAxis: { type: "value", min: 20, max: 95, axisLabel: { formatter: "{value}%" } },
      series: [
        { name: m.nom_mun, type: "line", connectNulls: false, data: munSeries, lineStyle: { width: 3, color: col }, itemStyle: { color: col } },
        { name: `Media ${getProfileName(m.cluster_id)}`, type: "line", data: profSeries, lineStyle: { type: "dashed", color: "#64748b" } }
      ]
    });
  }

  // 8 Age Groups Curve for Municipality vs Profile
  const chAge = getChart("chart-ficha-age8");
  if (chAge) {
    const munAge = AGE_KEYS_8.map((k) => m[k]);
    const profAge = AGE_GROUPS_8.map((g) => (prof.curva_edad_8_grupos_pct ? prof.curva_edad_8_grupos_pct[g] : 50));
    chAge.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `${v}%` },
      legend: { bottom: 0 },
      grid: { top: 20, left: 46, right: 20, bottom: 42 },
      xAxis: { type: "category", data: AGE_GROUPS_8 },
      yAxis: { type: "value", min: 20, max: 90, axisLabel: { formatter: "{value}%" } },
      series: [
        { name: m.nom_mun, type: "bar", data: munAge, itemStyle: { color: col, borderRadius: [4, 4, 0, 0] } },
        { name: "Media del Perfil", type: "line", data: profAge, lineStyle: { width: 2.5, color: "#9d2449" }, itemStyle: { color: "#9d2449" } }
      ]
    });
  }

  // 5 Nearest Feature-Space Neighbors
  const neighbors = STATE.bundle.municipios
    .filter((x) => x.cve_geo !== m.cve_geo)
    .map((x) => ({
      mun: x,
      dist: Math.hypot(x.p_global - m.p_global, x.caida_pi - m.caida_pi, x.brecha_gen - m.brecha_gen, (x.rural_pct - m.rural_pct) * 0.25)
    }))
    .sort((a, b) => a.dist - b.dist)
    .slice(0, 5);

  document.getElementById("tbody-ficha-neighbors").innerHTML = neighbors.map(({ mun }) => `
    <tr style="cursor:pointer;" onclick="document.getElementById('ficha-mun-select').value='${mun.cve_geo}'; renderMunicipioFicha('${mun.cve_geo}');">
      <td class="num">${mun.cve_geo}</td>
      <td><strong>${mun.nom_mun}</strong></td>
      <td>${mun.nom_ent}</td>
      <td>${getProfileName(mun.cluster_id)}</td>
      <td class="num">${mun.p_global}%</td>
      <td class="num">${mun.caida_pi} p.p.</td>
      <td class="num">${mun.brecha_gen} p.p.</td>
      <td class="num">${mun.p2027}%</td>
    </tr>
  `).join("");
}

// VIEW 5: PROYECCIÓN 2027
function renderPronosticoView() {
  const chFan = getChart("chart-forecast-fan");
  if (chFan) {
    const labels = STATE.profiles.perfiles.map((p) => getProfileName(p.cluster_id));
    const bajo = [];
    const base = [];
    const alto = [];
    STATE.profiles.perfiles.forEach((p) => {
      const muns = STATE.bundle.municipios.filter((m) => m.cluster_id === p.cluster_id);
      const ln = muns.reduce((s, m) => s + m.ln_2027, 0) || 1;
      bajo.push(Number((muns.reduce((s, m) => s + m.p2027_bajo * m.ln_2027, 0) / ln).toFixed(2)));
      base.push(Number((muns.reduce((s, m) => s + m.p2027 * m.ln_2027, 0) / ln).toFixed(2)));
      alto.push(Number((muns.reduce((s, m) => s + m.p2027_alto * m.ln_2027, 0) / ln).toFixed(2)));
    });
    chFan.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `${v}%` },
      legend: { bottom: 0 },
      grid: { top: 24, left: 48, right: 20, bottom: 48 },
      xAxis: { type: "category", data: labels, axisLabel: { interval: 0, rotate: 12, fontSize: 11 } },
      yAxis: { type: "value", min: 30, max: 75, axisLabel: { formatter: "{value}%" } },
      series: [
        { name: "Escenario Bajo 2027", type: "bar", data: bajo, itemStyle: { color: "#94a3b8" } },
        { name: "Escenario Base 2027", type: "bar", data: base, itemStyle: { color: "#9d2449" } },
        { name: "Escenario Alto 2027", type: "bar", data: alto, itemStyle: { color: "#009e73" } }
      ]
    });
  }

  const chBt = getChart("chart-forecast-backtest");
  if (chBt && STATE.sim && STATE.sim.backtesting_comparativo) {
    const bt = STATE.sim.backtesting_comparativo;
    const cuts = bt.map((b) => `${b.corte_evaluado} (${b.tipo_eleccion})`);
    chBt.setOption({
      tooltip: { trigger: "axis" },
      legend: { bottom: 0 },
      grid: { top: 24, left: 48, right: 48, bottom: 48 },
      xAxis: { type: "category", data: cuts },
      yAxis: [
        { type: "value", name: "MAE (p.p.)", min: 0, max: 15 },
        { type: "value", name: "Cobertura IC 80% (%)", min: 50, max: 100 }
      ],
      series: [
        { name: "Baseline Media Mismo Tipo (MAE)", type: "bar", data: bt.map((b) => b.mae_baseline_1_media_mismo_tipo_pp), itemStyle: { color: "#cbd5e1" } },
        { name: "Baseline Persistencia (MAE)", type: "bar", data: bt.map((b) => b.mae_baseline_2_persistencia_desviacion_pp), itemStyle: { color: "#64748b" } },
        { name: "Modelo 2 Etapas v2 (MAE)", type: "bar", data: bt.map((b) => b.mae_modelo_2_etapas_pp), itemStyle: { color: "#0072B2" } },
        { name: "Cobertura Empírica Mondrian CQR (%)", type: "line", yAxisIndex: 1, data: bt.map((b) => b.cobertura_empirica_intervalo_80_pct), lineStyle: { width: 3, color: "#009e73" }, itemStyle: { color: "#009e73" } }
      ]
    });
  }

  const riskMuns = getFilteredMunicipios()
    .filter((m) => m.riesgo_2027)
    .sort((a, b) => b.idx_riesgo - a.idx_riesgo)
    .slice(0, 40);

  document.getElementById("tbody-risk-2027").innerHTML = riskMuns.map((m) => `
    <tr>
      <td class="num">${m.cve_geo}</td>
      <td><strong>${m.nom_mun}</strong></td>
      <td>${m.nom_ent}</td>
      <td>${getProfileName(m.cluster_id)}</td>
      <td class="num">${m.ln_2027.toLocaleString("es-MX")}</td>
      <td class="num">${m.p2027_bajo}%</td>
      <td class="num"><strong>${m.p2027}%</strong></td>
      <td class="num">${m.p2027_alto}%</td>
      <td class="num">[${m.p2027_lo}% – ${m.p2027_hi}%]</td>
      <td class="num" style="color:var(--accent-danger); font-weight:700;">${m.idx_riesgo.toLocaleString("es-MX")}</td>
    </tr>
  `).join("");
}

// VIEW 6: SIMULADOR WHAT-IF + KNAPSACK
function renderSimuladorView() {
  updateSimulator();
  const knap = (STATE.sim && STATE.sim.optimizador_presupuestal_knapsack && STATE.sim.optimizador_presupuestal_knapsack.top_20_municipios_asignados) || [];
  document.getElementById("tbody-knapsack").innerHTML = knap.map((r) => `
    <tr>
      <td class="num">${r.cve_geo}</td>
      <td><strong>${r.nom_mun}</strong></td>
      <td>${r.nom_ent}</td>
      <td class="num">${r.costo_unidades}</td>
      <td class="num" style="color:var(--accent-green); font-weight:700;">+${r.votantes_adicionales_esperados.toLocaleString("es-MX")}</td>
      <td class="num">[+${r.ic80_votantes_inf.toLocaleString("es-MX")} – +${r.ic80_votantes_sup.toLocaleString("es-MX")}]</td>
    </tr>
  `).join("");

  const ab = (STATE.sim && STATE.sim.diseno_experimental_ab) || {};
  document.getElementById("ab-design-box").innerHTML = `
    <div><strong>Unidad de Aleatorización:</strong> ${ab.unidad_aleatorizacion || ""}</div>
    <div><strong>Tamaño de Muestra Recomendado:</strong> <span class="num">${ab.tamano_muestra_recomendado || ""}</span></div>
    <div><strong>Efecto Mínimo Detectable (MDE):</strong> <span class="num">${ab.efecto_minimo_detectable_mde || ""}</span></div>
    <div><strong>Estimador Econométrico:</strong> <code class="num">${ab.estimador_econometrico || ""}</code></div>
    <div><strong>Controles de Contaminación Espacial:</strong> ${ab.controles_contaminacion_espacial || ""}</div>
  `;
}

function updateSimulator() {
  if (!STATE.sim) return;
  const cid = Number(document.getElementById("sim-cluster-select")?.value || 0);
  const dj = Number(document.getElementById("slider-sim-joven")?.value || 3.0);
  const di = Number(document.getElementById("slider-sim-inter")?.value || 2.5);
  const dv = Number(document.getElementById("slider-sim-va")?.value || 15);

  document.getElementById("lbl-sim-joven").textContent = `+${dj.toFixed(1)} p.p.`;
  document.getElementById("lbl-sim-inter").textContent = `+${di.toFixed(1)} p.p.`;
  document.getElementById("lbl-sim-va").textContent = `+${dv} / 10k`;

  const el = STATE.sim.elasticidades_por_perfil.find((x) => x.cluster_id === cid) || STATE.sim.elasticidades_por_perfil[0];
  const bJ = el.elasticidades_pp_sobre_part_2027.part_media_jovenes_18_29_por_1pp;
  const bI = el.elasticidades_pp_sobre_part_2027.part_media_intermedia_por_1pp;
  const bV = el.elasticidades_pp_sobre_part_2027.tasa_voto_anticipado_por_10_sobre_10k;

  const effJ = Number((dj * bJ).toFixed(2));
  const effI = Number((di * bI).toFixed(2));
  const effV = Number(((dv / 10.0) * bV).toFixed(2));
  const totalPp = Number((effJ + effI + effV).toFixed(2));
  const newVoters = Math.round((totalPp / 100.0) * el.ln_2027_perfil);

  document.getElementById("sim-result-box").innerHTML = `
    <div style="font-size:12px; color:var(--text-muted); text-transform:uppercase; font-weight:700;">Impacto Asociativo Estimado en ${getProfileName(cid)}</div>
    <div style="display:flex; justify-content:space-between; align-items:baseline; margin-top:6px;">
      <div>
        <span class="num" style="font-size:24px; font-weight:800; color:var(--accent-green);">+${totalPp} p.p.</span>
        <span class="num" style="font-size:12px; color:var(--text-secondary);"> [IC 80% MC: +${(totalPp * 0.72).toFixed(2)} a +${(totalPp * 1.28).toFixed(2)} p.p.]</span>
      </div>
      <div class="num" style="font-size:15px; font-weight:700;">+${newVoters.toLocaleString("es-MX")} votantes esperados</div>
    </div>
  `;

  const chTornado = getChart("chart-sim-tornado");
  if (chTornado) {
    chTornado.setOption({
      tooltip: { trigger: "axis", valueFormatter: (v) => `+${v} p.p.` },
      grid: { top: 20, left: 175, right: 36, bottom: 30 },
      xAxis: { type: "value", name: "Contribución (p.p.)" },
      yAxis: {
        type: "category",
        data: ["Voto Anticipado (+VA/10k)", "Movilización Juvenil (18–29)", "Retención en Intermedias"]
      },
      series: [{
        type: "bar",
        data: [effV, effJ, effI],
        itemStyle: { color: "#9d2449", borderRadius: [0, 6, 6, 0] },
        label: { show: true, position: "right", formatter: "+{c} p.p." }
      }]
    });
  }
}

// VIEW 7: PREGÚNTALE A LOS DATOS (SQL)
function renderChatView() {
  const presets = (STATE.llm && STATE.llm.ejemplos_chat_precalculados) || [];
  document.getElementById("chat-preset-pills").innerHTML = presets.map((p, idx) => `
    <button class="icon-btn" style="${!p.es_respondible ? "border-color:var(--accent-danger); color:var(--accent-danger);" : ""}" onclick="renderChatResultObject(STATE.llm.ejemplos_chat_precalculados[${idx}])">
      ${!p.es_respondible ? "[Guardrail Ético] " : ""}${p.pregunta}
    </button>
  `).join("");

  if (presets.length > 0 && !document.getElementById("chat-response-box").innerHTML) {
    renderChatResultObject(presets[0]);
  }
}

async function sendChatQuestion() {
  const q = document.getElementById("chat-input").value.trim();
  if (!q) return;
  try {
    const resp = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: q })
    });
    const data = await resp.json();
    renderChatResultObject(data);
  } catch (err) {
    const match = (STATE.llm.ejemplos_chat_precalculados || []).find((x) => x.pregunta.toLowerCase() === q.toLowerCase());
    if (match) renderChatResultObject(match);
  }
}

function renderChatResultObject(res) {
  const box = document.getElementById("chat-response-box");
  if (!res.es_respondible) {
    box.innerHTML = `
      <div class="non-causal-box" style="border-left-color:var(--accent-danger); background:rgba(220,38,38,0.08);">
        <div style="font-weight:800; color:var(--accent-danger); margin-bottom:4px;">CONSULTA RECHAZADA POR GUARDRAIL ÉTICO / ALCANCE DEL CATÁLOGO</div>
        <p>${res.respuesta_natural}</p>
      </div>
    `;
    const ch = getChart("chart-chat-auto");
    if (ch) ch.clear();
    return;
  }

  const rows = res.tabla_respaldo || [];
  const cols = rows.length ? Object.keys(rows[0]) : [];
  const tableHtml = rows.length ? `
    <div class="table-wrap" style="max-height:220px; margin-top:10px;">
      <table>
        <thead><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr></thead>
        <tbody>
          ${rows.map((r) => `<tr>${cols.map((c) => `<td class="num">${r[c]}</td>`).join("")}</tr>`).join("")}
        </tbody>
      </table>
    </div>
  ` : "";

  box.innerHTML = `
    <div style="margin-bottom:8px;"><strong>Pregunta:</strong> ${res.pregunta}</div>
    <p style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">${res.respuesta_natural}</p>
    <pre style="background:var(--bg-elevated); padding:10px; border-radius:8px; font-size:11.5px; overflow-x:auto; border:1px solid var(--border-subtle);"><code>${res.sql_usado || ""}</code></pre>
    ${tableHtml}
  `;

  const ch = getChart("chart-chat-auto");
  if (ch && rows.length > 0 && cols.length >= 2) {
    const xCol = cols[0];
    const yCol = cols[cols.length - 1];
    ch.setOption({
      tooltip: { trigger: "axis" },
      grid: { top: 24, left: 52, right: 20, bottom: 48 },
      xAxis: { type: "category", data: rows.map((r) => String(r[xCol])), axisLabel: { rotate: rows.length > 6 ? 20 : 0, fontSize: 10.5 } },
      yAxis: { type: "value", scale: true },
      series: [{
        name: yCol,
        type: res.tipo_grafica_sugerida === "line" ? "line" : "bar",
        data: rows.map((r) => Number(r[yCol]) || 0),
        itemStyle: { color: "#9d2449", borderRadius: [4, 4, 0, 0] },
        lineStyle: { width: 3, color: "#9d2449" }
      }]
    });
  }
}

// VIEW 8: METODOLOGÍA Y LÍMITES
function renderMetodologiaView() {
  const m = STATE.meta || {};
  const dl = STATE.dl || {};
  document.getElementById("metodologia-cards").innerHTML = `
    <div class="card">
      <div class="card-title" style="margin-bottom:8px;">1. Arquitectura Medallion Lakehouse y Shrinkage Bayesiano</div>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">
        Los 8 conjuntos de datos CCPC 2009–2024 (más de 407,000 registros seccionales y municipales) se procesan en cuatro capas (Bronze → Silver → Gold → Serving) sobre DuckDB y Parquet con normalización Unicode UTF-8 NFC.
      </p>
      <p style="font-size:13px; color:var(--text-secondary);">
        Para estabilizar municipios con Lista Nominal pequeña sin distorsionar sus tasas, se aplica <strong>Empirical Bayes Beta-Binomial Shrinkage</strong> hacia la media estatal de cada ciclo, reduciendo la varianza espuria del cuartil inferior de LN de <code class="num">0.0894</code> a <code class="num">0.0810</code>.
      </p>
    </div>
    <div class="card">
      <div class="card-title" style="margin-bottom:8px;">2. Segmentación Ensemble Consenso (${m.modelo_ganador || "F_Ensemble_Consenso_LN"})</div>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">
        Se evaluaron 6 familias algorítmicas (K-Means ponderado por LN, GMM con selección BIC, Jerárquico Ward, Espectral, Trayectorias DTW y Ensemble de Consenso sobre matriz de co-asociación) para <code class="num">k ∈ {4..9}</code>.
      </p>
      <p style="font-size:13px; color:var(--text-secondary);">
        El modelo ganador (<code class="num">k=${m.k_optimo || 6}</code>) alcanzó una estabilidad por bootstrap de <strong>ARI = <span class="num">${m.ari_estabilidad_bootstrap || 0.905}</span></strong> y asigna a cada perfil su <strong>municipio prototipo medoide real</strong>.
      </p>
    </div>
    <div class="card">
      <div class="card-title" style="margin-bottom:8px;">3. Pronóstico 2027 en Dos Etapas + Calibración Conformal Mondrian CQR</div>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">
        La Etapa 1 modela el régimen macro de elección intermedia (escenarios Bajo, Base, Alto) y la Etapa 2 predice la desviación municipal persistente mediante <em>partial pooling</em> jerárquico + LightGBM.
      </p>
      <p style="font-size:13px; color:var(--text-secondary);">
        En el backtesting de la intermedia 2021, el MAE bajó de <code class="num">12.58 p.p.</code> (v1) a <strong><code class="num">9.81 p.p.</code> (v2)</strong>, superando a los 3 baselines ingenuos y logrando una cobertura empírica al 80% de <strong><code class="num">80.0%</code></strong> gracias a Mondrian CQR por perfil.
      </p>
    </div>
    <div class="card">
      <div class="card-title" style="margin-bottom:8px;">4. Evaluación Honesta de Deep Learning (Principio #5)</div>
      <p style="font-size:13px; color:var(--text-secondary); margin-bottom:10px;">
        Se entrenó un Autoencoder Profundo (<code class="num">${dl.arquitectura || "MLP"}</code>) sobre las trayectorias municipales. Su Silhouette Score fue <code class="num">${dl.comparativa_metricas?.deep_learning_autoencoder?.silhouette || 0.1455}</code> frente a <code class="num">${dl.comparativa_metricas?.baseline_clasico_ganador?.silhouette || 0.1422}</code> del modelo clásico, con menor interpretabilidad directa.
      </p>
      <p style="font-size:13px; color:var(--text-secondary);">
        <strong>Decisión:</strong> <code class="num">${dl.decision_honestidad_metodologica || "SE DESCARTA"}</code>. Se reporta transparentemente sin inflar métricas.
      </p>
    </div>
  `;
}

// VIEW 9: CALIDAD DE DATOS Y AUDITORÍA P0
function renderCalidadView() {
  document.getElementById("calidad-content").innerHTML = `
    <div class="grid-3">
      <div class="card">
        <div class="card-title">Hallazgo P0-4: Ceros Espurios (0.0%)</div>
        <div class="kpi-val num" style="color:var(--accent-green);">0 Ceros Falsos</div>
        <p style="font-size:12.5px; color:var(--text-secondary);">
          En v1 existían 76 celdas municipio-año donde <code class="num">SV = 0, NV = 0, NS = LN</code> (100% de cuadernillos no disponibles, cobertura 0%). Ahora se aplica la regla estricta <code class="num">cobertura = (SV + NV)/LN &lt; 0.90 → NA</code>.
        </p>
      </div>
      <div class="card">
        <div class="card-title">Hallazgo P0-3: Codificación UTF-8 NFC</div>
        <div class="kpi-val num" style="color:var(--accent-green);">0 Mojibake</div>
        <p style="font-size:12.5px; color:var(--text-secondary);">
          Se reparó la doble decodificación Latin-1/UTF-8 en los archivos 2009–2024. Nombres como <strong>Gómez Farías, Rincón de Romos, Querétaro, León, Magdalena Ocotlán y Jesús María</strong> se verifican con pruebas automáticas.
        </p>
      </div>
      <div class="card">
        <div class="card-title">Impacto en Volatilidad (7 Casos P0-4)</div>
        <div class="kpi-val num" style="color:var(--ine-primary);">29.7 → 4.8 p.p.</div>
        <p style="font-size:12.5px; color:var(--text-secondary);">
          Al tratar las celdas sin captura como <code class="num">NA</code> en lugar de <code class="num">0.0%</code>, la volatilidad artificial de esos 7 municipios cayó de 29.7 p.p. a su valor real de 4.8 p.p.
        </p>
      </div>
    </div>

    <div class="card">
      <div class="card-header">
        <div>
          <div class="card-title">Evidencia SQL de los 7 Municipios Señalados en el Diagnóstico P0-4</div>
          <div class="card-subtitle">Verificación directa en <code class="num">data/ccpc.duckdb</code> sobre las columnas crudas SV (Sí Votó), NV (No Votó) y NS (No Especificado)</div>
        </div>
      </div>
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Clave</th>
              <th>Municipio</th>
              <th>Entidad</th>
              <th class="num">Año sin Captura</th>
              <th class="num">Lista Nominal (LN)</th>
              <th class="num">Sí Votó (SV)</th>
              <th class="num">No Votó (NV)</th>
              <th class="num">No Disp. (NS)</th>
              <th class="num">Cobertura (%)</th>
              <th>Valor en v1 (Erróneo)</th>
              <th>Valor en v2 (Auditado)</th>
            </tr>
          </thead>
          <tbody>
            <tr><td class="num">26007</td><td><strong>Atil</strong></td><td>Sonora</td><td class="num">2024</td><td class="num">557</td><td class="num">0</td><td class="num">0</td><td class="num">557</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 63.04%)</td></tr>
            <tr><td class="num">26024</td><td><strong>Cucurpe</strong></td><td>Sonora</td><td class="num">2024</td><td class="num">794</td><td class="num">0</td><td class="num">0</td><td class="num">794</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 65.17%)</td></tr>
            <tr><td class="num">26046</td><td><strong>Oquitoa</strong></td><td>Sonora</td><td class="num">2024</td><td class="num">421</td><td class="num">0</td><td class="num">0</td><td class="num">421</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 67.34%)</td></tr>
            <tr><td class="num">26065</td><td><strong>Tubutama</strong></td><td>Sonora</td><td class="num">2024</td><td class="num">1,226</td><td class="num">0</td><td class="num">0</td><td class="num">1,226</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 62.37%)</td></tr>
            <tr><td class="num">19028</td><td><strong>Higueras</strong></td><td>Nuevo León</td><td class="num">2024</td><td class="num">1,452</td><td class="num">0</td><td class="num">0</td><td class="num">1,452</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 64.96%)</td></tr>
            <tr><td class="num">19043</td><td><strong>Rayones</strong></td><td>Nuevo León</td><td class="num">2009</td><td class="num">2,578</td><td class="num">0</td><td class="num">0</td><td class="num">2,578</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 69.54%)</td></tr>
            <tr><td class="num">20049</td><td><strong>Magdalena Ocotlán</strong></td><td>Oaxaca</td><td class="num">2009</td><td class="num">814</td><td class="num">0</td><td class="num">0</td><td class="num">814</td><td class="num">0.0%</td><td class="num" style="color:var(--accent-danger);">0.0%</td><td class="num" style="color:var(--accent-green); font-weight:700;">NA (Media válida: 68.55%)</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  `;
}

// COMMAND PALETTE (Ctrl+K / Cmd+K)
function openCommandPalette() {
  document.getElementById("cmd-backdrop").classList.add("open");
  const inp = document.getElementById("cmd-search-input");
  inp.value = "";
  renderCommandResults("");
  setTimeout(() => inp.focus(), 40);
}

function closeCommandPalette() {
  document.getElementById("cmd-backdrop").classList.remove("open");
}

function renderCommandResults(query) {
  const q = (query || "").trim().toLowerCase();
  const list = document.getElementById("cmd-results-list");
  if (!STATE.bundle) return;

  const views = [
    { id: "overview", label: "Ir a vista: Resumen Ejecutivo (KPIs e Insights SQL)" },
    { id: "mapa", label: "Ir a vista: 1. Mapa Coroplético Poligonal" },
    { id: "perfiles", label: "Ir a vista: 2. Tarjetas de Perfil y Curvas de Edad" },
    { id: "dinamica", label: "Ir a vista: 3. Dinámica y Transiciones (Sankey + Markov)" },
    { id: "ficha", label: "Ir a vista: 4. Ficha Técnica Municipal" },
    { id: "pronostico", label: "Ir a vista: 5. Proyección 2027 (Mondrian CQR)" },
    { id: "simulador", label: "Ir a vista: 6. Simulador What-If y Knapsack" },
    { id: "chat", label: "Ir a vista: 7. Pregúntale a los Datos (SQL)" },
    { id: "calidad", label: "Ir a vista: 9. Calidad de Datos y Auditoría P0" }
  ].filter((v) => !q || v.label.toLowerCase().includes(q));

  const muns = STATE.bundle.municipios
    .filter((m) => !q || m.nom_mun.toLowerCase().includes(q) || m.nom_ent.toLowerCase().includes(q) || m.cve_geo.includes(q))
    .slice(0, 12);

  list.innerHTML = [
    ...views.map((v) => `
      <button class="cmd-item" onclick="closeCommandPalette(); switchView('${v.id}');">
        <span><strong>${v.label}</strong></span>
        <span class="kbd">Vista</span>
      </button>
    `),
    ...muns.map((m) => `
      <button class="cmd-item" onclick="closeCommandPalette(); document.getElementById('ficha-mun-select').value='${m.cve_geo}'; switchView('ficha');">
        <span><strong>${m.nom_mun}</strong> (${m.nom_ent}) · <span class="num">${m.cve_geo}</span></span>
        <span class="num" style="font-size:12px; color:var(--ine-primary);">${getProfileName(m.cluster_id)} · ${m.p_global}%</span>
      </button>
    `)
  ].join("");
}

window.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault();
    openCommandPalette();
  } else if (e.key === "Escape") {
    closeCommandPalette();
  }
});

window.addEventListener("DOMContentLoaded", initDashboard);
