# Capa LLM: Narrativas Verificadas, Estrategias Cívicas y Chat con los Datos (`docs/capa_llm.md`)

## 1. Nombrado y Narrativa de Perfiles Territoriales (Tarea 7A)

Cada perfil fue generado exclusivamente a partir de `data/processed/perfiles_caracterizacion.json` y validado con el **verificador automático de cifras (`verify_narrative_grounding`)** y esquemas `Pydantic` (`80-120` palabras por narrativa, `<= 4` palabras por nombre).

### Perfil 0: Cohesión Comunitaria Sostenida
- **Lema:** *Territorios de alta participación constante en elecciones presidenciales e intermedias*
- **Narrativa (107 palabras):** El perfil territorial 0, denominado Cohesión Comunitaria Sostenida, agrupa 111 municipios del país con una lista nominal acumulada en 2024 de 1,718,428 personas inscritas, teniendo presencia destacada en entidades como Yucatán. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 79.26% y una diferencia promedio entre elecciones presidenciales e intermedias de 12.18 puntos porcentuales, con una pendiente temporal de 2.58 puntos por ciclo electoral. Su composición territorial presenta 11.93% de lista nominal en secciones rurales, una participación juvenil media de 75.14% frente a 81.82% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 7.42 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): Baca (Yucatán, clave INEGI 31004), con participación histórica media de 81.14% dentro de un perfil que promedia 79.26% de participación y 11.93% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`79.26`** — Participación media histórica 2009-2024 de 79.26% en los 111 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`12.18`** — Diferencia media entre elecciones presidenciales e intermedias de 12.18 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`11.93`** — Proporción media de lista nominal en secciones rurales equivalente a 11.93%.
- **Tono de comunicación recomendado:** Reconocimiento al compromiso comunitario, corresponsabilidad intergeneracional y preservación de asambleas informativas locales.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `73.22%` $\rightarrow$ **Meta 2027:** `75.72%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 1: Participación Rural y Femenina
- **Lema:** *Municipios con mayoría de secciones rurales, ascenso sostenido y liderazgo cívico de mujeres*
- **Narrativa (108 palabras):** El perfil territorial 1, denominado Participación Rural y Femenina, agrupa 537 municipios del país con una lista nominal acumulada en 2024 de 23,639,337 personas inscritas, teniendo presencia destacada en entidades como Jalisco. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 65.08% y una diferencia promedio entre elecciones presidenciales e intermedias de 4.52 puntos porcentuales, con una pendiente temporal de 0.18 puntos por ciclo electoral. Su composición territorial presenta 31.78% de lista nominal en secciones rurales, una participación juvenil media de 59.98% frente a 68.84% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 8.91 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): Mazamitla (Jalisco, clave INEGI 14061), con participación histórica media de 66.07% dentro de un perfil que promedia 65.08% de participación y 31.78% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`65.08`** — Participación media histórica 2009-2024 de 65.08% en los 537 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`4.52`** — Diferencia media entre elecciones presidenciales e intermedias de 4.52 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`31.78`** — Proporción media de lista nominal en secciones rurales equivalente a 31.78%.
- **Tono de comunicación recomendado:** Comunicación comunitaria cercana, perifoneo local, radio regional y fortalecimiento del liderazgo cívico de las mujeres.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Incrementar la asistencia a las urnas de las juventudes (18 a 29 años) en entornos urbanos y mixtos para reducir la brecha generacional frente al grupo de 60+ años.
- **Acción concreta:** Ejecutar circuitos universitarios y de educación media superior 'Mi Primer Voto 2027' junto con recordatorios digitales geolocalizados del sistema 'Ubica tu Casilla' del INE.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del grupo de 18 a 29 años en el perfil (%) | **Línea base:** `59.98%` $\rightarrow$ **Meta 2027:** `62.98%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 2: Impulso Cívico en Ascenso
- **Lema:** *Territorios con fuerte crecimiento de participación entre 2009 y 2024 y brecha en intermedias*
- **Narrativa (108 palabras):** El perfil territorial 2, denominado Impulso Cívico en Ascenso, agrupa 425 municipios del país con una lista nominal acumulada en 2024 de 9,287,589 personas inscritas, teniendo presencia destacada en entidades como Veracruz. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 61.78% y una diferencia promedio entre elecciones presidenciales e intermedias de 8.22 puntos porcentuales, con una pendiente temporal de 1.36 puntos por ciclo electoral. Su composición territorial presenta 57.89% de lista nominal en secciones rurales, una participación juvenil media de 49.83% frente a 69.45% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 10.0 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): Altotonga (Veracruz, clave INEGI 30011), con participación histórica media de 59.9% dentro de un perfil que promedia 61.78% de participación y 57.89% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`61.78`** — Participación media histórica 2009-2024 de 61.78% en los 425 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`8.22`** — Diferencia media entre elecciones presidenciales e intermedias de 8.22 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`57.89`** — Proporción media de lista nominal en secciones rurales equivalente a 57.89%.
- **Tono de comunicación recomendado:** Mensaje constructivo de consolidación democrática, enfocado en sostener el crecimiento en los comicios intermedios de 2027.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Fortalecer la cobertura informativa y accesibilidad electoral en secciones rurales y mixtas y promover el conocimiento oportuno de la ubicación de casillas.
- **Acción concreta:** Implementar brigadas itinerantes de capacitación cívica DECEyEC en cabeceras y localidades rurales, acompañadas de cápsulas informativas en radios comunitarias y lenguas nacionales.
- **Canales:** Radios comunitarias y perifoneo en localidades rurales y mixtas, Asambleas informativas presenciales coordinadas por Juntas Distritales Ejecutivas del INE, Materiales impresos y señalética comunitaria en centros de salud, mercados y plazas públicas
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media en elección intermedia en municipios del perfil (%) | **Línea base:** `57.68%` $\rightarrow$ **Meta 2027:** `59.68%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 3: Dinámica Local Volátil
- **Lema:** *Municipios con alta variabilidad entre ciclos electorales que requieren acompañamiento focalizado*
- **Narrativa (107 palabras):** El perfil territorial 3, denominado Dinámica Local Volátil, agrupa 554 municipios del país con una lista nominal acumulada en 2024 de 18,074,124 personas inscritas, teniendo presencia destacada en entidades como Puebla. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 58.03% y una diferencia promedio entre elecciones presidenciales e intermedias de 18.29 puntos porcentuales, con una pendiente temporal de 5.97 puntos por ciclo electoral. Su composición territorial presenta 31.45% de lista nominal en secciones rurales, una participación juvenil media de 50.36% frente a 64.12% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 8.29 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): Oriental (Puebla, clave INEGI 21109), con participación histórica media de 59.82% dentro de un perfil que promedia 58.03% de participación y 31.45% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`58.03`** — Participación media histórica 2009-2024 de 58.03% en los 554 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`18.29`** — Diferencia media entre elecciones presidenciales e intermedias de 18.29 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`31.45`** — Proporción media de lista nominal en secciones rurales equivalente a 31.45%.
- **Tono de comunicación recomendado:** Pedagogía cívica continua y fortalecimiento de condiciones operativas e informativas en cada proceso electoral.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `49.14%` $\rightarrow$ **Meta 2027:** `51.64%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 4: Dinámica Urbana Intermitente
- **Lema:** *Centros urbanos y mixtos con amplia brecha generacional entre jóvenes y adultos mayores*
- **Narrativa (107 palabras):** El perfil territorial 4, denominado Dinámica Urbana Intermitente, agrupa 659 municipios del país con una lista nominal acumulada en 2024 de 45,053,420 personas inscritas, teniendo presencia destacada en entidades como Oaxaca. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 49.97% y una diferencia promedio entre elecciones presidenciales e intermedias de 13.58 puntos porcentuales, con una pendiente temporal de 1.72 puntos por ciclo electoral. Su composición territorial presenta 27.52% de lista nominal en secciones rurales, una participación juvenil media de 40.45% frente a 56.88% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 6.72 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): La Antigua (Veracruz, clave INEGI 30017), con participación histórica media de 52.7% dentro de un perfil que promedia 49.97% de participación y 27.52% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`49.97`** — Participación media histórica 2009-2024 de 49.97% en los 659 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`13.58`** — Diferencia media entre elecciones presidenciales e intermedias de 13.58 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`27.52`** — Proporción media de lista nominal en secciones rurales equivalente a 27.52%.
- **Tono de comunicación recomendado:** Comunicación digital hiperlocal, vinculación con universidades y empleadores para facilitar el primer voto juvenil.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `43.23%` $\rightarrow$ **Meta 2027:** `45.73%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

### Perfil 5: Prioridad de Reactivación Cívica
- **Lema:** *Territorios con retos de abstención estructural en elecciones intermedias que requieren atención prioritaria*
- **Narrativa (108 palabras):** El perfil territorial 5, denominado Prioridad de Reactivación Cívica, agrupa 191 municipios del país con una lista nominal acumulada en 2024 de 557,450 personas inscritas, teniendo presencia destacada en entidades como Oaxaca. En el ciclo histórico 2009 a 2024 registra una tasa de participación media global de 49.76% y una diferencia promedio entre elecciones presidenciales e intermedias de 12.12 puntos porcentuales, con una pendiente temporal de 1.36 puntos por ciclo electoral. Su composición territorial presenta 22.57% de lista nominal en secciones rurales, una participación juvenil media de 34.63% frente a 56.17% en personas mayores de sesenta años, y una brecha media entre mujeres y hombres de 4.67 puntos.
- **Comunidad ilustrativa:** [DATO REAL · MUNICIPIO PROTOTIPO MEDOIDE DEL PERFIL, COMUNIDAD TERRITORIAL NO PERSONA INDIVIDUAL] Municipio prototipo real (medoide de menor distancia al centroide del perfil): San Pedro Molinos (Oaxaca, clave INEGI 20318), con participación histórica media de 52.38% dentro de un perfil que promedia 49.76% de participación y 22.57% de lista nominal en secciones rurales.
- **Datos clave con evidencia verificada:**
  - `part_media_global.media_pct` = **`49.76`** — Participación media histórica 2009-2024 de 49.76% en los 191 municipios del perfil.
  - `caida_presidencial_intermedia.media_pct` = **`12.12`** — Diferencia media entre elecciones presidenciales e intermedias de 12.12 puntos porcentuales.
  - `pct_ln_rural.media_pct` = **`22.57`** — Proporción media de lista nominal en secciones rurales equivalente a 22.57%.
- **Tono de comunicación recomendado:** Empatía institucional, eliminación de barreras de traslado e información accesible sobre ubicación de casillas y derechos ciudadanos.

#### Estrategia Recomendada (Tarea 7B — Alineada a ENCCÍVICA / DECEyEC)
- **Objetivo:** Reducir la brecha de abstención entre elecciones presidenciales e intermedias mediante campañas informativas sobre las atribuciones de la Cámara de Diputados en la elección 2027.
- **Acción concreta:** Desplegar jornadas de Diálogos Comunitarios y Foros Informativos Distritales en los 60 días previos a la jornada electoral de 2027, explicando qué se elige en una elección intermedia.
- **Canales:** Plataformas digitales, mensajería móvil e integración con el portal 'Ubica tu Casilla', Foros presenciales en universidades, tecnológicos y planteles de educación media superior, Comunicación institucional en transporte público y centros de trabajo
- **Aliados institucionales:** Juntas Locales y Distritales Ejecutivas del INE (DECEyEC), Organismos Públicos Locales Electorales (OPL) de las entidades predominantes, Instituciones de Educación Superior y Media Superior públicas y privadas, Organizaciones de la sociedad civil y redes comunitarias acreditadas sin filiación partidista
- **KPI medible:** Tasa de participación media del perfil en elección federal intermedia (%) | **Línea base:** `43.76%` $\rightarrow$ **Meta 2027:** `46.26%`
- **Consideración ética:** Preservar en todo momento la estricta neutralidad e imparcialidad constitucional del INE; evitar mensajes que culpabilicen al electorado por la abstención y recordar que el perfil describe condiciones agregadas del municipio (prevención de falacia ecológica).

