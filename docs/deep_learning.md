# Evaluación Condicional de Deep Learning: Autoencoder Temporal (`docs/deep_learning.md`)

## 1. Diseño del Experimento (Principio Inquebrantable #5: Honestidad Metodológica)

- **Arquitectura:** `Neural Autoencoder CPU (Arquitectura 16-6-16, tanh, seed=42)` con cuello de botella de dimensión latente `dim = 6`.
- **Error cuadrático medio de reconstrucción (MSE):** `0.091679`.
- **Concordancia con el modelo ganador de la Fase 3 (`ARI vs. Baseline`):** `0.3526`.

## 2. Tabla Comparativa Directa contra el Modelo Ganador (Fase 3)

| Métrica / Criterio | Ganador Fase 3 (`A_KMeans_Robust`) | Autoencoder Temporal + K-Means (`dim=6`) |
| :--- | :---: | :---: |
| **Silhouette (espacio de variables originales $\uparrow$)** | **`0.1341`** | `0.1010` (latente: `0.1676`) |
| **Davies-Bouldin (espacio original $\downarrow$)** | **`1.7826`** | `2.2699` |
| **Calinski-Harabasz (espacio original $\uparrow$)** | **`286.0`** | `206.4` |
| **Estabilidad Bootstrap ($n=100$, ARI $\uparrow$)** | `0.6535` | `0.5401` |
| **Tamaño mínimo de cluster ($\ge 3\%$)** | `3.19%` | `3.55%` |
| **Interpretabilidad para política pública cívica** | **ALTA (variables originales directas + reglas de árbol + SHAP exacto)** | MEDIA-BAJA (dimensiones latentes no lineales acopladas) |

## 3. Conclusión Explícita

**Veredicto:** **`NO MEJORA (SE CONSERVA EL BASELINE)`**.

- Si bien el Autoencoder Temporal comprime adecuadamente las trayectorias en el espacio latente (`MSE = 0.09168`) y presenta concordancia estructural con la partición base (`ARI = 0.3526`), **no supera al modelo ganador de la Fase 3 en separación dentro del espacio de variables observables** (`Silhouette 0.1010 vs. 0.1341`) y añade opacidad al mezclar no linealmente las tasas de participación y brechas sociodemográficas.
- Siguiendo el **Principio Inquebrantable #5 (Honestidad metodológica)** y las instrucciones del **Prompt 6**, **conservamos el modelo `A_KMeans_Robust` de la Fase 3 como modelo final de producción**.
