# Capa LLM: Narrativas Verificadas, Estrategias Cívicas y Chat con los Datos (`docs/capa_llm.md`)

## 1. Nombrado y Narrativa de Perfiles Territoriales (Tarea 7A)

Cada perfil fue generado exclusivamente a partir de `data/processed/perfiles_caracterizacion.json` y validado con el **verificador automático de cifras (`verify_narrative_grounding`)** y esquemas `Pydantic` (`80-120` palabras por narrativa, `<= 4` palabras por nombre).

### Perfil 0: Cohesión Comunitaria Sostenida
- **Lema:** *Territorios de alta participación constante en elecciones presidenciales e intermedias*
- **Narrativa (107 palabras):** El perfil territorial 0, denominado Cohesión Comunitaria Sostenida, agrupa 539 municipios del país con una lista nominal acumulada en 2024 de 8,089,025 personas inscritas, teniendo presencia destacada en entidades como JALISCO. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 67.76% y una diferencia promedio entre elecciones presidenciales e intermedias de 4.04 puntos porcentuales, con una pendiente temporal de 0.03 puntos por ciclo electoral. Su composición territorial presenta 34.87% de lista nominal en secciones rurales, una participación juvenil media de 62.28% frente a 69.85% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 7.91 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a GÃ³mez FarÃ­as (TAMAULIPAS), donde el padrón presenta 34.87% de secciones rurales y una participación histórica media de 67.76%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`67.76`** — Participación media histórica 2009-2024 de 67.76% en los 539 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`4.04`** — Diferencia media entre elecciones presidenciales e intermedias de 4.04 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`34.87`** — Proporción media de lista nominal en secciones rurales equivalente a 34.87%.
- **Tono de comunicación recomendado:** Reconocimiento al compromiso comunitario, corresponsabilidad intergeneracional y preservación de asambleas informativas locales.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Incrementar la asistencia a las urnas de las juventudes (18 a 29 años) en entornos urbanos y mixtos para reducir la brecha generacional frente al grupo de 60+ años.
- **Acción concreta:** Ejecutar circuitos universitarios y de educación media superior 'Mi Primer Voto 2027' junto con recordatorios digitales geolocalizados del sistema 'Ubica tu Casilla' del INE.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del grupo de 18 a 29 años en el perfil (%) | **Línea base:** `62.28%` $\rightarrow$ **Meta 2027:** `65.28%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 1: Participación Rural y Femenina
- **Lema:** *Municipios con mayoría de secciones rurales, ascenso sostenido y liderazgo cívico de mujeres*
- **Narrativa (108 palabras):** El perfil territorial 1, denominado Participación Rural y Femenina, agrupa 378 municipios del país con una lista nominal acumulada en 2024 de 6,851,597 personas inscritas, teniendo presencia destacada en entidades como OAXACA. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 59.2% y una diferencia promedio entre elecciones presidenciales e intermedias de 9.1 puntos porcentuales, con una pendiente temporal de 1.72 puntos por ciclo electoral. Su composición territorial presenta 55.92% de lista nominal en secciones rurales, una participación juvenil media de 49.18% frente a 65.57% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 11.35 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a Charo (MICHOACAN), donde el padrón presenta 55.92% de secciones rurales y una participación histórica media de 59.2%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`59.2`** — Participación media histórica 2009-2024 de 59.2% en los 378 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`9.1`** — Diferencia media entre elecciones presidenciales e intermedias de 9.1 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`55.92`** — Proporción media de lista nominal en secciones rurales equivalente a 55.92%.
- **Tono de comunicación recomendado:** Comunicación comunitaria cercana, perifoneo local, radio regional y fortalecimiento del liderazgo cívico de las mujeres.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Fortalecer la cobertura informativa y accesibilidad electoral en secciones rurales y mixtas y promover el conocimiento oportuno de la ubicación de casillas.
- **Acción concreta:** Implementar brigadas itinerantes de capacitación cívica DECEyEC en cabeceras y localidades rurales, acompañadas de cápsulas informativas en radios comunitarias y lenguas nacionales.
- **Canales:** Radios comunitarias y perifoneo en localidades rurales y mixtas, Asambleas informativas presenciales coordinadas por Juntas Distritales Ejecutivas del INE, Materiales impresos y señalética comunitaria en centros de salud, mercados y plazas públicas
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media en elección intermedia en municipios del perfil (%) | **Línea base:** `54.66%` $\rightarrow$ **Meta 2027:** `56.66%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 2: Impulso Cívico en Ascenso
- **Lema:** *Territorios con fuerte crecimiento de participación entre 2009 y 2024 y brecha en intermedias*
- **Narrativa (108 palabras):** El perfil territorial 2, denominado Impulso Cívico en Ascenso, agrupa 440 municipios del país con una lista nominal acumulada en 2024 de 13,283,697 personas inscritas, teniendo presencia destacada en entidades como OAXACA. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 55.13% y una diferencia promedio entre elecciones presidenciales e intermedias de 20.63 puntos porcentuales, con una pendiente temporal de 4.39 puntos por ciclo electoral. Su composición territorial presenta 22.39% de lista nominal en secciones rurales, una participación juvenil media de 47.09% frente a 61.02% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 7.31 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a San Pedro y San Pablo Teposcolula (OAXACA), donde el padrón presenta 22.39% de secciones rurales y una participación histórica media de 55.13%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`55.13`** — Participación media histórica 2009-2024 de 55.13% en los 440 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`20.63`** — Diferencia media entre elecciones presidenciales e intermedias de 20.63 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`22.39`** — Proporción media de lista nominal en secciones rurales equivalente a 22.39%.
- **Tono de comunicación recomendado:** Mensaje constructivo de consolidación democrática, enfocado en sostener el crecimiento en los comicios intermedios de 2027.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `44.81%` $\rightarrow$ **Meta 2027:** `47.31%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 3: Dinámica Local Volátil
- **Lema:** *Municipios con alta variabilidad entre ciclos electorales que requieren acompañamiento focalizado*
- **Narrativa (107 palabras):** El perfil territorial 3, denominado Dinámica Local Volátil, agrupa 79 municipios del país con una lista nominal acumulada en 2024 de 715,243 personas inscritas, teniendo presencia destacada en entidades como OAXACA. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 51.29% y una diferencia promedio entre elecciones presidenciales e intermedias de -5.93 puntos porcentuales, con una pendiente temporal de -1.37 puntos por ciclo electoral. Su composición territorial presenta 34.71% de lista nominal en secciones rurales, una participación juvenil media de 43.94% frente a 55.18% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 5.4 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a AmatitlÃ¡n (VERACRUZ), donde el padrón presenta 34.71% de secciones rurales y una participación histórica media de 51.29%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`51.29`** — Participación media histórica 2009-2024 de 51.29% en los 79 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`-5.93`** — Diferencia media entre elecciones presidenciales e intermedias de -5.93 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`34.71`** — Proporción media de lista nominal en secciones rurales equivalente a 34.71%.
- **Tono de comunicación recomendado:** Pedagogía cívica continua y fortalecimiento de condiciones operativas e informativas en cada proceso electoral.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Incrementar la asistencia a las urnas de las juventudes (18 a 29 años) en entornos urbanos y mixtos para reducir la brecha generacional frente al grupo de 60+ años.
- **Acción concreta:** Ejecutar circuitos universitarios y de educación media superior 'Mi Primer Voto 2027' junto con recordatorios digitales geolocalizados del sistema 'Ubica tu Casilla' del INE.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del grupo de 18 a 29 años en el perfil (%) | **Línea base:** `43.94%` $\rightarrow$ **Meta 2027:** `46.94%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 4: Dinámica Urbana Intermitente
- **Lema:** *Centros urbanos y mixtos con amplia brecha generacional entre jóvenes y adultos mayores*
- **Narrativa (107 palabras):** El perfil territorial 4, denominado Dinámica Urbana Intermitente, agrupa 553 municipios del país con una lista nominal acumulada en 2024 de 57,777,865 personas inscritas, teniendo presencia destacada en entidades como OAXACA. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 50.08% y una diferencia promedio entre elecciones presidenciales e intermedias de 10.99 puntos porcentuales, con una pendiente temporal de -0.01 puntos por ciclo electoral. Su composición territorial presenta 23.78% de lista nominal en secciones rurales, una participación juvenil media de 39.65% frente a 59.01% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 8.48 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a Salamanca (GUANAJUATO), donde el padrón presenta 23.78% de secciones rurales y una participación histórica media de 50.08%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`50.08`** — Participación media histórica 2009-2024 de 50.08% en los 553 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`10.99`** — Diferencia media entre elecciones presidenciales e intermedias de 10.99 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`23.78`** — Proporción media de lista nominal en secciones rurales equivalente a 23.78%.
- **Tono de comunicación recomendado:** Comunicación digital hiperlocal, vinculación con universidades y empleadores para facilitar el primer voto juvenil.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `44.59%` $\rightarrow$ **Meta 2027:** `47.09%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 5: Prioridad de Reactivación Cívica
- **Lema:** *Territorios con retos de abstención estructural en elecciones intermedias que requieren atención prioritaria*
- **Narrativa (108 palabras):** El perfil territorial 5, denominado Prioridad de Reactivación Cívica, agrupa 488 municipios del país con una lista nominal acumulada en 2024 de 11,612,921 personas inscritas, teniendo presencia destacada en entidades como OAXACA. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 49.62% y una diferencia promedio entre elecciones presidenciales e intermedias de 10.79 puntos porcentuales, con una pendiente temporal de 1.97 puntos por ciclo electoral. Su composición territorial presenta 35.22% de lista nominal en secciones rurales, una participación juvenil media de 39.92% frente a 54.33% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 4.6 puntos.
- **Comunidad ilustrativa:** [EJEMPLO FICTICIO ILUSTRATIVO DE COMUNIDAD TERRITORIAL, NO PERSONA INDIVIDUAL] Municipio tipo con características estadísticas similares a Vega de Alatorre (VERACRUZ), donde el padrón presenta 35.22% de secciones rurales y una participación histórica media de 49.62%.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`49.62`** — Participación media histórica 2009-2024 de 49.62% en los 488 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`10.79`** — Diferencia media entre elecciones presidenciales e intermedias de 10.79 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`35.22`** — Proporción media de lista nominal en secciones rurales equivalente a 35.22%.
- **Tono de comunicación recomendado:** Empatía institucional, eliminación de barreras de traslado e información accesible sobre ubicación de casillas y derechos ciudadanos.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `44.23%` $\rightarrow$ **Meta 2027:** `46.73%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

