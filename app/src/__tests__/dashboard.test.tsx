import React from "react";
import { describe, it, expect } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import {
  PROFILE_COLORS,
  computeWhatIfAdditionalVoters,
  findSpatialNeighbors,
  MunicipioRecord,
} from "@/lib/palette";

const mockMunicipios: MunicipioRecord[] = [
  {
    cve_geo: "01001",
    cve_ent: "01",
    nom_ent: "AGUASCALIENTES",
    cve_mun: "001",
    nom_mun: "Aguascalientes",
    def: "3",
    cluster_id: 0,
    prob: 0.92,
    lat: 21.88,
    lon: -102.29,
    p2009: 52.1,
    p2012: 63.4,
    p2015: 48.9,
    p2018: 61.2,
    p2021: 50.4,
    p2024: 62.8,
    p_global: 56.47,
    p_pres: 62.47,
    p_inter: 50.47,
    caida_pi: 12.0,
    pendiente: 0.85,
    volatilidad: 6.2,
    constancia: 66.7,
    brecha_gen: 4.5,
    brecha_edad: 18.2,
    p_joven: 48.1,
    p_60mas: 66.3,
    rural_pct: 12.4,
    urbana_pct: 84.1,
    ln_2024: 710000,
    va_2024: 185,
    va_tasa_10k: 2.6,
    baja_conf: false,
    lisa: "HH (Alto-Alto)",
    w_09_15: 1,
    w_12_18: 1,
    w_15_21: 0,
    w_18_24: 0,
    cambio_w: true,
    ln_2027: 735000,
    p2027: 51.2,
    p2027_lo: 45.1,
    p2027_hi: 57.3,
    riesgo_2027: false,
    idx_riesgo: 4200,
  },
  {
    cve_geo: "01005",
    cve_ent: "01",
    nom_ent: "AGUASCALIENTES",
    cve_mun: "005",
    nom_mun: "Jesús María",
    def: "1",
    cluster_id: 2,
    prob: 0.88,
    lat: 21.96,
    lon: -102.34,
    p2009: 51.0,
    p2012: 64.0,
    p2015: 49.0,
    p2018: 63.0,
    p2021: 52.0,
    p2024: 64.5,
    p_global: 57.25,
    p_pres: 63.83,
    p_inter: 50.67,
    caida_pi: 13.16,
    pendiente: 1.1,
    volatilidad: 6.8,
    constancia: 83.3,
    brecha_gen: 5.1,
    brecha_edad: 17.5,
    p_joven: 49.2,
    p_60mas: 66.7,
    rural_pct: 22.0,
    urbana_pct: 70.0,
    ln_2024: 98000,
    va_2024: 24,
    va_tasa_10k: 2.4,
    baja_conf: false,
    lisa: "HH (Alto-Alto)",
    w_09_15: 2,
    w_12_18: 2,
    w_15_21: 2,
    w_18_24: 2,
    cambio_w: false,
    ln_2027: 103000,
    p2027: 52.4,
    p2027_lo: 46.0,
    p2027_hi: 58.8,
    riesgo_2027: false,
    idx_riesgo: 1100,
  },
];

describe("Dashboard Core Utilities & Accessibility Palette", () => {
  it("calculates exact non-causal What-If additional voters from projected 2027 Lista Nominal", () => {
    expect(computeWhatIfAdditionalVoters(1000000, 2.5)).toBe(25000);
    expect(computeWhatIfAdditionalVoters(735000, 1.0)).toBe(7350);
  });

  it("finds closest spatial neighbors excluding the target municipality itself", () => {
    const neighbors = findSpatialNeighbors(mockMunicipios[0], mockMunicipios, 5);
    expect(neighbors).toHaveLength(1);
    expect(neighbors[0].cve_geo).toBe("01005");
  });

  it("provides Okabe-Ito colorblind-safe colors for all 6 profiles", () => {
    for (let i = 0; i < 6; i++) {
      expect(PROFILE_COLORS[i]).toBeDefined();
      expect(PROFILE_COLORS[i].hex).toMatch(/^#[0-9A-Fa-f]{6}$/);
    }
  });
});
