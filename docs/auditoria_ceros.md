# Auditoría de Ceros Falsos, Cobertura (`NS`) y Municipios Pequeños (Fase A1)

## 1. Diagnóstico de Causa Raíz (Evidencia SQL sobre CCPC 2009–2024)

En la versión `v1-baseline`, se observaban tasas de participación de `0.0%` en años específicos para municipios como **Atil, Higueras, Oquitoa, Cucurpe y Tubutama (2024)** o **Magdalena Ocotlán y Rayones (2009)**. La consulta directa a las medidas crudas (`LN`, `SV`, `NV`, `NS`) demuestra de manera concluyente que **ninguno de esos municipios tuvo 0 votantes reales**: en todos ellos **`NS (No Especificados) == LN (Lista Nominal)`**, es decir, el 100% de los electores quedó registrado bajo la clave `NS` (cuadernillos no disponibles para captura o requeridos por autoridades jurisdiccionales), resultando en una **cobertura de captura del `0.0%`**.

- **Total de celdas municipio-año con `SV == 0` (`100% NS`):** `76` observaciones en el panel 2009–2024.
- **Total de celdas municipio-año con `cobertura < 90%` (`(SV + NV) / LN < 0.90`):** `1892` observaciones.
- **Regla Oficial Implementada en v2:**
  $$\text{cobertura} = \frac{SV + NV}{LN}, \qquad \text{participacion} = \begin{cases} \frac{SV}{SV + NV} & \text{si } \text{cobertura} \ge 0.90 \\ \text{NA (NULL)} & \text{si } \text{cobertura} < 0.90 \end{cases}$$

## 2. Tabla Completa de Celdas Municipio-Año con `Cobertura < 90%` o `SV = 0`

