"use client";

import React, { useEffect, useMemo, useRef, useState } from "react";
import maplibregl from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { MunicipioRecord, PROFILE_COLORS } from "@/lib/palette";

interface MapProps {
  municipios: MunicipioRecord[];
  profileNames: Record<number, string>;
  selectedPeriod: string;
  selectedEntidad: string;
  selectedProfile: string;
  vistaNivel: "municipio" | "distrito" | "entidad";
  onSelectMunicipio: (m: MunicipioRecord) => void;
}

export default function MapLibreTerritorial({
  municipios,
  profileNames,
  selectedPeriod,
  selectedEntidad,
  selectedProfile,
  vistaNivel,
  onSelectMunicipio,
}: MapProps) {
  const mapContainerRef = useRef<HTMLDivElement | null>(null);
  const mapInstanceRef = useRef<maplibregl.Map | null>(null);
  const [hoveredMun, setHoveredMun] = useState<MunicipioRecord | null>(null);

  const filtered = useMemo(() => {
    return municipios.filter((m) => {
      if (selectedEntidad !== "TODAS" && m.nom_ent !== selectedEntidad) return false;
      const cid =
        selectedPeriod === "2009-2015"
          ? m.w_09_15
          : selectedPeriod === "2012-2018"
          ? m.w_12_18
          : selectedPeriod === "2015-2021"
          ? m.w_15_21
          : selectedPeriod === "2018-2024"
          ? m.w_18_24
          : m.cluster_id;
      if (selectedProfile !== "TODOS" && String(cid) !== selectedProfile) return false;
      return true;
    });
  }, [municipios, selectedEntidad, selectedProfile, selectedPeriod]);

  useEffect(() => {
    if (!mapContainerRef.current) return;
    let map: maplibregl.Map | null = null;
    try {
      map = new maplibregl.Map({
        container: mapContainerRef.current,
        style: {
          version: 8,
          sources: {},
          layers: [
            {
              id: "background",
              type: "background",
              paint: { "background-color": "#0F172A" },
            },
          ],
        },
        center: [-102.0, 23.5],
        zoom: 4.3,
        attributionControl: false,
      });

      map.on("load", () => {
        if (!map) return;
        const features = filtered.map((m) => {
          const activeCid =
            selectedPeriod === "2009-2015"
              ? m.w_09_15
              : selectedPeriod === "2012-2018"
              ? m.w_12_18
              : selectedPeriod === "2015-2021"
              ? m.w_15_21
              : selectedPeriod === "2018-2024"
              ? m.w_18_24
              : m.cluster_id;
          return {
            type: "Feature" as const,
            geometry: {
              type: "Point" as const,
              coordinates: [m.lon, m.lat],
            },
            properties: {
              cve_geo: m.cve_geo,
              nom_mun: m.nom_mun,
              nom_ent: m.nom_ent,
              cluster_id: activeCid,
              color: PROFILE_COLORS[activeCid]?.hex ?? "#0072B2",
              p_global: m.p_global,
              ln_2024: m.ln_2024,
            },
          };
        });

        map.addSource("municipios-src", {
          type: "geojson",
          data: { type: "FeatureCollection", features },
        });

        map.addLayer({
          id: "municipios-circles",
          type: "circle",
          source: "municipios-src",
          paint: {
            "circle-radius": vistaNivel === "entidad" ? 9 : vistaNivel === "distrito" ? 6.5 : 4.5,
            "circle-color": ["get", "color"],
            "circle-opacity": 0.88,
            "circle-stroke-width": 0.8,
            "circle-stroke-color": "#ffffff",
          },
        });
      });

      mapInstanceRef.current = map;
    } catch {
      // Fallback limpio en entornos sin WebGL (ej. JSDOM / headless CI)
    }

    return () => {
      if (map) {
        map.remove();
      }
      mapInstanceRef.current = null;
    };
  }, [filtered, selectedPeriod, vistaNivel]);

  // Proyección SVG interactiva sincronizada con el contenedor MapLibre para garantizar
  // accesibilidad por teclado (WCAG AA) y tooltips inmediatos tanto con WebGL como en modo ligero
  const svgPoints = useMemo(() => {
    return filtered.slice(0, 2500).map((m) => {
      const x = ((m.lon - -118.0) / (-86.0 - -118.0)) * 760 + 20;
      const y = ((33.0 - m.lat) / (33.0 - 14.0)) * 410 + 15;
      const activeCid =
        selectedPeriod === "2009-2015"
          ? m.w_09_15
          : selectedPeriod === "2012-2018"
          ? m.w_12_18
          : selectedPeriod === "2015-2021"
          ? m.w_15_21
          : selectedPeriod === "2018-2024"
          ? m.w_18_24
          : m.cluster_id;
      const periodRate =
        selectedPeriod === "2009"
          ? m.p2009
          : selectedPeriod === "2012"
          ? m.p2012
          : selectedPeriod === "2015"
          ? m.p2015
          : selectedPeriod === "2018"
          ? m.p2018
          : selectedPeriod === "2021"
          ? m.p2021
          : selectedPeriod === "2024"
          ? m.p2024
          : m.p_global;
      return { m, x, y, activeCid, periodRate, color: PROFILE_COLORS[activeCid]?.hex ?? "#0072B2" };
    });
  }, [filtered, selectedPeriod]);

  return (
    <div className="relative rounded-xl overflow-hidden border border-slate-300 bg-slate-900 text-white shadow-sm">
      {/* Contenedor MapLibre GL */}
      <div ref={mapContainerRef} className="absolute inset-0 opacity-30 pointer-events-none" />

      {/* Capa cartográfica interactiva y navegable por teclado (WCAG AA) */}
      <div className="relative z-10 p-3">
        <div className="flex flex-wrap items-center justify-between gap-2 mb-2 text-xs text-slate-300">
          <span>
            Vista activa: <strong className="text-white uppercase">{vistaNivel}</strong> | Corte:{" "}
            <strong className="text-white">{selectedPeriod}</strong> | Territorios mostrados:{" "}
            <strong className="text-white">{filtered.length.toLocaleString()}</strong>
          </span>
          <span className="text-amber-300 font-medium">
            Haz clic o usa Tab/Enter sobre un territorio para inspeccionar su ficha y vecinos
          </span>
        </div>

        <svg
          viewBox="0 0 800 440"
          className="w-full h-[380px] bg-slate-950/80 rounded-lg border border-slate-800"
          role="region"
          aria-label="Mapa coroplético interactivo de perfiles territoriales de participación electoral"
        >
          {svgPoints.map(({ m, x, y, activeCid, color }) => (
            <circle
              key={m.cve_geo}
              cx={x}
              cy={y}
              r={vistaNivel === "entidad" ? 5.5 : vistaNivel === "distrito" ? 4.0 : 2.8}
              fill={color}
              stroke="#0f172a"
              strokeWidth={0.5}
              tabIndex={0}
              role="button"
              aria-label={`${m.nom_mun}, ${m.nom_ent}: Perfil ${activeCid} (${profileNames[activeCid] ?? ""}), participación media ${m.p_global}%`}
              className="cursor-pointer transition-transform hover:scale-150 focus:scale-150"
              onMouseEnter={() => setHoveredMun(m)}
              onFocus={() => setHoveredMun(m)}
              onClick={() => onSelectMunicipio(m)}
              onKeyDown={(e) => {
                if (e.key === "Enter" || e.key === " ") {
                  e.preventDefault();
                  onSelectMunicipio(m);
                }
              }}
            />
          ))}
        </svg>

        {/* Tooltip flotante con métricas clave */}
        {hoveredMun && (
          <div
            data-testid="map-tooltip"
            className="mt-2 p-3 rounded-lg bg-slate-800/95 border border-slate-600 text-xs grid grid-cols-2 sm:grid-cols-4 gap-3"
          >
            <div>
              <div className="text-slate-400">Municipio (`cve_geo`)</div>
              <div className="font-bold text-white text-sm">
                {hoveredMun.nom_mun} ({hoveredMun.cve_geo})
              </div>
              <div className="text-slate-300">{hoveredMun.nom_ent} · Distrito {hoveredMun.def}</div>
            </div>
            <div>
              <div className="text-slate-400">Perfil Asignado</div>
              <div className="font-bold text-amber-300">
                Perfil {hoveredMun.cluster_id}: {profileNames[hoveredMun.cluster_id]}
              </div>
              <div className="text-slate-300">
                Prob. pertenencia: {(hoveredMun.prob * 100).toFixed(1)}% | LISA: {hoveredMun.lisa}
              </div>
            </div>
            <div>
              <div className="text-slate-400">Participación Histórica</div>
              <div className="font-bold text-white">
                Media: {hoveredMun.p_global}% (2024: {hoveredMun.p2024}%)
              </div>
              <div className="text-slate-300">
                Caída Pres→Inter: {hoveredMun.caida_pi} p.p. | Pendiente: {hoveredMun.pendiente} p.p.
              </div>
            </div>
            <div>
              <div className="text-slate-400">Padrón y Proyección 2027</div>
              <div className="font-bold text-emerald-300">
                Proy. 2027: {hoveredMun.p2027}% [{hoveredMun.p2027_lo}% – {hoveredMun.p2027_hi}%]
              </div>
              <div className="text-slate-300">
                LN 2024: {hoveredMun.ln_2024.toLocaleString()} | Rural: {hoveredMun.rural_pct}%
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
