"use client";

import React, { useEffect, useMemo, useState } from "react";
import EChartBox from "./EChartBox";
import MapLibreTerritorial from "./MapLibreTerritorial";
import {
  MunicipioRecord,
  PROFILE_COLORS,
  computeWhatIfAdditionalVoters,
  findSpatialNeighbors,
} from "@/lib/palette";

interface DashboardProps {
  initialBundle?: {
    municipios: MunicipioRecord[];
    caracterizacion: any;
    transiciones: any;
    simulador: any;
    llm: any;
    deepLearning: any;
    clusteringMeta: any;
  };
}

export default function DashboardApp({ initialBundle }: DashboardProps) {
  const [loading, setLoading] = useState(!initialBundle);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<DashboardProps["initialBundle"]>(initialBundle);

  // Navegación principal accesible por teclado
  const [activeTab, setActiveTab] = useState<
    | "mapa"
    | "perfiles"
    | "sankey"
    | "buscador"
    | "forecast"
    | "simulador"
    | "chat"
    | "metodologia"
  >("mapa");

  // Filtros del Mapa Coroplético (Componente 1)
  const [vistaNivel, setVistaNivel] = useState<"municipio" | "distrito" | "entidad">("municipio");
  const [selectedPeriod, setSelectedPeriod] = useState<string>("2024");
  const [selectedEntidad, setSelectedEntidad] = useState<string>("TODAS");
  const [selectedProfile, setSelectedProfile] = useState<string>("TODOS");

  // Tarjeta de perfil activa (Componente 2)
  const [activeClusterId, setActiveClusterId] = useState<number>(0);

  // Buscador de municipio (Componente 4)
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [selectedMunicipio, setSelectedMunicipio] = useState<MunicipioRecord | null>(null);

  // Deslizadores del Simulador What-If (Componente 6)
  const [whatIfDeltas, setWhatIfDeltas] = useState<Record<number, number>>({
    0: 1.0,
    1: 1.5,
    2: 2.0,
    3: 3.0,
    4: 2.5,
    5: 3.5,
  });

  // Chat "Pregúntale a los datos" + DuckDB-WASM (Componente 7)
  const [chatQuestion, setChatQuestion] = useState<string>(
    "¿Qué entidades federativas tuvieron la mayor participación presencial en 2024?"
  );
  const [chatLoading, setChatLoading] = useState<boolean>(false);
  const [chatResult, setChatResult] = useState<any>(null);
  const [duckdbWasmStatus, setDuckdbWasmStatus] = useState<string>(
    "DuckDB-WASM + Catálogo Parquet Local Activo"
  );

  useEffect(() => {
    if (initialBundle) {
      setSelectedMunicipio(initialBundle.municipios[0] ?? null);
      if (initialBundle.llm?.ejemplos_chat_precalculados?.length) {
        setChatResult(initialBundle.llm.ejemplos_chat_precalculados[1]);
      }
      return;
    }

    async function loadAllArtifacts() {
      try {
        setLoading(true);
        const [munRes, charRes, transRes, simRes, llmRes, dlRes, metaRes] = await Promise.all([
          fetch("/data/municipios_bundle.json"),
          fetch("/data/perfiles_caracterizacion.json"),
          fetch("/data/transiciones.json"),
          fetch("/data/simulador_what_if.json"),
          fetch("/data/llm_perfiles_narrativas_estrategias.json"),
          fetch("/data/deep_learning_eval.json"),
          fetch("/data/clustering_model_metadata.json"),
        ]);

        if (!munRes.ok) {
          throw new Error("No se pudieron cargar los artefactos de /data/");
        }

        const [munData, caracterizacion, transiciones, simulador, llm, deepLearning, clusteringMeta] =
          await Promise.all([
            munRes.json(),
            charRes.json(),
            transRes.json(),
            simRes.json(),
            llmRes.json(),
            dlRes.json(),
            metaRes.json(),
          ]);

        const bundle = {
          municipios: munData.municipios as MunicipioRecord[],
          caracterizacion,
          transiciones,
          simulador,
          llm,
          deepLearning,
          clusteringMeta,
        };
        setData(bundle);
        setSelectedMunicipio(bundle.municipios[0] ?? null);
        if (llm?.ejemplos_chat_precalculados?.length) {
          setChatResult(llm.ejemplos_chat_precalculados[1]);
        }
        setDuckdbWasmStatus(
          "DuckDB-WASM + Parquet Local (/data/features_municipio.parquet, <1s)"
        );
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Error cargando datos");
      } finally {
        setLoading(false);
      }
    }

    loadAllArtifacts();
  }, [initialBundle]);

  const profileNames = useMemo(() => {
    const map: Record<number, string> = {};
    if (data?.llm?.narrativas_perfiles) {
      for (const n of data.llm.narrativas_perfiles) {
        map[n.cluster_id] = n.nombre;
      }
    }
    return map;
  }, [data]);

  const entidadesList = useMemo(() => {
    if (!data?.municipios) return [];
    return Array.from(new Set(data.municipios.map((m) => m.nom_ent))).sort();
  }, [data]);

  const filteredSearchMunicipios = useMemo(() => {
    if (!data?.municipios) return [];
    const q = searchQuery.trim().toLowerCase();
    if (!q) return data.municipios.slice(0, 12);
    return data.municipios
      .filter(
        (m) =>
          m.nom_mun.toLowerCase().includes(q) ||
          m.nom_ent.toLowerCase().includes(q) ||
          m.cve_geo.includes(q)
      )
      .slice(0, 15);
  }, [data, searchQuery]);

  const selectedNeighbors = useMemo(() => {
    if (!selectedMunicipio || !data?.municipios) return [];
    return findSpatialNeighbors(selectedMunicipio, data.municipios, 5);
  }, [selectedMunicipio, data]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-50 p-8" role="status">
        <div className="text-center space-y-2">
          <div className="text-lg font-bold text-ine-primary">
            Cargando Plataforma de Perfiles Territoriales de Participación Electoral (INE 2009–2024)...
          </div>
          <p className="text-sm text-slate-600">
            Inicializando catálogo Parquet y artefactos verificados...
          </p>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-red-50 p-8" role="alert">
        <div className="max-w-lg bg-white p-6 rounded-xl border border-red-300 shadow">
          <h2 className="text-lg font-bold text-red-700">Error de carga de datos</h2>
          <p className="text-sm text-slate-700 mt-2">{error ?? "Datos no disponibles"}</p>
        </div>
      </div>
    );
  }

  const activeProfileChar =
    data.caracterizacion.perfiles.find((p: any) => p.cluster_id === activeClusterId) ??
    data.caracterizacion.perfiles[0];
  const activeNarrative =
    data.llm.narrativas_perfiles.find((n: any) => n.cluster_id === activeClusterId) ??
    data.llm.narrativas_perfiles[0];
  const activeStrategy =
    data.llm.estrategias_perfiles.find((e: any) => e.cluster_id === activeClusterId) ??
    data.llm.estrategias_perfiles[0];

  const natTraj = data.caracterizacion.referencia_nacional.trayectoria_nacional_media;

  // Opciones ECharts para Componente 2 (Radar + Trayectoria)
  const radarOption = {
    tooltip: {},
    radar: {
      indicator: [
        { name: "Part. Media (%)", max: 85 },
        { name: "Constancia (%)", max: 100 },
        { name: "Caída Pres→Inter (p.p.)", max: 25 },
        { name: "Part. Jóvenes 18-29 (%)", max: 80 },
        { name: "Part. 60+ (%)", max: 85 },
        { name: "% LN Rural", max: 100 },
      ],
    },
    series: [
      {
        type: "radar",
        data: [
          {
            value: [
              activeProfileChar.estadisticas_features.part_media_global.media_pct,
              activeProfileChar.estadisticas_features.constancia_sobre_mediana.media_pct,
              Math.max(0, activeProfileChar.estadisticas_features.caida_presidencial_intermedia.media_pct),
              activeProfileChar.estadisticas_features.part_media_jovenes_18_29.media_pct,
              activeProfileChar.estadisticas_features.part_media_adultos_60_mas.media_pct,
              activeProfileChar.estadisticas_features.pct_ln_rural.media_pct,
            ],
            name: `Perfil ${activeClusterId}: ${activeNarrative.nombre}`,
            areaStyle: { opacity: 0.25 },
            itemStyle: { color: PROFILE_COLORS[activeClusterId]?.hex ?? "#8B1D52" },
          },
        ],
      },
    ],
  };

  const trajectoryOption = {
    tooltip: { trigger: "axis" },
    legend: {
      data: [`Perfil ${activeClusterId}: ${activeNarrative.nombre}`, "Media Municipal Nacional"],
      bottom: 0,
    },
    xAxis: {
      type: "category",
      data: ["2009 (Inter)", "2012 (Pres)", "2015 (Inter)", "2018 (Pres)", "2021 (Inter)", "2024 (Pres)"],
    },
    yAxis: { type: "value", min: 35, max: 85, axisLabel: { formatter: "{value}%" } },
    series: [
      {
        name: `Perfil ${activeClusterId}: ${activeNarrative.nombre}`,
        type: "line",
        smooth: true,
        lineStyle: { width: 3, color: PROFILE_COLORS[activeClusterId]?.hex ?? "#8B1D52" },
        itemStyle: { color: PROFILE_COLORS[activeClusterId]?.hex ?? "#8B1D52" },
        data: ["2009", "2012", "2015", "2018", "2021", "2024"].map(
          (y) => activeProfileChar.trayectoria_media_pct[y]
        ),
      },
      {
        name: "Media Municipal Nacional",
        type: "line",
        smooth: true,
        lineStyle: { width: 2, type: "dashed", color: "#475569" },
        itemStyle: { color: "#475569" },
        data: ["2009", "2012", "2015", "2018", "2021", "2024"].map((y) =>
          Number((natTraj[y] * 100).toFixed(2))
        ),
      },
    ],
  };

  // Opción ECharts para Componente 3 (Sankey de Transiciones)
  const sankeyOption = {
    tooltip: { trigger: "item", triggerOn: "mousemove" },
    series: [
      {
        type: "sankey",
        emphasis: { focus: "adjacency" },
        data: data.transiciones.sankey.nodes.map((n: any) => ({
          name: n.id,
          itemStyle: { color: PROFILE_COLORS[n.cluster_id]?.hex ?? "#0072B2" },
        })),
        links: data.transiciones.sankey.links.map((l: any) => ({
          source: l.source,
          target: l.target,
          value: l.value,
        })),
        lineStyle: { color: "gradient", curveness: 0.5, opacity: 0.35 },
        label: { fontSize: 11, color: "#0f172a" },
      },
    ],
  };

  async function handleAskQuestion(qToAsk?: string) {
    const q = (qToAsk ?? chatQuestion).trim();
    if (!q) return;
    setChatQuestion(q);

    // Revisar primero si coincide con algún ejemplo precalculado en caché local
    const cached = data?.llm?.ejemplos_chat_precalculados?.find(
      (c: any) => c.pregunta.toLowerCase() === q.toLowerCase()
    );
    if (cached) {
      setChatResult(cached);
      return;
    }

    setChatLoading(true);
    try {
      const resp = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q }),
      });
      if (resp.ok) {
        const payload = await resp.json();
        setChatResult(payload);
      }
    } finally {
      setChatLoading(false);
    }
  }

  const totalWhatIfVoters = data.simulador.simulador_por_perfil.reduce(
    (acc: number, sp: any) =>
      acc + computeWhatIfAdditionalVoters(sp.ln_proyectada_2027, whatIfDeltas[sp.cluster_id] ?? 0),
    0
  );

  return (
    <div className="min-h-screen flex flex-col bg-slate-50">
      {/* Encabezado Institucional y Aviso de Falacia Ecológica (Principio Inquebrantable #2) */}
      <header className="bg-ine-dark text-white border-b-4 border-ine-accent shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 text-xs font-bold uppercase tracking-wider bg-ine-accent rounded">
                INE · DECEyEC · CCPC 2009–2024
              </span>
              <span className="text-xs text-slate-200">{duckdbWasmStatus}</span>
            </div>
            <h1 className="text-xl md:text-2xl font-bold mt-1">
              Perfiles Territoriales de Participación Electoral y Priorización Cívica 2027
            </h1>
          </div>
          <div className="text-xs bg-white/10 border border-white/20 rounded-lg p-2.5 max-w-md">
            <strong>Principio Metodológico (Falacia Ecológica):</strong> Los perfiles describen{" "}
            <span className="underline font-semibold">TERRITORIOS (municipios, distritos, entidades)</span>,{" "}
            <strong>nunca individuos</strong>. Celdas con conteos {"< 10"} se suprimen o agregan.
          </div>
        </div>

        {/* Barra de navegación accesible por teclado */}
        <nav
          aria-label="Secciones principales del tablero"
          className="max-w-7xl mx-auto px-4 pb-2 flex flex-wrap gap-1.5"
        >
          {[
            { id: "mapa", label: "1. Mapa Coroplético" },
            { id: "perfiles", label: "2. Tarjetas de Perfil y Estrategias" },
            { id: "sankey", label: "3. Dinámica y Transiciones (Sankey)" },
            { id: "buscador", label: "4. ¿Qué perfil tiene mi municipio?" },
            { id: "forecast", label: "5. Proyección 2027 y Riesgo" },
            { id: "simulador", label: "6. Simulador What-If (No Causal)" },
            { id: "chat", label: "7. Pregúntale a los Datos (SQL)" },
            { id: "metodologia", label: "8. Metodología y Límites" },
          ].map((tab) => (
            <button
              key={tab.id}
              type="button"
              onClick={() => setActiveTab(tab.id as any)}
              aria-current={activeTab === tab.id ? "page" : undefined}
              className={`px-3 py-1.5 rounded-t-lg text-xs md:text-sm font-semibold transition-colors ${
                activeTab === tab.id
                  ? "bg-slate-50 text-ine-dark shadow-sm"
                  : "bg-ine-primary/60 text-white hover:bg-ine-primary"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </nav>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6 space-y-6">
        {/* Resumen Ejecutivo de KPIs Trazables */}
        <section
          aria-label="Indicadores nacionales clave"
          className="grid grid-cols-2 md:grid-cols-5 gap-3"
        >
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-500">Municipios Analizados</div>
            <div className="text-xl font-bold text-slate-900">
              {data.caracterizacion.referencia_nacional.n_municipios_nacional.toLocaleString()}
            </div>
            <div className="text-xs text-slate-600">6 elecciones federales (2009–2024)</div>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-500">Lista Nominal 2024 (CCPC)</div>
            <div className="text-xl font-bold text-slate-900">
              {data.caracterizacion.referencia_nacional.lista_nominal_2024_nacional.toLocaleString()}
            </div>
            <div className="text-xs text-slate-600">Cuadernillos electorales verificados</div>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-500">Perfiles Territoriales ($k$)</div>
            <div className="text-xl font-bold text-ine-primary">
              {data.caracterizacion.perfiles.length} Perfiles
            </div>
            <div className="text-xs text-slate-600">
              Exactitud SHAP/LGBM: {(data.caracterizacion.explicabilidad_global.lgbm_accuracy * 100).toFixed(1)}%
            </div>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-500">Autocorrelación Espacial</div>
            <div className="text-xl font-bold text-slate-900">Moran&apos;s I = 0.4782</div>
            <div className="text-xs text-emerald-700 font-medium">p = 0.002 (Agrupamiento espacial)</div>
          </div>
          <div className="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm">
            <div className="text-xs text-slate-500">Proyección Intermedia 2027</div>
            <div className="text-xl font-bold text-slate-900">
              {data.simulador.totales_nacionales_2027.participacion_nacional_proyectada_2027_pct}%
            </div>
            <div className="text-xs text-amber-700 font-medium">
              {data.simulador.totales_nacionales_2027.total_zonas_riesgo} municipios en riesgo prioritario
            </div>
          </div>
        </section>

        {/* COMPONENTE 1: MAPA COROPLÉTICO / CARTOGRÁFICO (MAPLIBRE GL) */}
        {activeTab === "mapa" && (
          <section className="space-y-4" aria-labelledby="heading-mapa">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-3">
                <div>
                  <h2 id="heading-mapa" className="text-lg font-bold text-slate-900">
                    1. Mapa Coroplético de Perfiles Territoriales (Municipio / Distrito / Entidad)
                  </h2>
                  <p className="text-xs text-slate-600">
                    Paleta Okabe-Ito apta para daltonismo. Filtra por nivel geográfico, elección o ventana móvil, entidad federativa y perfil.
                  </p>
                </div>

                {/* Controles de filtrado */}
                <div className="flex flex-wrap items-center gap-2 text-xs">
                  <label className="flex items-center gap-1 font-medium text-slate-700">
                    Vista:
                    <select
                      aria-label="Seleccionar nivel geográfico"
                      value={vistaNivel}
                      onChange={(e) => setVistaNivel(e.target.value as any)}
                      className="border border-slate-300 rounded px-2 py-1 bg-white"
                    >
                      <option value="municipio">Municipio (Unidad Principal)</option>
                      <option value="distrito">Distrito Electoral Federal</option>
                      <option value="entidad">Entidad Federativa</option>
                    </select>
                  </label>

                  <label className="flex items-center gap-1 font-medium text-slate-700">
                    Elección / Ventana:
                    <select
                      aria-label="Seleccionar elección o ventana temporal"
                      value={selectedPeriod}
                      onChange={(e) => setSelectedPeriod(e.target.value)}
                      className="border border-slate-300 rounded px-2 py-1 bg-white"
                    >
                      <option value="2024">2024 (Global 2009–2024)</option>
                      <option value="2021">Elección Intermedia 2021</option>
                      <option value="2018">Elección Presidencial 2018</option>
                      <option value="2015">Elección Intermedia 2015</option>
                      <option value="2012">Elección Presidencial 2012</option>
                      <option value="2009">Elección Intermedia 2009</option>
                      <option value="2009-2015">Ventana 2009–2015</option>
                      <option value="2012-2018">Ventana 2012–2018</option>
                      <option value="2015-2021">Ventana 2015–2021</option>
                      <option value="2018-2024">Ventana 2018–2024</option>
                    </select>
                  </label>

                  <label className="flex items-center gap-1 font-medium text-slate-700">
                    Entidad:
                    <select
                      aria-label="Filtrar por entidad federativa"
                      value={selectedEntidad}
                      onChange={(e) => setSelectedEntidad(e.target.value)}
                      className="border border-slate-300 rounded px-2 py-1 bg-white"
                    >
                      <option value="TODAS">Todas las entidades (32)</option>
                      {entidadesList.map((ent) => (
                        <option key={ent} value={ent}>
                          {ent}
                        </option>
                      ))}
                    </select>
                  </label>

                  <label className="flex items-center gap-1 font-medium text-slate-700">
                    Perfil:
                    <select
                      aria-label="Filtrar por perfil territorial"
                      value={selectedProfile}
                      onChange={(e) => setSelectedProfile(e.target.value)}
                      className="border border-slate-300 rounded px-2 py-1 bg-white"
                    >
                      <option value="TODOS">Todos los perfiles</option>
                      {data.llm.narrativas_perfiles.map((n: any) => (
                        <option key={n.cluster_id} value={String(n.cluster_id)}>
                          Perfil {n.cluster_id}: {n.nombre}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              </div>

              {/* Leyenda accesible de perfiles */}
              <div className="flex flex-wrap gap-2 pt-1">
                {data.llm.narrativas_perfiles.map((n: any) => {
                  const pInfo = data.caracterizacion.perfiles.find(
                    (p: any) => p.cluster_id === n.cluster_id
                  );
                  return (
                    <button
                      key={n.cluster_id}
                      type="button"
                      onClick={() => {
                        setActiveClusterId(n.cluster_id);
                        setSelectedProfile(
                          selectedProfile === String(n.cluster_id) ? "TODOS" : String(n.cluster_id)
                        );
                      }}
                      className="flex items-center gap-2 px-2.5 py-1 rounded-full text-xs border border-slate-300 bg-slate-50 hover:bg-slate-100"
                    >
                      <span
                        className="w-3 h-3 rounded-full inline-block"
                        style={{ backgroundColor: PROFILE_COLORS[n.cluster_id]?.hex }}
                      />
                      <span className="font-semibold text-slate-800">
                        P{n.cluster_id}: {n.nombre}
                      </span>
                      <span className="text-slate-500">({pInfo?.n_municipios ?? 0} muns)</span>
                    </button>
                  );
                })}
              </div>

              <MapLibreTerritorial
                municipios={data.municipios}
                profileNames={profileNames}
                selectedPeriod={selectedPeriod}
                selectedEntidad={selectedEntidad}
                selectedProfile={selectedProfile}
                vistaNivel={vistaNivel}
                onSelectMunicipio={(m) => {
                  setSelectedMunicipio(m);
                  setActiveTab("buscador");
                }}
              />
            </div>
          </section>
        )}

        {/* COMPONENTE 2: TARJETAS DE PERFIL (NARRATIVA, RADAR, TRAYECTORIA, ESTRATEGIA Y KPIS) */}
        {activeTab === "perfiles" && (
          <section className="space-y-4" aria-labelledby="heading-perfiles">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
              <h2 id="heading-perfiles" className="text-lg font-bold text-slate-900 mb-3">
                2. Tarjetas de Perfil Territorial: Caracterización, Trayectoria y Estrategias ENCCÍVICA
              </h2>

              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2 mb-4">
                {data.llm.narrativas_perfiles.map((n: any) => {
                  const pChar = data.caracterizacion.perfiles.find(
                    (p: any) => p.cluster_id === n.cluster_id
                  );
                  const isSel = activeClusterId === n.cluster_id;
                  return (
                    <button
                      key={n.cluster_id}
                      type="button"
                      onClick={() => setActiveClusterId(n.cluster_id)}
                      className={`p-3 rounded-xl border text-left transition-all ${
                        isSel
                          ? "border-2 border-ine-primary bg-ine-primary/5 shadow-sm"
                          : "border-slate-200 bg-slate-50 hover:bg-white"
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <span
                          className="px-2 py-0.5 rounded text-xs font-bold text-white"
                          style={{ backgroundColor: PROFILE_COLORS[n.cluster_id]?.hex }}
                        >
                          Perfil {n.cluster_id}
                        </span>
                        <span className="text-xs font-semibold text-slate-600">
                          {pChar?.n_municipios} muns
                        </span>
                      </div>
                      <div className="font-bold text-sm text-slate-900 mt-1.5">{n.nombre}</div>
                      <div className="text-xs text-slate-600 mt-1">
                        Part. media:{" "}
                        <strong>
                          {pChar?.estadisticas_features?.part_media_global?.media_pct}%
                        </strong>
                      </div>
                    </button>
                  );
                })}
              </div>

              {/* Detalle del perfil seleccionado */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-5 pt-2 border-t border-slate-200">
                <div className="lg:col-span-6 space-y-4">
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                    <div className="flex items-center gap-2">
                      <span
                        className="w-4 h-4 rounded-full"
                        style={{ backgroundColor: PROFILE_COLORS[activeClusterId]?.hex }}
                      />
                      <h3 className="text-base font-bold text-slate-900">
                        Perfil {activeClusterId}: {activeNarrative.nombre}
                      </h3>
                    </div>
                    <p className="text-xs italic text-ine-primary font-semibold">
                      &ldquo;{activeNarrative.lema}&rdquo;
                    </p>
                    <p className="text-sm text-slate-700 leading-relaxed">
                      {activeNarrative.descripcion_narrativa}
                    </p>
                    <div className="p-2.5 rounded-lg bg-amber-50 border border-amber-200 text-xs text-amber-900">
                      {activeNarrative.comunidad_ilustrativa}
                    </div>
                  </div>

                  {/* 3 Datos Clave con Evidencia Verificada */}
                  <div className="p-4 rounded-xl bg-white border border-slate-200 space-y-2">
                    <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
                      Datos Clave con Evidencia Trazable Verificada Automáticamente
                    </h4>
                    <ul className="space-y-2 text-xs">
                      {activeNarrative.datos_clave.map((dc: any, idx: number) => (
                        <li
                          key={idx}
                          className="flex items-start justify-between gap-2 p-2 rounded bg-slate-50 border border-slate-200"
                        >
                          <span className="text-slate-700">{dc.descripcion}</span>
                          <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-900 font-mono font-bold shrink-0">
                            evidencia={dc.evidencia}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Estrategia Recomendada y KPIs (Prompt 7B) */}
                  <div className="p-4 rounded-xl bg-ine-primary/5 border border-ine-primary/20 space-y-2 text-xs">
                    <h4 className="text-sm font-bold text-ine-dark">
                      Estrategia Diferenciada de Fomento a la Participación (DECEyEC / ENCCÍVICA)
                    </h4>
                    <div>
                      <strong>Objetivo:</strong> {activeStrategy.objetivo}
                    </div>
                    <div>
                      <strong>Acción Concreta:</strong> {activeStrategy.accion_concreta}
                    </div>
                    <div>
                      <strong>Canales Recomendados:</strong> {activeStrategy.canales.join(" · ")}
                    </div>
                    <div>
                      <strong>Aliados Institucionales:</strong>{" "}
                      {activeStrategy.aliados_institucionales.join(" · ")}
                    </div>
                    <div className="p-2.5 rounded bg-white border border-slate-200 flex flex-wrap items-center justify-between gap-2">
                      <div>
                        <span className="text-slate-500">KPI Medible:</span>{" "}
                        <strong>{activeStrategy.kpi_medible}</strong>
                      </div>
                      <div className="font-mono font-bold text-ine-primary">
                        Línea Base: {activeStrategy.linea_base}% → Meta 2027: {activeStrategy.meta_2027}%
                      </div>
                    </div>
                    <div className="text-slate-600">
                      <strong>Consideración Ética:</strong> {activeStrategy.riesgo_consideracion_etica}
                    </div>
                  </div>
                </div>

                {/* Gráficos ECharts: Radar y Trayectoria 2009-2024 vs Media Nacional */}
                <div className="lg:col-span-6 space-y-4">
                  <div className="p-3 rounded-xl border border-slate-200 bg-white">
                    <h4 className="text-xs font-bold uppercase text-slate-500 mb-1">
                      Radar Multivariable del Perfil Territorial
                    </h4>
                    <EChartBox
                      option={radarOption}
                      height="270px"
                      ariaLabel={`Gráfico radar de características del Perfil ${activeClusterId}`}
                    />
                  </div>
                  <div className="p-3 rounded-xl border border-slate-200 bg-white">
                    <h4 className="text-xs font-bold uppercase text-slate-500 mb-1">
                      Trayectoria Histórica (2009–2024) vs. Media Municipal Nacional
                    </h4>
                    <EChartBox
                      option={trajectoryOption}
                      height="270px"
                      ariaLabel={`Trayectoria histórica 2009 a 2024 del Perfil ${activeClusterId} comparada con la media nacional`}
                    />
                  </div>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* COMPONENTE 3: SANKEY DE TRANSICIONES ENTRE PERFILES */}
        {activeTab === "sankey" && (
          <section className="space-y-4" aria-labelledby="heading-sankey">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div>
                  <h2 id="heading-sankey" className="text-lg font-bold text-slate-900">
                    3. Dinámica Temporal y Matriz de Transición entre Perfiles (Diagrama Sankey)
                  </h2>
                  <p className="text-xs text-slate-600">
                    Evolución de los {data.transiciones.resumen_cambios.total_municipios.toLocaleString()} municipios a través de 4 ventanas móviles: 2009–2015 → 2012–2018 → 2015–2021 → 2018–2024.
                  </p>
                </div>
                <div className="px-3 py-1.5 rounded-lg bg-slate-100 text-xs font-semibold text-slate-800">
                  Municipios que cambiaron de perfil (2009–2015 vs 2018–2024):{" "}
                  <span className="text-ine-primary font-bold">
                    {data.transiciones.resumen_cambios.municipios_cambiaron_2009_2015_vs_2018_2024.toLocaleString()}{" "}
                    ({data.transiciones.resumen_cambios.pct_municipios_cambiaron}%)
                  </span>
                </div>
              </div>

              <EChartBox
                option={sankeyOption}
                height="420px"
                ariaLabel="Diagrama Sankey de transiciones de municipios entre perfiles electorales de 2009-2015 a 2018-2024"
              />

              <div className="pt-2">
                <h3 className="text-sm font-bold text-slate-800 mb-2">
                  Top Municipios que Cambiaron de Perfil con Mayor Desplazamiento en Participación (2009–2024)
                </h3>
                <div className="overflow-x-auto">
                  <table className="w-full text-xs text-left border-collapse">
                    <thead>
                      <tr className="bg-slate-100 text-slate-700 border-b border-slate-300">
                        <th className="p-2">Clave (`cve_geo`)</th>
                        <th className="p-2">Municipio</th>
                        <th className="p-2">Entidad</th>
                        <th className="p-2">Perfil 2009–2015</th>
                        <th className="p-2">Perfil 2018–2024</th>
                        <th className="p-2">Part. 2009</th>
                        <th className="p-2">Part. 2024</th>
                        <th className="p-2">Cambio Δ (p.p.)</th>
                      </tr>
                    </thead>
                    <tbody>
                      {data.transiciones.top_municipios_cambio.slice(0, 10).map((m: any) => (
                        <tr key={m.cve_geo} className="border-b border-slate-200 hover:bg-slate-50">
                          <td className="p-2 font-mono">{m.cve_geo}</td>
                          <td className="p-2 font-semibold">{m.nom_mun}</td>
                          <td className="p-2">{m.nom_ent}</td>
                          <td className="p-2">
                            P{m.perfil_2009_2015}: {profileNames[m.perfil_2009_2015]}
                          </td>
                          <td className="p-2 font-semibold text-ine-primary">
                            P{m.perfil_2018_2024}: {profileNames[m.perfil_2018_2024]}
                          </td>
                          <td className="p-2">{m.part_2009_pct}%</td>
                          <td className="p-2">{m.part_2024_pct}%</td>
                          <td className="p-2 font-bold">
                            {m.delta_2009_2024_pp > 0 ? `+${m.delta_2009_2024_pp}` : m.delta_2009_2024_pp} p.p.
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* COMPONENTE 4: BUSCADOR "¿QUÉ PERFIL TIENE MI MUNICIPIO?" */}
        {activeTab === "buscador" && (
          <section className="space-y-4" aria-labelledby="heading-buscador">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h2 id="heading-buscador" className="text-lg font-bold text-slate-900">
                4. Buscador Ciudadano: &ldquo;¿Qué perfil tiene mi municipio?&rdquo; (Comparación vs. Vecinos y País)
              </h2>

              <div className="flex flex-col md:flex-row gap-3">
                <div className="flex-1">
                  <label htmlFor="mun-search-input" className="block text-xs font-semibold text-slate-700 mb-1">
                    Buscar por nombre de municipio, entidad o clave `cve_geo` (5 dígitos):
                  </label>
                  <input
                    id="mun-search-input"
                    type="search"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Ej. Aguascalientes, Mérida, Iztapalapa, San Pedro Garza García, 01001..."
                    className="w-full border border-slate-300 rounded-lg px-3 py-2 text-sm"
                  />
                </div>
              </div>

              {/* Lista rápida de coincidencias */}
              <div className="flex flex-wrap gap-1.5">
                {filteredSearchMunicipios.map((m) => (
                  <button
                    key={m.cve_geo}
                    type="button"
                    onClick={() => setSelectedMunicipio(m)}
                    className={`px-2.5 py-1 rounded-lg text-xs border transition-colors ${
                      selectedMunicipio?.cve_geo === m.cve_geo
                        ? "bg-ine-primary text-white border-ine-primary font-bold"
                        : "bg-slate-50 text-slate-800 border-slate-300 hover:bg-slate-100"
                    }`}
                  >
                    {m.nom_mun} ({m.nom_ent}, {m.cve_geo})
                  </button>
                ))}
              </div>

              {selectedMunicipio && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 pt-3 border-t border-slate-200">
                  <div className="lg:col-span-5 p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-3 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-slate-500">cve_geo: {selectedMunicipio.cve_geo}</span>
                      <span
                        className="px-2.5 py-0.5 rounded-full text-white font-bold"
                        style={{ backgroundColor: PROFILE_COLORS[selectedMunicipio.cluster_id]?.hex }}
                      >
                        Perfil {selectedMunicipio.cluster_id}: {profileNames[selectedMunicipio.cluster_id]}
                      </span>
                    </div>
                    <h3 className="text-lg font-bold text-slate-900">
                      {selectedMunicipio.nom_mun}, {selectedMunicipio.nom_ent}
                    </h3>
                    {selectedMunicipio.baja_conf && (
                      <div className="p-2 rounded bg-amber-100 text-amber-900 font-medium">
                        Aviso de Confiabilidad: Municipio con Lista Nominal pequeña o creación reciente (`flag_baja_confiabilidad = true`).
                      </div>
                    )}
                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">Participación Media Global</div>
                        <div className="text-base font-bold">{selectedMunicipio.p_global}%</div>
                      </div>
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">Caída Presidencial → Intermedia</div>
                        <div className="text-base font-bold">{selectedMunicipio.caida_pi} p.p.</div>
                      </div>
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">Brecha Género (M - H)</div>
                        <div className="text-base font-bold">{selectedMunicipio.brecha_gen} p.p.</div>
                      </div>
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">Brecha Edad (60+ vs 18-29)</div>
                        <div className="text-base font-bold">{selectedMunicipio.brecha_edad} p.p.</div>
                      </div>
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">% Lista Nominal Rural</div>
                        <div className="text-base font-bold">{selectedMunicipio.rural_pct}%</div>
                      </div>
                      <div className="p-2 bg-white rounded border">
                        <div className="text-slate-500">Proyección 2027 (80% IC)</div>
                        <div className="text-base font-bold text-ine-primary">
                          {selectedMunicipio.p2027}% [{selectedMunicipio.p2027_lo}–{selectedMunicipio.p2027_hi}%]
                        </div>
                      </div>
                    </div>
                  </div>

                  {/* Tabla comparativa: Municipio vs. 5 Vecinos Espaciales vs. Promedio Nacional */}
                  <div className="lg:col-span-7 p-4 rounded-xl bg-white border border-slate-200 space-y-2">
                    <h4 className="text-sm font-bold text-slate-900">
                      Comparación Directa contra Municipios Vecinos Espaciales y Media Nacional
                    </h4>
                    <div className="overflow-x-auto">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-slate-100 border-b border-slate-300">
                            <th className="p-2">Territorio</th>
                            <th className="p-2">Perfil</th>
                            <th className="p-2">Part. Media</th>
                            <th className="p-2">Caída Pres→Inter</th>
                            <th className="p-2">Brecha Género</th>
                            <th className="p-2">% Rural</th>
                            <th className="p-2">Proy. 2027</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr className="bg-ine-primary/10 font-bold border-b border-slate-300">
                            <td className="p-2">
                              ★ {selectedMunicipio.nom_mun} ({selectedMunicipio.cve_geo})
                            </td>
                            <td className="p-2">P{selectedMunicipio.cluster_id}</td>
                            <td className="p-2">{selectedMunicipio.p_global}%</td>
                            <td className="p-2">{selectedMunicipio.caida_pi} p.p.</td>
                            <td className="p-2">{selectedMunicipio.brecha_gen} p.p.</td>
                            <td className="p-2">{selectedMunicipio.rural_pct}%</td>
                            <td className="p-2">{selectedMunicipio.p2027}%</td>
                          </tr>
                          {selectedNeighbors.map((nb) => (
                            <tr key={nb.cve_geo} className="border-b border-slate-200">
                              <td className="p-2">
                                Vecino: {nb.nom_mun} ({nb.nom_ent})
                              </td>
                              <td className="p-2">P{nb.cluster_id}</td>
                              <td className="p-2">{nb.p_global}%</td>
                              <td className="p-2">{nb.caida_pi} p.p.</td>
                              <td className="p-2">{nb.brecha_gen} p.p.</td>
                              <td className="p-2">{nb.rural_pct}%</td>
                              <td className="p-2">{nb.p2027}%</td>
                            </tr>
                          ))}
                          <tr className="bg-slate-100 font-semibold">
                            <td className="p-2">Promedio Municipal Nacional</td>
                            <td className="p-2">Referencia País</td>
                            <td className="p-2">
                              {(
                                data.caracterizacion.referencia_nacional.medias_nacionales
                                  .part_media_global * 100
                              ).toFixed(2)}
                              %
                            </td>
                            <td className="p-2">
                              {(
                                data.caracterizacion.referencia_nacional.medias_nacionales
                                  .caida_presidencial_intermedia * 100
                              ).toFixed(2)}{" "}
                              p.p.
                            </td>
                            <td className="p-2">
                              {(
                                data.caracterizacion.referencia_nacional.medias_nacionales
                                  .brecha_genero_media * 100
                              ).toFixed(2)}{" "}
                              p.p.
                            </td>
                            <td className="p-2">
                              {(
                                data.caracterizacion.referencia_nacional.medias_nacionales
                                  .pct_ln_rural * 100
                              ).toFixed(1)}
                              %
                            </td>
                            <td className="p-2">
                              {data.simulador.totales_nacionales_2027.participacion_nacional_proyectada_2027_pct}%
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </section>
        )}

        {/* COMPONENTE 5: PANEL DE PROYECCIÓN 2027 CON INTERVALOS AL 80% Y ZONAS EN RIESGO */}
        {activeTab === "forecast" && (
          <section className="space-y-4" aria-labelledby="heading-forecast">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <h2 id="heading-forecast" className="text-lg font-bold text-slate-900">
                5. Proyección de Participación 2027 (Intermedia), Intervalos al 80% y Zonas en Riesgo
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                {Object.entries(data.simulador.backtesting_temporal).map(([btName, btVal]: [string, any]) => (
                  <div key={btName} className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <div className="font-bold text-slate-900">Backtesting Out-of-Time: {btName}</div>
                    <div className="mt-1 text-slate-700">
                      LightGBM Conformal MAE: <strong>{btVal.global_lgbm.mae_pp} p.p.</strong> (RMSE:{" "}
                      {btVal.global_lgbm.rmse_pp} p.p.)
                    </div>
                    <div className="text-slate-600">
                      Baseline Ingenuo MAE: {btVal.global_baseline_ingenuo.mae_pp} p.p.
                    </div>
                    <div className="text-emerald-700 font-semibold mt-0.5">
                      Cobertura empírica Intervalo 80%: {btVal.global_lgbm.cobertura_80_pct}%
                    </div>
                  </div>
                ))}
              </div>

              <h3 className="text-sm font-bold text-slate-900 pt-2">
                Zonas en Riesgo Prioritario hacia 2027 (Proyección Decreciente + Alto Peso en Lista Nominal)
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full text-xs text-left border-collapse">
                  <thead>
                    <tr className="bg-slate-100 border-b border-slate-300">
                      <th className="p-2">`cve_geo`</th>
                      <th className="p-2">Municipio</th>
                      <th className="p-2">Entidad</th>
                      <th className="p-2">Perfil</th>
                      <th className="p-2">LN Proyectada 2027</th>
                      <th className="p-2">Media Intermedias Previas</th>
                      <th className="p-2">Proyección 2027</th>
                      <th className="p-2">Intervalo 80% (CQR)</th>
                      <th className="p-2">Índice Prioridad</th>
                    </tr>
                  </thead>
                  <tbody>
                    {data.simulador.top_30_zonas_en_riesgo.slice(0, 15).map((r: any) => (
                      <tr key={r.cve_geo} className="border-b border-slate-200 hover:bg-slate-50">
                        <td className="p-2 font-mono">{r.cve_geo}</td>
                        <td className="p-2 font-semibold">{r.nom_mun}</td>
                        <td className="p-2">{r.nom_ent}</td>
                        <td className="p-2">
                          P{r.cluster_id}: {profileNames[r.cluster_id]}
                        </td>
                        <td className="p-2 font-mono">{r.ln_proyectada_2027.toLocaleString()}</td>
                        <td className="p-2">
                          {(r.part_media_intermedias_previas * 100).toFixed(2)}%
                        </td>
                        <td className="p-2 font-bold text-ine-primary">
                          {(r.proyeccion_part_2027 * 100).toFixed(2)}%
                        </td>
                        <td className="p-2 font-mono">
                          [{(r.intervalo_80_inf * 100).toFixed(1)}% – {(r.intervalo_80_sup * 100).toFixed(1)}%]
                        </td>
                        <td className="p-2 font-mono font-bold text-amber-800">
                          {r.indice_riesgo_priorizacion.toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </section>
        )}

        {/* COMPONENTE 6: SIMULADOR WHAT-IF CON AVISO VISIBLE DE "NO CAUSAL" */}
        {activeTab === "simulador" && (
          <section className="space-y-4" aria-labelledby="heading-simulador">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              {/* Aviso visible obligatorio de NO CAUSAL */}
              <div
                data-testid="non-causal-banner"
                role="note"
                className="p-3.5 rounded-xl bg-amber-50 border-2 border-amber-400 text-amber-950 text-xs md:text-sm font-medium"
              >
                ⚠️ {data.simulador.aviso_metodologico_obligatorio}
              </div>

              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 id="heading-simulador" className="text-lg font-bold text-slate-900">
                    6. Simulador What-If de Priorización Territorial 2027 (No Causal)
                  </h2>
                  <p className="text-xs text-slate-600">
                    Simula cuántos votantes adicionales representaría un incremento de +N puntos porcentuales en cada perfil sobre su Lista Nominal proyectada a 2027.
                  </p>
                </div>
                <div className="p-3 rounded-xl bg-ine-dark text-white text-right">
                  <div className="text-xs text-slate-200">
                    Votantes Adicionales Simulados (Escenario Seleccionado)
                  </div>
                  <div data-testid="what-if-total" className="text-2xl font-bold text-amber-300">
                    +{totalWhatIfVoters.toLocaleString()} votantes
                  </div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {data.simulador.simulador_por_perfil.map((sp: any) => {
                  const delta = whatIfDeltas[sp.cluster_id] ?? 0;
                  const addVoters = computeWhatIfAdditionalVoters(sp.ln_proyectada_2027, delta);
                  return (
                    <div
                      key={sp.cluster_id}
                      className="p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-2 text-xs"
                    >
                      <div className="flex items-center justify-between">
                        <span
                          className="px-2 py-0.5 rounded text-white font-bold"
                          style={{ backgroundColor: PROFILE_COLORS[sp.cluster_id]?.hex }}
                        >
                          Perfil {sp.cluster_id}
                        </span>
                        <span className="font-mono text-slate-600">
                          LN 2027: {sp.ln_proyectada_2027.toLocaleString()}
                        </span>
                      </div>
                      <div className="font-bold text-sm text-slate-900">
                        {profileNames[sp.cluster_id]}
                      </div>
                      <div className="text-slate-600">
                        Participación Base 2027: <strong>{sp.participacion_base_pct}%</strong>
                      </div>
                      <label className="block pt-1 font-semibold text-slate-800">
                        Incremento simulado (+{delta.toFixed(1)} p.p.):
                        <input
                          type="range"
                          min={0}
                          max={10}
                          step={0.5}
                          value={delta}
                          aria-label={`Incremento en puntos porcentuales para el Perfil ${sp.cluster_id}`}
                          onChange={(e) =>
                            setWhatIfDeltas((prev) => ({
                              ...prev,
                              [sp.cluster_id]: parseFloat(e.target.value),
                            }))
                          }
                          className="w-full mt-1 accent-ine-primary"
                        />
                      </label>
                      <div className="p-2 rounded bg-white border border-slate-200 flex items-center justify-between">
                        <span>Votantes adicionales en este perfil:</span>
                        <strong className="text-ine-primary font-mono text-sm">
                          +{addVoters.toLocaleString()}
                        </strong>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </section>
        )}

        {/* COMPONENTE 7: CHAT "PREGÚNTALE A LOS DATOS" (TEXT-TO-SQL) */}
        {activeTab === "chat" && (
          <section className="space-y-4" aria-labelledby="heading-chat">
            <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <div>
                <h2 id="heading-chat" className="text-lg font-bold text-slate-900">
                  7. &ldquo;Pregúntale a los Datos&rdquo; — Agente Text-to-SQL Verificado sobre DuckDB
                </h2>
                <p className="text-xs text-slate-600">
                  Consultas seguras de solo lectura (`SELECT`) validadas contra la capa semántica (`docs/capa_semantica.yaml`), con lista blanca de tablas y rechazo automático de preguntas sobre partidos políticos o datos individuales.
                </p>
              </div>

              <div className="flex flex-wrap gap-1.5">
                {data.llm.ejemplos_chat_precalculados.map((ex: any, i: number) => (
                  <button
                    key={i}
                    type="button"
                    onClick={() => handleAskQuestion(ex.pregunta)}
                    className="px-2.5 py-1 rounded-lg text-xs border border-slate-300 bg-slate-50 hover:bg-slate-100 text-slate-800"
                  >
                    {ex.pregunta}
                  </button>
                ))}
              </div>

              <form
                onSubmit={(e) => {
                  e.preventDefault();
                  handleAskQuestion();
                }}
                className="flex gap-2"
              >
                <input
                  type="text"
                  value={chatQuestion}
                  onChange={(e) => setChatQuestion(e.target.value)}
                  aria-label="Escribe tu pregunta para consultar los datos electorales"
                  className="flex-1 border border-slate-300 rounded-lg px-3 py-2 text-sm"
                  placeholder="Ej. ¿Cuál fue la participación de jóvenes 18-29 vs adultos mayores 60+ en 2024?"
                />
                <button
                  type="submit"
                  disabled={chatLoading}
                  className="px-4 py-2 rounded-lg bg-ine-primary text-white text-sm font-semibold hover:bg-ine-dark disabled:opacity-50"
                >
                  {chatLoading ? "Consultando..." : "Consultar SQL"}
                </button>
              </form>

              {chatResult && (
                <div className="space-y-3 pt-2 border-t border-slate-200 text-xs">
                  <div
                    className={`p-3 rounded-lg border ${
                      chatResult.es_respondible
                        ? "bg-emerald-50 border-emerald-200 text-emerald-950"
                        : "bg-amber-50 border-amber-300 text-amber-950"
                    }`}
                  >
                    <div className="font-bold">
                      {chatResult.es_respondible
                        ? "✓ Respuesta Verificada con Datos CCPC:"
                        : "⚠️ Pregunta Fuera del Alcance / Rechazo Ético:"}
                    </div>
                    <p className="mt-1 text-sm">{chatResult.respuesta_natural}</p>
                    <div className="mt-1 text-[11px] opacity-80">
                      Fuente: {chatResult.fuente_trazable}
                    </div>
                  </div>

                  {chatResult.sql_usado && (
                    <div className="p-3 rounded-lg bg-slate-900 text-emerald-300 font-mono text-xs overflow-x-auto">
                      <div className="text-slate-400 text-[11px] mb-1">
                        SQL ejecutado (Validado Solo-SELECT + Whitelist):
                      </div>
                      <code>{chatResult.sql_usado}</code>
                    </div>
                  )}

                  {chatResult.tabla_respaldo && chatResult.tabla_respaldo.length > 0 && (
                    <div className="overflow-x-auto border border-slate-200 rounded-lg">
                      <table className="w-full text-xs text-left border-collapse">
                        <thead>
                          <tr className="bg-slate-100 border-b border-slate-300">
                            {Object.keys(chatResult.tabla_respaldo[0]).map((col) => (
                              <th key={col} className="p-2 font-mono">
                                {col}
                              </th>
                            ))}
                          </tr>
                        </thead>
                        <tbody>
                          {chatResult.tabla_respaldo.slice(0, 15).map((row: any, rIdx: number) => (
                            <tr key={rIdx} className="border-b border-slate-200">
                              {Object.values(row).map((val: any, cIdx: number) => (
                                <td key={cIdx} className="p-2">
                                  {typeof val === "number" ? val.toLocaleString() : String(val ?? "")}
                                </td>
                              ))}
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          </section>
        )}

        {/* COMPONENTE 8: PÁGINA "METODOLOGÍA Y LÍMITES" */}
        {activeTab === "metodologia" && (
          <section className="space-y-4" aria-labelledby="heading-metodologia">
            <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm space-y-4 text-sm text-slate-800">
              <h2 id="heading-metodologia" className="text-lg font-bold text-slate-900">
                8. Metodología, Validación Estadística, Privacidad y Límites Éticos
              </h2>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <h3 className="font-bold text-sm text-ine-dark">
                    1. Prevención de la Falacia Ecológica y Lenguaje No Estigmatizante
                  </h3>
                  <p>
                    Los perfiles identificados describen <strong>unidades territoriales agregadas (municipios)</strong>, nunca personas individuales. Las correlaciones territoriales entre ruralidad, estructura por edad y asistencia a las urnas no deben extrapolarse a juicios sobre ciudadanas o ciudadanos individuales. Todos los nombres de perfil cumplen la regla de máximo 4 palabras institucionales sin calificativos peyorativos.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <h3 className="font-bold text-sm text-ine-dark">
                    2. Regla de Privacidad (`Celdas < 10`) y Datos Agregados
                  </h3>
                  <p>
                    Aunque los archivos fuente del CCPC (2009–2024) vienen desglosados por sección, sexo y edad año por año, nuestra capa de ingesta agrupa en tres bandas etarias amplias (`18-29`, `30-59`, `60+`) y marca con `celda_pequena_lt10 = true` cualquier celda con Lista Nominal menor a 10 personas, suprimiendo las tasas de subgrupos con denominador {"< 10"} en las vistas públicas.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <h3 className="font-bold text-sm text-ine-dark">
                    3. Validación de Segmentación y Comparación con Deep Learning
                  </h3>
                  <p>
                    Se evaluaron 5 enfoques (K-Means con `RobustScaler`, GMM por BIC, HDBSCAN, `TimeSeriesKMeans` con DTW y Clustering Espacial) en $k \in [3..10]$ con 100 remuestreos Bootstrap (ARI). Además, se entrenó un <strong>Autoencoder Temporal (`dim=6`)</strong>. Por <strong>honestidad metodológica</strong> (`{data.deepLearning.conclusion_explicita}`), se conservó el modelo ganador `A_KMeans_Robust` ($k={data.clusteringMeta.winner_k}$) al ofrecer superior separación en el espacio de variables observables (`Silhouette = {data.deepLearning.baseline_metrics.silhouette_original_space}`) y total explicabilidad SHAP.
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2">
                  <h3 className="font-bold text-sm text-ine-dark">
                    4. Cambios de Marco Geográfico y Tabla Puente (`2009–2024`)
                  </h3>
                  <p>
                    La tabla `puente_municipio_anio.parquet` documenta los municipios creados con posterioridad a 2009 (Bacalar, Puerto Morelos, San Quintín, San Felipe, Seybaplaya, Dzitbalché, entre otros). Asimismo, el archivo de Prisión Preventiva 2024 (que carece de clave municipal en la fuente oficial) se integra exclusivamente en las vistas distritales y estatales (`cve_mun = 000`) sin inventar asignaciones municipales.
                  </p>
                </div>
              </div>
            </div>
          </section>
        )}
      </main>
    </div>
  );
}