| Año | `cve_geo` | Entidad | Municipio | `LN` | `SV` | `NV` | `NS` | Cobertura (%) | Part. v1 (`SV/LN`) | Part. v2 (`SV/(SV+NV)`) | Causa Raíz |
| :---: | :---: | :--- | :--- | ---: | ---: | ---: | ---: | ---: | ---: | :---: | :--- |
| 2009 | `07055` | Chiapas | Metapa | 4,026 | 0 | 0 | 4,026 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `08055` | Chihuahua | Rosales | 13,054 | 0 | 0 | 13,054 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `11008` | Guanajuato | Manuel Doblado | 30,635 | 0 | 0 | 30,635 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `19044` | Nuevo León | Rayones | 2,421 | 0 | 0 | 2,421 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `20048` | Oaxaca | Magdalena Ocotlán | 769 | 0 | 0 | 769 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `20346` | Oaxaca | San Sebastián Teitipac | 1,654 | 0 | 0 | 1,654 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2009 | `20510` | Oaxaca | Santo Domingo Ixcatlán | 564 | 0 | 0 | 564 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2012 | `20247` | Oaxaca | San Mateo del Mar | 8,027 | 0 | 0 | 8,027 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `19031` | Nuevo León | Iturbide | 2,915 | 0 | 0 | 2,915 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20015` | Oaxaca | Chahuites | 7,586 | 0 | 0 | 7,586 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20029` | Oaxaca | Eloxochitlán de Flores Magón | 2,545 | 0 | 0 | 2,545 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20038` | Oaxaca | Huautepec | 3,706 | 0 | 0 | 3,706 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20047` | Oaxaca | Magdalena Mixtepec | 699 | 0 | 0 | 699 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20058` | Oaxaca | Mazatlán Villa de Flores | 8,073 | 0 | 0 | 8,073 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20109` | Oaxaca | San Baltazar Chichicápam | 2,293 | 0 | 0 | 2,293 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20127` | Oaxaca | San Dionisio del Mar | 3,721 | 0 | 0 | 3,721 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20129` | Oaxaca | San Dionisio Ocotlán | 918 | 0 | 0 | 918 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20135` | Oaxaca | San Francisco Cajonos | 356 | 0 | 0 | 356 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20138` | Oaxaca | San Francisco del Mar | 4,895 | 0 | 0 | 4,895 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20139` | Oaxaca | San Francisco Huehuetlán | 727 | 0 | 0 | 727 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20140` | Oaxaca | San Francisco Ixhuatán | 6,725 | 0 | 0 | 6,725 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20142` | Oaxaca | San Francisco Lachigoló | 2,233 | 0 | 0 | 2,233 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20160` | Oaxaca | San Jerónimo Tecóatl | 1,102 | 0 | 0 | 1,102 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20228` | Oaxaca | San Lorenzo Cuaunecuiltitla | 471 | 0 | 0 | 471 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20271` | Oaxaca | San Miguel Panixtlahuaca | 3,762 | 0 | 0 | 3,762 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20277` | Oaxaca | San Miguel Suchixtepec | 1,958 | 0 | 0 | 1,958 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20287` | Oaxaca | San Nicolás | 888 | 0 | 0 | 888 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20311` | Oaxaca | San Pedro Jocotipac | 641 | 0 | 0 | 641 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20317` | Oaxaca | San Pedro Mixtepec | 732 | 0 | 0 | 732 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20354` | Oaxaca | Santa Ana Ateixtlahuaca | 321 | 0 | 0 | 321 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20370` | Oaxaca | Santa Catarina Quioquitani | 312 | 0 | 0 | 312 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20375` | Oaxaca | Santa Cruz Acatepec | 903 | 0 | 0 | 903 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20435` | Oaxaca | Santa María Teopoxco | 2,800 | 0 | 0 | 2,800 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20437` | Oaxaca | Santa María Texcatitlán | 779 | 0 | 0 | 779 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20467` | Oaxaca | Santiago Ixtayutla | 7,335 | 0 | 0 | 7,335 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `20489` | Oaxaca | Santiago Tepetlapa | 95 | 0 | 0 | 95 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `26033` | Sonora | San Felipe de Jesús | 508 | 0 | 0 | 508 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `31039` | Yucatán | Ixil | 2,821 | 0 | 0 | 2,821 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `07086` | Chiapas | Soyaló | 7,087 | 0 | 0 | 7,087 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `13004` | Hidalgo | Agua Blanca de Iturbide | 7,073 | 0 | 0 | 7,073 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `13027` | Hidalgo | Huehuetla | 16,429 | 0 | 0 | 16,429 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `13052` | Hidalgo | San Bartolo Tutotepec | 12,797 | 0 | 0 | 12,797 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `13056` | Hidalgo | Santiago Tulantepec de Lugo Guerrero | 25,028 | 0 | 0 | 25,028 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `20166` | Oaxaca | San José Estancia Grande | 749 | 0 | 0 | 749 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `20224` | Oaxaca | San Juan Yucuita | 570 | 0 | 0 | 570 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `20257` | Oaxaca | San Miguel Achiutla | 537 | 0 | 0 | 537 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `20357` | Oaxaca | Santa Ana Tavela | 626 | 0 | 0 | 626 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `20396` | Oaxaca | Santa Magdalena Jicotlán | 72 | 0 | 0 | 72 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `21047` | Puebla | Chapulco | 4,888 | 0 | 0 | 4,888 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `31064` | Yucatán | Sanahcat | 1,377 | 0 | 0 | 1,377 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2018 | `31103` | Yucatán | Xocchel | 2,590 | 0 | 0 | 2,590 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `07064` | Chiapas | Oxchuc | 37,899 | 0 | 0 | 37,899 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `07081` | Chiapas | Siltepec | 17,646 | 0 | 0 | 17,646 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `07106` | Chiapas | Venustiano Carranza | 46,800 | 0 | 0 | 46,800 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `07124` | Chiapas | Honduras de la Sierra | 8,171 | 0 | 0 | 8,171 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `20072` | Oaxaca | Reforma de Pineda | 2,308 | 0 | 0 | 2,308 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `20247` | Oaxaca | San Mateo del Mar | 10,221 | 0 | 0 | 10,221 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `20422` | Oaxaca | Santa María Mixtequilla | 3,570 | 0 | 0 | 3,570 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `20442` | Oaxaca | Santa María Xadani | 6,748 | 0 | 0 | 6,748 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `21134` | Puebla | San Martín Totoltepec | 611 | 0 | 0 | 611 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2021 | `31105` | Yucatán | Yaxkukul | 2,707 | 0 | 0 | 2,707 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `07030` | Chiapas | Chicomuselo | 26,330 | 0 | 0 | 26,330 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `07066` | Chiapas | Pantelhó | 15,256 | 0 | 0 | 15,256 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `16112` | Michoacán | Ziracuaretiro | 14,251 | 0 | 0 | 14,251 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `19029` | Nuevo León | Higueras | 1,541 | 0 | 0 | 1,541 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `20073` | Oaxaca | La Reforma | 2,523 | 0 | 0 | 2,523 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `20280` | Oaxaca | San Miguel Tenango | 637 | 0 | 0 | 637 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `20357` | Oaxaca | Santa Ana Tavela | 654 | 0 | 0 | 654 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `20559` | Oaxaca | Capulálpam de Méndez | 1,215 | 0 | 0 | 1,215 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `26006` | Sonora | Atil | 747 | 0 | 0 | 747 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `26016` | Sonora | Cucurpe | 1,009 | 0 | 0 | 1,009 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `26031` | Sonora | Oquitoa | 446 | 0 | 0 | 446 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2024 | `26043` | Sonora | Tubutama | 1,381 | 0 | 0 | 1,381 | 0.00% | 0.00% | **NA (Excluido)** | 100% NS (Cuadernillos no disponibles / reservados por autoridad) |
| 2015 | `16108` | Michoacán | Zacapu | 55,807 | 769 | 596 | 54,442 | 2.45% | 1.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16048` | Michoacán | Jungapeo | 15,128 | 320 | 156 | 14,652 | 3.15% | 2.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30073` | Veracruz | Huatusco | 33,741 | 714 | 647 | 32,380 | 4.03% | 2.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `19049` | Nuevo León | Santiago | 32,087 | 880 | 522 | 30,685 | 4.37% | 2.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12065` | Guerrero | Tlalchapa | 9,677 | 373 | 199 | 9,105 | 5.91% | 3.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20039` | Oaxaca | Huautla de Jiménez | 20,404 | 413 | 904 | 19,087 | 6.45% | 2.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30061` | Veracruz | Chinameca | 12,026 | 399 | 472 | 11,155 | 7.24% | 3.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13060` | Hidalgo | Tenango de Doria | 12,041 | 544 | 346 | 11,151 | 7.39% | 4.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13036` | Hidalgo | Metepec | 9,055 | 491 | 251 | 8,313 | 8.19% | 5.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15036` | Estado de México | Huehuetoca | 80,654 | 2,748 | 3,948 | 73,958 | 8.30% | 3.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20473` | Oaxaca | Santiago Laollaga | 2,881 | 194 | 110 | 2,577 | 10.55% | 6.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07117` | Chiapas | San Andrés Duraznal | 3,400 | 316 | 47 | 3,037 | 10.68% | 9.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16024` | Michoacán | Cherán | 14,085 | 762 | 772 | 12,551 | 10.89% | 5.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16024` | Michoacán | Cherán | 15,001 | 783 | 881 | 13,337 | 11.09% | 5.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21075` | Puebla | Huehuetlán el Grande | 4,960 | 416 | 156 | 4,388 | 11.53% | 8.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12074` | Guerrero | Zirándaro | 13,976 | 1,142 | 563 | 12,271 | 12.20% | 8.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26052` | Sonora | Pitiquito | 6,420 | 498 | 288 | 5,634 | 12.24% | 7.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31047` | Yucatán | Maní | 4,321 | 452 | 79 | 3,790 | 12.29% | 10.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08047` | Chihuahua | Moris | 3,738 | 171 | 306 | 3,261 | 12.76% | 4.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07088` | Chiapas | Suchiate | 18,840 | 948 | 1,476 | 16,416 | 12.87% | 5.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20262` | Oaxaca | San Miguel Chicahua | 1,555 | 132 | 70 | 1,353 | 12.99% | 8.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20217` | Oaxaca | San Juan Tamazola | 2,155 | 191 | 95 | 1,869 | 13.27% | 8.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16024` | Michoacán | Cherán | 13,060 | 1,066 | 833 | 11,161 | 14.54% | 8.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13015` | Hidalgo | Cuautepec de Hinojosa | 41,972 | 3,517 | 2,601 | 35,854 | 14.58% | 8.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07035` | Chiapas | Frontera Hidalgo | 8,157 | 533 | 668 | 6,956 | 14.72% | 6.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05012` | Coahuila | Guerrero | 1,890 | 186 | 100 | 1,604 | 15.13% | 9.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07029` | Chiapas | Chicoasén | 4,266 | 507 | 164 | 3,595 | 15.73% | 11.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16024` | Michoacán | Cherán | 12,619 | 1,155 | 839 | 10,625 | 15.80% | 9.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20170` | Oaxaca | San José Tenango | 11,215 | 842 | 936 | 9,437 | 15.85% | 7.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30013` | Veracruz | Amatitlán | 5,977 | 691 | 328 | 4,958 | 17.05% | 11.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07122` | Chiapas | Emiliano Zapata | 8,457 | 1,124 | 319 | 7,014 | 17.06% | 13.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `11012` | Guanajuato | Cuerámaro | 21,815 | 2,019 | 1,783 | 18,013 | 17.43% | 9.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20051` | Oaxaca | Magdalena Tequisistlán | 5,138 | 474 | 427 | 4,237 | 17.54% | 9.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20305` | Oaxaca | San Pedro Huamelula | 7,703 | 1,108 | 311 | 6,284 | 18.42% | 14.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20419` | Oaxaca | Santa María Jalapa del Marqués | 8,755 | 981 | 632 | 7,142 | 18.42% | 11.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20303` | Oaxaca | San Pedro Comitancillo | 3,772 | 481 | 244 | 3,047 | 19.22% | 12.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29057` | Tlaxcala | San Lucas Tecopilco | 2,619 | 397 | 136 | 2,086 | 20.35% | 15.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25009` | Sinaloa | Escuinapa | 40,712 | 4,910 | 3,411 | 32,391 | 20.44% | 12.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12032` | Guerrero | General Canuto A. Neri | 4,677 | 768 | 248 | 3,661 | 21.72% | 16.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20043` | Oaxaca | Heroica Ciudad de Juchitán de Zaragoza | 68,277 | 4,078 | 10,828 | 53,371 | 21.83% | 5.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26038` | Sonora | Sáric | 1,807 | 94 | 305 | 1,408 | 22.08% | 5.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30208` | Veracruz | Carlos A. Carrillo | 16,793 | 2,271 | 1,581 | 12,941 | 22.94% | 13.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20306` | Oaxaca | San Pedro Huilotepec | 2,501 | 416 | 209 | 1,876 | 24.99% | 16.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31073` | Yucatán | Tahdziú | 2,960 | 698 | 42 | 2,220 | 25.00% | 23.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `19034` | Nuevo León | Linares | 57,501 | 7,782 | 7,026 | 42,693 | 25.75% | 13.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16049` | Michoacán | Lagunillas | 4,954 | 897 | 393 | 3,664 | 26.04% | 18.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20456` | Oaxaca | Santiago Ayuquililla | 1,878 | 297 | 197 | 1,384 | 26.30% | 15.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08051` | Chihuahua | Ocampo | 6,496 | 1,028 | 706 | 4,762 | 26.69% | 15.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26003` | Sonora | Altar | 7,121 | 1,114 | 796 | 5,211 | 26.82% | 15.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30047` | Veracruz | Cosamaloapan de Carpio | 42,022 | 7,429 | 4,582 | 30,011 | 28.58% | 17.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24050` | San Luis Potosí | Villa de Ramos | 25,587 | 5,169 | 2,219 | 18,199 | 28.87% | 20.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21008` | Puebla | Ahuazotepec | 7,541 | 1,533 | 694 | 5,314 | 29.53% | 20.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20161` | Oaxaca | San Jerónimo Tlacochahuaya | 3,970 | 372 | 802 | 2,796 | 29.57% | 9.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20184` | Oaxaca | San Juan Cacahuatepec | 6,227 | 900 | 946 | 4,381 | 29.65% | 14.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07024` | Chiapas | Chanal | 7,024 | 1,687 | 402 | 4,935 | 29.74% | 24.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25004` | Sinaloa | Concordia | 20,583 | 4,007 | 2,210 | 14,366 | 30.20% | 19.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07085` | Chiapas | Solosuchiapa | 5,681 | 1,438 | 329 | 3,914 | 31.10% | 25.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `11021` | Guanajuato | Moroleón | 41,583 | 6,577 | 6,382 | 28,624 | 31.16% | 15.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20056` | Oaxaca | Mártires de Tacubaya | 1,057 | 296 | 35 | 726 | 31.32% | 28.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30095` | Veracruz | Juan Rodríguez Clara | 25,823 | 4,740 | 3,378 | 17,705 | 31.44% | 18.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26048` | Sonora | La Colorada | 2,479 | 639 | 144 | 1,696 | 31.59% | 25.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20525` | Oaxaca | Santo Domingo Zanatepec | 8,020 | 697 | 1,849 | 5,474 | 31.75% | 8.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20234` | Oaxaca | San Lucas Zoquiápam | 4,374 | 802 | 589 | 2,983 | 31.80% | 18.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20200` | Oaxaca | San Juan Ihualtepec | 577 | 107 | 77 | 393 | 31.89% | 18.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14112` | Jalisco | Valle de Guadalupe | 5,462 | 1,011 | 750 | 3,701 | 32.24% | 18.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21029` | Puebla | Cañada Morelos | 15,222 | 3,169 | 1,772 | 10,281 | 32.46% | 20.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20325` | Oaxaca | San Pedro Tapanatepec | 9,457 | 1,248 | 1,865 | 6,344 | 32.92% | 13.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07120` | Chiapas | Rincón Chamula San Pedro | 5,366 | 1,211 | 568 | 3,587 | 33.15% | 22.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20304` | Oaxaca | San Pedro el Alto | 2,230 | 309 | 435 | 1,486 | 33.36% | 13.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30052` | Veracruz | Coxquihui | 11,482 | 2,944 | 905 | 7,633 | 33.52% | 25.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20087` | Oaxaca | San Andrés Huaxpaltepec | 4,229 | 344 | 1,076 | 2,809 | 33.58% | 8.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30079` | Veracruz | Isla | 28,743 | 5,248 | 4,431 | 19,064 | 33.67% | 18.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12053` | Guerrero | San Luis Acatlán | 25,171 | 6,066 | 2,476 | 16,629 | 33.94% | 24.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16021` | Michoacán | Charapan | 10,243 | 2,684 | 852 | 6,707 | 34.52% | 26.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26044` | Sonora | Villa Hidalgo | 1,680 | 422 | 168 | 1,090 | 35.12% | 25.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20372` | Oaxaca | Santa Catarina Ticuá | 730 | 181 | 77 | 472 | 35.34% | 24.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20247` | Oaxaca | San Mateo del Mar | 10,676 | 769 | 3,010 | 6,897 | 35.40% | 7.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `21093` | Puebla | Juan Galindo | 5,461 | 1,517 | 433 | 3,511 | 35.71% | 27.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12062` | Guerrero | Tixtla de Guerrero | 28,551 | 4,356 | 5,929 | 18,266 | 36.02% | 15.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20035` | Oaxaca | Guevea De Humboldt | 4,076 | 588 | 882 | 2,606 | 36.06% | 14.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31103` | Yucatán | Xocchel | 2,752 | 858 | 160 | 1,734 | 36.99% | 31.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16057` | Michoacán | Nahuatzen | 22,965 | 5,602 | 2,947 | 14,416 | 37.23% | 24.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14019` | Jalisco | Bolaños | 5,783 | 1,694 | 481 | 3,608 | 37.61% | 29.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20515` | Oaxaca | Santo Domingo Tehuantepec | 51,532 | 12,630 | 6,828 | 32,074 | 37.76% | 24.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21122` | Puebla | San Diego la Mesa Tochimiltzingo | 883 | 187 | 150 | 546 | 38.17% | 21.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30184` | Veracruz | Tlilapan | 4,278 | 839 | 795 | 2,644 | 38.20% | 19.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21108` | Puebla | Olintla | 8,895 | 2,477 | 927 | 5,491 | 38.27% | 27.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07056` | Chiapas | Mitontic | 7,062 | 2,140 | 584 | 4,338 | 38.57% | 30.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14019` | Jalisco | Bolaños | 5,898 | 1,815 | 464 | 3,619 | 38.64% | 30.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30168` | Veracruz | José Azueta | 17,540 | 3,913 | 2,961 | 10,666 | 39.19% | 22.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07116` | Chiapas | Montecristo de Guerrero | 5,425 | 1,790 | 348 | 3,287 | 39.41% | 33.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21050` | Puebla | Chiconcuautla | 11,400 | 3,693 | 818 | 6,889 | 39.57% | 32.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15030` | Estado de México | Chicoloapan | 119,557 | 24,437 | 23,042 | 72,078 | 39.71% | 20.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14011` | Jalisco | Atengo | 4,573 | 1,348 | 522 | 2,703 | 40.89% | 29.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21206` | Puebla | Zacapala | 3,380 | 1,037 | 350 | 1,993 | 41.04% | 30.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24049` | San Luis Potosí | Villa de la Paz | 3,804 | 1,023 | 540 | 2,241 | 41.09% | 26.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30144` | Veracruz | Santiago Tuxtla | 43,254 | 10,543 | 7,233 | 25,478 | 41.10% | 24.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14081` | Jalisco | San Sebastián del Oeste | 4,615 | 1,418 | 490 | 2,707 | 41.34% | 30.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20397` | Oaxaca | Santa María Alotepec | 1,940 | 287 | 524 | 1,129 | 41.80% | 14.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07092` | Chiapas | Tapilula | 8,603 | 2,775 | 864 | 4,964 | 42.30% | 32.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20358` | Oaxaca | Santa Ana Tlapacoyan | 1,681 | 291 | 422 | 968 | 42.42% | 17.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30003` | Veracruz | Acayucan | 62,342 | 17,205 | 9,698 | 35,439 | 43.15% | 27.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20484` | Oaxaca | Santiago Pinotepa Nacional | 36,113 | 5,809 | 9,790 | 20,514 | 43.19% | 16.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13076` | Hidalgo | Tulancingo de Bravo | 123,570 | 30,563 | 23,063 | 69,944 | 43.40% | 24.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15042` | Estado de México | Ixtapan del Oro | 5,116 | 1,968 | 269 | 2,879 | 43.73% | 38.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20404` | Oaxaca | Santa María Chilchotla | 13,593 | 2,664 | 3,333 | 7,596 | 44.12% | 19.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31099` | Yucatán | Uayma | 3,106 | 1,241 | 161 | 1,704 | 45.14% | 39.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20540` | Oaxaca | Tamazulápam del Espíritu Santo | 4,838 | 748 | 1,437 | 2,653 | 45.16% | 15.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20473` | Oaxaca | Santiago Laollaga | 2,858 | 960 | 345 | 1,553 | 45.66% | 33.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20405` | Oaxaca | Santa María Chimalapa | 5,465 | 1,338 | 1,182 | 2,945 | 46.11% | 24.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26046` | Sonora | Caborca | 67,682 | 12,986 | 18,259 | 36,437 | 46.16% | 19.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20413` | Oaxaca | Santa María Guienagati | 2,389 | 477 | 633 | 1,279 | 46.46% | 19.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20077` | Oaxaca | San Agustín Amatengo | 1,254 | 457 | 126 | 671 | 46.49% | 36.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20330` | Oaxaca | San Pedro Topiltepec | 275 | 82 | 46 | 147 | 46.55% | 29.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15033` | Estado de México | Donato Guerra | 23,599 | 8,338 | 2,829 | 12,432 | 47.32% | 35.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30120` | Veracruz | Otatitlán | 4,246 | 1,312 | 710 | 2,224 | 47.62% | 30.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16057` | Michoacán | Nahuatzen | 20,196 | 4,810 | 4,822 | 10,564 | 47.69% | 23.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07008` | Chiapas | Ángel Albino Corzo | 19,768 | 6,212 | 3,252 | 10,304 | 47.88% | 31.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `11028` | Guanajuato | Salvatierra | 82,940 | 18,875 | 20,926 | 43,139 | 47.99% | 22.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20415` | Oaxaca | Santa María Huazolotitlán | 7,748 | 2,090 | 1,630 | 4,028 | 48.01% | 26.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `05038` | Coahuila | Zaragoza | 7,243 | 2,125 | 1,368 | 3,750 | 48.23% | 29.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20225` | Oaxaca | San Lorenzo | 3,724 | 1,007 | 794 | 1,923 | 48.36% | 27.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20047` | Oaxaca | Magdalena Mixtepec | 863 | 166 | 252 | 445 | 48.44% | 19.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16028` | Michoacán | Churintzio | 5,908 | 1,387 | 1,498 | 3,023 | 48.83% | 23.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20071` | Oaxaca | Putla Villa de Guerrero | 22,351 | 4,517 | 6,406 | 11,428 | 48.87% | 20.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07124` | Chiapas | Rincón Chamula San Pedro | 936 | 292 | 167 | 477 | 49.04% | 31.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07118` | Chiapas | Santiago El Pinar | 2,340 | 740 | 411 | 1,189 | 49.19% | 31.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21193` | Puebla | Tzicatlacoyan | 5,202 | 1,774 | 787 | 2,641 | 49.23% | 34.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30177` | Veracruz | Tlacotalpan | 10,429 | 3,271 | 1,895 | 5,263 | 49.53% | 31.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21174` | Puebla | Tianguismanalco | 8,107 | 2,880 | 1,149 | 4,078 | 49.70% | 35.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20195` | Oaxaca | San Juan del Río | 1,003 | 216 | 285 | 502 | 49.95% | 21.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20125` | Oaxaca | San Cristóbal LachiRíoag | 1,023 | 325 | 186 | 512 | 49.95% | 31.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20198` | Oaxaca | San Juan Guelavía | 2,339 | 330 | 839 | 1,170 | 49.98% | 14.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20159` | Oaxaca | San Jerónimo Taviche | 1,106 | 229 | 324 | 553 | 50.00% | 20.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20146` | Oaxaca | San Francisco Sola | 1,326 | 240 | 423 | 663 | 50.00% | 18.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20125` | Oaxaca | San Cristóbal Lachirioag | 1,040 | 312 | 208 | 520 | 50.00% | 30.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20429` | Oaxaca | Santa María Quiegolani | 1,170 | 325 | 260 | 585 | 50.00% | 27.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20313` | Oaxaca | San Pedro Mártir | 1,384 | 370 | 322 | 692 | 50.00% | 26.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26018` | Sonora | Divisaderos | 1,118 | 443 | 116 | 559 | 50.00% | 39.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31060` | Yucatán | Quintana Roo | 966 | 443 | 40 | 483 | 50.00% | 45.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26007` | Sonora | Bacadéhuachi | 1,148 | 476 | 98 | 574 | 50.00% | 41.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26018` | Sonora | Divisaderos | 1,164 | 485 | 97 | 582 | 50.00% | 41.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26040` | Sonora | Suaqui Grande | 1,402 | 598 | 103 | 701 | 50.00% | 42.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26050` | Sonora | Mazatán | 1,460 | 607 | 123 | 730 | 50.00% | 41.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20072` | Oaxaca | Reforma de Pineda | 2,332 | 817 | 349 | 1,166 | 50.00% | 35.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31005` | Yucatán | Bokobá | 2,042 | 945 | 76 | 1,021 | 50.00% | 46.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21011` | Puebla | Albino Zertuche | 1,445 | 578 | 145 | 722 | 50.03% | 40.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20159` | Oaxaca | San Jerónimo Taviche | 1,439 | 300 | 420 | 719 | 50.03% | 20.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20564` | Oaxaca | Yogana | 1,035 | 238 | 280 | 517 | 50.05% | 23.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26007` | Sonora | Bacadéhuachi | 1,033 | 457 | 60 | 516 | 50.05% | 44.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30117` | Veracruz | Oluta | 11,994 | 3,696 | 2,308 | 5,990 | 50.06% | 30.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20433` | Oaxaca | Santa María Temaxcalapa | 753 | 174 | 203 | 376 | 50.07% | 23.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20031` | Oaxaca | Fresnillo de Trujano | 814 | 279 | 129 | 406 | 50.12% | 34.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08046` | Chihuahua | Morelos | 5,592 | 1,643 | 1,162 | 2,787 | 50.16% | 29.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31101` | Yucatán | Umán | 40,503 | 14,836 | 5,496 | 20,171 | 50.20% | 36.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20051` | Oaxaca | Magdalena Tequisistlán | 5,514 | 2,097 | 673 | 2,744 | 50.24% | 38.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07011` | Chiapas | Bella Vista | 14,917 | 3,966 | 3,556 | 7,395 | 50.43% | 26.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13032` | Hidalgo | Jaltocán | 7,715 | 2,749 | 1,143 | 3,823 | 50.45% | 35.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30056` | Veracruz | Chacaltianguis | 9,128 | 3,121 | 1,496 | 4,511 | 50.58% | 34.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21037` | Puebla | Coyomeapan | 8,935 | 3,660 | 873 | 4,402 | 50.73% | 40.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23004` | Quintana Roo | Isla Mujeres | 17,928 | 3,895 | 5,234 | 8,799 | 50.92% | 21.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30131` | Veracruz | Playa Vicente | 28,813 | 9,804 | 4,952 | 14,057 | 51.21% | 34.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07010` | Chiapas | Bejucal de Ocampo | 6,019 | 1,790 | 1,296 | 2,933 | 51.27% | 29.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14029` | Jalisco | Cuautla | 2,247 | 792 | 370 | 1,085 | 51.71% | 35.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30016` | Veracruz | Angel R. Cabada | 25,717 | 8,269 | 5,080 | 12,368 | 51.91% | 32.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20145` | Oaxaca | San Francisco Ozolotepec | 1,287 | 381 | 294 | 612 | 52.45% | 29.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20502` | Oaxaca | Santiago Yucuyachi | 799 | 129 | 292 | 378 | 52.69% | 16.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20373` | Oaxaca | Santa Catarina Yosonotú | 1,002 | 296 | 233 | 473 | 52.79% | 29.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30114` | Veracruz | Naranjal | 3,479 | 1,402 | 437 | 1,640 | 52.86% | 40.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20422` | Oaxaca | Santa María Mixtequilla | 3,781 | 1,581 | 424 | 1,776 | 53.03% | 41.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28036` | Tamaulipas | San Nicolás | 934 | 370 | 126 | 438 | 53.10% | 39.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07124` | Chiapas | Honduras de la Sierra | 7,975 | 1,986 | 2,272 | 3,717 | 53.39% | 24.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19050` | Nuevo León | Vallecillo | 2,445 | 945 | 365 | 1,135 | 53.58% | 38.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08058` | Chihuahua | San Francisco de Conchos | 2,742 | 1,024 | 448 | 1,270 | 53.68% | 37.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07070` | Chiapas | El Porvenir | 9,009 | 3,463 | 1,374 | 4,172 | 53.69% | 38.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26056` | Sonora | San Miguel de Horcasitas | 5,540 | 1,667 | 1,309 | 2,564 | 53.72% | 30.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `18020` | Nayarit | La Yesca | 8,349 | 354 | 4,133 | 3,862 | 53.74% | 4.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20366` | Oaxaca | Santa Catarina Loxicha | 2,356 | 390 | 882 | 1,084 | 53.99% | 16.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07121` | Chiapas | El Parral | 11,969 | 1,923 | 4,595 | 5,451 | 54.46% | 16.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30175` | Veracruz | Tlacojalpan | 3,522 | 1,167 | 753 | 1,602 | 54.51% | 33.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07084` | Chiapas | Socoltenango | 10,800 | 2,546 | 3,367 | 4,887 | 54.75% | 23.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20076` | Oaxaca | Salina Cruz | 67,355 | 22,562 | 14,390 | 30,403 | 54.86% | 33.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20460` | Oaxaca | Santiago Choápam | 3,236 | 802 | 974 | 1,460 | 54.88% | 24.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `08033` | Chihuahua | Huejotitán | 1,392 | 332 | 433 | 627 | 54.96% | 23.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16025` | Michoacán | Chilchota | 28,753 | 9,938 | 5,871 | 12,944 | 54.98% | 34.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25013` | Sinaloa | Mocorito | 35,352 | 12,648 | 6,852 | 15,852 | 55.16% | 35.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25017` | Sinaloa | Sinaloa | 62,809 | 20,912 | 13,861 | 28,036 | 55.36% | 33.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16021` | Michoacán | Charapan | 9,962 | 4,317 | 1,249 | 4,396 | 55.87% | 43.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25018` | Sinaloa | Navolato | 103,304 | 34,470 | 23,334 | 45,500 | 55.96% | 33.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14015` | Jalisco | Autlán de Navarro | 50,872 | 14,725 | 13,750 | 22,397 | 55.97% | 28.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07091` | Chiapas | Tapalapa | 3,753 | 1,736 | 375 | 1,642 | 56.25% | 46.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30212` | Veracruz | Santiago Sochiapan | 8,928 | 2,847 | 2,186 | 3,895 | 56.37% | 31.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07067` | Chiapas | Pantepec | 8,648 | 4,270 | 630 | 3,748 | 56.66% | 49.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21138` | Puebla | San Nicolás Buenos Aires | 7,814 | 3,342 | 1,086 | 3,386 | 56.67% | 42.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16091` | Michoacán | Tingambato | 12,268 | 4,890 | 2,080 | 5,298 | 56.81% | 39.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26039` | Sonora | Soyopa | 2,083 | 1,019 | 167 | 897 | 56.94% | 48.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08042` | Chihuahua | Manuel Benavides | 1,931 | 808 | 293 | 830 | 57.02% | 41.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19036` | Nuevo León | Melchor Ocampo | 1,355 | 639 | 135 | 581 | 57.12% | 47.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21155` | Puebla | Tehuacán | 239,406 | 80,153 | 56,703 | 102,550 | 57.16% | 33.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21066` | Puebla | General Felipe Ángeles | 13,860 | 5,232 | 2,698 | 5,930 | 57.22% | 37.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31024` | Yucatán | Chumayel | 2,776 | 1,413 | 176 | 1,187 | 57.24% | 50.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20122` | Oaxaca | San Carlos Yautepec | 8,001 | 2,498 | 2,097 | 3,406 | 57.43% | 31.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30204` | Veracruz | Tres Valles | 32,364 | 11,631 | 6,967 | 13,766 | 57.47% | 35.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12054` | Guerrero | San Marcos | 34,646 | 13,771 | 6,155 | 14,720 | 57.51% | 39.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21195` | Puebla | Vicente Guerrero | 16,757 | 7,653 | 1,989 | 7,115 | 57.54% | 45.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31029` | Yucatán | Dzilam González | 5,278 | 2,741 | 307 | 2,230 | 57.75% | 51.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26051` | Sonora | Opodepe | 2,170 | 898 | 357 | 915 | 57.83% | 41.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31098` | Yucatán | Tzucacab | 9,866 | 4,641 | 1,080 | 4,145 | 57.99% | 47.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32015` | Zacatecas | El Plateado de Joaquín Amaro | 1,668 | 647 | 321 | 700 | 58.03% | 38.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26013` | Sonora | Bavispe | 1,322 | 648 | 120 | 554 | 58.09% | 49.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20065` | Oaxaca | Nuevo Zoquiápam | 1,218 | 246 | 463 | 509 | 58.21% | 20.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21190` | Puebla | Totoltepec de Guerrero | 983 | 383 | 190 | 410 | 58.29% | 38.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26042` | Sonora | Trincheras | 1,677 | 777 | 207 | 693 | 58.68% | 46.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20183` | Oaxaca | San Juan Bautista Valle Nacional | 16,638 | 4,991 | 4,800 | 6,847 | 58.85% | 30.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20300` | Oaxaca | San Pedro Atoyac | 2,945 | 1,422 | 319 | 1,204 | 59.12% | 48.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16027` | Michoacán | Chucándiro | 4,886 | 1,593 | 1,297 | 1,996 | 59.15% | 32.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14028` | Jalisco | Cuautitlán de García Barragán | 13,667 | 6,570 | 1,532 | 5,565 | 59.28% | 48.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08014` | Chihuahua | Coronado | 1,906 | 942 | 193 | 771 | 59.55% | 49.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20164` | Oaxaca | San José Chiltepec | 8,099 | 3,143 | 1,686 | 3,270 | 59.62% | 38.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20108` | Oaxaca | San Antonio Tepetlapa | 2,803 | 730 | 943 | 1,130 | 59.69% | 26.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19008` | Nuevo León | Bustamante | 3,530 | 1,726 | 393 | 1,411 | 60.03% | 48.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31049` | Yucatán | Mayapán | 2,992 | 1,649 | 148 | 1,195 | 60.06% | 55.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31037` | Yucatán | Huhí | 3,756 | 1,968 | 289 | 1,499 | 60.09% | 52.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31103` | Yucatán | Xocchel | 2,464 | 1,288 | 194 | 982 | 60.15% | 52.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31071` | Yucatán | Sudzal | 1,555 | 851 | 89 | 615 | 60.45% | 54.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14049` | Jalisco | Jamay | 17,264 | 5,772 | 4,667 | 6,825 | 60.47% | 33.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20128` | Oaxaca | San Dionisio Ocotepec | 7,464 | 2,197 | 2,324 | 2,943 | 60.57% | 29.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13001` | Hidalgo | Acatlán | 16,424 | 5,335 | 4,636 | 6,453 | 60.71% | 32.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12040` | Guerrero | Juan R. Escudero | 17,646 | 6,774 | 3,939 | 6,933 | 60.71% | 38.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25003` | Sinaloa | Badiraguato | 23,078 | 7,311 | 6,708 | 9,059 | 60.75% | 31.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16028` | Michoacán | Churintzio | 7,235 | 1,270 | 3,130 | 2,835 | 60.82% | 17.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `32041` | Zacatecas | El Salvador | 2,105 | 1,085 | 196 | 824 | 60.86% | 51.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21116` | Puebla | Quecholac | 33,324 | 13,826 | 6,477 | 13,021 | 60.93% | 41.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14058` | Jalisco | Santa María del Oro | 1,996 | 840 | 385 | 771 | 61.37% | 42.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07034` | Chiapas | Frontera Comalapa | 52,538 | 20,021 | 12,258 | 20,259 | 61.44% | 38.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21054` | Puebla | Chignahuapan | 44,566 | 20,286 | 7,108 | 17,172 | 61.47% | 45.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07042` | Chiapas | Ixhuatán | 7,359 | 3,503 | 1,038 | 2,818 | 61.71% | 47.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21104` | Puebla | Nicolás Bravo | 5,097 | 2,253 | 893 | 1,951 | 61.72% | 44.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20078` | Oaxaca | San Agustín Atenango | 1,551 | 416 | 544 | 591 | 61.90% | 26.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28012` | Tamaulipas | González | 32,840 | 11,414 | 8,926 | 12,500 | 61.94% | 34.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26027` | Sonora | Naco | 4,441 | 1,849 | 908 | 1,684 | 62.08% | 41.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08039` | Chihuahua | López | 3,473 | 1,590 | 569 | 1,314 | 62.17% | 45.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14011` | Jalisco | Atengo | 4,423 | 1,828 | 923 | 1,672 | 62.20% | 41.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26010` | Sonora | Bacoachi | 1,416 | 660 | 222 | 534 | 62.29% | 46.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26048` | Sonora | La Colorada | 2,581 | 1,275 | 333 | 973 | 62.30% | 49.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20192` | Oaxaca | San Juan Cotzocón | 15,847 | 3,308 | 6,580 | 5,959 | 62.40% | 20.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31001` | Yucatán | Abalá | 5,248 | 2,955 | 322 | 1,971 | 62.44% | 56.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20182` | Oaxaca | San Juan Bautista Tuxtepec | 113,778 | 48,678 | 22,414 | 42,686 | 62.48% | 42.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15017` | Estado de México | Ayapango | 5,144 | 2,397 | 823 | 1,924 | 62.60% | 46.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26019` | Sonora | Fronteras | 6,884 | 2,770 | 1,543 | 2,571 | 62.65% | 40.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15099` | Estado de México | Texcalyacac | 4,661 | 2,342 | 580 | 1,739 | 62.69% | 50.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16066` | Michoacán | Paracho | 28,648 | 10,575 | 7,406 | 10,667 | 62.77% | 36.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20414` | Oaxaca | Santa María Huatulco | 39,417 | 15,435 | 9,334 | 14,648 | 62.84% | 39.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21209` | Puebla | Zapotitlán | 6,679 | 3,075 | 1,132 | 2,472 | 62.99% | 46.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12033` | Guerrero | General Heliodoro Castillo | 21,398 | 8,156 | 5,326 | 7,916 | 63.01% | 38.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07082` | Chiapas | Simojovel | 32,431 | 16,241 | 4,244 | 11,946 | 63.16% | 50.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07092` | Chiapas | Tapilula | 9,165 | 4,468 | 1,332 | 3,365 | 63.28% | 48.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20557` | Oaxaca | Unión Hidalgo | 10,171 | 1,801 | 4,636 | 3,734 | 63.29% | 17.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `13009` | Hidalgo | Atitalaquia | 21,326 | 6,852 | 6,652 | 7,822 | 63.32% | 32.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08060` | Chihuahua | Santa Bárbara | 8,500 | 1,696 | 3,695 | 3,109 | 63.42% | 19.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07106` | Chiapas | Venustiano Carranza | 41,601 | 11,544 | 14,897 | 15,160 | 63.56% | 27.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14051` | Jalisco | Jilotlán de los Dolores | 6,550 | 1,459 | 2,709 | 2,382 | 63.63% | 22.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21165` | Puebla | Tepeojuma | 6,715 | 3,047 | 1,227 | 2,441 | 63.65% | 45.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07092` | Chiapas | Tapilula | 9,510 | 4,628 | 1,426 | 3,456 | 63.66% | 48.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `15080` | Estado de México | Soyaniquilpan de Juárez | 7,832 | 3,907 | 1,080 | 2,845 | 63.67% | 49.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31010` | Yucatán | Cantamayec | 1,673 | 973 | 93 | 607 | 63.72% | 58.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24025` | San Luis Potosí | Salinas | 20,546 | 8,192 | 4,904 | 7,450 | 63.74% | 39.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21194` | Puebla | Venustiano Carranza | 20,886 | 9,054 | 4,259 | 7,573 | 63.74% | 43.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05030` | Coahuila | Saltillo | 657,319 | 263,041 | 156,033 | 238,245 | 63.76% | 40.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16057` | Michoacán | Nahuatzen | 21,482 | 7,257 | 6,443 | 7,782 | 63.77% | 33.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13015` | Hidalgo | Cuautepec de Hinojosa | 46,252 | 17,098 | 12,445 | 16,709 | 63.87% | 36.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13079` | Hidalgo | Xochicoatlán | 5,787 | 3,033 | 670 | 2,084 | 63.99% | 52.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `08067` | Chihuahua | Valle de Zaragoza | 2,671 | 975 | 735 | 961 | 64.02% | 36.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16097` | Michoacán | Tumbiscatío | 5,472 | 2,400 | 1,107 | 1,965 | 64.09% | 43.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07117` | Chiapas | San Andrés Duraznal | 4,003 | 2,003 | 564 | 1,436 | 64.13% | 50.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12030` | Guerrero | Eduardo Neri | 38,955 | 15,367 | 9,629 | 13,959 | 64.17% | 39.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30151` | Veracruz | Tamalín | 8,686 | 4,436 | 1,140 | 3,110 | 64.20% | 51.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26043` | Sonora | Tubutama | 1,454 | 664 | 270 | 520 | 64.24% | 45.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12079` | Guerrero | Cochoapa el Grande | 14,727 | 6,790 | 2,671 | 5,266 | 64.24% | 46.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08011` | Chihuahua | Camargo | 36,532 | 8,486 | 14,990 | 13,056 | 64.26% | 23.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07042` | Chiapas | Ixhuatán | 6,755 | 3,589 | 752 | 2,414 | 64.26% | 53.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16100` | Michoacán | Tuzantla | 12,689 | 5,474 | 2,694 | 4,521 | 64.37% | 43.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20149` | Oaxaca | San Francisco Tlapancingo | 1,637 | 430 | 624 | 583 | 64.39% | 26.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19029` | Nuevo León | Higueras | 1,438 | 742 | 184 | 512 | 64.39% | 51.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30128` | Veracruz | La Perla | 12,850 | 4,414 | 3,872 | 4,564 | 64.48% | 34.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16021` | Michoacán | Charapan | 9,174 | 4,020 | 1,909 | 3,245 | 64.63% | 43.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30140` | Veracruz | Saltabarranca | 4,879 | 2,029 | 1,133 | 1,717 | 64.81% | 41.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21143` | Puebla | San Salvador el Seco | 21,269 | 9,555 | 4,243 | 7,471 | 64.87% | 44.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25003` | Sinaloa | Badiraguato | 22,814 | 9,302 | 5,510 | 8,002 | 64.93% | 40.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20164` | Oaxaca | San José Chiltepec | 8,670 | 4,302 | 1,332 | 3,036 | 64.98% | 49.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14017` | Jalisco | Ayutla | 10,512 | 4,113 | 2,722 | 3,677 | 65.02% | 39.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08018` | Chihuahua | Cusihuiriachi | 5,557 | 2,128 | 1,495 | 1,934 | 65.20% | 38.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28035` | Tamaulipas | San Fernando | 38,481 | 16,913 | 8,198 | 13,370 | 65.26% | 43.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28027` | Tamaulipas | Nuevo Laredo | 340,557 | 123,668 | 98,752 | 118,137 | 65.31% | 36.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07005` | Chiapas | Amatán | 16,480 | 7,832 | 2,969 | 5,679 | 65.54% | 47.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16001` | Michoacán | Acuitzio | 7,925 | 2,004 | 3,195 | 2,726 | 65.60% | 25.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31030` | Yucatán | Dzitás | 3,137 | 1,825 | 234 | 1,078 | 65.64% | 58.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31021` | Yucatán | Chichimilá | 6,990 | 4,125 | 466 | 2,399 | 65.68% | 59.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29054` | Tlaxcala | Emiliano Zapata | 3,624 | 1,985 | 398 | 1,241 | 65.76% | 54.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13002` | Hidalgo | Acaxochitlán | 29,946 | 11,395 | 8,310 | 10,241 | 65.80% | 38.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11035` | Guanajuato | Santa Cruz de Juventino Rosas | 60,770 | 21,791 | 18,266 | 20,713 | 65.92% | 35.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20156` | Oaxaca | San Jerónimo Coatlán | 3,057 | 1,020 | 997 | 1,040 | 65.98% | 33.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08035` | Chihuahua | Janos | 7,582 | 2,731 | 2,279 | 2,572 | 66.08% | 36.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20264` | Oaxaca | San Miguel Coatlán | 2,032 | 494 | 849 | 689 | 66.09% | 24.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20332` | Oaxaca | Villa de Tututepec de Melchor Ocampo | 31,726 | 6,741 | 14,237 | 10,748 | 66.12% | 21.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21047` | Puebla | Chapulco | 5,784 | 2,853 | 972 | 1,959 | 66.13% | 49.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20127` | Oaxaca | San Dionisio del Mar | 4,122 | 1,998 | 728 | 1,396 | 66.13% | 48.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31039` | Yucatán | Ixil | 3,219 | 1,853 | 279 | 1,087 | 66.23% | 57.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20265` | Oaxaca | San Miguel del Puerto | 6,583 | 1,689 | 2,673 | 2,221 | 66.26% | 25.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08045` | Chihuahua | Meoqui | 37,879 | 12,402 | 12,738 | 12,739 | 66.37% | 32.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31093` | Yucatán | Tixkokob | 12,798 | 7,029 | 1,465 | 4,304 | 66.37% | 54.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07005` | Chiapas | Amatán | 14,462 | 8,131 | 1,472 | 4,859 | 66.40% | 56.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20464` | Oaxaca | Santiago Huauclilla | 432 | 84 | 203 | 145 | 66.44% | 19.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21083` | Puebla | Ixcamilpa de Guerrero | 3,024 | 1,441 | 568 | 1,015 | 66.44% | 47.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15042` | Estado de México | Ixtapan del Oro | 4,770 | 2,687 | 482 | 1,601 | 66.44% | 56.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04013` | Campeche | Seybaplaya | 12,016 | 5,832 | 2,154 | 4,030 | 66.46% | 48.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21217` | Puebla | Zoquitlán | 12,477 | 6,218 | 2,079 | 4,180 | 66.50% | 49.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20064` | Oaxaca | Nejapa de Madero | 5,976 | 1,982 | 1,994 | 2,000 | 66.53% | 33.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20263` | Oaxaca | San Miguel Chimalapa | 4,577 | 1,155 | 1,893 | 1,529 | 66.59% | 25.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20353` | Oaxaca | Santa Ana | 1,519 | 367 | 645 | 507 | 66.62% | 24.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20529` | Oaxaca | Santo Tomás Tamazulapan | 1,531 | 330 | 690 | 511 | 66.62% | 21.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26050` | Sonora | Mazatán | 1,517 | 874 | 137 | 506 | 66.64% | 57.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20527` | Oaxaca | Santo Tomás Mazaltepec | 1,694 | 562 | 567 | 565 | 66.65% | 33.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07089` | Chiapas | Sunuapa | 1,860 | 1,077 | 163 | 620 | 66.67% | 57.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31016` | Yucatán | Chacsinkín | 1,962 | 1,238 | 70 | 654 | 66.67% | 63.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31043` | Yucatán | Kaua | 2,196 | 1,373 | 91 | 732 | 66.67% | 62.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21138` | Puebla | San Nicolás Buenos Aires | 7,402 | 3,705 | 1,235 | 2,462 | 66.74% | 50.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07036` | Chiapas | La Grandeza | 4,509 | 2,040 | 970 | 1,499 | 66.76% | 45.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20264` | Oaxaca | San Miguel Coatlán | 2,149 | 699 | 736 | 714 | 66.78% | 32.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08015` | Chihuahua | Coyame del Sotol | 2,275 | 1,137 | 383 | 755 | 66.81% | 49.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16091` | Michoacán | Tingambato | 10,752 | 5,242 | 1,944 | 3,566 | 66.83% | 48.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07018` | Chiapas | Coapilla | 6,867 | 3,491 | 1,100 | 2,276 | 66.86% | 50.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08023` | Chihuahua | Galeana | 5,561 | 2,014 | 1,706 | 1,841 | 66.89% | 36.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16005` | Michoacán | Angangueo | 8,106 | 3,613 | 1,813 | 2,680 | 66.94% | 44.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14022` | Jalisco | Cihuatlán | 27,129 | 9,716 | 8,453 | 8,960 | 66.97% | 35.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29027` | Tlaxcala | Tenancingo | 9,116 | 3,601 | 2,506 | 3,009 | 66.99% | 39.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19015` | Nuevo León | Dr. Coss | 2,900 | 1,256 | 687 | 957 | 67.00% | 43.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08058` | Chihuahua | San Francisco de Conchos | 2,570 | 1,256 | 467 | 847 | 67.04% | 48.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08015` | Chihuahua | Coyame del Sotol | 2,290 | 1,072 | 464 | 754 | 67.07% | 46.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16091` | Michoacán | Tingambato | 11,564 | 4,981 | 2,784 | 3,799 | 67.15% | 43.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26052` | Sonora | Pitiquito | 5,921 | 2,704 | 1,272 | 1,945 | 67.15% | 45.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26014` | Sonora | Benjamín Hill | 3,815 | 1,653 | 913 | 1,249 | 67.26% | 43.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26070` | Sonora | General Plutarco Elías Calles | 10,243 | 3,879 | 3,021 | 3,343 | 67.36% | 37.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16091` | Michoacán | Tingambato | 9,899 | 4,941 | 1,734 | 3,224 | 67.43% | 49.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20250` | Oaxaca | San Mateo Peñasco | 1,514 | 564 | 457 | 493 | 67.44% | 37.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21062` | Puebla | Eloxochitlán | 8,683 | 5,004 | 866 | 2,813 | 67.60% | 57.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07006` | Chiapas | Amatenango de la Frontera | 23,022 | 9,116 | 6,453 | 7,453 | 67.63% | 39.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21210` | Puebla | Zapotitlán de Méndez | 4,022 | 2,260 | 466 | 1,296 | 67.78% | 56.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07037` | Chiapas | Huehuetán | 24,867 | 7,091 | 9,782 | 7,994 | 67.85% | 28.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20211` | Oaxaca | San Juan Ozolotepec | 2,152 | 701 | 760 | 691 | 67.89% | 32.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26011` | Sonora | Banámichi | 1,459 | 841 | 151 | 467 | 67.99% | 57.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `29057` | Tlaxcala | San Lucas Tecopilco | 2,299 | 957 | 610 | 732 | 68.16% | 41.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26025` | Sonora | Magdalena | 22,663 | 8,373 | 7,088 | 7,202 | 68.22% | 36.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12065` | Guerrero | Tlalchapa | 9,941 | 4,548 | 2,242 | 3,151 | 68.30% | 45.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20012` | Oaxaca | El Barrio de la Soledad | 10,408 | 5,177 | 1,935 | 3,296 | 68.33% | 49.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28042` | Tamaulipas | Villagrán | 4,443 | 2,423 | 614 | 1,406 | 68.35% | 54.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08029` | Chihuahua | Guadalupe y Calvo | 33,189 | 12,291 | 10,440 | 10,458 | 68.49% | 37.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14021` | Jalisco | Casimiro Castillo | 16,078 | 5,459 | 5,572 | 5,047 | 68.61% | 33.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07026` | Chiapas | Chenalhó | 37,994 | 17,800 | 8,299 | 11,895 | 68.69% | 46.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30212` | Veracruz | Santiago Sochiapan | 8,363 | 2,660 | 3,085 | 2,618 | 68.70% | 31.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31094` | Yucatán | Tixmehuac | 3,795 | 2,457 | 153 | 1,185 | 68.77% | 64.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16047` | Michoacán | Juárez | 10,733 | 5,079 | 2,307 | 3,347 | 68.82% | 47.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25017` | Sinaloa | Sinaloa | 64,798 | 24,338 | 20,314 | 20,146 | 68.91% | 37.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08020` | Chihuahua | Chínipas | 4,906 | 2,324 | 1,061 | 1,521 | 69.00% | 47.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20190` | Oaxaca | San Juan Colorado | 5,989 | 2,432 | 1,705 | 1,852 | 69.08% | 40.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07118` | Chiapas | Santiago El Pinar | 1,690 | 876 | 292 | 522 | 69.11% | 51.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19038` | Nuevo León | Mina | 4,944 | 2,356 | 1,062 | 1,526 | 69.13% | 47.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12013` | Guerrero | Azoyú | 10,656 | 5,325 | 2,044 | 3,287 | 69.15% | 49.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `12026` | Guerrero | Cuetzala del Progreso | 6,231 | 2,978 | 1,331 | 1,922 | 69.15% | 47.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20434` | Oaxaca | Santa María Temaxcaltepec | 1,682 | 592 | 572 | 518 | 69.20% | 35.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31087` | Yucatán | Tetiz | 4,082 | 2,386 | 441 | 1,255 | 69.26% | 58.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26024` | Sonora | Imuris | 10,476 | 3,828 | 3,428 | 3,220 | 69.26% | 36.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21024` | Puebla | Axutla | 1,218 | 553 | 291 | 374 | 69.29% | 45.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07105` | Chiapas | Unión Juárez | 10,580 | 4,048 | 3,288 | 3,244 | 69.34% | 38.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07096` | Chiapas | Tila | 47,198 | 26,365 | 6,413 | 14,420 | 69.45% | 55.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12041` | Guerrero | Leonardo Bravo | 16,216 | 8,283 | 2,981 | 4,952 | 69.46% | 51.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08008` | Chihuahua | Batopilas | 8,191 | 2,440 | 3,253 | 2,498 | 69.50% | 29.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07062` | Chiapas | Ostuacán | 13,447 | 6,964 | 2,390 | 4,093 | 69.56% | 51.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21098` | Puebla | Mazapiltepec de Juárez | 2,092 | 1,087 | 369 | 636 | 69.60% | 51.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26070` | Sonora | General Plutarco Elías Calles | 10,257 | 3,816 | 3,334 | 3,107 | 69.71% | 37.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12057` | Guerrero | Tecoanapa | 29,140 | 15,034 | 5,288 | 8,818 | 69.74% | 51.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31088` | Yucatán | Teya | 1,616 | 947 | 180 | 489 | 69.74% | 58.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20393` | Oaxaca | Santa Lucía Miahuatlán | 1,935 | 489 | 861 | 585 | 69.77% | 25.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07073` | Chiapas | Reforma | 31,935 | 14,607 | 7,713 | 9,615 | 69.89% | 45.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19030` | Nuevo León | Hualahuises | 6,147 | 2,927 | 1,374 | 1,846 | 69.97% | 47.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20181` | Oaxaca | San Juan Bautista Tlacoatzintepec | 1,800 | 1,126 | 134 | 540 | 70.00% | 62.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16037` | Michoacán | Huaniqueo | 7,961 | 2,750 | 2,838 | 2,373 | 70.19% | 34.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08007` | Chihuahua | Balleza | 13,759 | 4,966 | 4,693 | 4,100 | 70.20% | 36.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08056` | Chihuahua | Rosario | 2,143 | 944 | 563 | 636 | 70.32% | 44.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20337` | Oaxaca | San Pedro Yólox | 1,675 | 770 | 408 | 497 | 70.33% | 45.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31077` | Yucatán | Tekal de Venegas | 2,357 | 1,481 | 177 | 699 | 70.34% | 62.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29014` | Tlaxcala | Hueyotlipan | 11,283 | 5,001 | 2,952 | 3,330 | 70.49% | 44.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21196` | Puebla | Xayacatlán de Bravo | 1,428 | 797 | 210 | 421 | 70.52% | 55.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19001` | Nuevo León | Abasolo | 2,512 | 1,418 | 355 | 739 | 70.58% | 56.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21117` | Puebla | Quimixtlán | 13,166 | 7,468 | 1,846 | 3,852 | 70.74% | 56.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15059` | Estado de México | Nextlalpan | 31,281 | 12,947 | 9,194 | 9,140 | 70.78% | 41.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08061` | Chihuahua | Satevó | 4,064 | 1,835 | 1,042 | 1,187 | 70.79% | 45.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19028` | Nuevo León | Hidalgo | 13,163 | 5,655 | 3,670 | 3,838 | 70.84% | 42.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20265` | Oaxaca | San Miguel del Puerto | 4,986 | 1,885 | 1,653 | 1,448 | 70.96% | 37.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19029` | Nuevo León | Higueras | 1,475 | 879 | 170 | 426 | 71.12% | 59.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20509` | Oaxaca | Santo Domingo Ingenio | 6,567 | 3,300 | 1,371 | 1,896 | 71.13% | 50.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26037` | Sonora | Santa Cruz | 1,347 | 657 | 303 | 387 | 71.27% | 48.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26038` | Sonora | Sáric | 1,800 | 970 | 313 | 517 | 71.28% | 53.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16021` | Michoacán | Charapan | 8,568 | 4,702 | 1,407 | 2,459 | 71.30% | 54.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07067` | Chiapas | Pantepec | 7,459 | 4,559 | 762 | 2,138 | 71.34% | 61.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12021` | Guerrero | Coyuca de Benítez | 50,996 | 22,130 | 14,258 | 14,608 | 71.35% | 43.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19001` | Nuevo León | Abasolo | 2,596 | 1,469 | 385 | 742 | 71.42% | 56.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19016` | Nuevo León | Dr. González | 3,331 | 1,666 | 713 | 952 | 71.42% | 50.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26038` | Sonora | Sáric | 2,022 | 1,102 | 343 | 577 | 71.46% | 54.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30164` | Veracruz | Tepatlaxco | 6,679 | 4,180 | 597 | 1,902 | 71.52% | 62.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08028` | Chihuahua | Guadalupe | 4,872 | 2,227 | 1,258 | 1,387 | 71.53% | 45.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21175` | Puebla | Tilapa | 7,215 | 3,305 | 1,864 | 2,046 | 71.64% | 45.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26045` | Sonora | Villa Pesqueira | 2,005 | 1,229 | 209 | 567 | 71.72% | 61.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19036` | Nuevo León | Melchor Ocampo | 1,698 | 1,005 | 213 | 480 | 71.73% | 59.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31034` | Yucatán | Hocabá | 4,984 | 3,069 | 507 | 1,408 | 71.75% | 61.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31054` | Yucatán | Muxupip | 2,241 | 1,449 | 163 | 629 | 71.93% | 64.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07071` | Chiapas | Pueblo Nuevo Solistahuacán | 17,589 | 9,941 | 2,714 | 4,934 | 71.95% | 56.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25002` | Sinaloa | Angostura | 37,425 | 17,649 | 9,283 | 10,493 | 71.96% | 47.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16025` | Michoacán | Chilchota | 30,638 | 13,430 | 8,621 | 8,587 | 71.97% | 43.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `11007` | Guanajuato | Celaya | 350,417 | 104,458 | 147,975 | 97,984 | 72.04% | 29.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08067` | Chihuahua | Valle de Zaragoza | 4,378 | 1,984 | 1,170 | 1,224 | 72.04% | 45.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07031` | Chiapas | Chilón | 71,900 | 34,706 | 17,094 | 20,100 | 72.04% | 48.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20530` | Oaxaca | Santos Reyes Nopala | 11,022 | 3,428 | 4,519 | 3,075 | 72.10% | 31.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31045` | Yucatán | Kopomá | 2,072 | 1,253 | 242 | 577 | 72.15% | 60.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08004` | Chihuahua | Aquiles Serdán | 13,607 | 4,218 | 5,601 | 3,788 | 72.16% | 31.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `11001` | Guanajuato | Abasolo | 64,501 | 23,844 | 22,719 | 17,938 | 72.19% | 36.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08057` | Chihuahua | San Francisco de Borja | 2,335 | 674 | 1,012 | 649 | 72.21% | 28.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07123` | Chiapas | Mezcalapa | 17,488 | 8,489 | 4,149 | 4,850 | 72.27% | 48.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20061` | Oaxaca | Monjas | 2,193 | 803 | 782 | 608 | 72.28% | 36.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31045` | Yucatán | Kopomá | 1,922 | 1,133 | 257 | 532 | 72.32% | 58.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21007` | Puebla | Ahuatlán | 2,490 | 1,129 | 675 | 686 | 72.45% | 45.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16059` | Michoacán | Nuevo Parangaricutiro | 15,655 | 7,343 | 4,004 | 4,308 | 72.48% | 46.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19031` | Nuevo León | Iturbide | 3,299 | 1,990 | 402 | 907 | 72.51% | 60.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12053` | Guerrero | San Luis Acatlán | 27,802 | 13,165 | 7,007 | 7,630 | 72.56% | 47.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15118` | Estado de México | Zacualpan | 10,586 | 5,521 | 2,168 | 2,897 | 72.63% | 52.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08065` | Chihuahua | Urique | 14,047 | 6,341 | 3,862 | 3,844 | 72.63% | 45.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20240` | Oaxaca | San Martín Itunyoso | 1,784 | 691 | 605 | 488 | 72.65% | 38.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14105` | Jalisco | Totatiche | 3,981 | 1,941 | 952 | 1,088 | 72.67% | 48.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12009` | Guerrero | Atlamajalcingo del Monte | 3,784 | 1,907 | 843 | 1,034 | 72.67% | 50.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29035` | Tlaxcala | Tocatlán | 4,897 | 2,571 | 989 | 1,337 | 72.70% | 52.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07053` | Chiapas | Mazapa de Madero | 5,822 | 3,211 | 1,022 | 1,589 | 72.71% | 55.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31069` | Yucatán | Sotuta | 6,002 | 3,378 | 989 | 1,635 | 72.76% | 56.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16013` | Michoacán | Carácuaro | 7,441 | 3,897 | 1,518 | 2,026 | 72.77% | 52.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31067` | Yucatán | Seyé | 8,041 | 4,863 | 992 | 2,186 | 72.81% | 60.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07074` | Chiapas | Las Rosas | 19,188 | 10,358 | 3,615 | 5,215 | 72.82% | 53.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31086` | Yucatán | Tepakán | 2,048 | 1,339 | 153 | 556 | 72.85% | 65.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19035` | Nuevo León | Marín | 4,984 | 2,394 | 1,237 | 1,353 | 72.85% | 48.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15078` | Estado de México | San Simón de Guerrero | 4,938 | 3,041 | 557 | 1,340 | 72.86% | 61.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25018` | Sinaloa | Navolato | 112,620 | 43,541 | 38,554 | 30,525 | 72.90% | 38.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20121` | Oaxaca | Heroica Villa de San Blas Atempa | 15,550 | 8,353 | 2,983 | 4,214 | 72.90% | 53.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08015` | Chihuahua | Coyame del Sotol | 2,299 | 1,207 | 469 | 623 | 72.90% | 52.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20496` | Oaxaca | Santiago Xanica | 2,196 | 681 | 920 | 595 | 72.91% | 31.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31017` | Yucatán | Chankom | 3,898 | 2,657 | 185 | 1,056 | 72.91% | 68.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07083` | Chiapas | Sitalá | 8,586 | 4,868 | 1,392 | 2,326 | 72.91% | 56.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32028` | Zacatecas | Mezquital del Oro | 2,349 | 1,188 | 527 | 634 | 73.01% | 50.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `10020` | Durango | Otáez | 3,876 | 1,316 | 1,518 | 1,042 | 73.12% | 33.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14063` | Jalisco | Mezquitic | 14,624 | 7,502 | 3,192 | 3,930 | 73.13% | 51.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26029` | Sonora | Nacozari de García | 10,017 | 4,609 | 2,718 | 2,690 | 73.15% | 46.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14063` | Jalisco | Mezquitic | 13,570 | 7,023 | 2,903 | 3,644 | 73.15% | 51.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20519` | Oaxaca | Santo Domingo Tomaltepec | 2,361 | 639 | 1,088 | 634 | 73.15% | 27.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07003` | Chiapas | Acapetahua | 19,567 | 6,172 | 8,143 | 5,252 | 73.16% | 31.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16074` | Michoacán | Quiroga | 22,943 | 9,991 | 6,795 | 6,157 | 73.16% | 43.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20567` | Oaxaca | San Mateo Yucutindoo | 1,934 | 619 | 796 | 519 | 73.16% | 32.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12020` | Guerrero | Copanatoyac | 11,925 | 6,152 | 2,573 | 3,200 | 73.17% | 51.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10026` | Durango | San Bernardo | 2,730 | 1,062 | 937 | 731 | 73.22% | 38.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21159` | Puebla | Teotlalco | 2,622 | 1,299 | 624 | 699 | 73.34% | 49.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12027` | Guerrero | Cutzamala de Pinzón | 18,296 | 8,210 | 5,213 | 4,873 | 73.37% | 44.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20059` | Oaxaca | Miahuatlán de Porfirio Díaz | 30,977 | 4,171 | 18,557 | 8,249 | 73.37% | 13.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07122` | Chiapas | El Parral | 909 | 496 | 171 | 242 | 73.38% | 54.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12066` | Guerrero | Tlalixtaquilla de Maldonado | 5,058 | 2,360 | 1,353 | 1,345 | 73.41% | 46.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19041` | Nuevo León | Parás | 1,851 | 1,124 | 236 | 491 | 73.47% | 60.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19020` | Nuevo León | General Bravo | 5,852 | 2,692 | 1,610 | 1,550 | 73.51% | 46.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20331` | Oaxaca | San Pedro Totolápam | 2,479 | 860 | 963 | 656 | 73.54% | 34.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16112` | Michoacán | Ziracuaretiro | 13,168 | 5,587 | 4,099 | 3,482 | 73.56% | 42.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20456` | Oaxaca | Santiago Ayuquililla | 2,014 | 896 | 586 | 532 | 73.58% | 44.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12043` | Guerrero | Mártir de Cuilapan | 12,304 | 5,949 | 3,107 | 3,248 | 73.60% | 48.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31106` | Yucatán | Yobaín | 2,118 | 1,367 | 192 | 559 | 73.61% | 64.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20506` | Oaxaca | Santo Domingo Armenta | 2,406 | 1,252 | 520 | 634 | 73.65% | 52.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08035` | Chihuahua | Janos | 7,083 | 1,166 | 4,052 | 1,865 | 73.67% | 16.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07098` | Chiapas | Totolapa | 5,621 | 3,366 | 777 | 1,478 | 73.71% | 59.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20191` | Oaxaca | San Juan Comaltepec | 1,681 | 419 | 820 | 442 | 73.71% | 24.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12068` | Guerrero | Tlapehuala | 16,842 | 8,854 | 3,560 | 4,428 | 73.71% | 52.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21039` | Puebla | Cuapiaxtla De Madero | 6,876 | 3,236 | 1,833 | 1,807 | 73.72% | 47.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08046` | Chihuahua | Morelos | 4,619 | 736 | 2,670 | 1,213 | 73.74% | 15.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15067` | Estado de México | Otzoloapan | 4,171 | 2,306 | 770 | 1,095 | 73.75% | 55.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16036` | Michoacán | Huandacareo | 10,456 | 2,646 | 5,073 | 2,737 | 73.82% | 25.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16033` | Michoacán | Gabriel Zamora | 16,582 | 6,013 | 6,239 | 4,330 | 73.89% | 36.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08065` | Chihuahua | Urique | 13,326 | 6,469 | 3,380 | 3,477 | 73.91% | 48.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31106` | Yucatán | Yobaín | 1,971 | 1,317 | 140 | 514 | 73.92% | 66.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31106` | Yucatán | Yobaín | 2,146 | 1,427 | 160 | 559 | 73.95% | 66.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `32007` | Zacatecas | Concepción del Oro | 9,441 | 4,875 | 2,108 | 2,458 | 73.96% | 51.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `14029` | Jalisco | Cuautla | 2,067 | 1,070 | 459 | 538 | 73.97% | 51.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24001` | San Luis Potosí | Ahualulco | 13,632 | 6,901 | 3,185 | 3,546 | 73.99% | 50.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08043` | Chihuahua | Matachí | 2,935 | 743 | 1,429 | 763 | 74.00% | 25.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `03002` | Baja California Sur | Mulegé | 37,886 | 16,217 | 11,829 | 9,840 | 74.03% | 42.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29046` | Tlaxcala | Santa Cruz Quilehtla | 5,169 | 2,784 | 1,044 | 1,341 | 74.06% | 53.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20446` | Oaxaca | Santa María Yosoyúa | 1,150 | 525 | 327 | 298 | 74.09% | 45.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08008` | Chihuahua | Batopilas de Manuel Gómez Morín | 8,045 | 3,603 | 2,365 | 2,077 | 74.18% | 44.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31095` | Yucatán | Tixpéhual | 4,164 | 2,708 | 381 | 1,075 | 74.18% | 65.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19012` | Nuevo León | Ciénega de Flores | 31,320 | 10,826 | 12,428 | 8,066 | 74.25% | 34.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07011` | Chiapas | Bella Vista | 13,832 | 6,946 | 3,334 | 3,552 | 74.32% | 50.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14021` | Jalisco | Casimiro Castillo | 16,751 | 5,963 | 6,487 | 4,301 | 74.32% | 35.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08061` | Chihuahua | Satevó | 4,491 | 1,366 | 1,972 | 1,153 | 74.33% | 30.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31100` | Yucatán | Ucú | 2,769 | 1,691 | 369 | 709 | 74.40% | 61.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28004` | Tamaulipas | Antiguo Morelos | 7,388 | 4,016 | 1,481 | 1,891 | 74.40% | 54.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08046` | Chihuahua | Morelos | 5,402 | 2,835 | 1,186 | 1,381 | 74.44% | 52.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21010` | Puebla | Ajalpan | 41,977 | 24,823 | 6,432 | 10,722 | 74.46% | 59.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15098` | Estado de México | Texcaltitlán | 12,979 | 7,455 | 2,211 | 3,313 | 74.47% | 57.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31058` | Yucatán | Peto | 18,070 | 10,262 | 3,200 | 4,608 | 74.50% | 56.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25002` | Sinaloa | Angostura | 35,903 | 18,940 | 7,811 | 9,152 | 74.51% | 52.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08022` | Chihuahua | Dr. Belisario Domínguez | 3,064 | 865 | 1,418 | 781 | 74.51% | 28.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15004` | Estado de México | Almoloya de Alquisiras | 11,863 | 6,641 | 2,202 | 3,020 | 74.54% | 55.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26032` | Sonora | Sahuaripa | 4,638 | 2,025 | 1,436 | 1,177 | 74.62% | 43.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31028` | Yucatán | Dzilam de Bravo | 2,375 | 1,578 | 195 | 602 | 74.65% | 66.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15102` | Estado de México | Tianguistenco | 62,882 | 30,836 | 16,114 | 15,932 | 74.66% | 49.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24056` | San Luis Potosí | Zaragoza | 20,721 | 9,978 | 5,494 | 5,249 | 74.67% | 48.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25003` | Sinaloa | Badiraguato | 22,950 | 10,126 | 7,011 | 5,813 | 74.67% | 44.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `03001` | Baja California Sur | Comondú | 50,686 | 23,028 | 14,836 | 12,822 | 74.70% | 45.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31100` | Yucatán | Ucú | 2,571 | 1,594 | 327 | 650 | 74.72% | 62.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12047` | Guerrero | Ometepec | 40,253 | 20,457 | 9,634 | 10,162 | 74.75% | 50.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16066` | Michoacán | Parácuaro | 27,223 | 11,130 | 9,231 | 6,862 | 74.79% | 40.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14098` | Jalisco | Tlajomulco de Zúñiga | 331,698 | 128,058 | 120,278 | 83,362 | 74.87% | 38.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04010` | Campeche | Candelaria | 36,016 | 15,878 | 11,088 | 9,050 | 74.87% | 44.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23001` | Quintana Roo | Benito Juárez | 497,563 | 125,647 | 247,015 | 124,901 | 74.90% | 25.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26027` | Sonora | Naco | 4,928 | 2,488 | 1,203 | 1,237 | 74.90% | 50.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26048` | Sonora | La Colorada | 2,704 | 1,725 | 301 | 678 | 74.93% | 63.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19022` | Nuevo León | General Terán | 13,304 | 5,608 | 4,362 | 3,334 | 74.94% | 42.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31105` | Yucatán | Yaxkukul | 2,319 | 1,485 | 254 | 580 | 74.99% | 64.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31016` | Yucatán | Chacsinkín | 2,455 | 1,704 | 137 | 614 | 74.99% | 69.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07071` | Chiapas | Pueblo Nuevo Solistahuacán | 19,015 | 11,728 | 2,533 | 4,754 | 75.00% | 61.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21170` | Puebla | Tepeyahualco de Cuauhtémoc | 2,712 | 1,682 | 352 | 678 | 75.00% | 62.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07058` | Chiapas | Nicolás Ruíz | 2,805 | 1,314 | 790 | 701 | 75.01% | 46.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20498` | Oaxaca | Santiago Yaitepec | 2,749 | 1,411 | 651 | 687 | 75.01% | 51.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31043` | Yucatán | Kaua | 2,477 | 1,706 | 152 | 619 | 75.01% | 68.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14111` | Jalisco | Unión de Tula | 11,775 | 5,016 | 3,817 | 2,942 | 75.01% | 42.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31105` | Yucatán | Yaxkukul | 2,442 | 1,643 | 189 | 610 | 75.02% | 67.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20151` | Oaxaca | San Ildefonso Amatlán | 1,574 | 591 | 591 | 392 | 75.10% | 37.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19036` | Nuevo León | Melchor Ocampo | 2,088 | 1,078 | 492 | 518 | 75.19% | 51.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26046` | Sonora | Caborca | 57,916 | 20,312 | 23,236 | 14,368 | 75.19% | 35.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08012` | Chihuahua | Carichí | 7,242 | 3,595 | 1,862 | 1,785 | 75.35% | 49.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24019` | San Luis Potosí | Lagunillas | 4,857 | 2,335 | 1,326 | 1,196 | 75.38% | 48.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08055` | Chihuahua | Rosales | 13,468 | 6,360 | 3,795 | 3,313 | 75.40% | 47.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16005` | Michoacán | Angangueo | 8,327 | 4,172 | 2,109 | 2,046 | 75.43% | 50.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07053` | Chiapas | Mazapa de Madero | 5,541 | 2,499 | 1,681 | 1,361 | 75.44% | 45.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07033` | Chiapas | Francisco León | 5,324 | 3,037 | 980 | 1,307 | 75.45% | 57.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21064` | Puebla | Esperanza | 10,175 | 5,537 | 2,144 | 2,494 | 75.49% | 54.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19033` | Nuevo León | Lampazos de Naranjo | 4,754 | 2,731 | 858 | 1,165 | 75.49% | 57.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12037` | Guerrero | Igualapa | 7,292 | 4,328 | 1,179 | 1,785 | 75.52% | 59.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `10012` | Durango | Lerdo | 101,002 | 30,296 | 46,117 | 24,589 | 75.65% | 30.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30086` | Veracruz | Ixmatlahuacan | 4,809 | 2,304 | 1,335 | 1,170 | 75.67% | 47.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12070` | Guerrero | Xalpatláhuac | 9,715 | 5,144 | 2,208 | 2,363 | 75.68% | 52.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25011` | Sinaloa | Guasave | 217,198 | 89,721 | 74,729 | 52,748 | 75.71% | 41.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23008` | Quintana Roo | Solidaridad | 151,709 | 31,455 | 83,500 | 36,754 | 75.77% | 20.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29035` | Tlaxcala | Tocatlán | 4,666 | 2,669 | 867 | 1,130 | 75.78% | 57.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16074` | Michoacán | Quiroga | 20,498 | 9,692 | 5,843 | 4,963 | 75.79% | 47.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20528` | Oaxaca | Santo Tomás Ocotepec | 2,675 | 1,212 | 816 | 647 | 75.81% | 45.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07067` | Chiapas | Pantepec | 9,245 | 5,411 | 1,613 | 2,221 | 75.98% | 58.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12051` | Guerrero | Pungarabato | 28,388 | 12,523 | 9,052 | 6,813 | 76.00% | 44.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19003` | Nuevo León | Los Aldamas | 2,214 | 1,140 | 543 | 531 | 76.02% | 51.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05029` | Coahuila | Sacramento | 1,889 | 1,243 | 193 | 453 | 76.02% | 65.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07120` | Chiapas | Rincón Chamula San Pedro | 5,125 | 2,397 | 1,499 | 1,229 | 76.02% | 46.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12078` | Guerrero | Iliatenco | 6,738 | 3,900 | 1,228 | 1,610 | 76.11% | 57.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30140` | Veracruz | Saltabarranca | 4,875 | 2,211 | 1,500 | 1,164 | 76.12% | 45.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20168` | Oaxaca | San José Lachiguiri | 2,721 | 1,036 | 1,036 | 649 | 76.15% | 38.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20277` | Oaxaca | San Miguel Suchixtepec | 2,256 | 714 | 1,004 | 538 | 76.15% | 31.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07106` | Chiapas | Venustiano Carranza | 48,266 | 18,254 | 18,518 | 11,494 | 76.19% | 37.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32033` | Zacatecas | Moyahua de Estrada | 4,942 | 1,901 | 1,865 | 1,176 | 76.20% | 38.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14089` | Jalisco | Tecolotlán | 14,103 | 7,254 | 3,494 | 3,355 | 76.21% | 51.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12069` | Guerrero | La Unión de Isidoro Montes de Oca | 21,328 | 11,215 | 5,041 | 5,072 | 76.22% | 52.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `10007` | Durango | Gómez Palacio | 236,295 | 67,940 | 112,208 | 56,147 | 76.24% | 28.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26060` | Sonora | Empalme | 41,003 | 16,203 | 15,066 | 9,734 | 76.26% | 39.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19025` | Nuevo León | General Zuazua | 46,179 | 14,601 | 20,621 | 10,957 | 76.27% | 31.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21154` | Puebla | Tecomatlán | 4,809 | 1,913 | 1,756 | 1,140 | 76.29% | 39.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `27004` | Tabasco | Centro | 505,371 | 257,271 | 128,356 | 119,744 | 76.31% | 50.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08027` | Chihuahua | Guachochi | 35,538 | 15,752 | 11,367 | 8,419 | 76.31% | 44.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16027` | Michoacán | Chucándiro | 6,256 | 1,256 | 3,518 | 1,482 | 76.31% | 20.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12012` | Guerrero | Ayutla de los Libres | 39,471 | 19,419 | 10,702 | 9,350 | 76.31% | 49.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08035` | Chihuahua | Janos | 8,150 | 3,016 | 3,207 | 1,927 | 76.36% | 37.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16032` | Michoacán | Erongarícuaro | 12,770 | 6,865 | 2,888 | 3,017 | 76.37% | 53.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20499` | Oaxaca | Santiago Yaveo | 4,397 | 1,134 | 2,225 | 1,038 | 76.39% | 25.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `15040` | Estado de México | Ixtapaluca | 254,593 | 92,426 | 102,148 | 60,019 | 76.43% | 36.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24024` | San Luis Potosí | Rioverde | 82,932 | 32,878 | 30,522 | 19,532 | 76.45% | 39.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `21142` | Puebla | San Pedro Yeloixtlahuaca | 2,966 | 1,444 | 825 | 697 | 76.50% | 48.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15111` | Estado de México | Valle de Bravo | 50,958 | 27,967 | 11,043 | 11,948 | 76.55% | 54.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07045` | Chiapas | Ixtapangajoya | 4,898 | 2,905 | 846 | 1,147 | 76.58% | 59.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21007` | Puebla | Ahuatlán | 2,400 | 1,162 | 676 | 562 | 76.58% | 48.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25015` | Sinaloa | Salvador Alvarado | 60,843 | 28,879 | 17,739 | 14,225 | 76.62% | 47.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24020` | San Luis Potosí | Matehuala | 67,069 | 24,130 | 27,270 | 15,669 | 76.64% | 35.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12030` | Guerrero | Eduardo Neri | 32,431 | 15,543 | 9,320 | 7,568 | 76.66% | 47.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30189` | Veracruz | Tuxtilla | 1,944 | 1,144 | 347 | 453 | 76.70% | 58.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21185` | Puebla | Tlapanalá | 7,178 | 3,647 | 1,861 | 1,670 | 76.73% | 50.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07010` | Chiapas | Bejucal de Ocampo | 4,878 | 1,675 | 2,073 | 1,130 | 76.83% | 34.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25007` | Sinaloa | Choix | 24,087 | 11,403 | 7,108 | 5,576 | 76.85% | 47.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07110` | Chiapas | Yajalón | 25,265 | 15,418 | 4,007 | 5,840 | 76.89% | 61.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31012` | Yucatán | Cenotillo | 3,146 | 2,016 | 406 | 724 | 76.99% | 64.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20555` | Oaxaca | Trinidad Zaachila | 2,636 | 1,397 | 633 | 606 | 77.01% | 53.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23011` | Quintana Roo | Puerto Morelos | 12,006 | 3,125 | 6,121 | 2,760 | 77.01% | 26.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13021` | Hidalgo | Emiliano Zapata | 10,867 | 5,452 | 2,920 | 2,495 | 77.04% | 50.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21075` | Puebla | Huehuetlán el Grande | 4,970 | 2,830 | 999 | 1,141 | 77.04% | 56.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04009` | Campeche | Escárcega | 44,630 | 18,182 | 16,216 | 10,232 | 77.07% | 40.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20397` | Oaxaca | Santa María Alotepec | 2,094 | 769 | 845 | 480 | 77.08% | 36.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12006` | Guerrero | Apaxtla | 8,032 | 4,098 | 2,093 | 1,841 | 77.08% | 51.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20050` | Oaxaca | Magdalena Teitipac | 3,107 | 472 | 1,923 | 712 | 77.08% | 15.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `19017` | Nuevo León | Galeana | 27,245 | 13,522 | 7,488 | 6,235 | 77.12% | 49.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12001` | Guerrero | Acapulco de Juárez | 576,122 | 201,148 | 243,206 | 131,768 | 77.13% | 34.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24013` | San Luis Potosí | Ciudad Valles | 136,996 | 62,207 | 43,470 | 31,319 | 77.14% | 45.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08054` | Chihuahua | Riva Palacio | 6,361 | 800 | 4,109 | 1,452 | 77.17% | 12.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12023` | Guerrero | Cuajinicuilapa | 17,989 | 9,349 | 4,534 | 4,106 | 77.17% | 51.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24009` | San Luis Potosí | Cerro de San Pedro | 5,142 | 3,189 | 781 | 1,172 | 77.21% | 62.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30098` | Veracruz | Lerdo de Tejada | 15,334 | 7,461 | 4,383 | 3,490 | 77.24% | 48.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16060` | Michoacán | Nuevo Urecho | 6,290 | 3,353 | 1,506 | 1,431 | 77.25% | 53.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16101` | Michoacán | Tzintzuntzan | 9,953 | 2,433 | 5,261 | 2,259 | 77.30% | 24.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29021` | Tlaxcala | Nanacamilpa de Mariano Arista | 14,640 | 7,255 | 4,064 | 3,321 | 77.32% | 49.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07063` | Chiapas | Osumacinta | 2,960 | 1,960 | 329 | 671 | 77.33% | 66.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15078` | Estado de México | San Simón de Guerrero | 5,548 | 3,334 | 959 | 1,255 | 77.38% | 60.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31024` | Yucatán | Chumayel | 2,593 | 1,815 | 192 | 586 | 77.40% | 70.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04011` | Campeche | Calakmul | 20,986 | 9,947 | 6,299 | 4,740 | 77.41% | 47.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07095` | Chiapas | Teopisca | 23,126 | 10,944 | 6,961 | 5,221 | 77.42% | 47.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30007` | Veracruz | Camarón de Tejeda | 4,624 | 2,290 | 1,291 | 1,043 | 77.44% | 49.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20167` | Oaxaca | San José Independencia | 3,242 | 2,016 | 495 | 731 | 77.45% | 62.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `17005` | Morelos | Coatlán del Río | 8,361 | 4,602 | 1,874 | 1,885 | 77.45% | 55.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `19039` | Nuevo León | Montemorelos | 44,653 | 17,745 | 16,851 | 10,057 | 77.48% | 39.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `06010` | Colima | Tecomán | 78,842 | 33,845 | 27,277 | 17,720 | 77.52% | 42.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21208` | Puebla | Zacatlán | 59,565 | 31,569 | 14,622 | 13,374 | 77.55% | 53.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16026` | Michoacán | Chinicuila | 3,990 | 1,762 | 1,333 | 895 | 77.57% | 44.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20153` | Oaxaca | San Ildefonso Villa Alta | 2,515 | 894 | 1,058 | 563 | 77.61% | 35.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04007` | Campeche | Palizada | 6,978 | 4,431 | 985 | 1,562 | 77.62% | 63.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20568` | Oaxaca | Zapotitlán Lagunas | 2,201 | 1,067 | 642 | 492 | 77.65% | 48.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32025` | Zacatecas | Luis Moya | 9,484 | 4,846 | 2,520 | 2,118 | 77.67% | 51.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07070` | Chiapas | El Porvenir | 10,510 | 5,467 | 2,699 | 2,344 | 77.70% | 52.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13059` | Hidalgo | Tecozautla | 29,419 | 13,316 | 9,562 | 6,541 | 77.77% | 45.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07039` | Chiapas | Huixtán | 14,929 | 8,516 | 3,097 | 3,316 | 77.79% | 57.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20011` | Oaxaca | Ayotzintepec | 5,262 | 2,792 | 1,302 | 1,168 | 77.80% | 53.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21150` | Puebla | Santo Tomás Hueyotlipan | 6,130 | 3,573 | 1,199 | 1,358 | 77.85% | 58.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19036` | Nuevo León | Melchor Ocampo | 1,937 | 1,131 | 377 | 429 | 77.85% | 58.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16027` | Michoacán | Chucándiro | 5,168 | 2,224 | 1,800 | 1,144 | 77.86% | 43.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26002` | Sonora | Agua Prieta | 71,928 | 24,440 | 31,581 | 15,907 | 77.88% | 33.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27004` | Tabasco | Centro | 483,874 | 164,465 | 212,692 | 106,717 | 77.95% | 33.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20316` | Oaxaca | San Pedro Mixtepec | 31,769 | 5,708 | 19,065 | 6,996 | 77.98% | 17.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05026` | Coahuila | Progreso | 2,845 | 1,575 | 644 | 626 | 78.00% | 55.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31081` | Yucatán | Tekom | 2,869 | 2,051 | 187 | 631 | 78.01% | 71.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29030` | Tlaxcala | Terrenate | 11,674 | 6,785 | 2,323 | 2,566 | 78.02% | 58.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12071` | Guerrero | Xochihuehuetlán | 5,968 | 3,046 | 1,612 | 1,310 | 78.05% | 51.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07075` | Chiapas | Sabanilla | 17,906 | 11,851 | 2,125 | 3,930 | 78.05% | 66.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07010` | Chiapas | Bejucal de Ocampo | 5,358 | 2,425 | 1,759 | 1,174 | 78.09% | 45.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21054` | Puebla | Chignahuapan | 49,747 | 27,299 | 11,554 | 10,894 | 78.10% | 54.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20419` | Oaxaca | Santa María Jalapa del Marqués | 9,703 | 5,821 | 1,758 | 2,124 | 78.11% | 59.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08063` | Chihuahua | Temósachic | 5,198 | 2,413 | 1,648 | 1,137 | 78.13% | 46.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12026` | Guerrero | Cuetzala del Progreso | 6,335 | 3,157 | 1,794 | 1,384 | 78.15% | 49.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20011` | Oaxaca | Ayotzintepec | 4,970 | 3,019 | 866 | 1,085 | 78.17% | 60.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21036` | Puebla | Coxcatlán | 14,760 | 8,355 | 3,184 | 3,221 | 78.18% | 56.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20204` | Oaxaca | San Juan Lachigalla | 2,245 | 1,015 | 741 | 489 | 78.22% | 45.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07096` | Chiapas | Tila | 55,320 | 31,164 | 12,117 | 12,039 | 78.24% | 56.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07066` | Chiapas | Pantelhó | 15,173 | 5,914 | 5,962 | 3,297 | 78.27% | 38.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20084` | Oaxaca | San Agustín Yatareni | 3,119 | 1,063 | 1,379 | 677 | 78.29% | 34.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16055` | Michoacán | Morelos | 7,748 | 3,547 | 2,522 | 1,679 | 78.33% | 45.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31084` | Yucatán | Temax | 5,345 | 3,592 | 595 | 1,158 | 78.33% | 67.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14097` | Jalisco | Tizapán el Alto | 18,712 | 8,129 | 6,534 | 4,049 | 78.36% | 43.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26019` | Sonora | Fronteras | 6,165 | 3,157 | 1,676 | 1,332 | 78.39% | 51.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `12012` | Guerrero | Ayutla de los Libres | 34,545 | 7,818 | 19,265 | 7,462 | 78.40% | 22.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07093` | Chiapas | Tecpatán | 28,489 | 16,663 | 5,673 | 6,153 | 78.40% | 58.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31081` | Yucatán | Tekom | 2,757 | 1,920 | 242 | 595 | 78.42% | 69.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08019` | Chihuahua | Chihuahua | 755,279 | 338,355 | 253,949 | 162,975 | 78.42% | 44.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21032` | Puebla | Coatzingo | 2,346 | 1,315 | 525 | 506 | 78.43% | 56.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07082` | Chiapas | Simojovel | 29,206 | 17,719 | 5,196 | 6,291 | 78.46% | 60.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31090` | Yucatán | Timucuy | 5,190 | 3,731 | 342 | 1,117 | 78.48% | 71.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20388` | Oaxaca | Santa Gertrudis | 2,394 | 853 | 1,026 | 515 | 78.49% | 35.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26038` | Sonora | Sáric | 1,848 | 833 | 618 | 397 | 78.52% | 45.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08051` | Chihuahua | Ocampo | 6,102 | 3,271 | 1,521 | 1,310 | 78.53% | 53.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15017` | Estado de México | Ayapango | 5,683 | 3,437 | 1,030 | 1,216 | 78.60% | 60.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26062` | Sonora | Alamos | 19,332 | 9,655 | 5,542 | 4,135 | 78.61% | 49.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08047` | Chihuahua | Moris | 3,681 | 1,504 | 1,390 | 787 | 78.62% | 40.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13072` | Hidalgo | Tlanchinol | 21,070 | 8,345 | 8,222 | 4,503 | 78.63% | 39.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30042` | Veracruz | Coatzintla | 39,832 | 16,487 | 14,879 | 8,466 | 78.75% | 41.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12073` | Guerrero | Zapotitlán Tablas | 7,678 | 4,318 | 1,729 | 1,631 | 78.76% | 56.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07040` | Chiapas | Huixtla | 38,273 | 19,716 | 10,436 | 8,121 | 78.78% | 51.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20251` | Oaxaca | San Mateo Piñas | 1,533 | 728 | 480 | 325 | 78.80% | 47.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20220` | Oaxaca | San Juan Tepeuxila | 1,752 | 540 | 841 | 371 | 78.82% | 30.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21201` | Puebla | Xochiltepec | 2,541 | 1,294 | 709 | 538 | 78.83% | 50.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07108` | Chiapas | Villa Corzo | 48,460 | 21,083 | 17,135 | 10,242 | 78.87% | 43.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20331` | Oaxaca | San Pedro Totolápam | 2,305 | 851 | 967 | 487 | 78.87% | 36.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26069` | Sonora | Yécora | 4,369 | 2,323 | 1,123 | 923 | 78.87% | 53.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16062` | Michoacán | Ocampo | 17,783 | 8,915 | 5,114 | 3,754 | 78.89% | 50.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `27009` | Tabasco | Jalapa | 27,884 | 16,960 | 5,044 | 5,880 | 78.91% | 60.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31019` | Yucatán | Chemax | 24,693 | 16,055 | 3,441 | 5,197 | 78.95% | 65.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20036` | Oaxaca | Mesones Hidalgo | 3,439 | 1,046 | 1,670 | 723 | 78.98% | 30.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16056` | Michoacán | Múgica | 32,731 | 13,953 | 11,909 | 6,869 | 79.01% | 42.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31059` | Yucatán | Progreso | 49,340 | 24,947 | 14,043 | 10,350 | 79.02% | 50.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26025` | Sonora | Magdalena | 26,226 | 10,665 | 10,063 | 5,498 | 79.04% | 40.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20303` | Oaxaca | San Pedro Comitancillo | 3,320 | 869 | 1,755 | 696 | 79.04% | 26.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20134` | Oaxaca | San Francisco Cahuacuá | 2,034 | 738 | 870 | 426 | 79.06% | 36.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15063` | Estado de México | Ocoyoacac | 55,507 | 30,362 | 13,523 | 11,622 | 79.06% | 54.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10013` | Durango | Mapimí | 17,958 | 8,270 | 5,929 | 3,759 | 79.07% | 46.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31103` | Yucatán | Xocchel | 2,719 | 1,899 | 251 | 569 | 79.07% | 69.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26053` | Sonora | Puerto Peñasco | 42,192 | 17,671 | 15,698 | 8,823 | 79.09% | 41.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20199` | Oaxaca | San Juan Guichicovi | 21,767 | 8,437 | 8,780 | 4,550 | 79.10% | 38.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16016` | Michoacán | Coeneo | 19,173 | 7,900 | 7,266 | 4,007 | 79.10% | 41.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31011` | Yucatán | Celestún | 5,995 | 4,047 | 696 | 1,252 | 79.12% | 67.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16011` | Michoacán | Briseñas | 6,266 | 3,492 | 1,466 | 1,308 | 79.13% | 55.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26030` | Sonora | Nogales | 175,379 | 58,047 | 80,728 | 36,604 | 79.13% | 33.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25013` | Sinaloa | Mocorito | 36,315 | 16,128 | 12,611 | 7,576 | 79.14% | 44.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20379` | Oaxaca | Santa Cruz Mixtepec | 2,662 | 1,307 | 800 | 555 | 79.15% | 49.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05012` | Coahuila | Guerrero | 1,780 | 1,087 | 322 | 371 | 79.16% | 61.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30056` | Veracruz | Chacaltianguis | 8,867 | 4,426 | 2,594 | 1,847 | 79.17% | 49.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21130` | Puebla | San José Miahuatlán | 10,016 | 1,249 | 6,681 | 2,086 | 79.17% | 12.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12014` | Guerrero | Benito Juárez | 12,547 | 7,196 | 2,744 | 2,607 | 79.22% | 57.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13021` | Hidalgo | Emiliano Zapata | 12,125 | 6,330 | 3,278 | 2,517 | 79.24% | 52.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26003` | Sonora | Altar | 6,217 | 3,475 | 1,452 | 1,290 | 79.25% | 55.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26063` | Sonora | Etchojoa | 44,395 | 20,435 | 14,749 | 9,211 | 79.25% | 46.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10002` | Durango | Canelas | 3,149 | 1,135 | 1,361 | 653 | 79.26% | 36.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07010` | Chiapas | Bejucal de Ocampo | 6,108 | 1,956 | 2,887 | 1,265 | 79.29% | 32.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10010` | Durango | Hidalgo | 3,319 | 1,566 | 1,067 | 686 | 79.33% | 47.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08050` | Chihuahua | Nuevo Casas Grandes | 53,863 | 21,093 | 21,656 | 11,114 | 79.37% | 39.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13037` | Hidalgo | Metztitlán | 17,335 | 9,483 | 4,278 | 3,574 | 79.38% | 54.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `31036` | Yucatán | Homún | 5,219 | 3,746 | 397 | 1,076 | 79.38% | 71.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16047` | Michoacán | Juárez | 11,089 | 5,728 | 3,075 | 2,286 | 79.38% | 51.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19022` | Nuevo León | Gral. Terán | 13,935 | 6,376 | 4,687 | 2,872 | 79.39% | 45.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31049` | Yucatán | Mayapán | 2,835 | 2,124 | 127 | 584 | 79.40% | 74.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31097` | Yucatán | Tunkás | 2,971 | 2,035 | 324 | 612 | 79.40% | 68.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21128` | Puebla | San Jerónimo Xayacatlán | 3,192 | 1,920 | 615 | 657 | 79.42% | 60.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26035` | Sonora | San Pedro de la Cueva | 2,052 | 1,260 | 370 | 422 | 79.43% | 61.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31085` | Yucatán | Temozón | 12,519 | 8,687 | 1,258 | 2,574 | 79.44% | 69.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26071` | Sonora | Benito Juárez | 15,810 | 7,519 | 5,041 | 3,250 | 79.44% | 47.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08012` | Chihuahua | Carichí | 7,720 | 3,950 | 2,185 | 1,585 | 79.47% | 51.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19033` | Nuevo León | Lampazos de Naranjo | 5,240 | 2,878 | 1,287 | 1,075 | 79.48% | 54.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16008` | Michoacán | Aquila | 16,067 | 4,960 | 7,812 | 3,295 | 79.49% | 30.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25015` | Sinaloa | Salvador Alvarado | 66,841 | 30,339 | 22,807 | 13,695 | 79.51% | 45.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20070` | Oaxaca | Pluma Hidalgo | 2,227 | 1,054 | 717 | 456 | 79.52% | 47.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31068` | Yucatán | Sinanché | 2,717 | 1,941 | 220 | 556 | 79.54% | 71.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07054` | Chiapas | Mazatán | 20,854 | 10,627 | 5,963 | 4,264 | 79.55% | 50.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14039` | Jalisco | El Grullo | 21,611 | 8,127 | 9,074 | 4,410 | 79.59% | 37.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07119` | Chiapas | Capitán Luis Ángel Vidal | 3,030 | 1,706 | 708 | 616 | 79.67% | 56.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26024` | Sonora | Imuris | 9,169 | 4,135 | 3,170 | 1,864 | 79.67% | 45.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10009` | Durango | Guanaceví | 7,335 | 3,431 | 2,413 | 1,491 | 79.67% | 46.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26067` | Sonora | Quiriego | 3,361 | 1,999 | 679 | 683 | 79.68% | 59.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30175` | Veracruz | Tlacojalpan | 3,569 | 2,142 | 702 | 725 | 79.69% | 60.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07061` | Chiapas | Ocozocoautla de Espinosa | 70,707 | 33,903 | 22,445 | 14,359 | 79.69% | 47.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08020` | Chihuahua | Chínipas | 5,049 | 2,570 | 1,454 | 1,025 | 79.70% | 50.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20232` | Oaxaca | San Lucas Ojitlán | 15,259 | 10,013 | 2,153 | 3,093 | 79.73% | 65.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `28005` | Tamaulipas | Burgos | 4,848 | 3,310 | 556 | 982 | 79.74% | 68.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20108` | Oaxaca | San Antonio Tepetlapa | 2,584 | 501 | 1,560 | 523 | 79.76% | 19.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28016` | Tamaulipas | Hidalgo | 15,169 | 7,910 | 4,192 | 3,067 | 79.78% | 52.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08018` | Chihuahua | Cusihuiriachi | 5,018 | 925 | 3,080 | 1,013 | 79.81% | 18.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24006` | San Luis Potosí | Catorce | 6,691 | 3,871 | 1,470 | 1,350 | 79.82% | 57.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26049` | Sonora | Hermosillo | 600,058 | 235,287 | 244,062 | 120,709 | 79.88% | 39.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15093` | Estado de México | Teotihuacán | 46,841 | 22,617 | 14,831 | 9,393 | 79.95% | 48.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21022` | Puebla | Atzitzihuacán | 9,014 | 5,245 | 1,962 | 1,807 | 79.95% | 58.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19044` | Nuevo León | Rayones | 3,040 | 1,985 | 446 | 609 | 79.97% | 65.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07071` | Chiapas | Pueblo Nuevo Solistahuacán | 17,840 | 7,269 | 6,998 | 3,573 | 79.97% | 40.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20099` | Oaxaca | San Andrés Zautla | 2,988 | 1,823 | 567 | 598 | 79.99% | 61.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08006` | Chihuahua | Bachíniva | 5,786 | 2,897 | 1,732 | 1,157 | 80.00% | 50.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16033` | Michoacán | Gabriel Zamora | 15,944 | 8,661 | 4,095 | 3,188 | 80.01% | 54.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15026` | Estado de México | Chalco | 211,299 | 74,111 | 94,965 | 42,223 | 80.02% | 35.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13026` | Hidalgo | Huazalingo | 9,716 | 5,906 | 1,874 | 1,936 | 80.07% | 60.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25020` | Sinaloa | Juan José Ríos | 30,496 | 13,412 | 11,013 | 6,071 | 80.09% | 43.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21175` | Puebla | Tilapa | 6,800 | 3,713 | 1,736 | 1,351 | 80.13% | 54.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29015` | Tlaxcala | Ixtacuixtla de Mariano Matamoros | 27,916 | 13,847 | 8,527 | 5,542 | 80.15% | 49.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23009` | Quintana Roo | Tulum | 24,212 | 10,059 | 9,347 | 4,806 | 80.15% | 41.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14070` | Jalisco | Villa Purificación | 9,975 | 4,710 | 3,285 | 1,980 | 80.15% | 47.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20450` | Oaxaca | Santa María Zoquitlán | 2,601 | 874 | 1,211 | 516 | 80.16% | 33.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20178` | Oaxaca | San Juan Bautista Lo de Soto | 2,013 | 1,250 | 364 | 399 | 80.18% | 62.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07027` | Chiapas | Chiapa de Corzo | 79,887 | 42,181 | 21,909 | 15,797 | 80.23% | 52.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20310` | Oaxaca | San Pedro Jicayán | 7,455 | 4,571 | 1,410 | 1,474 | 80.23% | 61.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30179` | Veracruz | Tlachichilco | 8,268 | 3,861 | 2,776 | 1,631 | 80.27% | 46.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19044` | Nuevo León | Rayones | 3,143 | 2,257 | 267 | 619 | 80.31% | 71.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07050` | Chiapas | La Libertad | 4,401 | 3,137 | 399 | 865 | 80.35% | 71.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14069` | Jalisco | Puerto Vallarta | 211,251 | 85,558 | 84,176 | 41,517 | 80.35% | 40.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07057` | Chiapas | Motozintla | 54,481 | 23,943 | 19,834 | 10,704 | 80.35% | 43.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07120` | Chiapas | Emiliano Zapata | 2,301 | 1,453 | 396 | 452 | 80.36% | 63.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21124` | Puebla | San Felipe Tepatlán | 2,859 | 1,904 | 394 | 561 | 80.38% | 66.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `27004` | Tabasco | Centro | 439,602 | 118,701 | 234,832 | 86,069 | 80.42% | 27.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20365` | Oaxaca | Santa Catarina Lachatao | 996 | 555 | 246 | 195 | 80.42% | 55.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31062` | Yucatán | Sacalum | 3,670 | 2,622 | 330 | 718 | 80.44% | 71.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20475` | Oaxaca | Santiago Llano Grande | 2,660 | 1,642 | 498 | 520 | 80.45% | 61.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04003` | Campeche | Carmen | 167,626 | 67,029 | 67,867 | 32,730 | 80.47% | 39.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14012` | Jalisco | Atenguillo | 3,511 | 1,898 | 928 | 685 | 80.49% | 54.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20276` | Oaxaca | San Miguel Soyaltepec | 26,770 | 18,018 | 3,534 | 5,218 | 80.51% | 67.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31008` | Yucatán | Calotmul | 3,352 | 2,461 | 238 | 653 | 80.52% | 73.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30175` | Veracruz | Tlacojalpan | 3,595 | 1,386 | 1,509 | 700 | 80.53% | 38.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21140` | Puebla | San Pablo Anicano | 3,011 | 1,815 | 610 | 586 | 80.54% | 60.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23006` | Quintana Roo | Lázaro Cárdenas | 18,658 | 9,545 | 5,489 | 3,624 | 80.58% | 51.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08027` | Chihuahua | Guachochi | 36,612 | 16,074 | 13,434 | 7,104 | 80.60% | 43.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26036` | Sonora | Santa Ana | 12,874 | 5,883 | 4,503 | 2,488 | 80.67% | 45.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20499` | Oaxaca | Santiago Yaveo | 3,925 | 1,357 | 1,810 | 758 | 80.69% | 34.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21185` | Puebla | Tlapanalá | 6,723 | 4,131 | 1,294 | 1,298 | 80.69% | 61.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08023` | Chihuahua | Galeana | 4,885 | 2,259 | 1,683 | 943 | 80.70% | 46.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31069` | Yucatán | Sotuta | 5,671 | 3,608 | 971 | 1,092 | 80.74% | 63.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14006` | Jalisco | Ameca | 53,513 | 24,123 | 19,093 | 10,297 | 80.76% | 45.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26064` | Sonora | Huatabampo | 56,837 | 29,572 | 16,329 | 10,936 | 80.76% | 52.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16003` | Michoacán | Álvaro Obregón | 16,440 | 8,368 | 4,929 | 3,143 | 80.88% | 50.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20350` | Oaxaca | San Vicente Coatlán | 2,998 | 516 | 1,909 | 573 | 80.89% | 17.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20002` | Oaxaca | Acatlán de Pérez Figueroa | 31,395 | 19,925 | 5,471 | 5,999 | 80.89% | 63.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31035` | Yucatán | Hoctún | 5,132 | 3,587 | 565 | 980 | 80.90% | 69.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `11023` | Guanajuato | Pénjamo | 118,842 | 41,846 | 54,310 | 22,686 | 80.91% | 35.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16074` | Michoacán | Quiroga | 21,749 | 10,286 | 7,314 | 4,149 | 80.92% | 47.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `17031` | Morelos | Zacatepec | 30,262 | 15,850 | 8,642 | 5,770 | 80.93% | 52.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29005` | Tlaxcala | Atltzayanca | 13,881 | 8,818 | 2,417 | 2,646 | 80.94% | 63.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16072` | Michoacán | Puruándiro | 62,786 | 22,036 | 28,808 | 11,942 | 80.98% | 35.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19001` | Nuevo León | Abasolo | 2,288 | 1,369 | 484 | 435 | 80.99% | 59.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12063` | Guerrero | Tlacoachistlahuaca | 13,270 | 7,832 | 2,917 | 2,521 | 81.00% | 59.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20120` | Oaxaca | San Bernardo Mixtepec | 2,190 | 853 | 921 | 416 | 81.00% | 38.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20268` | Oaxaca | San Miguel el Grande | 2,706 | 1,539 | 653 | 514 | 81.01% | 56.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30204` | Veracruz | Tres Valles | 33,126 | 9,440 | 17,396 | 6,290 | 81.01% | 28.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21215` | Puebla | Zongozotla | 3,773 | 2,428 | 629 | 716 | 81.02% | 64.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31066` | Yucatán | Santa Elena | 2,839 | 1,957 | 344 | 538 | 81.05% | 68.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16032` | Michoacán | Erongarícuaro | 11,327 | 6,775 | 2,411 | 2,141 | 81.10% | 59.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07096` | Chiapas | Tila | 44,551 | 19,797 | 16,341 | 8,413 | 81.12% | 44.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12067` | Guerrero | Tlapa de Comonfort | 54,995 | 20,985 | 23,625 | 10,385 | 81.12% | 38.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13007` | Hidalgo | Almoloya | 9,868 | 5,217 | 2,791 | 1,860 | 81.15% | 52.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08008` | Chihuahua | Batopilas de Manuel Gómez Morín | 8,145 | 3,624 | 2,986 | 1,535 | 81.15% | 44.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26053` | Sonora | Puerto Peñasco | 54,996 | 21,166 | 23,479 | 10,351 | 81.18% | 38.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07054` | Chiapas | Mazatán | 18,337 | 6,599 | 8,287 | 3,451 | 81.18% | 35.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32027` | Zacatecas | Melchor Ocampo | 2,528 | 1,821 | 232 | 475 | 81.21% | 72.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30149` | Veracruz | Soledad de Doblado | 20,608 | 8,865 | 7,874 | 3,869 | 81.23% | 43.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11007` | Guanajuato | Celaya | 373,130 | 158,860 | 144,502 | 69,768 | 81.30% | 42.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31034` | Yucatán | Hocabá | 4,860 | 3,169 | 783 | 908 | 81.32% | 65.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24007` | San Luis Potosí | Cedral | 13,154 | 6,401 | 4,301 | 2,452 | 81.36% | 48.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07095` | Chiapas | Teopisca | 26,293 | 15,933 | 5,463 | 4,897 | 81.38% | 60.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15067` | Estado de México | Otzoloapan | 4,201 | 2,905 | 514 | 782 | 81.39% | 69.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `22011` | Querétaro | Pedro Escobedo | 46,464 | 24,708 | 13,112 | 8,644 | 81.40% | 53.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27005` | Tabasco | Comalcalco | 141,000 | 79,716 | 35,121 | 26,163 | 81.44% | 56.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27012` | Tabasco | Macuspana | 111,696 | 48,345 | 42,628 | 20,723 | 81.45% | 43.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `20499` | Oaxaca | Santiago Yaveo | 4,077 | 1,877 | 1,444 | 756 | 81.46% | 46.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20213` | Oaxaca | San Juan Quiahije | 2,356 | 759 | 1,161 | 436 | 81.49% | 32.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12031` | Guerrero | Florencio Villarreal | 16,246 | 8,514 | 4,727 | 3,005 | 81.50% | 52.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16016` | Michoacán | Coeneo | 20,163 | 8,500 | 7,936 | 3,727 | 81.52% | 42.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32027` | Zacatecas | Melchor Ocampo | 2,345 | 1,414 | 498 | 433 | 81.54% | 60.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16086` | Michoacán | Tangancícuaro | 30,423 | 10,665 | 14,142 | 5,616 | 81.54% | 35.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15123` | Estado de México | Luvianos | 21,979 | 13,025 | 4,899 | 4,055 | 81.55% | 59.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08025` | Chihuahua | Gómez Farías | 7,268 | 3,131 | 2,797 | 1,340 | 81.56% | 43.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24048` | San Luis Potosí | Villa de Guadalupe | 7,366 | 3,850 | 2,158 | 1,358 | 81.56% | 52.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16015` | Michoacán | Coalcomán de Vázquez Pallares | 15,176 | 6,667 | 5,714 | 2,795 | 81.58% | 43.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19028` | Nuevo León | Hidalgo | 12,798 | 7,023 | 3,419 | 2,356 | 81.59% | 54.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08048` | Chihuahua | Namiquipa | 19,627 | 8,001 | 8,013 | 3,613 | 81.59% | 40.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20206` | Oaxaca | San Juan Lalana | 10,557 | 5,395 | 3,220 | 1,942 | 81.60% | 51.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08059` | Chihuahua | San Francisco del Oro | 4,181 | 2,308 | 1,106 | 767 | 81.66% | 55.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20092` | Oaxaca | San Andrés Paxtlán | 3,210 | 956 | 1,666 | 588 | 81.68% | 29.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20393` | Oaxaca | Santa Lucía Miahuatlán | 2,071 | 880 | 812 | 379 | 81.70% | 42.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04010` | Campeche | Candelaria | 28,778 | 15,701 | 7,823 | 5,254 | 81.74% | 54.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26030` | Sonora | Nogales | 216,066 | 70,025 | 106,663 | 39,378 | 81.78% | 32.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16095` | Michoacán | Tlazazalca | 7,875 | 2,697 | 3,743 | 1,435 | 81.78% | 34.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12004` | Guerrero | Alcozauca de Guerrero | 13,773 | 7,256 | 4,008 | 2,509 | 81.78% | 52.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08019` | Chihuahua | Chihuahua | 716,719 | 300,713 | 285,446 | 130,560 | 81.78% | 41.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20385` | Oaxaca | Santa Cruz Xitla | 3,256 | 834 | 1,829 | 593 | 81.79% | 25.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20483` | Oaxaca | Santiago Nuyoó | 1,484 | 668 | 546 | 270 | 81.81% | 45.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `18004` | Nayarit | Bahía de Banderas | 139,756 | 53,019 | 61,337 | 25,400 | 81.83% | 37.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16018` | Michoacán | Copándaro | 7,283 | 3,608 | 2,352 | 1,323 | 81.83% | 49.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20385` | Oaxaca | Santa Cruz Xitla | 3,639 | 975 | 2,003 | 661 | 81.84% | 26.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14040` | Jalisco | Guachinango | 3,596 | 2,030 | 913 | 653 | 81.84% | 56.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31074` | Yucatán | Tahmek | 3,200 | 2,321 | 298 | 581 | 81.84% | 72.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07025` | Chiapas | Chapultenango | 5,389 | 3,336 | 1,076 | 977 | 81.87% | 61.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21063` | Puebla | Epatlán | 3,707 | 2,262 | 773 | 672 | 81.87% | 61.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07046` | Chiapas | Jiquipilas | 30,615 | 18,946 | 6,125 | 5,544 | 81.89% | 61.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24042` | San Luis Potosí | Tanquián de Escobedo | 10,434 | 6,270 | 2,276 | 1,888 | 81.91% | 60.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `17018` | Morelos | Temixco | 86,374 | 41,872 | 28,886 | 15,616 | 81.92% | 48.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16088` | Michoacán | Taretan | 12,326 | 6,130 | 3,968 | 2,228 | 81.92% | 49.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `13020` | Hidalgo | Eloxochitlán | 2,430 | 1,083 | 908 | 439 | 81.93% | 44.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19012` | Nuevo León | Ciénega de Flores | 39,601 | 12,109 | 20,342 | 7,150 | 81.94% | 30.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20012` | Oaxaca | El Barrio de la Soledad | 10,208 | 6,026 | 2,340 | 1,842 | 81.96% | 59.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26042` | Sonora | Trincheras | 1,426 | 848 | 321 | 257 | 81.98% | 59.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20150` | Oaxaca | San Gabriel Mixtepec | 3,127 | 1,260 | 1,304 | 563 | 82.00% | 40.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16036` | Michoacán | Huandacareo | 9,494 | 4,918 | 2,868 | 1,708 | 82.01% | 51.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26052` | Sonora | Pitiquito | 6,220 | 3,294 | 1,808 | 1,118 | 82.03% | 52.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16100` | Michoacán | Tuzantla | 12,470 | 7,508 | 2,722 | 2,240 | 82.04% | 60.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07110` | Chiapas | Yajalón | 23,467 | 9,514 | 9,739 | 4,214 | 82.04% | 40.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20030` | Oaxaca | El Espinal | 6,791 | 4,438 | 1,134 | 1,219 | 82.05% | 65.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20076` | Oaxaca | Salina Cruz | 60,635 | 13,976 | 35,785 | 10,874 | 82.07% | 23.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24002` | San Luis Potosí | Alaquines | 6,125 | 3,535 | 1,492 | 1,098 | 82.07% | 57.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04004` | Campeche | Champotón | 58,657 | 28,268 | 19,874 | 10,515 | 82.07% | 48.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `31063` | Yucatán | Samahil | 3,625 | 2,713 | 263 | 649 | 82.10% | 74.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16058` | Michoacán | Nocupétaro | 6,694 | 2,532 | 2,964 | 1,198 | 82.10% | 37.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16094` | Michoacán | Tlalpujahua | 19,522 | 10,722 | 5,309 | 3,491 | 82.12% | 54.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21095` | Puebla | Lafragua | 5,751 | 3,738 | 986 | 1,027 | 82.14% | 65.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15040` | Estado de México | Ixtapaluca | 344,843 | 182,509 | 100,820 | 61,514 | 82.16% | 52.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14077` | Jalisco | San Marcos | 3,298 | 1,964 | 746 | 588 | 82.17% | 59.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26054` | Sonora | Rayón | 2,188 | 1,405 | 393 | 390 | 82.18% | 64.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `17008` | Morelos | Emiliano Zapata | 67,407 | 27,957 | 27,450 | 12,000 | 82.20% | 41.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26036` | Sonora | Santa Ana | 12,646 | 6,106 | 4,290 | 2,250 | 82.21% | 48.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `13033` | Hidalgo | Juárez Hidalgo | 2,413 | 1,187 | 797 | 429 | 82.22% | 49.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21083` | Puebla | Ixcamilpa de Guerrero | 3,066 | 1,983 | 538 | 545 | 82.22% | 64.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12037` | Guerrero | Igualapa | 8,003 | 5,187 | 1,394 | 1,422 | 82.23% | 64.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31035` | Yucatán | Hoctún | 4,529 | 3,271 | 454 | 804 | 82.25% | 72.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24032` | San Luis Potosí | Santa Catarina | 9,599 | 4,889 | 3,007 | 1,703 | 82.26% | 50.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14035` | Jalisco | Ejutla | 2,027 | 1,034 | 634 | 359 | 82.29% | 51.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12042` | Guerrero | Malinaltepec | 18,231 | 10,101 | 4,902 | 3,228 | 82.29% | 55.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19015` | Nuevo León | Doctor Coss | 2,725 | 1,433 | 811 | 481 | 82.35% | 52.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19045` | Nuevo León | Sabinas Hidalgo | 29,104 | 13,628 | 10,340 | 5,136 | 82.35% | 46.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21125` | Puebla | San Gabriel Chilac | 10,317 | 3,284 | 5,213 | 1,820 | 82.36% | 31.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `32046` | Zacatecas | Tepetongo | 6,311 | 3,290 | 1,910 | 1,111 | 82.40% | 52.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26068` | Sonora | Rosario | 4,789 | 2,703 | 1,243 | 843 | 82.40% | 56.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16008` | Michoacán | Aquila | 17,928 | 11,539 | 3,234 | 3,155 | 82.40% | 64.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16071` | Michoacán | Purépero | 14,105 | 6,911 | 4,713 | 2,481 | 82.41% | 49.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31006` | Yucatán | Buctzotz | 7,431 | 5,101 | 1,026 | 1,304 | 82.45% | 68.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31017` | Yucatán | Chankom | 3,602 | 2,779 | 191 | 632 | 82.45% | 77.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14022` | Jalisco | Cihuatlán | 28,630 | 14,063 | 9,545 | 5,022 | 82.46% | 49.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30031` | Veracruz | Camerino Z. Mendoza | 23,682 | 12,346 | 7,182 | 4,154 | 82.46% | 52.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29048` | Tlaxcala | Santa Catarina Ayometla | 7,145 | 4,458 | 1,435 | 1,252 | 82.48% | 62.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13005` | Hidalgo | Ajacuba | 14,659 | 8,356 | 3,736 | 2,567 | 82.49% | 57.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05034` | Coahuila | Sierra Mojada | 3,624 | 1,846 | 1,144 | 634 | 82.51% | 50.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29012` | Tlaxcala | Españita | 6,568 | 3,700 | 1,720 | 1,148 | 82.52% | 56.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12060` | Guerrero | Tepecoacuilco de Trujano | 24,274 | 11,983 | 8,049 | 4,242 | 82.52% | 49.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20545` | Oaxaca | Teotitlán de Flores Magón | 6,696 | 1,750 | 3,776 | 1,170 | 82.53% | 26.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16012` | Michoacán | Buenavista | 29,291 | 13,204 | 10,969 | 5,118 | 82.53% | 45.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15044` | Estado de México | Xalatlaco | 18,208 | 10,022 | 5,006 | 3,180 | 82.54% | 55.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04009` | Campeche | Escárcega | 37,448 | 17,959 | 12,963 | 6,526 | 82.57% | 47.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04011` | Campeche | Calakmul | 19,724 | 11,210 | 5,079 | 3,435 | 82.58% | 56.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20548` | Oaxaca | Tepelmeme Villa de Morelos | 1,114 | 189 | 731 | 194 | 82.59% | 16.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08061` | Chihuahua | Satevó | 4,051 | 2,124 | 1,222 | 705 | 82.60% | 52.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31031` | Yucatán | Dzoncauich | 2,905 | 2,093 | 307 | 505 | 82.62% | 72.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29045` | Tlaxcala | Santa Apolonia Teacalco | 3,774 | 2,559 | 559 | 656 | 82.62% | 67.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14067` | Jalisco | Pihuamo | 9,855 | 4,673 | 3,469 | 1,713 | 82.62% | 47.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16089` | Michoacán | Tarímbaro | 55,484 | 24,520 | 21,321 | 9,643 | 82.62% | 44.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07051` | Chiapas | Mapastepec | 34,776 | 14,256 | 14,480 | 6,040 | 82.63% | 40.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15007` | Estado de México | Amanalco | 17,591 | 11,130 | 3,414 | 3,047 | 82.68% | 63.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `03003` | Baja California Sur | La Paz | 186,569 | 83,540 | 70,744 | 32,285 | 82.70% | 44.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19017` | Nuevo León | Galeana | 30,786 | 16,627 | 8,835 | 5,324 | 82.71% | 54.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26065` | Sonora | Navojoa | 113,338 | 50,120 | 43,618 | 19,600 | 82.71% | 44.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `05014` | Coahuila | Jiménez | 8,266 | 4,168 | 2,669 | 1,429 | 82.71% | 50.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31095` | Yucatán | Tixpéhual | 4,378 | 3,123 | 499 | 756 | 82.73% | 71.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20088` | Oaxaca | San Andrés Huayápam | 3,791 | 2,023 | 1,114 | 654 | 82.75% | 53.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `29040` | Tlaxcala | Xaltocan | 7,249 | 3,814 | 2,187 | 1,248 | 82.78% | 52.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26053` | Sonora | Puerto Peñasco | 45,480 | 18,275 | 19,377 | 7,828 | 82.79% | 40.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07003` | Chiapas | Acapetahua | 20,009 | 11,380 | 5,188 | 3,441 | 82.80% | 56.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07047` | Chiapas | Jitotol | 14,091 | 9,584 | 2,084 | 2,423 | 82.80% | 68.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19015` | Nuevo León | Doctor Coss | 2,717 | 1,462 | 788 | 467 | 82.81% | 53.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26069` | Sonora | Yécora | 4,323 | 2,782 | 798 | 743 | 82.81% | 64.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20364` | Oaxaca | Santa Catarina Juquila | 10,520 | 3,082 | 5,636 | 1,802 | 82.87% | 29.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31057` | Yucatán | Panabá | 5,596 | 4,178 | 460 | 958 | 82.88% | 74.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15125` | Estado de México | Tonanitla | 8,032 | 4,994 | 1,664 | 1,374 | 82.89% | 62.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20499` | Oaxaca | Santiago Yaveo | 5,029 | 1,703 | 2,466 | 860 | 82.90% | 33.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26067` | Sonora | Quiriego | 3,457 | 2,134 | 733 | 590 | 82.93% | 61.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07096` | Chiapas | Tila | 50,649 | 32,570 | 9,439 | 8,640 | 82.94% | 64.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29054` | Tlaxcala | Emiliano Zapata | 3,324 | 2,313 | 444 | 567 | 82.94% | 69.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13001` | Hidalgo | Acatlán | 15,141 | 4,201 | 8,360 | 2,580 | 82.96% | 27.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04004` | Campeche | Champotón | 60,338 | 32,223 | 17,836 | 10,279 | 82.96% | 53.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28011` | Tamaulipas | Gómez Farías | 7,282 | 4,256 | 1,788 | 1,238 | 83.00% | 58.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07072` | Chiapas | Rayón | 6,161 | 4,211 | 903 | 1,047 | 83.01% | 68.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26060` | Sonora | Empalme | 41,399 | 13,270 | 21,097 | 7,032 | 83.01% | 32.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31015` | Yucatán | Cuzamá | 4,033 | 2,809 | 540 | 684 | 83.04% | 69.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04010` | Campeche | Candelaria | 30,987 | 16,127 | 9,610 | 5,250 | 83.06% | 52.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04003` | Campeche | Carmen | 188,096 | 89,969 | 66,262 | 31,865 | 83.06% | 47.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04002` | Campeche | Calkiní | 38,336 | 24,612 | 7,235 | 6,489 | 83.07% | 64.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `11006` | Guanajuato | Atarjea | 4,535 | 2,937 | 832 | 766 | 83.11% | 64.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07079` | Chiapas | San Juan Cancuc | 21,322 | 14,571 | 3,154 | 3,597 | 83.13% | 68.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `12038` | Guerrero | Ixcateopan de Cuauhtémoc | 5,383 | 3,474 | 1,001 | 908 | 83.13% | 64.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07073` | Chiapas | Reforma | 29,686 | 17,560 | 7,126 | 5,000 | 83.16% | 59.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `11015` | Guanajuato | Guanajuato | 113,204 | 43,183 | 50,988 | 19,033 | 83.19% | 38.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31061` | Yucatán | Río Lagartos | 2,660 | 2,009 | 204 | 447 | 83.20% | 75.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19016` | Nuevo León | Doctor González | 3,273 | 1,936 | 787 | 550 | 83.20% | 59.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26046` | Sonora | Caborca | 62,598 | 24,792 | 27,294 | 10,512 | 83.21% | 39.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21081` | Puebla | Huitziltepec | 4,397 | 2,554 | 1,105 | 738 | 83.22% | 58.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31032` | Yucatán | Espita | 12,156 | 7,971 | 2,145 | 2,040 | 83.22% | 65.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27003` | Tabasco | Centla | 68,974 | 36,657 | 20,793 | 11,524 | 83.29% | 53.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `29059` | Tlaxcala | San Lorenzo Axocomanitla | 3,150 | 1,193 | 1,432 | 525 | 83.33% | 37.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21052` | Puebla | Chietla | 27,641 | 15,135 | 7,902 | 4,604 | 83.34% | 54.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16103` | Michoacán | Uruapan | 269,331 | 122,649 | 101,868 | 44,814 | 83.36% | 45.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20506` | Oaxaca | Santo Domingo Armenta | 2,332 | 1,281 | 663 | 388 | 83.36% | 54.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `06006` | Colima | Armería | 20,876 | 10,549 | 6,855 | 3,472 | 83.37% | 50.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30105` | Veracruz | Mecayapan | 14,207 | 6,768 | 5,077 | 2,362 | 83.37% | 47.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26070` | Sonora | General Plutarco Elías Calles | 10,737 | 4,900 | 4,055 | 1,782 | 83.40% | 45.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `12080` | Guerrero | Marquelia | 8,322 | 2,660 | 4,281 | 1,381 | 83.41% | 31.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21092` | Puebla | Juan C. Bonilla | 16,552 | 9,459 | 4,348 | 2,745 | 83.42% | 57.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20471` | Oaxaca | Santiago Lachiguiri | 3,622 | 1,342 | 1,680 | 600 | 83.43% | 37.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07106` | Chiapas | Venustiano Carranza | 44,631 | 25,930 | 11,308 | 7,393 | 83.44% | 58.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25014` | Sinaloa | Rosario | 38,428 | 16,794 | 15,289 | 6,345 | 83.49% | 43.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20182` | Oaxaca | San Juan Bautista Tuxtepec | 110,628 | 37,007 | 55,356 | 18,265 | 83.49% | 33.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12003` | Guerrero | Ajuchitlán del Progreso | 26,305 | 14,324 | 7,641 | 4,340 | 83.50% | 54.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30018` | Veracruz | Apazapan | 3,298 | 1,586 | 1,169 | 543 | 83.54% | 48.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04013` | Campeche | Seybaplaya | 11,547 | 7,166 | 2,481 | 1,900 | 83.55% | 62.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26061` | Sonora | Guaymas | 115,520 | 47,699 | 48,821 | 19,000 | 83.55% | 41.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31045` | Yucatán | Kopomá | 1,995 | 1,374 | 293 | 328 | 83.56% | 68.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14060` | Jalisco | Mascota | 10,999 | 6,120 | 3,071 | 1,808 | 83.56% | 55.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31015` | Yucatán | Cuzamá | 4,144 | 2,899 | 564 | 681 | 83.57% | 69.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30030` | Veracruz | Calcahualco | 7,867 | 3,260 | 3,317 | 1,290 | 83.60% | 41.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20509` | Oaxaca | Santo Domingo Ingenio | 6,868 | 4,252 | 1,490 | 1,126 | 83.61% | 61.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12069` | Guerrero | La Unión de Isidoro Montes de Oca | 21,830 | 12,891 | 5,361 | 3,578 | 83.61% | 59.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30072` | Veracruz | Hidalgotitlán | 12,300 | 6,798 | 3,486 | 2,016 | 83.61% | 55.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08054` | Chihuahua | Riva Palacio | 7,847 | 3,014 | 3,547 | 1,286 | 83.61% | 38.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16004` | Michoacán | Angamacutiro | 12,431 | 6,571 | 3,824 | 2,036 | 83.62% | 52.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31068` | Yucatán | Sinanché | 2,438 | 1,784 | 255 | 399 | 83.63% | 73.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31015` | Yucatán | Cuzamá | 3,794 | 2,721 | 453 | 620 | 83.66% | 71.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14088` | Jalisco | Tecalitlán | 14,386 | 7,188 | 4,848 | 2,350 | 83.66% | 49.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `13024` | Hidalgo | Huasca de Ocampo | 14,319 | 4,384 | 7,612 | 2,323 | 83.78% | 30.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08005` | Chihuahua | Ascensión | 18,655 | 6,332 | 9,299 | 3,024 | 83.79% | 33.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07040` | Chiapas | Huixtla | 37,283 | 10,831 | 20,411 | 6,041 | 83.80% | 29.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `05026` | Coahuila | Progreso | 2,876 | 1,823 | 587 | 466 | 83.80% | 63.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20140` | Oaxaca | San Francisco Ixhuatán | 6,994 | 4,547 | 1,315 | 1,132 | 83.81% | 65.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31062` | Yucatán | Sacalum | 3,475 | 2,653 | 260 | 562 | 83.83% | 76.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32016` | Zacatecas | General Pánfilo Natera | 18,315 | 9,174 | 6,181 | 2,960 | 83.84% | 50.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16025` | Michoacán | Chilchota | 26,743 | 14,606 | 7,815 | 4,322 | 83.84% | 54.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21111` | Puebla | Palmar de Bravo | 29,236 | 17,306 | 7,210 | 4,720 | 83.86% | 59.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08009` | Chihuahua | Bocoyna | 21,351 | 10,729 | 7,177 | 3,445 | 83.86% | 50.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29059` | Tlaxcala | San Lorenzo Axocomanitla | 3,762 | 2,218 | 937 | 607 | 83.86% | 58.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `18013` | Nayarit | San Pedro Lagunillas | 6,325 | 2,253 | 3,052 | 1,020 | 83.87% | 35.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19038` | Nuevo León | Mina | 4,709 | 2,893 | 1,057 | 759 | 83.88% | 61.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08007` | Chihuahua | Balleza | 13,068 | 7,277 | 3,686 | 2,105 | 83.89% | 55.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31061` | Yucatán | Río Lagartos | 2,909 | 2,199 | 242 | 468 | 83.91% | 75.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30093` | Veracruz | Jesús Carranza | 19,322 | 9,032 | 7,182 | 3,108 | 83.91% | 46.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14050` | Jalisco | Jesús María | 16,286 | 7,665 | 6,006 | 2,615 | 83.94% | 47.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30186` | Veracruz | Tonayán | 4,282 | 3,022 | 574 | 686 | 83.98% | 70.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08057` | Chihuahua | San Francisco de Borja | 2,360 | 1,417 | 565 | 378 | 83.98% | 60.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12029` | Guerrero | Chilpancingo de los Bravo | 175,010 | 66,423 | 80,575 | 28,012 | 83.99% | 37.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21127` | Puebla | San Jerónimo Tecuanipan | 3,794 | 1,248 | 1,939 | 607 | 84.00% | 32.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27002` | Tabasco | Cárdenas | 168,338 | 77,260 | 64,165 | 26,913 | 84.01% | 45.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14125` | Jalisco | San Ignacio Cerro Gordo | 14,383 | 6,416 | 5,668 | 2,299 | 84.02% | 44.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08050` | Chihuahua | Nuevo Casas Grandes | 48,323 | 21,283 | 19,319 | 7,721 | 84.02% | 44.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `03004` | Baja California Sur | Los Cabos | 178,732 | 65,270 | 84,920 | 28,542 | 84.03% | 36.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20225` | Oaxaca | San Lorenzo | 3,927 | 2,723 | 577 | 627 | 84.03% | 69.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `08046` | Chihuahua | Morelos | 3,107 | 1,365 | 1,246 | 496 | 84.04% | 43.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08045` | Chihuahua | Meoqui | 32,949 | 10,263 | 17,427 | 5,259 | 84.04% | 31.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08010` | Chihuahua | Buenaventura | 18,426 | 8,795 | 6,693 | 2,938 | 84.06% | 47.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20138` | Oaxaca | San Francisco del Mar | 5,858 | 3,895 | 1,031 | 932 | 84.09% | 66.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07004` | Chiapas | Altamirano | 23,837 | 10,274 | 9,772 | 3,791 | 84.10% | 43.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31078` | Yucatán | Tekantó | 2,960 | 2,226 | 264 | 470 | 84.12% | 75.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31018` | Yucatán | Chapab | 3,221 | 2,369 | 341 | 511 | 84.14% | 73.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `31025` | Yucatán | Dzán | 3,543 | 2,639 | 342 | 562 | 84.14% | 74.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `19004` | Nuevo León | Allende | 23,274 | 10,675 | 8,911 | 3,688 | 84.15% | 45.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19049` | Nuevo León | Santiago | 40,354 | 20,750 | 13,213 | 6,391 | 84.16% | 51.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15117` | Estado de México | Zacazonapan | 4,075 | 2,539 | 891 | 645 | 84.17% | 62.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07049` | Chiapas | Larráinzar | 19,194 | 10,318 | 5,839 | 3,037 | 84.18% | 53.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07075` | Chiapas | Sabanilla | 20,850 | 14,877 | 2,676 | 3,297 | 84.19% | 71.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26005` | Sonora | Arizpe | 2,970 | 1,771 | 730 | 469 | 84.21% | 59.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31008` | Yucatán | Calotmul | 3,211 | 2,444 | 260 | 507 | 84.21% | 76.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08017` | Chihuahua | Cuauhtémoc | 144,991 | 56,971 | 65,139 | 22,881 | 84.22% | 39.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26058` | Sonora | Bácum | 17,612 | 7,706 | 7,136 | 2,770 | 84.27% | 43.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31079` | Yucatán | Tekax | 32,682 | 19,714 | 7,828 | 5,140 | 84.27% | 60.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `13073` | Hidalgo | Tlaxcoapan | 19,917 | 6,983 | 9,802 | 3,132 | 84.27% | 35.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08064` | Chihuahua | El Tule | 2,342 | 1,412 | 562 | 368 | 84.29% | 60.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30054` | Veracruz | Cuichapa | 9,057 | 4,804 | 2,831 | 1,422 | 84.30% | 53.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20037` | Oaxaca | Heroica Ciudad de Huajuapan de León | 52,749 | 7,982 | 36,514 | 8,253 | 84.35% | 15.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21023` | Puebla | Atzitzintla | 6,645 | 4,237 | 1,369 | 1,039 | 84.36% | 63.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07022` | Chiapas | Chalchihuitán | 13,678 | 9,066 | 2,475 | 2,137 | 84.38% | 66.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29017` | Tlaxcala | Mazatecochco de José María Morelos | 7,968 | 4,974 | 1,750 | 1,244 | 84.39% | 62.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13028` | Hidalgo | Huejutla de Reyes | 88,351 | 49,604 | 24,954 | 13,793 | 84.39% | 56.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `18016` | Nayarit | Tecuala | 29,221 | 15,254 | 9,406 | 4,561 | 84.39% | 52.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16026` | Michoacán | Chinicuila | 3,857 | 1,915 | 1,340 | 602 | 84.39% | 49.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13081` | Hidalgo | Zacualtipán de Ángeles | 29,025 | 14,171 | 10,324 | 4,530 | 84.39% | 48.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30143` | Veracruz | San Juan Evangelista | 23,874 | 12,285 | 7,864 | 3,725 | 84.40% | 51.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08050` | Chihuahua | Nuevo Casas Grandes | 50,651 | 18,968 | 23,781 | 7,902 | 84.40% | 37.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07061` | Chiapas | Ocozocoautla de Espinosa | 62,686 | 36,908 | 16,000 | 9,778 | 84.40% | 58.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20415` | Oaxaca | Santa María Huazolotitlán | 8,439 | 4,873 | 2,252 | 1,314 | 84.43% | 57.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07028` | Chiapas | Chiapilla | 3,970 | 1,389 | 1,963 | 618 | 84.43% | 34.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26056` | Sonora | San Miguel de Horcasitas | 4,722 | 2,524 | 1,463 | 735 | 84.43% | 53.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26015` | Sonora | Cananea | 31,009 | 11,759 | 14,427 | 4,823 | 84.45% | 37.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05038` | Coahuila | Zaragoza | 11,467 | 5,644 | 4,040 | 1,783 | 84.45% | 49.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `24016` | San Luis Potosí | Ebano | 30,498 | 16,099 | 9,657 | 4,742 | 84.45% | 52.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07078` | Chiapas | San Fernando | 25,478 | 16,533 | 4,984 | 3,961 | 84.45% | 64.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07081` | Chiapas | Siltepec | 18,925 | 9,723 | 6,260 | 2,942 | 84.45% | 51.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28023` | Tamaulipas | Méndez | 3,964 | 2,444 | 904 | 616 | 84.46% | 61.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `12047` | Guerrero | Ometepec | 36,276 | 10,706 | 19,933 | 5,637 | 84.46% | 29.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `13075` | Hidalgo | Tula de Allende | 79,979 | 26,201 | 41,357 | 12,421 | 84.47% | 32.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04007` | Campeche | Palizada | 7,401 | 4,907 | 1,345 | 1,149 | 84.48% | 66.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19019` | Nuevo León | San Pedro Garza García | 103,718 | 58,070 | 29,552 | 16,096 | 84.48% | 55.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20460` | Oaxaca | Santiago Choápam | 3,597 | 1,233 | 1,806 | 558 | 84.49% | 34.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31094` | Yucatán | Tixmehuac | 3,425 | 2,708 | 186 | 531 | 84.50% | 79.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26002` | Sonora | Agua Prieta | 60,678 | 24,312 | 26,962 | 9,404 | 84.50% | 40.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16064` | Michoacán | Panindícuaro | 13,795 | 6,845 | 4,814 | 2,136 | 84.52% | 49.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20447` | Oaxaca | Santa María Yucuhiti | 4,754 | 2,208 | 1,810 | 736 | 84.52% | 46.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07011` | Chiapas | Bella Vista | 14,584 | 8,409 | 3,918 | 2,257 | 84.52% | 57.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07073` | Chiapas | Reforma | 30,917 | 16,874 | 9,259 | 4,784 | 84.53% | 54.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26026` | Sonora | Moctezuma | 4,022 | 2,640 | 760 | 622 | 84.54% | 65.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26068` | Sonora | Rosario | 4,740 | 2,720 | 1,287 | 733 | 84.54% | 57.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19043` | Nuevo León | Los Ramones | 5,221 | 2,768 | 1,646 | 807 | 84.54% | 53.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07093` | Chiapas | Tecpatán | 16,339 | 9,648 | 4,167 | 2,524 | 84.55% | 59.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29060` | Tlaxcala | Benito Juárez | 4,280 | 2,222 | 1,397 | 661 | 84.56% | 51.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07046` | Chiapas | Jiquipilas | 33,061 | 19,813 | 8,144 | 5,104 | 84.56% | 59.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08016` | Chihuahua | La Cruz | 3,713 | 2,012 | 1,128 | 573 | 84.57% | 54.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08028` | Chihuahua | Guadalupe | 4,612 | 2,308 | 1,593 | 711 | 84.58% | 50.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12073` | Guerrero | Zapotitlán Tablas | 6,242 | 3,871 | 1,409 | 962 | 84.59% | 62.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12022` | Guerrero | Coyuca de Catalán | 31,923 | 14,990 | 12,017 | 4,916 | 84.60% | 46.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13038` | Hidalgo | Mineral del Chico | 7,626 | 4,438 | 2,014 | 1,174 | 84.61% | 58.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31104` | Yucatán | Yaxcabá | 10,233 | 7,321 | 1,337 | 1,575 | 84.61% | 71.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16055` | Michoacán | Morelos | 8,326 | 3,909 | 3,136 | 1,281 | 84.61% | 46.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07107` | Chiapas | Villacomaltitlán | 23,295 | 12,513 | 7,198 | 3,584 | 84.61% | 53.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07023` | Chiapas | Chamula | 74,171 | 34,900 | 27,861 | 11,410 | 84.62% | 47.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31002` | Yucatán | Acanceh | 12,757 | 9,037 | 1,758 | 1,962 | 84.62% | 70.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07045` | Chiapas | Ixtapangajoya | 4,378 | 3,232 | 473 | 673 | 84.63% | 73.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26012` | Sonora | Baviácora | 3,247 | 2,304 | 444 | 499 | 84.63% | 70.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20252` | Oaxaca | San Mateo Río Hondo | 2,419 | 1,553 | 495 | 371 | 84.66% | 64.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14053` | Jalisco | Juanacatlán | 9,474 | 5,166 | 2,855 | 1,453 | 84.66% | 54.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08025` | Chihuahua | Gómez Farías | 6,854 | 2,839 | 2,964 | 1,051 | 84.67% | 41.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15043` | Estado de México | Ixtlahuaca | 107,519 | 63,210 | 27,835 | 16,474 | 84.68% | 58.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `05026` | Coahuila | Progreso | 2,794 | 1,193 | 1,173 | 428 | 84.68% | 42.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15088` | Estado de México | Temoaya | 60,456 | 26,180 | 25,020 | 9,256 | 84.69% | 43.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14033` | Jalisco | Chiquilistlán | 4,653 | 2,654 | 1,287 | 712 | 84.70% | 57.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14025` | Jalisco | Cocula | 25,514 | 13,182 | 8,433 | 3,899 | 84.72% | 51.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20515` | Oaxaca | Santo Domingo Tehuantepec | 45,356 | 18,691 | 19,734 | 6,931 | 84.72% | 41.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `12032` | Guerrero | General Canuto A. Neri | 4,505 | 2,711 | 1,106 | 688 | 84.73% | 60.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08004` | Chihuahua | Aquiles Serdán | 9,492 | 2,519 | 5,525 | 1,448 | 84.75% | 26.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13028` | Hidalgo | Huejutla de Reyes | 74,746 | 28,376 | 34,969 | 11,401 | 84.75% | 37.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26036` | Sonora | Santa Ana | 12,040 | 6,390 | 3,814 | 1,836 | 84.75% | 53.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11004` | Guanajuato | Apaseo el Alto | 50,108 | 21,829 | 20,650 | 7,629 | 84.77% | 43.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20252` | Oaxaca | San Mateo Río Hondo | 2,595 | 1,669 | 531 | 395 | 84.78% | 64.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31019` | Yucatán | Chemax | 26,267 | 18,600 | 3,672 | 3,995 | 84.79% | 70.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08026` | Chihuahua | Gran Morelos | 3,381 | 1,737 | 1,130 | 514 | 84.80% | 51.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05002` | Coahuila | Acuña | 130,100 | 60,212 | 50,117 | 19,771 | 84.80% | 46.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07079` | Chiapas | San Juan Cancuc | 23,069 | 14,366 | 5,198 | 3,505 | 84.81% | 62.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15072` | Estado de México | Polotitlán | 11,855 | 6,634 | 3,420 | 1,801 | 84.81% | 55.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `27009` | Tabasco | Jalapa | 29,026 | 16,689 | 7,934 | 4,403 | 84.83% | 57.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `03001` | Baja California Sur | Comondú | 53,666 | 27,205 | 18,326 | 8,135 | 84.84% | 50.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19047` | Nuevo León | San Nicolás de los Garza | 365,168 | 187,984 | 121,854 | 55,330 | 84.85% | 51.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14085` | Jalisco | Talpa de Allende | 11,195 | 6,585 | 2,915 | 1,695 | 84.86% | 58.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20310` | Oaxaca | San Pedro Jicayán | 8,302 | 4,968 | 2,079 | 1,255 | 84.88% | 59.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14045` | Jalisco | La Huerta | 19,521 | 9,922 | 6,656 | 2,943 | 84.92% | 50.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31047` | Yucatán | Maní | 4,220 | 3,255 | 329 | 636 | 84.93% | 77.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20414` | Oaxaca | Santa María Huatulco | 28,985 | 9,782 | 14,839 | 4,364 | 84.94% | 33.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12025` | Guerrero | Cuautepec | 11,313 | 7,186 | 2,424 | 1,703 | 84.95% | 63.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30012` | Veracruz | Alvarado | 41,448 | 21,229 | 13,982 | 6,237 | 84.95% | 51.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07008` | Chiapas | Angel Albino Corzo | 18,826 | 11,273 | 4,721 | 2,832 | 84.96% | 59.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08024` | Chihuahua | Santa Isabel | 4,665 | 2,355 | 1,609 | 701 | 84.97% | 50.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20410` | Oaxaca | Santa María del Tule | 6,392 | 1,842 | 3,590 | 960 | 84.98% | 28.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15070` | Estado de México | Papalotla | 4,024 | 2,603 | 817 | 604 | 84.99% | 64.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08062` | Chihuahua | Saucillo | 25,132 | 10,954 | 10,406 | 3,772 | 84.99% | 43.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31034` | Yucatán | Hocabá | 4,666 | 3,309 | 657 | 700 | 85.00% | 70.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31075` | Yucatán | Teabo | 4,660 | 3,577 | 384 | 699 | 85.00% | 76.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07103` | Chiapas | Tuzantán | 23,326 | 12,529 | 7,300 | 3,497 | 85.01% | 53.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12013` | Guerrero | Azoyú | 11,033 | 6,705 | 2,674 | 1,654 | 85.01% | 60.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24018` | San Luis Potosí | Huehuetlán | 10,226 | 6,176 | 2,517 | 1,533 | 85.01% | 60.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07040` | Chiapas | Huixtla | 40,992 | 20,255 | 14,602 | 6,135 | 85.03% | 49.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19020` | Nuevo León | Gral. Bravo | 6,497 | 3,549 | 1,977 | 971 | 85.05% | 54.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31095` | Yucatán | Tixpéhual | 4,508 | 3,275 | 560 | 673 | 85.07% | 72.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31106` | Yucatán | Yobaín | 2,030 | 1,527 | 200 | 303 | 85.07% | 75.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16068` | Michoacán | Penjamillo | 15,754 | 7,864 | 5,539 | 2,351 | 85.08% | 49.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `17014` | Morelos | Mazatepec | 7,443 | 4,736 | 1,597 | 1,110 | 85.09% | 63.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `27006` | Tabasco | Cunduacán | 91,994 | 51,403 | 26,889 | 13,702 | 85.11% | 55.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `21017` | Puebla | Atempan | 13,125 | 3,926 | 7,245 | 1,954 | 85.11% | 29.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07065` | Chiapas | Palenque | 96,107 | 55,027 | 26,792 | 14,288 | 85.13% | 57.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08004` | Chihuahua | Aquiles Serdán | 15,706 | 6,355 | 7,017 | 2,334 | 85.14% | 40.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08066` | Chihuahua | Uruachi | 5,498 | 1,209 | 3,472 | 817 | 85.14% | 21.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20123` | Oaxaca | San Cristóbal Amatlán | 3,967 | 1,832 | 1,546 | 589 | 85.15% | 46.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14063` | Jalisco | Mezquitic | 16,085 | 9,530 | 4,172 | 2,383 | 85.18% | 59.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08045` | Chihuahua | Meoqui | 34,632 | 14,740 | 14,766 | 5,126 | 85.20% | 42.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14088` | Jalisco | Tecalitlán | 12,853 | 7,096 | 3,856 | 1,901 | 85.21% | 55.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21081` | Puebla | Huitziltepec | 4,025 | 2,676 | 754 | 595 | 85.22% | 66.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21148` | Puebla | Santa Isabel Cholula | 8,072 | 3,623 | 3,257 | 1,192 | 85.23% | 44.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08062` | Chihuahua | Saucillo | 25,681 | 11,429 | 10,460 | 3,792 | 85.23% | 44.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21066` | Puebla | General Felipe Ángeles | 15,469 | 8,843 | 4,344 | 2,282 | 85.25% | 57.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19010` | Nuevo León | El Carmen | 32,600 | 10,403 | 17,388 | 4,809 | 85.25% | 31.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13023` | Hidalgo | Francisco I. Madero | 29,325 | 16,585 | 8,418 | 4,322 | 85.26% | 56.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07029` | Chiapas | Chicoasén | 4,441 | 2,992 | 795 | 654 | 85.27% | 67.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07062` | Chiapas | Ostuacán | 12,924 | 8,691 | 2,330 | 1,903 | 85.28% | 67.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21081` | Puebla | Huitziltepec | 3,889 | 1,044 | 2,273 | 572 | 85.29% | 26.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14051` | Jalisco | Jilotlán de los Dolores | 6,348 | 2,778 | 2,637 | 933 | 85.30% | 43.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30114` | Veracruz | Naranjal | 3,579 | 1,967 | 1,087 | 525 | 85.33% | 54.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15005` | Estado de México | Almoloya de Juárez | 111,693 | 64,616 | 30,696 | 16,381 | 85.33% | 57.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `05012` | Coahuila | Guerrero | 1,807 | 1,153 | 389 | 265 | 85.33% | 63.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `12051` | Guerrero | Pungarabato | 29,294 | 12,687 | 12,311 | 4,296 | 85.33% | 43.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26060` | Sonora | Empalme | 39,170 | 17,511 | 15,920 | 5,739 | 85.35% | 44.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16103` | Michoacán | Uruapan | 210,335 | 57,814 | 121,753 | 30,768 | 85.37% | 27.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28037` | Tamaulipas | Soto la Marina | 19,992 | 11,184 | 5,884 | 2,924 | 85.37% | 55.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14054` | Jalisco | Juchitlán | 5,139 | 2,694 | 1,694 | 751 | 85.39% | 52.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07048` | Chiapas | Juárez | 16,446 | 9,678 | 4,365 | 2,403 | 85.39% | 58.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16007` | Michoacán | Aporo | 2,698 | 1,839 | 465 | 394 | 85.40% | 68.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08023` | Chihuahua | Galeana | 4,365 | 2,349 | 1,379 | 637 | 85.41% | 53.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20310` | Oaxaca | San Pedro Jicayán | 7,889 | 4,943 | 1,795 | 1,151 | 85.41% | 62.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26024` | Sonora | Imuris | 9,668 | 4,253 | 4,007 | 1,408 | 85.44% | 43.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20542` | Oaxaca | Tataltepec de Valdés | 4,072 | 1,695 | 1,784 | 593 | 85.44% | 41.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21203` | Puebla | Xochitlán Todos Santos | 4,816 | 2,915 | 1,200 | 701 | 85.44% | 60.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `27010` | Tabasco | Jalpa de Méndez | 62,418 | 41,335 | 12,006 | 9,077 | 85.46% | 66.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20105` | Oaxaca | San Antonio Huitepec | 2,147 | 1,042 | 793 | 312 | 85.47% | 48.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12035` | Guerrero | Huitzuco de los Figueroa | 28,330 | 12,745 | 11,470 | 4,115 | 85.47% | 44.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `27008` | Tabasco | Huimanguillo | 137,159 | 68,323 | 48,923 | 19,913 | 85.48% | 49.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30128` | Veracruz | La Perla | 14,046 | 8,047 | 3,961 | 2,038 | 85.49% | 57.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31063` | Yucatán | Samahil | 3,977 | 3,051 | 349 | 577 | 85.49% | 76.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20405` | Oaxaca | Santa María Chimalapa | 4,846 | 1,941 | 2,202 | 703 | 85.49% | 40.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `01001` | Aguascalientes | Aguascalientes | 533,517 | 191,384 | 264,795 | 77,338 | 85.50% | 35.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12075` | Guerrero | Zitlala | 15,299 | 9,454 | 3,630 | 2,215 | 85.52% | 61.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30173` | Veracruz | Tierra Blanca | 73,928 | 33,990 | 29,236 | 10,702 | 85.52% | 45.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15124` | Estado de México | San José del Rincón | 64,471 | 34,872 | 20,267 | 9,332 | 85.53% | 54.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20175` | Oaxaca | San Juan Bautista Cuicatlán | 6,995 | 2,595 | 3,389 | 1,011 | 85.55% | 37.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20469` | Oaxaca | Santiago Jocotepec | 8,849 | 5,244 | 2,328 | 1,277 | 85.57% | 59.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30193` | Veracruz | Villa Aldama | 8,397 | 5,600 | 1,586 | 1,211 | 85.58% | 66.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29025` | Tlaxcala | San Pablo del Monte | 54,385 | 30,520 | 16,022 | 7,843 | 85.58% | 56.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `18006` | Nayarit | Huajicori | 6,596 | 3,014 | 2,631 | 951 | 85.58% | 45.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32002` | Zacatecas | Apulco | 4,204 | 1,968 | 1,630 | 606 | 85.59% | 46.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08002` | Chihuahua | Aldama | 17,965 | 5,531 | 9,845 | 2,589 | 85.59% | 30.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12070` | Guerrero | Xalpatláhuac | 9,099 | 5,282 | 2,507 | 1,310 | 85.60% | 58.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `24001` | San Luis Potosí | Ahualulco | 14,796 | 8,032 | 4,634 | 2,130 | 85.60% | 54.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25012` | Sinaloa | Mazatlán | 350,510 | 166,480 | 133,572 | 50,458 | 85.60% | 47.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04009` | Campeche | Escárcega | 39,866 | 22,136 | 11,997 | 5,733 | 85.62% | 55.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19051` | Nuevo León | Villaldama | 3,672 | 2,511 | 633 | 528 | 85.62% | 68.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20154` | Oaxaca | San Jacinto Amilpas | 9,719 | 3,086 | 5,236 | 1,397 | 85.63% | 31.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20453` | Oaxaca | Santiago Apóstol | 3,452 | 1,181 | 1,775 | 496 | 85.63% | 34.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26057` | Sonora | Ures | 8,849 | 5,295 | 2,283 | 1,271 | 85.64% | 59.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15040` | Estado de México | Ixtapaluca | 314,782 | 124,998 | 144,599 | 45,185 | 85.65% | 39.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31092` | Yucatán | Tixcacalcupul | 5,049 | 3,830 | 496 | 723 | 85.68% | 75.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15116` | Estado de México | Xonacatlán | 41,550 | 26,159 | 9,444 | 5,947 | 85.69% | 62.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21075` | Puebla | Huehuetlán el Grande | 5,054 | 3,198 | 1,134 | 722 | 85.71% | 63.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21020` | Puebla | Atoyatempan | 4,905 | 3,327 | 878 | 700 | 85.73% | 67.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08023` | Chihuahua | Galeana | 3,841 | 1,286 | 2,007 | 548 | 85.73% | 33.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19051` | Nuevo León | Villaldama | 3,883 | 2,641 | 690 | 552 | 85.78% | 68.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12044` | Guerrero | Metlatónoc | 12,561 | 7,256 | 3,520 | 1,785 | 85.79% | 57.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20542` | Oaxaca | Tataltepec de Valdés | 3,766 | 1,959 | 1,272 | 535 | 85.79% | 52.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16049` | Michoacán | Lagunillas | 4,753 | 3,032 | 1,046 | 675 | 85.80% | 63.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08065` | Chihuahua | Urique | 13,061 | 2,947 | 8,260 | 1,854 | 85.81% | 22.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `29035` | Tlaxcala | Tocatlán | 3,623 | 984 | 2,125 | 514 | 85.81% | 27.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `17008` | Morelos | Emiliano Zapata | 57,082 | 29,363 | 19,624 | 8,095 | 85.82% | 51.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14090` | Jalisco | Techaluta de Montenegro | 3,438 | 1,989 | 962 | 487 | 85.83% | 57.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14051` | Jalisco | Jilotlán de los Dolores | 6,446 | 3,868 | 1,665 | 913 | 85.84% | 60.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16066` | Michoacán | Paracho | 25,430 | 12,839 | 8,992 | 3,599 | 85.85% | 50.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26027` | Sonora | Naco | 4,602 | 2,608 | 1,343 | 651 | 85.85% | 56.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31079` | Yucatán | Tekax | 29,361 | 19,344 | 5,864 | 4,153 | 85.86% | 65.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07050` | Chiapas | La Libertad | 4,500 | 3,371 | 493 | 636 | 85.87% | 74.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08044` | Chihuahua | Matamoros | 4,126 | 2,365 | 1,178 | 583 | 85.87% | 57.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16098` | Michoacán | Turicato | 24,434 | 13,367 | 7,618 | 3,449 | 85.88% | 54.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07018` | Chiapas | Coapilla | 5,294 | 2,357 | 2,190 | 747 | 85.89% | 44.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15008` | Estado de México | Amatepec | 20,579 | 13,257 | 4,422 | 2,900 | 85.91% | 64.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31003` | Yucatán | Akil | 8,328 | 5,415 | 1,740 | 1,173 | 85.91% | 65.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19002` | Nuevo León | Agualeguas | 3,792 | 2,416 | 842 | 534 | 85.92% | 63.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21118` | Puebla | Rafael Lara Grajales | 14,413 | 7,901 | 4,484 | 2,028 | 85.93% | 54.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30170` | Veracruz | Texhuacán | 4,368 | 2,050 | 1,704 | 614 | 85.94% | 46.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30025` | Veracruz | Tlaltetela | 9,092 | 4,758 | 3,056 | 1,278 | 85.94% | 52.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19022` | Nuevo León | General Terán | 13,008 | 6,820 | 4,362 | 1,826 | 85.96% | 52.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31004` | Yucatán | Baca | 4,519 | 3,286 | 599 | 634 | 85.97% | 72.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21106` | Puebla | Ocotepec | 3,837 | 2,419 | 880 | 538 | 85.98% | 63.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16113` | Michoacán | Zitácuaro | 120,433 | 51,106 | 52,445 | 16,882 | 85.98% | 42.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07071` | Chiapas | Pueblo Nuevo Solistahuacán | 18,664 | 11,681 | 4,372 | 2,611 | 86.01% | 62.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08009` | Chihuahua | Bocoyna | 20,625 | 11,255 | 6,485 | 2,885 | 86.01% | 54.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08065` | Chihuahua | Urique | 12,492 | 2,764 | 7,981 | 1,747 | 86.02% | 22.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26049` | Sonora | Hermosillo | 552,672 | 237,165 | 238,217 | 77,290 | 86.02% | 42.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15073` | Estado de México | Rayón | 7,901 | 5,151 | 1,647 | 1,103 | 86.04% | 65.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13025` | Hidalgo | Huautla | 15,402 | 6,679 | 6,573 | 2,150 | 86.04% | 43.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30078` | Veracruz | Ilamatlán | 9,483 | 4,549 | 3,614 | 1,320 | 86.08% | 47.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15088` | Estado de México | Temoaya | 66,560 | 37,944 | 19,367 | 9,249 | 86.10% | 57.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13035` | Hidalgo | Lolotla | 7,167 | 4,532 | 1,640 | 995 | 86.12% | 63.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08057` | Chihuahua | San Francisco de Borja | 2,652 | 785 | 1,499 | 368 | 86.12% | 29.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `29050` | Tlaxcala | San José Teacalco | 4,210 | 2,589 | 1,037 | 584 | 86.13% | 61.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07112` | Chiapas | Aldama | 3,757 | 2,405 | 831 | 521 | 86.13% | 64.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29011` | Tlaxcala | Muñoz de Domingo Arenas | 3,737 | 2,292 | 927 | 518 | 86.14% | 61.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08038` | Chihuahua | Julimes | 4,572 | 1,646 | 2,293 | 633 | 86.15% | 36.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20122` | Oaxaca | San Carlos Yautepec | 6,875 | 2,778 | 3,147 | 950 | 86.18% | 40.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15095` | Estado de México | Tepetlixpa | 14,706 | 8,411 | 4,263 | 2,032 | 86.18% | 57.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `27002` | Tabasco | Cárdenas | 182,041 | 86,393 | 70,510 | 25,138 | 86.19% | 47.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16082` | Michoacán | Susupuato | 6,896 | 4,654 | 1,290 | 952 | 86.19% | 67.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07103` | Chiapas | Tuzantán | 19,312 | 7,296 | 9,350 | 2,666 | 86.20% | 37.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16040` | Michoacán | Indaparapeo | 13,669 | 7,018 | 4,765 | 1,886 | 86.20% | 51.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07013` | Chiapas | Bochil | 26,048 | 15,245 | 7,212 | 3,591 | 86.21% | 58.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07016` | Chiapas | Catazajá | 13,299 | 9,122 | 2,344 | 1,833 | 86.22% | 68.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31044` | Yucatán | Kinchil | 5,021 | 3,836 | 493 | 692 | 86.22% | 76.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13065` | Hidalgo | Tetepango | 9,564 | 6,095 | 2,151 | 1,318 | 86.22% | 63.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15058` | Estado de México | Naucalpan de Juárez | 710,816 | 393,180 | 220,003 | 97,633 | 86.26% | 55.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16056` | Michoacán | Múgica | 34,242 | 14,203 | 15,336 | 4,703 | 86.27% | 41.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30166` | Veracruz | Tepetzintla | 10,581 | 5,816 | 3,314 | 1,451 | 86.29% | 54.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16007` | Michoacán | Aporo | 2,562 | 1,747 | 464 | 351 | 86.30% | 68.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05031` | Coahuila | San Buenaventura | 17,812 | 10,014 | 5,362 | 2,436 | 86.32% | 56.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30121` | Veracruz | Oteapan | 7,921 | 3,110 | 3,729 | 1,082 | 86.34% | 39.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30027` | Veracruz | Banderilla | 16,059 | 5,731 | 8,135 | 2,193 | 86.34% | 35.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `11016` | Guanajuato | Huanímaro | 16,307 | 8,775 | 5,306 | 2,226 | 86.35% | 53.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19018` | Nuevo León | García | 157,626 | 59,604 | 76,513 | 21,509 | 86.35% | 37.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16068` | Michoacán | Penjamillo | 16,116 | 7,295 | 6,623 | 2,198 | 86.36% | 45.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07054` | Chiapas | Mazatán | 20,125 | 10,917 | 6,464 | 2,744 | 86.37% | 54.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31052` | Yucatán | Motul | 27,265 | 16,950 | 6,604 | 3,711 | 86.39% | 62.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21137` | Puebla | San Miguel Xoxtla | 9,787 | 6,034 | 2,421 | 1,332 | 86.39% | 61.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12046` | Guerrero | Olinalá | 18,413 | 11,493 | 4,415 | 2,505 | 86.40% | 62.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16094` | Michoacán | Tlalpujahua | 18,989 | 11,086 | 5,320 | 2,583 | 86.40% | 58.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `13004` | Hidalgo | Agua Blanca de Iturbide | 7,426 | 2,562 | 3,854 | 1,010 | 86.40% | 34.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31011` | Yucatán | Celestún | 5,500 | 3,906 | 846 | 748 | 86.40% | 71.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26057` | Sonora | Ures | 9,972 | 4,973 | 3,644 | 1,355 | 86.41% | 49.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12044` | Guerrero | Metlatónoc | 11,211 | 6,739 | 2,949 | 1,523 | 86.42% | 60.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `06008` | Colima | Manzanillo | 126,616 | 60,246 | 49,171 | 17,199 | 86.42% | 47.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26055` | Sonora | San Luis Río Colorado | 169,145 | 56,645 | 89,526 | 22,974 | 86.42% | 33.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07008` | Chiapas | Angel Albino Corzo | 21,815 | 8,951 | 9,904 | 2,960 | 86.43% | 41.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15007` | Estado de México | Amanalco | 16,143 | 10,374 | 3,582 | 2,187 | 86.45% | 64.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21167` | Puebla | Tepexco | 4,881 | 3,254 | 966 | 661 | 86.46% | 66.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07016` | Chiapas | Catazajá | 13,744 | 9,159 | 2,724 | 1,861 | 86.46% | 66.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16078` | Michoacán | San Lucas | 16,376 | 4,262 | 9,897 | 2,217 | 86.46% | 26.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07069` | Chiapas | Pijijiapan | 36,121 | 21,440 | 9,796 | 4,885 | 86.48% | 59.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13032` | Hidalgo | Jaltocán | 7,382 | 3,309 | 3,075 | 998 | 86.48% | 44.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08062` | Chihuahua | Saucillo | 23,900 | 8,193 | 12,477 | 3,230 | 86.49% | 34.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21167` | Puebla | Tepexco | 5,419 | 3,326 | 1,361 | 732 | 86.49% | 61.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `09013` | Ciudad de México | Xochimilco | 324,394 | 110,840 | 169,740 | 43,814 | 86.49% | 34.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15068` | Estado de México | Otzolotepec | 50,540 | 25,110 | 18,604 | 6,826 | 86.49% | 49.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30149` | Veracruz | Soledad De Doblado | 22,609 | 11,096 | 8,460 | 3,053 | 86.50% | 49.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19028` | Nuevo León | Hidalgo | 13,313 | 7,605 | 3,912 | 1,796 | 86.51% | 57.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20035` | Oaxaca | Guevea de Humboldt | 3,760 | 1,659 | 1,594 | 507 | 86.52% | 44.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30166` | Veracruz | Tepetzintla | 10,224 | 6,587 | 2,260 | 1,377 | 86.53% | 64.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12078` | Guerrero | Iliatenco | 6,512 | 4,174 | 1,461 | 877 | 86.53% | 64.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26065` | Sonora | Navojoa | 125,018 | 45,996 | 62,193 | 16,829 | 86.54% | 36.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16092` | Michoacán | Tingüindín | 11,042 | 5,886 | 3,670 | 1,486 | 86.54% | 53.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `17028` | Morelos | Xochitepec | 53,465 | 22,964 | 23,308 | 7,193 | 86.55% | 42.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07015` | Chiapas | Cacahoatán | 32,162 | 20,206 | 7,632 | 4,324 | 86.56% | 62.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07017` | Chiapas | Cintalapa | 66,210 | 33,320 | 23,989 | 8,901 | 86.56% | 50.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25010` | Sinaloa | El Fuerte | 74,337 | 36,242 | 28,107 | 9,988 | 86.56% | 48.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30148` | Veracruz | Soledad Atzompa | 15,855 | 8,124 | 5,602 | 2,129 | 86.57% | 51.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07009` | Chiapas | Arriaga | 30,789 | 16,243 | 10,412 | 4,134 | 86.57% | 52.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20307` | Oaxaca | San Pedro Ixcatlán | 7,808 | 5,425 | 1,335 | 1,048 | 86.58% | 69.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12033` | Guerrero | General Heliodoro Castillo | 23,299 | 9,488 | 10,687 | 3,124 | 86.59% | 40.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29053` | Tlaxcala | San Damián Texóloc | 4,901 | 3,131 | 1,113 | 657 | 86.59% | 63.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21184` | Puebla | Tlapacoya | 5,345 | 3,547 | 1,082 | 716 | 86.60% | 66.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07109` | Chiapas | Villaflores | 76,462 | 41,480 | 24,744 | 10,238 | 86.61% | 54.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20038` | Oaxaca | Huautepec | 4,504 | 3,062 | 839 | 603 | 86.61% | 67.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20010` | Oaxaca | Ayoquezco de Aldama | 3,847 | 1,292 | 2,040 | 515 | 86.61% | 33.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21189` | Puebla | Tochtepec | 12,916 | 4,149 | 7,038 | 1,729 | 86.61% | 32.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07076` | Chiapas | Salto De Agua | 46,228 | 31,528 | 8,515 | 6,185 | 86.62% | 68.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31009` | Yucatán | Cansahcab | 3,866 | 2,826 | 523 | 517 | 86.63% | 73.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12034` | Guerrero | Huamuxtitlán | 11,681 | 7,263 | 2,856 | 1,562 | 86.63% | 62.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12010` | Guerrero | Atlixtac | 15,473 | 9,773 | 3,636 | 2,064 | 86.66% | 63.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20121` | Oaxaca | San Blas Atempa | 12,982 | 7,914 | 3,338 | 1,730 | 86.67% | 60.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11030` | Guanajuato | San Felipe | 80,941 | 34,406 | 35,759 | 10,776 | 86.69% | 42.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11044` | Guanajuato | Villagrán | 45,588 | 23,975 | 15,546 | 6,067 | 86.69% | 52.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26055` | Sonora | San Luis Río Colorado | 139,010 | 45,042 | 75,482 | 18,486 | 86.70% | 32.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04006` | Campeche | Hopelchén | 26,997 | 17,317 | 6,090 | 3,590 | 86.70% | 64.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16008` | Michoacán | Aquila | 19,904 | 11,162 | 6,097 | 2,645 | 86.71% | 56.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12080` | Guerrero | Marquelia | 10,149 | 5,832 | 2,971 | 1,346 | 86.74% | 57.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07042` | Chiapas | Ixhuatán | 7,556 | 4,840 | 1,714 | 1,002 | 86.74% | 64.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08027` | Chihuahua | Guachochi | 37,596 | 17,405 | 15,206 | 4,985 | 86.74% | 46.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20394` | Oaxaca | Santa Lucía Monteverde | 4,269 | 2,039 | 1,664 | 566 | 86.74% | 47.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31053` | Yucatán | Muna | 9,694 | 6,636 | 1,773 | 1,285 | 86.74% | 68.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `17001` | Morelos | Amacuzac | 13,796 | 6,929 | 5,039 | 1,828 | 86.75% | 50.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `21072` | Puebla | Huauchinango | 60,090 | 22,473 | 29,655 | 7,962 | 86.75% | 37.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16064` | Michoacán | Panindícuaro | 14,245 | 7,243 | 5,117 | 1,885 | 86.77% | 50.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30120` | Veracruz | Otatitlán | 4,190 | 2,052 | 1,584 | 554 | 86.78% | 48.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20167` | Oaxaca | San José Independencia | 3,481 | 2,487 | 534 | 460 | 86.79% | 71.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12007` | Guerrero | Arcelia | 23,808 | 12,631 | 8,031 | 3,146 | 86.79% | 53.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14027` | Jalisco | Concepción de Buenos Aires | 5,609 | 3,363 | 1,505 | 741 | 86.79% | 59.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `14044` | Jalisco | Huejuquilla el Alto | 5,552 | 3,203 | 1,616 | 733 | 86.80% | 57.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `11016` | Guanajuato | Huanímaro | 17,734 | 9,407 | 5,986 | 2,341 | 86.80% | 53.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30124` | Veracruz | Pánuco | 69,048 | 34,450 | 25,494 | 9,104 | 86.81% | 49.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12002` | Guerrero | Ahuacuotzingo | 16,901 | 10,247 | 4,426 | 2,228 | 86.82% | 60.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32004` | Zacatecas | Benito Juárez | 3,827 | 2,180 | 1,143 | 504 | 86.83% | 56.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31075` | Yucatán | Teabo | 4,955 | 3,721 | 582 | 652 | 86.84% | 75.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07078` | Chiapas | San Fernando | 29,625 | 17,727 | 8,000 | 3,898 | 86.84% | 59.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07082` | Chiapas | Simojovel | 36,203 | 21,594 | 9,855 | 4,754 | 86.87% | 59.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07029` | Chiapas | Chicoasén | 4,660 | 3,165 | 884 | 611 | 86.89% | 67.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `25009` | Sinaloa | Escuinapa | 38,710 | 12,866 | 20,769 | 5,075 | 86.89% | 33.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29015` | Tlaxcala | Ixtacuixtla de Mariano Matamoros | 31,614 | 17,930 | 9,540 | 4,144 | 86.89% | 56.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07018` | Chiapas | Coapilla | 5,913 | 4,323 | 815 | 775 | 86.89% | 73.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31101` | Yucatán | Umán | 49,785 | 27,461 | 15,799 | 6,525 | 86.89% | 55.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31080` | Yucatán | Tekit | 8,485 | 6,445 | 928 | 1,112 | 86.89% | 75.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15090` | Estado de México | Tenango del Aire | 9,620 | 6,204 | 2,157 | 1,259 | 86.91% | 64.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32002` | Zacatecas | Apulco | 4,326 | 1,632 | 2,128 | 566 | 86.92% | 37.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31055` | Yucatán | Opichén | 4,510 | 3,269 | 652 | 589 | 86.94% | 72.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30058` | Veracruz | Chiconamel | 4,933 | 3,417 | 872 | 644 | 86.95% | 69.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `27012` | Tabasco | Macuspana | 116,099 | 66,476 | 34,472 | 15,151 | 86.95% | 57.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31012` | Yucatán | Cenotillo | 3,045 | 2,232 | 416 | 397 | 86.96% | 73.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30089` | Veracruz | Xalapa | 394,200 | 214,736 | 128,107 | 51,357 | 86.97% | 54.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31037` | Yucatán | Huhí | 4,346 | 3,176 | 604 | 566 | 86.98% | 73.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29050` | Tlaxcala | San José Teacalco | 4,769 | 3,088 | 1,060 | 621 | 86.98% | 64.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07059` | Chiapas | Ocosingo | 123,395 | 43,812 | 63,520 | 16,063 | 86.98% | 35.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20004` | Oaxaca | Asunción Cacalotepec | 1,769 | 672 | 867 | 230 | 87.00% | 37.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12051` | Guerrero | Pungarabato | 29,152 | 15,226 | 10,136 | 3,790 | 87.00% | 52.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15115` | Estado de México | Villa Victoria | 58,702 | 37,635 | 13,437 | 7,630 | 87.00% | 64.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08037` | Chihuahua | Juárez | 1,144,591 | 376,067 | 619,888 | 148,636 | 87.01% | 32.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30200` | Veracruz | Zentla | 8,945 | 5,225 | 2,559 | 1,161 | 87.02% | 58.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20411` | Oaxaca | Santa María Ecatepec | 2,182 | 824 | 1,075 | 283 | 87.03% | 37.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20127` | Oaxaca | San Dionisio del Mar | 4,250 | 2,687 | 1,012 | 551 | 87.04% | 63.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07073` | Chiapas | Reforma | 27,717 | 12,156 | 11,970 | 3,591 | 87.04% | 43.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08008` | Chihuahua | Batopilas | 8,115 | 1,716 | 5,348 | 1,051 | 87.05% | 21.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30020` | Veracruz | Astacinga | 4,509 | 2,614 | 1,312 | 583 | 87.07% | 57.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07009` | Chiapas | Arriaga | 32,044 | 16,020 | 11,881 | 4,143 | 87.07% | 49.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12039` | Guerrero | Zihuatanejo de Azueta | 93,095 | 38,083 | 42,978 | 12,034 | 87.07% | 40.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19042` | Nuevo León | Pesquería | 70,795 | 19,961 | 41,691 | 9,143 | 87.09% | 28.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24036` | San Luis Potosí | Tamasopo | 22,830 | 12,798 | 7,085 | 2,947 | 87.09% | 56.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30005` | Veracruz | Acula | 4,016 | 1,982 | 1,516 | 518 | 87.10% | 49.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12063` | Guerrero | Tlacoachistlahuaca | 14,779 | 9,011 | 3,862 | 1,906 | 87.10% | 60.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13053` | Hidalgo | San Felipe Orizatlán | 27,615 | 16,293 | 7,761 | 3,561 | 87.10% | 59.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20044` | Oaxaca | Loma Bonita | 28,951 | 16,767 | 8,452 | 3,732 | 87.11% | 57.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07104` | Chiapas | Tzimol | 10,623 | 7,686 | 1,570 | 1,367 | 87.13% | 72.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07031` | Chiapas | Chilón | 89,329 | 59,265 | 18,578 | 11,486 | 87.14% | 66.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13079` | Hidalgo | Xochicoatlán | 5,382 | 3,209 | 1,481 | 692 | 87.14% | 59.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28037` | Tamaulipas | Soto la Marina | 18,742 | 11,380 | 4,953 | 2,409 | 87.15% | 60.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07093` | Chiapas | Tecpatán | 28,333 | 12,756 | 11,939 | 3,638 | 87.16% | 45.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28007` | Tamaulipas | Camargo | 12,770 | 6,160 | 4,971 | 1,639 | 87.17% | 48.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20503` | Oaxaca | Santiago Zacatepec | 3,465 | 802 | 2,219 | 444 | 87.19% | 23.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16049` | Michoacán | Lagunillas | 5,549 | 3,303 | 1,535 | 711 | 87.19% | 59.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08037` | Chihuahua | Juárez | 1,069,317 | 445,138 | 487,191 | 136,988 | 87.19% | 41.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14081` | Jalisco | San Sebastián del Oeste | 4,874 | 2,913 | 1,338 | 623 | 87.22% | 59.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26012` | Sonora | Baviácora | 3,446 | 2,087 | 919 | 440 | 87.23% | 60.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26058` | Sonora | Bácum | 17,328 | 8,887 | 6,230 | 2,211 | 87.24% | 51.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `06007` | Colima | Ixtlahuacán | 5,369 | 3,400 | 1,284 | 685 | 87.24% | 63.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31007` | Yucatán | Cacalchén | 5,307 | 3,905 | 725 | 677 | 87.24% | 73.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08036` | Chihuahua | Jiménez | 28,856 | 10,521 | 14,654 | 3,681 | 87.24% | 36.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29022` | Tlaxcala | Acuamanala de Miguel Hidalgo | 4,871 | 3,490 | 760 | 621 | 87.25% | 71.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15007` | Estado de México | Amanalco | 19,899 | 12,019 | 5,344 | 2,536 | 87.26% | 60.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07046` | Chiapas | Jiquipilas | 31,904 | 19,254 | 8,592 | 4,058 | 87.28% | 60.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08055` | Chihuahua | Rosales | 14,477 | 7,362 | 5,274 | 1,841 | 87.28% | 50.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `25008` | Sinaloa | Elota | 25,282 | 10,810 | 11,257 | 3,215 | 87.28% | 42.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19030` | Nuevo León | Hualahuises | 6,307 | 3,693 | 1,812 | 802 | 87.28% | 58.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07099` | Chiapas | La Trinitaria | 57,293 | 37,997 | 12,017 | 7,279 | 87.30% | 66.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30124` | Veracruz | Pánuco | 68,376 | 39,698 | 19,995 | 8,683 | 87.30% | 58.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08036` | Chihuahua | Jiménez | 29,905 | 15,457 | 10,652 | 3,796 | 87.31% | 51.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25013` | Sinaloa | Mocorito | 35,982 | 18,426 | 12,996 | 4,560 | 87.33% | 51.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20057` | Oaxaca | Matías Romero Avendaño | 29,309 | 16,191 | 9,404 | 3,714 | 87.33% | 55.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15048` | Estado de México | Jiquipilco | 51,235 | 30,903 | 13,842 | 6,490 | 87.33% | 60.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `26028` | Sonora | Nácori Chico | 1,469 | 1,093 | 190 | 186 | 87.34% | 74.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16002` | Michoacán | Aguililla | 11,009 | 3,607 | 6,009 | 1,393 | 87.35% | 32.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20210` | Oaxaca | San Juan Ñumí | 4,822 | 1,401 | 2,812 | 609 | 87.37% | 29.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08007` | Chihuahua | Balleza | 12,293 | 3,537 | 7,204 | 1,552 | 87.37% | 28.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30078` | Veracruz | Ilamatlán | 8,453 | 4,283 | 3,104 | 1,066 | 87.39% | 50.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `29058` | Tlaxcala | Santa Ana Nopalucan | 4,886 | 2,265 | 2,005 | 616 | 87.39% | 46.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19018` | Nuevo León | García | 247,932 | 103,185 | 113,497 | 31,250 | 87.40% | 41.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11029` | Guanajuato | San Diego de la Unión | 27,250 | 13,563 | 10,256 | 3,431 | 87.41% | 49.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24004` | San Luis Potosí | Armadillo de los Infante | 3,721 | 2,417 | 837 | 467 | 87.45% | 64.96% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30083` | Veracruz | Ixhuatlán del Café | 13,438 | 6,163 | 5,589 | 1,686 | 87.45% | 45.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31063` | Yucatán | Samahil | 3,748 | 2,954 | 324 | 470 | 87.46% | 78.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `18002` | Nayarit | Ahuacatlán | 12,518 | 6,591 | 4,358 | 1,569 | 87.47% | 52.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21061` | Puebla | Domingo Arenas | 5,018 | 3,179 | 1,211 | 628 | 87.49% | 63.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07030` | Chiapas | Chicomuselo | 25,599 | 15,845 | 6,556 | 3,198 | 87.51% | 61.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15080` | Estado de México | Soyaniquilpan de Juárez | 11,734 | 8,477 | 1,792 | 1,465 | 87.51% | 72.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `06007` | Colima | Ixtlahuacán | 5,257 | 3,391 | 1,210 | 656 | 87.52% | 64.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `24035` | San Luis Potosí | Soledad de Graciano Sánchez | 212,807 | 102,947 | 83,320 | 26,540 | 87.53% | 48.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `01008` | Aguascalientes | San José de Gracía | 7,778 | 5,021 | 1,787 | 970 | 87.53% | 64.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07020` | Chiapas | La Concordia | 32,883 | 21,653 | 7,132 | 4,098 | 87.54% | 65.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21012` | Puebla | Aljojuca | 5,194 | 3,551 | 996 | 647 | 87.54% | 68.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13008` | Hidalgo | Apan | 33,190 | 18,320 | 10,736 | 4,134 | 87.54% | 55.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16080` | Michoacán | Salvador Escalante | 29,002 | 10,109 | 15,282 | 3,611 | 87.55% | 34.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20066` | Oaxaca | Oaxaca de Juárez | 216,381 | 69,584 | 119,880 | 26,917 | 87.56% | 32.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20192` | Oaxaca | San Juan Cotzocón | 14,262 | 5,745 | 6,743 | 1,774 | 87.56% | 40.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07035` | Chiapas | Frontera Hidalgo | 10,095 | 6,247 | 2,593 | 1,255 | 87.57% | 61.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16002` | Michoacán | Aguililla | 15,799 | 3,096 | 10,740 | 1,963 | 87.58% | 19.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26025` | Sonora | Magdalena | 25,338 | 10,628 | 11,562 | 3,148 | 87.58% | 41.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12058` | Guerrero | Técpan de Galeana | 45,293 | 22,103 | 17,565 | 5,625 | 87.58% | 48.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07037` | Chiapas | Huehuetán | 27,948 | 16,301 | 8,179 | 3,468 | 87.59% | 58.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30007` | Veracruz | Camarón de Tejeda | 5,023 | 3,605 | 795 | 623 | 87.60% | 71.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16098` | Michoacán | Turicato | 23,611 | 7,283 | 13,403 | 2,925 | 87.61% | 30.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21154` | Puebla | Tecomatlán | 4,794 | 2,245 | 1,956 | 593 | 87.63% | 46.83% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31055` | Yucatán | Opichén | 5,144 | 3,837 | 671 | 636 | 87.64% | 74.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19034` | Nuevo León | Linares | 68,791 | 28,278 | 32,009 | 8,504 | 87.64% | 41.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31047` | Yucatán | Maní | 4,062 | 3,206 | 354 | 502 | 87.64% | 78.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `05010` | Coahuila | Frontera | 61,400 | 32,412 | 21,402 | 7,586 | 87.64% | 52.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07055` | Chiapas | Metapa | 4,914 | 3,170 | 1,137 | 607 | 87.65% | 64.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `13016` | Hidalgo | Chapantongo | 9,215 | 4,491 | 3,586 | 1,138 | 87.65% | 48.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15081` | Estado de México | Sultepec | 18,738 | 12,209 | 4,216 | 2,313 | 87.66% | 65.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26055` | Sonora | San Luis Río Colorado | 150,587 | 53,142 | 78,858 | 18,587 | 87.66% | 35.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `28040` | Tamaulipas | Valle Hermoso | 47,439 | 21,884 | 19,707 | 5,848 | 87.67% | 46.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24044` | San Luis Potosí | Vanegas | 5,314 | 3,234 | 1,425 | 655 | 87.67% | 60.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30164` | Veracruz | Tepatlaxco | 5,990 | 3,321 | 1,931 | 738 | 87.68% | 55.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08037` | Chihuahua | Juárez | 1,249,327 | 519,967 | 575,457 | 153,903 | 87.68% | 41.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12034` | Guerrero | Huamuxtitlán | 11,243 | 6,798 | 3,062 | 1,383 | 87.70% | 60.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `07090` | Chiapas | Tapachula | 192,727 | 65,894 | 103,129 | 23,704 | 87.70% | 34.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07023` | Chiapas | Chamula | 62,270 | 39,237 | 15,378 | 7,655 | 87.71% | 63.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15079` | Estado de México | Santo Tomás | 7,024 | 4,870 | 1,291 | 863 | 87.71% | 69.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `17018` | Morelos | Temixco | 81,175 | 33,577 | 37,631 | 9,967 | 87.72% | 41.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15090` | Estado de México | Tenango del Aire | 8,935 | 5,665 | 2,173 | 1,097 | 87.72% | 63.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `27014` | Tabasco | Paraíso | 74,833 | 43,697 | 21,961 | 9,175 | 87.74% | 58.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20006` | Oaxaca | Asunción Ixtaltepec | 11,914 | 8,077 | 2,377 | 1,460 | 87.75% | 67.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21012` | Puebla | Aljojuca | 4,858 | 3,510 | 753 | 595 | 87.75% | 72.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30009` | Veracruz | Alpatláhuac | 6,075 | 2,718 | 2,613 | 744 | 87.75% | 44.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08060` | Chihuahua | Santa Bárbara | 8,797 | 5,030 | 2,690 | 1,077 | 87.76% | 57.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31055` | Yucatán | Opichén | 5,416 | 4,045 | 708 | 663 | 87.76% | 74.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07122` | Chiapas | Emiliano Zapata | 9,217 | 5,669 | 2,420 | 1,128 | 87.76% | 61.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21193` | Puebla | Tzicatlacoyan | 5,075 | 3,430 | 1,024 | 621 | 87.76% | 67.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `02007` | Baja California | San Felipe | 15,169 | 7,077 | 6,236 | 1,856 | 87.76% | 46.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07048` | Chiapas | Juárez | 15,158 | 9,697 | 3,608 | 1,853 | 87.78% | 63.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `24026` | San Luis Potosí | San Antonio | 6,750 | 4,732 | 1,193 | 825 | 87.78% | 70.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20201` | Oaxaca | San Juan Juquila Mixes | 2,543 | 788 | 1,445 | 310 | 87.81% | 30.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20364` | Oaxaca | Santa Catarina Juquila | 11,364 | 7,638 | 2,341 | 1,385 | 87.81% | 67.21% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `24007` | San Luis Potosí | Cedral | 13,707 | 8,224 | 3,813 | 1,670 | 87.82% | 60.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12052` | Guerrero | Quechultenango | 22,506 | 12,741 | 7,023 | 2,742 | 87.82% | 56.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19024` | Nuevo León | Gral. Zaragoza | 5,558 | 3,872 | 1,009 | 677 | 87.82% | 69.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16014` | Michoacán | Coahuayana | 9,747 | 5,414 | 3,146 | 1,187 | 87.82% | 55.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07001` | Chiapas | Acacoyagua | 13,180 | 7,284 | 4,291 | 1,605 | 87.82% | 55.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20201` | Oaxaca | San Juan Juquila Mixes | 2,621 | 527 | 1,775 | 319 | 87.83% | 20.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25016` | Sinaloa | San Ignacio | 15,867 | 8,370 | 5,566 | 1,931 | 87.83% | 52.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `17026` | Morelos | Tlayacapan | 15,264 | 10,036 | 3,372 | 1,856 | 87.84% | 65.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16017` | Michoacán | Contepec | 21,831 | 13,114 | 6,063 | 2,654 | 87.84% | 60.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19042` | Nuevo León | Pesquería | 50,678 | 18,149 | 26,370 | 6,159 | 87.85% | 35.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08002` | Chihuahua | Aldama | 19,842 | 9,619 | 7,813 | 2,410 | 87.85% | 48.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12007` | Guerrero | Arcelia | 23,969 | 12,581 | 8,480 | 2,908 | 87.87% | 52.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `17021` | Morelos | Tetecala | 6,513 | 4,491 | 1,232 | 790 | 87.87% | 68.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16046` | Michoacán | José Sixto Verduzco | 21,421 | 11,365 | 7,459 | 2,597 | 87.88% | 53.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21199` | Puebla | Xiutetelco | 28,304 | 15,991 | 8,883 | 3,430 | 87.88% | 56.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12068` | Guerrero | Tlapehuala | 16,824 | 9,928 | 4,858 | 2,038 | 87.89% | 59.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20022` | Oaxaca | Concepción Pápalo | 2,114 | 1,234 | 624 | 256 | 87.89% | 58.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31047` | Yucatán | Maní | 4,534 | 3,323 | 662 | 549 | 87.89% | 73.29% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08052` | Chihuahua | Ojinaga | 27,154 | 11,337 | 12,530 | 3,287 | 87.89% | 41.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15039` | Estado de México | Isidro Fabela | 9,323 | 5,941 | 2,254 | 1,128 | 87.90% | 63.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19046` | Nuevo León | Salinas Victoria | 29,618 | 15,111 | 10,925 | 3,582 | 87.91% | 51.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14008` | Jalisco | Arandas | 55,804 | 28,837 | 20,227 | 6,740 | 87.92% | 51.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12046` | Guerrero | Olinalá | 16,948 | 10,435 | 4,468 | 2,045 | 87.93% | 61.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16030` | Michoacán | Ecuandureo | 11,256 | 5,772 | 4,129 | 1,355 | 87.96% | 51.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08031` | Chihuahua | Guerrero | 30,790 | 13,514 | 13,577 | 3,699 | 87.99% | 43.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `18018` | Nayarit | Tuxpan | 23,768 | 14,109 | 6,805 | 2,854 | 87.99% | 59.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05007` | Coahuila | Cuatro Ciénegas | 9,465 | 5,470 | 2,859 | 1,136 | 88.00% | 57.79% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31067` | Yucatán | Seyé | 7,309 | 5,419 | 1,013 | 877 | 88.00% | 74.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `20413` | Oaxaca | Santa María Guienagati | 1,876 | 722 | 929 | 225 | 88.01% | 38.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13066` | Hidalgo | Tezontepec de Aldama | 36,395 | 20,993 | 11,038 | 4,364 | 88.01% | 57.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04011` | Campeche | Calakmul | 18,972 | 12,291 | 4,408 | 2,273 | 88.02% | 64.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `05038` | Coahuila | Zaragoza | 9,784 | 3,338 | 5,275 | 1,171 | 88.03% | 34.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08062` | Chihuahua | Saucillo | 24,621 | 12,249 | 9,426 | 2,946 | 88.03% | 49.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19018` | Nuevo León | García | 199,021 | 62,669 | 112,580 | 23,772 | 88.06% | 31.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `24035` | San Luis Potosí | Soledad de Graciano Sánchez | 247,180 | 123,870 | 93,787 | 29,523 | 88.06% | 50.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16064` | Michoacán | Panindícuaro | 14,925 | 3,428 | 9,717 | 1,780 | 88.07% | 22.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20207` | Oaxaca | San Juan Mazatlán | 12,302 | 7,264 | 3,571 | 1,467 | 88.08% | 59.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04005` | Campeche | Hecelchakán | 22,098 | 15,781 | 3,682 | 2,635 | 88.08% | 71.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13016` | Hidalgo | Chapantongo | 8,756 | 3,827 | 3,885 | 1,044 | 88.08% | 43.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28027` | Tamaulipas | Nuevo Laredo | 310,391 | 141,200 | 132,220 | 36,971 | 88.09% | 45.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `10028` | Durango | San Juan de Guadalupe | 4,476 | 2,407 | 1,536 | 533 | 88.09% | 53.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21001` | Puebla | Acajete | 44,025 | 25,153 | 13,638 | 5,234 | 88.11% | 57.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31017` | Yucatán | Chankom | 3,903 | 3,196 | 243 | 464 | 88.11% | 81.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19046` | Nuevo León | Salinas Victoria | 39,283 | 18,328 | 16,289 | 4,666 | 88.12% | 46.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20481` | Oaxaca | Santiago Niltepec | 3,976 | 1,304 | 2,200 | 472 | 88.13% | 32.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `23009` | Quintana Roo | Tulum | 30,419 | 17,713 | 9,096 | 3,610 | 88.13% | 58.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07028` | Chiapas | Chiapilla | 4,644 | 3,122 | 971 | 551 | 88.14% | 67.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07015` | Chiapas | Cacahoatán | 29,892 | 14,160 | 12,187 | 3,545 | 88.14% | 47.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29031` | Tlaxcala | Tetla de la Solidaridad | 23,180 | 12,721 | 7,712 | 2,747 | 88.15% | 54.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `23002` | Quintana Roo | Cozumel | 62,121 | 23,154 | 31,609 | 7,358 | 88.16% | 37.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32044` | Zacatecas | Tabasco | 13,020 | 6,745 | 4,733 | 1,542 | 88.16% | 51.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12024` | Guerrero | Cualác | 5,126 | 3,407 | 1,112 | 607 | 88.16% | 66.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07045` | Chiapas | Ixtapangajoya | 4,632 | 3,246 | 838 | 548 | 88.17% | 70.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `24033` | San Luis Potosí | Santa María del Río | 30,535 | 18,445 | 8,478 | 3,612 | 88.17% | 60.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16013` | Michoacán | Carácuaro | 7,178 | 4,670 | 1,659 | 849 | 88.17% | 65.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20481` | Oaxaca | Santiago Niltepec | 4,211 | 3,014 | 699 | 498 | 88.17% | 71.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08067` | Chihuahua | Valle de Zaragoza | 4,440 | 2,432 | 1,483 | 525 | 88.18% | 54.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31032` | Yucatán | Espita | 11,473 | 7,738 | 2,379 | 1,356 | 88.18% | 67.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `17008` | Morelos | Emiliano Zapata | 46,426 | 20,180 | 20,765 | 5,481 | 88.19% | 43.47% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29046` | Tlaxcala | Santa Cruz Quilehtla | 5,712 | 3,849 | 1,189 | 674 | 88.20% | 67.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08060` | Chihuahua | Santa Bárbara | 8,619 | 5,131 | 2,471 | 1,017 | 88.20% | 59.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26063` | Sonora | Etchojoa | 45,701 | 20,678 | 19,635 | 5,388 | 88.21% | 45.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08013` | Chihuahua | Casas Grandes | 12,176 | 5,594 | 5,147 | 1,435 | 88.21% | 45.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07097` | Chiapas | Tonalá | 71,696 | 33,664 | 29,589 | 8,443 | 88.22% | 46.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25014` | Sinaloa | Rosario | 37,933 | 21,073 | 12,394 | 4,466 | 88.23% | 55.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14073` | Jalisco | San Cristóbal de la Barranca | 3,063 | 1,673 | 1,030 | 360 | 88.25% | 54.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26056` | Sonora | San Miguel de Horcasitas | 6,043 | 2,098 | 3,235 | 710 | 88.25% | 34.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07107` | Chiapas | Villa Comaltitlán | 22,480 | 13,035 | 6,807 | 2,638 | 88.27% | 57.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `30075` | Veracruz | Hueyapan de Ocampo | 29,441 | 15,907 | 10,080 | 3,454 | 88.27% | 54.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12042` | Guerrero | Malinaltepec | 16,753 | 9,548 | 5,240 | 1,965 | 88.27% | 56.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14059` | Jalisco | La Manzanilla de la Paz | 3,428 | 2,222 | 805 | 401 | 88.30% | 64.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08050` | Chihuahua | Nuevo Casas Grandes | 45,892 | 13,281 | 27,252 | 5,359 | 88.32% | 28.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20427` | Oaxaca | Santa María Petapa | 10,719 | 3,668 | 5,800 | 1,251 | 88.33% | 34.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07028` | Chiapas | Chiapilla | 4,945 | 3,554 | 814 | 577 | 88.33% | 71.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15087` | Estado de México | Temascaltepec | 23,868 | 15,902 | 5,182 | 2,784 | 88.34% | 66.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08029` | Chihuahua | Guadalupe y Calvo | 27,457 | 6,472 | 17,785 | 3,200 | 88.35% | 23.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08059` | Chihuahua | San Francisco del Oro | 4,232 | 2,697 | 1,042 | 493 | 88.35% | 63.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14107` | Jalisco | Tuxcacuesco | 4,269 | 2,744 | 1,028 | 497 | 88.36% | 64.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21085` | Puebla | Ixtacamaxtitlán | 17,912 | 11,960 | 3,868 | 2,084 | 88.37% | 66.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21177` | Puebla | San Sebastián Tlacotepec | 8,172 | 5,675 | 1,547 | 950 | 88.37% | 69.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16020` | Michoacán | Cuitzeo | 21,090 | 5,691 | 12,949 | 2,450 | 88.38% | 26.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `17001` | Morelos | Amacuzac | 13,141 | 7,938 | 3,677 | 1,526 | 88.39% | 60.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16066` | Michoacán | Paracho | 23,630 | 13,053 | 7,835 | 2,742 | 88.40% | 55.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07076` | Chiapas | Salto de Agua | 43,607 | 29,711 | 8,836 | 5,060 | 88.40% | 68.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32054` | Zacatecas | Villa Hidalgo | 13,660 | 8,413 | 3,662 | 1,585 | 88.40% | 61.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15043` | Estado de México | Ixtlahuaca | 100,673 | 45,951 | 43,044 | 11,678 | 88.40% | 45.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26060` | Sonora | Empalme | 41,658 | 16,905 | 19,922 | 4,831 | 88.40% | 40.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21026` | Puebla | Calpan | 11,145 | 6,168 | 3,686 | 1,291 | 88.42% | 55.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20102` | Oaxaca | San Antonino Monte Verde | 4,654 | 1,829 | 2,286 | 539 | 88.42% | 39.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31053` | Yucatán | Muna | 10,528 | 7,263 | 2,046 | 1,219 | 88.42% | 68.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16006` | Michoacán | Apatzingán | 92,583 | 31,859 | 50,013 | 10,711 | 88.43% | 34.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07057` | Chiapas | Motozintla | 48,110 | 27,202 | 15,347 | 5,561 | 88.44% | 56.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `24022` | San Luis Potosí | Moctezuma | 14,720 | 8,618 | 4,401 | 1,701 | 88.44% | 58.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21089` | Puebla | Jolalpan | 9,478 | 6,020 | 2,363 | 1,095 | 88.45% | 63.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07094` | Chiapas | Tenejapa | 31,813 | 21,112 | 7,026 | 3,675 | 88.45% | 66.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25001` | Sinaloa | Ahome | 321,132 | 172,443 | 111,629 | 37,060 | 88.46% | 53.70% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16066` | Michoacán | Paracho | 23,519 | 7,140 | 13,665 | 2,714 | 88.46% | 30.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16029` | Michoacán | Churumuco | 10,623 | 5,855 | 3,543 | 1,225 | 88.47% | 55.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `08066` | Chihuahua | Uruachi | 5,021 | 2,932 | 1,510 | 579 | 88.47% | 58.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30168` | Veracruz | José Azueta | 17,679 | 8,546 | 7,097 | 2,036 | 88.48% | 48.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07074` | Chiapas | Las Rosas | 17,991 | 11,734 | 4,186 | 2,071 | 88.49% | 65.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08001` | Chihuahua | Ahumada | 9,922 | 5,052 | 3,728 | 1,142 | 88.49% | 50.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20537` | Oaxaca | Soledad Etla | 5,299 | 3,271 | 1,419 | 609 | 88.51% | 61.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16043` | Michoacán | Jacona | 54,444 | 21,478 | 26,711 | 6,255 | 88.51% | 39.45% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07107` | Chiapas | Villa Comaltitlán | 21,059 | 12,539 | 6,102 | 2,418 | 88.52% | 59.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20490` | Oaxaca | Santiago Tetepec | 3,451 | 2,266 | 789 | 396 | 88.53% | 65.66% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21168` | Puebla | Tepexi de Rodríguez | 13,545 | 5,986 | 6,005 | 1,554 | 88.53% | 44.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21160` | Puebla | Tepanco de López | 17,354 | 10,512 | 4,853 | 1,989 | 88.54% | 60.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `18007` | Nayarit | Ixtlán del Río | 22,183 | 10,873 | 8,769 | 2,541 | 88.55% | 49.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08003` | Chihuahua | Allende | 7,260 | 4,380 | 2,049 | 831 | 88.55% | 60.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20292` | Oaxaca | San Pablo Huitzo | 5,627 | 3,373 | 1,610 | 644 | 88.56% | 59.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07036` | Chiapas | La Grandeza | 4,902 | 3,250 | 1,091 | 561 | 88.56% | 66.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15010` | Estado de México | Apaxco | 24,117 | 13,877 | 7,480 | 2,760 | 88.56% | 57.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20087` | Oaxaca | San Andrés Huaxpaltepec | 4,405 | 2,880 | 1,021 | 504 | 88.56% | 65.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05020` | Coahuila | Múzquiz | 53,018 | 27,359 | 19,598 | 6,061 | 88.57% | 51.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08011` | Chihuahua | Camargo | 37,986 | 19,083 | 14,568 | 4,335 | 88.59% | 50.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16079` | Michoacán | Santa Ana Maya | 10,891 | 5,319 | 4,330 | 1,242 | 88.60% | 48.84% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `28013` | Tamaulipas | Güémez | 12,684 | 8,383 | 2,855 | 1,446 | 88.60% | 66.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07100` | Chiapas | Tumbalá | 22,625 | 16,279 | 3,767 | 2,579 | 88.60% | 71.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04009` | Campeche | Escárcega | 42,567 | 22,176 | 15,542 | 4,849 | 88.61% | 52.10% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30047` | Veracruz | Cosamaloapan | 41,255 | 21,046 | 15,511 | 4,698 | 88.61% | 51.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `05031` | Coahuila | San Buenaventura | 18,728 | 10,166 | 6,430 | 2,132 | 88.62% | 54.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `29018` | Tlaxcala | Contla de Juan Cuamatzi | 27,928 | 16,625 | 8,124 | 3,179 | 88.62% | 59.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07006` | Chiapas | Amatenango de la Frontera | 21,173 | 13,591 | 5,174 | 2,408 | 88.63% | 64.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08066` | Chihuahua | Uruachi | 4,922 | 2,975 | 1,388 | 559 | 88.64% | 60.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `32004` | Zacatecas | Benito Juárez | 3,478 | 2,133 | 950 | 395 | 88.64% | 61.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14113` | Jalisco | Valle de Juárez | 6,307 | 3,444 | 2,147 | 716 | 88.65% | 54.61% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `27007` | Tabasco | Emiliano Zapata | 24,620 | 15,153 | 6,674 | 2,793 | 88.66% | 61.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16090` | Michoacán | Tepalcatepec | 16,097 | 8,288 | 5,983 | 1,826 | 88.66% | 51.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12025` | Guerrero | Cuautepec | 10,662 | 7,094 | 2,359 | 1,209 | 88.66% | 66.54% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `04001` | Campeche | Campeche | 218,115 | 123,550 | 69,843 | 24,722 | 88.67% | 56.64% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31058` | Yucatán | Peto | 16,396 | 11,274 | 3,264 | 1,858 | 88.67% | 68.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20344` | Oaxaca | San Sebastián Río Hondo | 2,872 | 1,279 | 1,268 | 325 | 88.68% | 44.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08065` | Chihuahua | Urique | 13,777 | 7,404 | 4,814 | 1,559 | 88.68% | 53.74% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14072` | Jalisco | El Salto | 80,660 | 35,450 | 36,085 | 9,125 | 88.69% | 43.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `12080` | Guerrero | Marquelia | 9,872 | 5,962 | 2,794 | 1,116 | 88.70% | 60.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08059` | Chihuahua | San Francisco del Oro | 4,448 | 1,563 | 2,384 | 501 | 88.74% | 35.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13080` | Hidalgo | Yahualica | 13,978 | 8,094 | 4,310 | 1,574 | 88.74% | 57.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20570` | Oaxaca | Zimatlán de Álvarez | 15,245 | 9,907 | 3,622 | 1,716 | 88.74% | 64.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `23005` | Quintana Roo | José María Morelos | 29,871 | 21,273 | 5,236 | 3,362 | 88.74% | 71.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `28005` | Tamaulipas | Burgos | 4,453 | 1,875 | 2,077 | 501 | 88.75% | 42.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `12045` | Guerrero | Mochitlán | 8,063 | 5,171 | 1,985 | 907 | 88.75% | 64.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31017` | Yucatán | Chankom | 3,344 | 2,744 | 224 | 376 | 88.76% | 82.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `31011` | Yucatán | Celestún | 4,510 | 3,312 | 691 | 507 | 88.76% | 73.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07087` | Chiapas | Suchiapa | 16,543 | 11,177 | 3,507 | 1,859 | 88.76% | 67.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04012` | Campeche | Dzitblache | 11,472 | 7,763 | 2,421 | 1,288 | 88.77% | 67.67% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26002` | Sonora | Agua Prieta | 64,815 | 26,604 | 30,939 | 7,272 | 88.78% | 41.05% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32054` | Zacatecas | Villa Hidalgo | 14,181 | 8,847 | 3,743 | 1,591 | 88.78% | 62.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `15017` | Estado de México | Ayapango | 6,197 | 4,047 | 1,455 | 695 | 88.78% | 65.31% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15009` | Estado de México | Amecameca | 40,264 | 25,576 | 10,173 | 4,515 | 88.79% | 63.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16034` | Michoacán | Hidalgo | 83,492 | 38,803 | 35,336 | 9,353 | 88.80% | 46.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25018` | Sinaloa | Navolato | 108,381 | 46,844 | 49,411 | 12,126 | 88.81% | 43.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21091` | Puebla | Jopala | 9,753 | 6,159 | 2,503 | 1,091 | 88.81% | 63.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15122` | Estado de México | Valle de Chalco Solidaridad | 247,882 | 103,426 | 116,735 | 27,721 | 88.82% | 41.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `28034` | Tamaulipas | San Carlos | 7,039 | 3,997 | 2,255 | 787 | 88.82% | 56.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08032` | Chihuahua | Hidalgo del Parral | 79,994 | 25,369 | 45,683 | 8,942 | 88.82% | 31.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24047` | San Luis Potosí | Villa de Arriaga | 11,569 | 8,099 | 2,177 | 1,293 | 88.82% | 70.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21071` | Puebla | Huatlatlauca | 5,094 | 3,457 | 1,068 | 569 | 88.83% | 67.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30146` | Veracruz | Soconusco | 10,631 | 6,618 | 2,826 | 1,187 | 88.83% | 62.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `26008` | Sonora | Bacanora | 2,302 | 1,453 | 592 | 257 | 88.84% | 63.12% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `14054` | Jalisco | Juchitlán | 4,873 | 3,003 | 1,326 | 544 | 88.84% | 61.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13082` | Hidalgo | Zapotlán de Juárez | 17,645 | 10,555 | 5,121 | 1,969 | 88.84% | 59.82% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07083` | Chiapas | Sitalá | 9,633 | 7,350 | 1,209 | 1,074 | 88.85% | 76.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15124` | Estado de México | San José del Rincón | 75,381 | 36,933 | 30,044 | 8,404 | 88.85% | 49.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07116` | Chiapas | Montecristo de Guerrero | 6,273 | 4,095 | 1,479 | 699 | 88.86% | 65.28% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07085` | Chiapas | Solosuchiapa | 6,059 | 4,271 | 1,113 | 675 | 88.86% | 70.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07038` | Chiapas | Huitiupán | 16,187 | 12,558 | 1,827 | 1,802 | 88.87% | 77.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07026` | Chiapas | Chenalhó | 33,289 | 21,304 | 8,284 | 3,701 | 88.88% | 64.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26061` | Sonora | Guaymas | 108,384 | 46,296 | 50,039 | 12,049 | 88.88% | 42.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15063` | Estado de México | Ocoyoacac | 47,899 | 30,450 | 12,126 | 5,323 | 88.89% | 63.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13071` | Hidalgo | Tlanalapa | 8,518 | 5,610 | 1,962 | 946 | 88.89% | 65.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25011` | Sinaloa | Guasave | 199,924 | 97,471 | 80,254 | 22,199 | 88.90% | 48.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16004` | Michoacán | Angamacutiro | 13,062 | 7,236 | 4,378 | 1,448 | 88.91% | 55.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12031` | Guerrero | Florencio Villarreal | 15,612 | 9,380 | 4,502 | 1,730 | 88.92% | 60.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `02002` | Baja California | Mexicali | 866,896 | 365,828 | 405,056 | 96,012 | 88.92% | 42.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11027` | Guanajuato | Salamanca | 212,517 | 104,066 | 84,919 | 23,532 | 88.93% | 48.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07080` | Chiapas | San Lucas | 5,370 | 3,637 | 1,139 | 594 | 88.94% | 67.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31007` | Yucatán | Cacalchén | 6,028 | 4,397 | 965 | 666 | 88.95% | 72.94% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14103` | Jalisco | Tonaya | 5,831 | 2,809 | 2,378 | 644 | 88.96% | 48.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `24035` | San Luis Potosí | Soledad de Graciano Sánchez | 146,121 | 62,435 | 67,553 | 16,133 | 88.96% | 42.73% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `17023` | Morelos | Tlalnepantla | 5,607 | 3,558 | 1,430 | 619 | 88.96% | 63.46% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `28043` | Tamaulipas | Xicoténcatl | 18,460 | 11,338 | 5,085 | 2,037 | 88.97% | 61.42% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14098` | Jalisco | Tlajomulco de Zúñiga | 141,163 | 61,999 | 63,591 | 15,573 | 88.97% | 43.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08036` | Chihuahua | Jiménez | 30,396 | 13,736 | 13,307 | 3,353 | 88.97% | 45.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19047` | Nuevo León | San Nicolás de los Garza | 367,132 | 183,678 | 142,978 | 40,476 | 88.98% | 50.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31084` | Yucatán | Temax | 5,355 | 4,196 | 569 | 590 | 88.98% | 78.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07030` | Chiapas | Chicomuselo | 22,088 | 8,634 | 11,022 | 2,432 | 88.99% | 39.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20503` | Oaxaca | Santiago Zacatepec | 3,533 | 916 | 2,228 | 389 | 88.99% | 25.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25005` | Sinaloa | Cosalá | 12,559 | 7,152 | 4,025 | 1,382 | 89.00% | 56.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20540` | Oaxaca | Tamazulápam del Espíritu Santo | 5,180 | 1,943 | 2,667 | 570 | 89.00% | 37.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `05014` | Coahuila | Jiménez | 8,917 | 4,716 | 3,220 | 981 | 89.00% | 52.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30191` | Veracruz | Vega de Alatorre | 15,129 | 8,837 | 4,628 | 1,664 | 89.00% | 58.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31010` | Yucatán | Cantamayec | 1,902 | 1,550 | 143 | 209 | 89.01% | 81.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32036` | Zacatecas | Ojocaliente | 30,889 | 15,916 | 11,580 | 3,393 | 89.02% | 51.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30139` | Veracruz | Río Blanco | 32,892 | 12,679 | 16,602 | 3,611 | 89.02% | 38.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08010` | Chihuahua | Buenaventura | 19,342 | 8,355 | 8,864 | 2,123 | 89.02% | 43.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30033` | Veracruz | Castillo de Teayo | 15,025 | 8,207 | 5,170 | 1,648 | 89.03% | 54.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19026` | Nuevo León | Guadalupe | 540,971 | 269,881 | 211,764 | 59,326 | 89.03% | 49.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25004` | Sinaloa | Concordia | 19,849 | 9,806 | 7,867 | 2,176 | 89.04% | 49.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08001` | Chihuahua | Ahumada | 9,268 | 5,447 | 2,805 | 1,016 | 89.04% | 58.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `11029` | Guanajuato | San Diego de la Unión | 30,537 | 16,532 | 10,659 | 3,346 | 89.04% | 54.14% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08018` | Chihuahua | Cusihuiriachi | 5,223 | 949 | 3,702 | 572 | 89.05% | 18.17% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `11044` | Guanajuato | Villagrán | 50,956 | 27,217 | 18,163 | 5,576 | 89.06% | 53.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14045` | Jalisco | La Huerta | 18,702 | 9,892 | 6,767 | 2,043 | 89.08% | 52.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08034` | Chihuahua | Ignacio Zaragoza | 6,006 | 1,581 | 3,770 | 655 | 89.09% | 26.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29024` | Tlaxcala | Panotla | 22,075 | 13,645 | 6,023 | 2,407 | 89.10% | 61.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `12036` | Guerrero | Iguala de la Independencia | 105,572 | 40,946 | 53,123 | 11,503 | 89.10% | 38.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `18005` | Nayarit | Compostela | 63,924 | 27,287 | 29,673 | 6,964 | 89.11% | 42.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24038` | San Luis Potosí | Tampacán | 11,183 | 8,054 | 1,911 | 1,218 | 89.11% | 72.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14087` | Jalisco | Tapalpa | 16,564 | 10,599 | 4,161 | 1,804 | 89.11% | 63.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20274` | Oaxaca | San Miguel Quetzaltepec | 5,016 | 1,836 | 2,634 | 546 | 89.11% | 36.60% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21080` | Puebla | Huitzilan de Serdán | 9,430 | 6,213 | 2,192 | 1,025 | 89.13% | 65.89% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14081` | Jalisco | San Sebastián del Oeste | 4,706 | 3,193 | 1,002 | 511 | 89.14% | 67.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13016` | Hidalgo | Chapantongo | 10,523 | 7,079 | 2,302 | 1,142 | 89.15% | 67.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30118` | Veracruz | Omealca | 16,876 | 9,075 | 5,970 | 1,831 | 89.15% | 53.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26063` | Sonora | Etchojoa | 41,937 | 23,745 | 13,642 | 4,550 | 89.15% | 56.62% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07101` | Chiapas | Tuxtla Chico | 32,842 | 18,243 | 11,042 | 3,557 | 89.17% | 55.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `19009` | Nuevo León | Cadereyta Jiménez | 85,415 | 33,504 | 42,664 | 9,247 | 89.17% | 39.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15098` | Estado de México | Texcaltitlán | 13,979 | 8,545 | 3,922 | 1,512 | 89.18% | 61.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15021` | Estado de México | Coatepec Harinas | 26,702 | 16,559 | 7,256 | 2,887 | 89.19% | 62.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07068` | Chiapas | Pichucalco | 22,679 | 14,171 | 6,056 | 2,452 | 89.19% | 62.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07114` | Chiapas | Maravilla Tejenapa | 8,486 | 5,543 | 2,027 | 916 | 89.21% | 65.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `14040` | Jalisco | Guachinango | 3,670 | 2,221 | 1,053 | 396 | 89.21% | 60.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30120` | Veracruz | Otatitlán | 4,100 | 2,679 | 979 | 442 | 89.22% | 65.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21027` | Puebla | Caltepec | 3,572 | 2,555 | 632 | 385 | 89.22% | 71.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04010` | Campeche | Candelaria | 33,301 | 18,148 | 11,565 | 3,588 | 89.23% | 54.50% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21048` | Puebla | Chiautla | 17,301 | 9,089 | 6,349 | 1,863 | 89.23% | 52.53% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12054` | Guerrero | San Marcos | 30,312 | 16,004 | 11,049 | 3,259 | 89.25% | 52.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19045` | Nuevo León | Sabinas Hidalgo | 26,724 | 16,063 | 7,788 | 2,873 | 89.25% | 60.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30058` | Veracruz | Chiconamel | 4,856 | 2,541 | 1,793 | 522 | 89.25% | 52.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20244` | Oaxaca | San Martín Toxpalan | 2,587 | 1,371 | 938 | 278 | 89.25% | 53.00% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20481` | Oaxaca | Santiago Niltepec | 4,459 | 3,111 | 869 | 479 | 89.26% | 69.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19045` | Nuevo León | Sabinas Hidalgo | 27,700 | 14,539 | 10,186 | 2,975 | 89.26% | 52.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `21016` | Puebla | Aquixtla | 6,004 | 4,202 | 1,158 | 644 | 89.27% | 69.99% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07084` | Chiapas | Socoltenango | 13,016 | 8,625 | 2,995 | 1,396 | 89.27% | 66.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30198` | Veracruz | Zacualpan | 4,875 | 2,910 | 1,443 | 522 | 89.29% | 59.69% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31036` | Yucatán | Homún | 5,501 | 4,295 | 617 | 589 | 89.29% | 78.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12085` | Guerrero | Santa Cruz del Rincón | 4,960 | 2,920 | 1,509 | 531 | 89.29% | 58.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08026` | Chihuahua | Gran Morelos | 4,049 | 1,214 | 2,402 | 433 | 89.31% | 29.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20028` | Oaxaca | Heroica Ciudad de Ejutla de Crespo | 16,499 | 10,818 | 3,917 | 1,764 | 89.31% | 65.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14024` | Jalisco | San Gabriel | 11,889 | 7,161 | 3,457 | 1,271 | 89.31% | 60.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `12021` | Guerrero | Coyuca de Benítez | 49,623 | 27,473 | 16,846 | 5,304 | 89.31% | 55.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07110` | Chiapas | Yajalón | 29,503 | 19,637 | 6,714 | 3,152 | 89.32% | 66.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08054` | Chihuahua | Riva Palacio | 7,296 | 1,899 | 4,618 | 779 | 89.32% | 26.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16009` | Michoacán | Ario | 26,009 | 13,807 | 9,425 | 2,777 | 89.32% | 53.09% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `14054` | Jalisco | Juchitlán | 5,098 | 2,830 | 1,724 | 544 | 89.33% | 55.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30023` | Veracruz | Atzacan | 15,897 | 9,434 | 4,768 | 1,695 | 89.34% | 59.34% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `24057` | San Luis Potosí | El Naranjo | 15,033 | 8,629 | 4,802 | 1,602 | 89.34% | 57.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `26059` | Sonora | Cajeme | 304,118 | 125,802 | 145,909 | 32,407 | 89.34% | 41.37% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `15121` | Estado de México | Zumpango | 181,302 | 93,071 | 68,930 | 19,301 | 89.35% | 51.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07113` | Chiapas | Benemérito de las Américas | 13,087 | 7,228 | 4,466 | 1,393 | 89.36% | 55.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11022` | Guanajuato | Ocampo | 17,804 | 9,165 | 6,745 | 1,894 | 89.36% | 51.48% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20513` | Oaxaca | Santo Domingo Petapa | 7,107 | 4,633 | 1,718 | 756 | 89.36% | 65.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `08030` | Chihuahua | Guazapares | 6,611 | 1,878 | 4,030 | 703 | 89.37% | 28.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `15039` | Estado de México | Isidro Fabela | 6,140 | 3,724 | 1,764 | 652 | 89.38% | 60.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `19025` | Nuevo León | General Zuazua | 37,967 | 15,289 | 18,647 | 4,031 | 89.38% | 40.27% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `07093` | Chiapas | Tecpatán | 15,515 | 10,516 | 3,352 | 1,647 | 89.38% | 67.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14001` | Jalisco | Acatic | 18,449 | 8,791 | 7,707 | 1,951 | 89.42% | 47.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20296` | Oaxaca | San Pablo Villa de Mitla | 10,083 | 6,879 | 2,138 | 1,066 | 89.43% | 68.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `11017` | Guanajuato | Irapuato | 342,148 | 130,247 | 175,733 | 36,168 | 89.43% | 38.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31007` | Yucatán | Cacalchén | 5,478 | 4,222 | 677 | 579 | 89.43% | 77.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `32005` | Zacatecas | Calera | 32,376 | 16,886 | 12,070 | 3,420 | 89.44% | 52.16% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26061` | Sonora | Guaymas | 118,819 | 42,736 | 63,546 | 12,537 | 89.45% | 35.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `25005` | Sinaloa | Cosalá | 11,421 | 5,321 | 4,895 | 1,205 | 89.45% | 46.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15111` | Estado de México | Valle de Bravo | 47,568 | 26,819 | 15,733 | 5,016 | 89.46% | 56.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31058` | Yucatán | Peto | 15,711 | 10,805 | 3,250 | 1,656 | 89.46% | 68.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07002` | Chiapas | Acala | 15,920 | 9,404 | 4,838 | 1,678 | 89.46% | 59.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `08019` | Chihuahua | Chihuahua | 679,186 | 351,498 | 256,114 | 71,574 | 89.46% | 51.75% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16011` | Michoacán | Briseñas | 6,372 | 3,665 | 2,036 | 671 | 89.47% | 57.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `13054` | Hidalgo | San Salvador | 22,508 | 7,169 | 12,969 | 2,370 | 89.47% | 31.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16043` | Michoacán | Jacona | 47,355 | 20,158 | 22,220 | 4,977 | 89.49% | 42.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15059` | Estado de México | Nextlalpan | 26,750 | 16,814 | 7,127 | 2,809 | 89.50% | 62.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30076` | Veracruz | Huiloapan de Cuauhtémoc | 5,391 | 3,528 | 1,297 | 566 | 89.50% | 65.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31085` | Yucatán | Temozón | 10,746 | 8,531 | 1,087 | 1,128 | 89.50% | 79.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27010` | Tabasco | Jalpa de Méndez | 58,867 | 35,327 | 17,363 | 6,177 | 89.51% | 60.01% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `13051` | Hidalgo | San Agustín Tlaxiaca | 25,145 | 10,827 | 11,682 | 2,636 | 89.52% | 43.06% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07057` | Chiapas | Motozintla | 45,105 | 17,304 | 23,075 | 4,726 | 89.52% | 38.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `14117` | Jalisco | Cañadas de Obregón | 3,742 | 2,012 | 1,338 | 392 | 89.52% | 53.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `05014` | Coahuila | Jiménez | 7,681 | 3,065 | 3,812 | 804 | 89.53% | 39.90% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12072` | Guerrero | Xochistlahuaca | 19,365 | 13,994 | 3,345 | 2,026 | 89.54% | 72.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `31036` | Yucatán | Homún | 6,318 | 5,004 | 653 | 661 | 89.54% | 79.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15005` | Estado de México | Almoloya de Juárez | 103,163 | 50,857 | 41,513 | 10,793 | 89.54% | 49.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08064` | Chihuahua | El Tule | 2,189 | 467 | 1,493 | 229 | 89.54% | 21.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `20024` | Oaxaca | Cosolapa | 9,658 | 5,911 | 2,737 | 1,010 | 89.54% | 61.20% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `26056` | Sonora | San Miguel de Horcasitas | 7,027 | 3,193 | 3,100 | 734 | 89.55% | 45.44% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `21093` | Puebla | Juan Galindo | 6,208 | 3,935 | 1,625 | 648 | 89.56% | 63.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `08047` | Chihuahua | Moris | 3,756 | 2,138 | 1,226 | 392 | 89.56% | 56.92% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `21008` | Puebla | Ahuazotepec | 6,977 | 3,036 | 3,213 | 728 | 89.57% | 43.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `08001` | Chihuahua | Ahumada | 8,262 | 2,221 | 5,179 | 862 | 89.57% | 26.88% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `30116` | Veracruz | Nogales | 35,356 | 19,728 | 11,940 | 3,688 | 89.57% | 55.80% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `25008` | Sinaloa | Elota | 32,892 | 17,931 | 11,535 | 3,426 | 89.58% | 54.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14034` | Jalisco | Degollado | 19,686 | 9,215 | 8,421 | 2,050 | 89.59% | 46.81% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11046` | Guanajuato | Yuriria | 63,401 | 27,233 | 29,569 | 6,599 | 89.59% | 42.95% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `31036` | Yucatán | Homún | 6,470 | 5,128 | 669 | 673 | 89.60% | 79.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13018` | Hidalgo | Chilcuautla | 13,204 | 8,072 | 3,759 | 1,373 | 89.60% | 61.13% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `12052` | Guerrero | Quechultenango | 21,203 | 12,981 | 6,019 | 2,203 | 89.61% | 61.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `06004` | Colima | Cuauhtémoc | 22,909 | 13,341 | 7,188 | 2,380 | 89.61% | 58.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `12066` | Guerrero | Tlalixtaquilla de Maldonado | 5,732 | 3,299 | 1,838 | 595 | 89.62% | 57.55% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07050` | Chiapas | La Libertad | 4,625 | 3,735 | 410 | 480 | 89.62% | 80.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07074` | Chiapas | Las Rosas | 20,517 | 12,689 | 5,699 | 2,129 | 89.62% | 61.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25010` | Sinaloa | El Fuerte | 74,275 | 38,600 | 27,972 | 7,703 | 89.63% | 51.97% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `15062` | Estado de México | Nopaltepec | 7,030 | 5,055 | 1,246 | 729 | 89.63% | 71.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11039` | Guanajuato | Tarimoro | 31,224 | 14,776 | 13,212 | 3,236 | 89.64% | 47.32% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12040` | Guerrero | Juan R. Escudero | 18,104 | 11,089 | 5,140 | 1,875 | 89.64% | 61.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `11009` | Guanajuato | Comonfort | 50,948 | 20,662 | 25,017 | 5,269 | 89.66% | 40.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `20153` | Oaxaca | San Ildefonso Villa Alta | 2,747 | 955 | 1,508 | 284 | 89.66% | 34.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `30164` | Veracruz | Tepatlaxco | 5,330 | 3,012 | 1,767 | 551 | 89.66% | 56.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31104` | Yucatán | Yaxcabá | 9,755 | 7,648 | 1,099 | 1,008 | 89.67% | 78.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `16057` | Michoacán | Nahuatzen | 18,897 | 12,139 | 4,807 | 1,951 | 89.68% | 64.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `32009` | Zacatecas | Chalchihuites | 8,370 | 4,719 | 2,787 | 864 | 89.68% | 56.38% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `12014` | Guerrero | Benito Juárez | 12,832 | 4,488 | 7,020 | 1,324 | 89.68% | 34.98% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31010` | Yucatán | Cantamayec | 1,785 | 1,468 | 133 | 184 | 89.69% | 82.24% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `13025` | Hidalgo | Huautla | 15,826 | 10,482 | 3,713 | 1,631 | 89.69% | 66.23% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `31019` | Yucatán | Chemax | 19,879 | 15,734 | 2,097 | 2,048 | 89.70% | 79.15% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `24033` | San Luis Potosí | Santa María del Río | 28,569 | 16,791 | 8,837 | 2,941 | 89.71% | 58.77% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19018` | Nuevo León | García | 110,468 | 54,160 | 44,938 | 11,370 | 89.71% | 49.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31089` | Yucatán | Ticul | 27,919 | 19,357 | 5,689 | 2,873 | 89.71% | 69.33% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `30057` | Veracruz | Chalma | 9,798 | 7,237 | 1,553 | 1,008 | 89.71% | 73.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19010` | Nuevo León | El Carmen | 13,425 | 6,669 | 5,375 | 1,381 | 89.71% | 49.68% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `12007` | Guerrero | Arcelia | 24,883 | 9,462 | 12,866 | 2,555 | 89.73% | 38.03% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `24050` | San Luis Potosí | Villa de Ramos | 27,971 | 16,601 | 8,500 | 2,870 | 89.74% | 59.35% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `31080` | Yucatán | Tekit | 6,991 | 5,676 | 598 | 717 | 89.74% | 81.19% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19042` | Nuevo León | Pesquería | 25,840 | 13,331 | 9,859 | 2,650 | 89.74% | 51.59% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25011` | Sinaloa | Guasave | 208,774 | 118,536 | 68,847 | 21,391 | 89.75% | 56.78% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07047` | Chiapas | Jitotol | 12,397 | 9,659 | 1,468 | 1,270 | 89.76% | 77.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13080` | Hidalgo | Yahualica | 19,265 | 12,697 | 4,597 | 1,971 | 89.77% | 65.91% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `26058` | Sonora | Bácum | 17,971 | 9,086 | 7,047 | 1,838 | 89.77% | 50.56% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14050` | Jalisco | Jesús María | 17,613 | 8,175 | 7,637 | 1,801 | 89.77% | 46.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14095` | Jalisco | Tequila | 34,920 | 18,379 | 12,971 | 3,570 | 89.78% | 52.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16019` | Michoacán | Cotija | 17,716 | 7,849 | 8,056 | 1,811 | 89.78% | 44.30% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `04007` | Campeche | Palizada | 6,891 | 4,942 | 1,245 | 704 | 89.78% | 71.72% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `19009` | Nuevo León | Cadereyta Jiménez | 66,346 | 32,425 | 27,144 | 6,777 | 89.79% | 48.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `16038` | Michoacán | Huetamo | 34,940 | 9,442 | 21,933 | 3,565 | 89.80% | 27.02% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `10011` | Durango | Indé | 4,391 | 2,155 | 1,788 | 448 | 89.80% | 49.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31002` | Yucatán | Acanceh | 11,578 | 8,849 | 1,548 | 1,181 | 89.80% | 76.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `18020` | Nayarit | La Yesca | 5,843 | 2,952 | 2,295 | 596 | 89.80% | 50.52% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `04003` | Campeche | Carmen | 182,978 | 87,063 | 77,267 | 18,648 | 89.81% | 47.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `26059` | Sonora | Cajeme | 324,814 | 117,531 | 174,205 | 33,078 | 89.82% | 36.18% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `05011` | Coahuila | General Cepeda | 9,144 | 6,133 | 2,080 | 931 | 89.82% | 67.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07085` | Chiapas | Solosuchiapa | 6,417 | 4,581 | 1,183 | 653 | 89.82% | 71.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `27014` | Tabasco | Paraíso | 64,696 | 36,489 | 21,627 | 6,580 | 89.83% | 56.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `14016` | Jalisco | Ayotlán | 32,412 | 15,676 | 13,440 | 3,296 | 89.83% | 48.36% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2009 | `23006` | Quintana Roo | Lázaro Cárdenas | 14,986 | 8,580 | 4,883 | 1,523 | 89.84% | 57.25% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `18010` | Nayarit | Rosamorada | 26,292 | 15,542 | 8,080 | 2,670 | 89.84% | 59.11% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `20552` | Oaxaca | Tlalixtac de Cabrera | 6,620 | 1,367 | 4,581 | 672 | 89.85% | 20.65% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `15047` | Estado de México | Jilotzingo | 14,896 | 9,960 | 3,425 | 1,511 | 89.86% | 66.86% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `20192` | Oaxaca | San Juan Cotzocón | 16,714 | 8,940 | 6,079 | 1,695 | 89.86% | 53.49% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `13058` | Hidalgo | Tasquillo | 14,015 | 5,242 | 7,352 | 1,421 | 89.86% | 37.40% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `17025` | Morelos | Tlaquiltenango | 22,972 | 13,028 | 7,618 | 2,326 | 89.87% | 56.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `19032` | Nuevo León | Juárez | 302,939 | 127,013 | 145,274 | 30,652 | 89.88% | 41.93% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07060` | Chiapas | Ocotepec | 6,989 | 3,624 | 2,658 | 707 | 89.88% | 51.85% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `16041` | Michoacán | Irimbo | 11,974 | 6,775 | 3,988 | 1,211 | 89.89% | 56.58% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `11002` | Guanajuato | Acámbaro | 95,103 | 40,019 | 45,470 | 9,614 | 89.89% | 42.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `07062` | Chiapas | Ostuacán | 13,741 | 8,988 | 3,364 | 1,389 | 89.89% | 65.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `21073` | Puebla | Huehuetla | 11,914 | 8,443 | 2,267 | 1,204 | 89.89% | 70.87% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `30067` | Veracruz | Emiliano Zapata | 44,300 | 17,149 | 22,679 | 4,472 | 89.91% | 38.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2021 | `16049` | Michoacán | Lagunillas | 5,292 | 3,039 | 1,720 | 533 | 89.93% | 57.43% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `10017` | Durango | Nuevo Ideal | 22,895 | 7,928 | 12,662 | 2,305 | 89.93% | 34.63% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `12055` | Guerrero | San Miguel Totolapan | 14,432 | 8,336 | 4,644 | 1,452 | 89.94% | 57.76% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `04003` | Campeche | Carmen | 178,050 | 100,093 | 60,049 | 17,908 | 89.94% | 56.22% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `32026` | Zacatecas | Mazapil | 14,626 | 10,313 | 2,842 | 1,471 | 89.94% | 70.51% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `16075` | Michoacán | Cojumatlán de Régules | 8,951 | 5,064 | 2,987 | 900 | 89.95% | 56.57% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `25008` | Sinaloa | Elota | 29,975 | 17,706 | 9,258 | 3,011 | 89.95% | 59.07% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `29058` | Tlaxcala | Santa Ana Nopalucan | 6,337 | 4,199 | 1,502 | 636 | 89.96% | 66.26% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `07014` | Chiapas | El Bosque | 15,416 | 10,081 | 3,789 | 1,546 | 89.97% | 65.39% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2018 | `31038` | Yucatán | Hunucmá | 23,400 | 15,922 | 5,133 | 2,345 | 89.98% | 68.04% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2015 | `07033` | Chiapas | Francisco León | 4,261 | 2,459 | 1,375 | 427 | 89.98% | 57.71% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `25014` | Sinaloa | Rosario | 39,655 | 20,784 | 14,902 | 3,969 | 89.99% | 52.41% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2024 | `13047` | Hidalgo | Pachuca de Soto | 248,154 | 141,649 | 81,676 | 24,829 | 89.99% | 57.08% | **NA (Excluido)** | Cobertura < 90% por alto NS parcial |
| 2012 | `20253` | Oaxaca | San Mateo Sindihui | 1,400 | 0 | 1,400 | 0 | 100.00% | 0.00% | **NA (Excluido)** | 0% SV (Municipio sin captura de marcas de voto en 2012, registrado en NV) |
| 2012 | `20273` | Oaxaca | San Miguel Piedras | 829 | 0 | 829 | 0 | 100.00% | 0.00% | **NA (Excluido)** | 0% SV (Municipio sin captura de marcas de voto en 2012, registrado en NV) |
| 2012 | `20327` | Oaxaca | San Pedro Teozacoalco | 421 | 0 | 421 | 0 | 100.00% | 0.00% | **NA (Excluido)** | 0% SV (Municipio sin captura de marcas de voto en 2012, registrado en NV) |
