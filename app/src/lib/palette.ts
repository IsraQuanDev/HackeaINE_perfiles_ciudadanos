// Paleta Okabe-Ito / Colorbrewer apta para daltonismo y con contraste WCAG AA
export const PROFILE_COLORS: Record<number, { hex: string; bg: string; text: string; border: string }> = {
  0: { hex: "#0072B2", bg: "bg-[#0072B2]/10", text: "text-[#0072B2]", border: "border-[#0072B2]" }, // Azul oscuro
  1: { hex: "#009E73", bg: "bg-[#009E73]/10", text: "text-[#009E73]", border: "border-[#009E73]" }, // Verde azulado
  2: { hex: "#56B4E9", bg: "bg-[#56B4E9]/15", text: "text-[#0369A1]", border: "border-[#0284C7]" }, // Azul cielo
  3: { hex: "#E69F00", bg: "bg-[#E69F00]/15", text: "text-[#B45309]", border: "border-[#D97706]" }, // Ámbar / Naranja
  4: { hex: "#CC79A7", bg: "bg-[#CC79A7]/15", text: "text-[#9D174D]", border: "border-[#BE185D]" }, // Magenta suave
  5: { hex: "#D55E00", bg: "bg-[#D55E00]/15", text: "text-[#B91C1C]", border: "border-[#DC2626]" }, // Bermellón
};

export interface MunicipioRecord {
  cve_geo: string;
  cve_ent: string;
  nom_ent: string;
  cve_mun: string;
  nom_mun: string;
  def: string;
  cluster_id: number;
  prob: number;
  lat: number;
  lon: number;
  p2009: number;
  p2012: number;
  p2015: number;
  p2018: number;
  p2021: number;
  p2024: number;
  p_global: number;
  p_pres: number;
  p_inter: number;
  caida_pi: number;
  pendiente: number;
  volatilidad: number;
  constancia: number;
  brecha_gen: number;
  brecha_edad: number;
  p_joven: number;
  p_60mas: number;
  rural_pct: number;
  urbana_pct: number;
  ln_2024: number;
  va_2024: number;
  va_tasa_10k: number;
  baja_conf: boolean;
  lisa: string;
  w_09_15: number;
  w_12_18: number;
  w_15_21: number;
  w_18_24: number;
  cambio_w: boolean;
  ln_2027: number;
  p2027: number;
  p2027_lo: number;
  p2027_hi: number;
  riesgo_2027: boolean;
  idx_riesgo: number;
}

export function computeWhatIfAdditionalVoters(lnProyectada2027: number, deltaPoints: number): number {
  return Math.round(lnProyectada2027 * (deltaPoints / 100.0));
}

export function findSpatialNeighbors(
  target: MunicipioRecord,
  allMunicipios: MunicipioRecord[],
  k = 5
): MunicipioRecord[] {
  return allMunicipios
    .filter((m) => m.cve_geo !== target.cve_geo)
    .map((m) => ({
      mun: m,
      dist: Math.hypot(m.lat - target.lat, m.lon - target.lon) + (m.cve_ent === target.cve_ent ? 0 : 2.5),
    }))
    .sort((a, b) => a.dist - b.dist)
    .slice(0, k)
    .map((item) => item.mun);
}
