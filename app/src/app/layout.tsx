import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "INE | Perfiles Territoriales de Participación Electoral 2009–2024 (Reto 1)",
  description:
    "Plataforma de análisis territorial, explicabilidad SHAP, proyección 2027 y estrategias cívicas diferenciadas basada en los Conteos Censales de Participación Ciudadana (CCPC 2009-2024) del INE.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="es">
      <body className="min-h-screen bg-slate-50 text-slate-900 antialiased">
        {children}
      </body>
    </html>
  );
}
