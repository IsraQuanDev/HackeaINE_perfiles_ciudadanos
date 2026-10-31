import { test, expect } from "@playwright/test";

test.describe("Dashboard INE Perfiles Territoriales E2E Flow", () => {
  test("renders all 8 institutional sections without console errors and captures screenshots", async ({
    page,
  }) => {
    const consoleErrors: string[] = [];
    page.on("console", (msg) => {
      if (msg.type() === "error") {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto("/");

    // Verificar encabezado institucional y advertencia de falacia ecológica
    await expect(
      page.getByRole("heading", {
        name: /Perfiles Territoriales de Participación Electoral/i,
      })
    ).toBeVisible({ timeout: 15000 });
    await expect(page.getByText(/Falacia Ecológica/i)).toBeVisible();

    // 1. Mapa Coroplético
    await expect(
      page.getByRole("heading", { name: /1\. Mapa Coroplético de Perfiles Territoriales/i })
    ).toBeVisible();

    // 2. Tarjetas de Perfil
    await page.getByRole("button", { name: /2\. Tarjetas de Perfil/i }).click();
    await expect(
      page.getByRole("heading", { name: /2\. Tarjetas de Perfil Territorial/i })
    ).toBeVisible();

    // 3. Diagrama Sankey
    await page.getByRole("button", { name: /3\. Dinámica y Transiciones/i }).click();
    await expect(
      page.getByRole("heading", { name: /3\. Dinámica Temporal y Matriz de Transición/i })
    ).toBeVisible();

    // 4. Buscador Municipal
    await page.getByRole("button", { name: /4\. ¿Qué perfil tiene mi municipio\?/i }).click();
    await expect(
      page.getByRole("heading", { name: /4\. Buscador Ciudadano/i })
    ).toBeVisible();

    // 5. Proyección 2027
    await page.getByRole("button", { name: /5\. Proyección 2027/i }).click();
    await expect(
      page.getByRole("heading", { name: /5\. Proyección de Participación 2027/i })
    ).toBeVisible();

    // 6. Simulador What-If (No Causal)
    await page.getByRole("button", { name: /6\. Simulador What-If/i }).click();
    await expect(page.getByTestId("non-causal-banner")).toContainText(/NO CAUSAL/i);

    // 7. Chat Pregúntale a los Datos
    await page.getByRole("button", { name: /7\. Pregúntale a los Datos/i }).click();
    await expect(
      page.getByRole("heading", { name: /7\. “Pregúntale a los Datos”/i })
    ).toBeVisible();

    // 8. Metodología y Límites
    await page.getByRole("button", { name: /8\. Metodología y Límites/i }).click();
    await expect(
      page.getByRole("heading", { name: /8\. Metodología, Validación Estadística/i })
    ).toBeVisible();

    expect(consoleErrors).toEqual([]);
  });
});
