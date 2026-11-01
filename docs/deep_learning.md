# Evaluación Condicional de Deep Learning: Autoencoder Temporal (`docs/deep_learning.md`)

## 1. Diseño del Experimento (Principio Inquebrantable #5: Honestidad Metodológica)

- **Arquitectura:** `Neural Autoencoder CPU (Arquitectura 16-6-16, tanh, seed=42)` con cuello de botella de dimensión latente `dim = 6`.
- **Error cuadrático medio de reconstrucción (MSE):** `0.077975`.
- **Concordancia con el modelo ganador de la Fase 3 (`ARI vs. Baseline`):** `0.3989`.

## 2. Tabla Comparativa Directa contra el Modelo Ganador (Fase 3)

| Métrica / Criterio | Ganador Fase 3 (`A_KMeans_Robust`) | Autoencoder Temporal + K-Means (`dim=6`) |
| :--- | :---: | :---: |
| **Silhouette (espacio de variables originales $\uparrow$)** | **`0.1705`** | `0.1187` (latente: `0.1941`) |
| **Davies-Bouldin (espacio original $\downarrow$)** | **`1.5907`** | `2.0080` |
| **Calinski-Harabasz (espacio original $\uparrow$)** | **`393.3`** | `318.2` |
| **Estabilidad Bootstrap ($n=100$, ARI $\uparrow$)** | `0.7808` | `0.8047` |
| **Tamaño mínimo de cluster ($\ge 3\%$)** | `4.48%` | `4.52%` |
| **Interpretabilidad para política pública cívica** | **ALTA (variables originales directas + reglas de árbol + SHAP exacto)** | MEDIA-BAJA (dimensiones latentes no lineales acopladas) |

## 3. Conclusión Explícita

**Veredicto:** **`NO MEJORA (SE CONSERVA EL BASELINE)`**.

- Si bien el Autoencoder Temporal comprime adecuadamente las trayectorias en el espacio latente (`MSE = 0.07798`) y presenta concordancia estructural con la partición base (`ARI = 0.3989`), **no supera al modelo ganador de la Fase 3 en separación dentro del espacio de variables observables** (`Silhouette 0.1187 vs. 0.1705`) y añade opacidad al mezclar no linealmente las tasas de participación y brechas sociodemográficas.
- Siguiendo el **Principio Inquebrantable #5 (Honestidad metodológica)** y las instrucciones del **Prompt 6**, **conservamos el modelo `A_KMeans_Robust` de la Fase 3 como modelo final de producción**.
