# Guion de video - Oscar Aguilera

**Duración objetivo:** 7:20 (máximo permitido: 8:00).  
**Antes de grabar:** notebook abierto, todas las celdas ejecutadas, panel de archivos visible y zoom suficiente para leer tablas y gráficos.

## 0:00-0:50 | Dataset y decisión de diseño

**Mostrar:** primera celda y planteamiento.

Hola. Soy Oscar Aguilera y presentaré mi examen aplicado de Machine Learning I. Elegí el Bike Sharing Dataset de UCI, específicamente el archivo diario `day.csv`. Contiene 731 observaciones y 16 columnas originales sobre arriendos de Capital Bikeshare durante 2011 y 2012. La variable objetivo es `cnt`, el total de arriendos diarios, por lo que el problema es de regresión.

La elección tiene relevancia práctica: una predicción razonable ayuda a planificar disponibilidad, redistribución y dotación. Utilicé 11 predictores: cuatro continuos, tres nominales y cuatro ordinales o binarios. Excluí el identificador y la fecha cruda. Además, eliminé `casual` y `registered` porque su suma es exactamente `cnt`; usarlas habría producido fuga de la variable objetivo y un resultado artificialmente perfecto.

## 0:50-2:25 | EDA y preprocesamiento

**Mostrar:** `shape`, nulos, boxplots, objetivo, correlación, scatter y diagrama del pipeline.

La inspección confirmó 731 filas, ausencia de valores faltantes y tipos coherentes. Aun así, incorporé imputadores defensivos: mediana para numéricas y moda para categóricas, pensando en reproducibilidad con datos futuros.

Para outliers apliqué el método IQR en temperatura, sensación térmica, humedad y viento. No eliminé días, porque condiciones meteorológicas extremas son plausibles y pueden ser justamente los casos más importantes para operación. En cambio, incluí un recorte IQR dentro del pipeline. Sus límites se aprenden solo con entrenamiento.

La distribución de `cnt` tiene skewness cercana a menos 0,047, muy por debajo de uno; por eso no apliqué logaritmo y mantuve una escala interpretable en número de arriendos.

En el heatmap, año y temperatura presentan asociación importante con la demanda. También detecté multicolinealidad entre `temp` y `atemp`, con correlación superior a 0,99. Las mantuve porque Ridge regulariza los coeficientes y Random Forest puede seleccionar entre variables redundantes.

La división fue 80 por ciento entrenamiento y 20 por ciento test, con semilla 42, antes de imputar, recortar, codificar o escalar. El `ColumnTransformer` usa One Hot Encoder para estación, mes y día de semana; Ordinal Encoder para año, feriado, día laboral y estado meteorológico; y estandarización para las numéricas. En modelado, todo este preprocesamiento está dentro de cada pipeline y se reajusta en cada fold de validación cruzada, evitando data leakage.

## 2:25-3:30 | PCA y K-Means

**Mostrar:** tabla de varianza, scree plot, loadings, codo/silhouette, clusters y perfil.

Después del preprocesamiento quedaron 31 columnas. Apliqué PCA solo sobre entrenamiento. Seleccioné 11 componentes, que explican aproximadamente 85,61 por ciento de la varianza: está dentro del intervalo solicitado de 80 a 90 por ciento y cercano al punto medio de 85.

Reporté la contribución de las variables a PC1 y PC2 y proyecté las observaciones en ese espacio. Luego evalué K-Means entre K igual a 2 y 10. K igual a 2 obtuvo el mejor Silhouette Score y una reducción de inercia coherente con el codo.

Sin usar `cnt` para formar los grupos, aparecieron dos regímenes útiles. El cluster cero reúne 299 días más cálidos y promedia cerca de 5.606 arriendos. El cluster uno reúne 285 días más fríos, con algo más de viento, y promedia cerca de 3.464. Esto conecta el análisis no supervisado con negocio: el primer régimen exige mayor capacidad y redistribución, mientras el segundo admite una operación más conservadora.

## 3:30-5:35 | Modelos y tabla comparativa

**Mostrar:** grids, mejores parámetros, CSV comparativo y residuales.

Entrené dos familias complementarias. Ridge representa un modelo penalizado, con alphas desde 0,001 hasta 100. Random Forest representa un ensamble de árboles y ajusté número de estimadores, profundidad máxima y mínimo de muestras por división. Ambos usaron GridSearchCV con cinco folds, RMSE como criterio y semilla 42 cuando corresponde.

El mejor alpha de Ridge fue 10. Su RMSE de test fue aproximadamente 827,97, MAE 608,98 y R cuadrado 0,8290. Para Random Forest, la mejor configuración fue 400 árboles, profundidad sin límite y mínimo de dos muestras por división. Su RMSE de test fue 679,67, MAE 441,68 y R cuadrado 0,8848.

La tabla incluye métricas de entrenamiento y test, MAPE, tiempo de entrenamiento y tiempo de inferencia, y está exportada como CSV. No elegí el modelo por MAPE, porque algunos días de demanda muy baja hacen que el porcentaje sea inestable.

Random Forest es el modelo final por su menor RMSE y mayor R cuadrado en test. Sin embargo, su RMSE crece desde aproximadamente 258,62 en train hasta 679,67 en test, evidenciando sobreajuste. Ridge tiene menor brecha, mayor interpretabilidad y menor costo, pero pierde precisión. Por eso mi decisión favorece Random Forest como herramienta predictiva, manteniendo Ridge como referencia transparente y monitoreando la brecha train-test.

## 5:35-7:20 | Interpretación, errores y cierre

**Mostrar:** importancia, diez mayores errores y conclusiones.

Las variables más relevantes se relacionan con año, temperatura, sensación térmica, estado del clima y estacionalidad. Esto coincide con el EDA: el crecimiento entre 2011 y 2012 y el confort térmico explican gran parte de la demanda. En variables correlacionadas, como `temp` y `atemp`, el bosque puede repartir la importancia; por eso no interpreto cada valor de forma aislada.

También identifiqué las diez observaciones con mayor error absoluto. Se concentran en días de demanda excepcional respecto de lo esperable por clima y calendario. La explicación más plausible es información omitida, como eventos, interrupciones, promociones o disponibilidad por estación. Este análisis muestra dónde no confiar ciegamente en el promedio del modelo.

Las principales limitaciones son cinco: solo hay una ciudad y dos años; faltan eventos y variables operacionales; el split aleatorio puede ser optimista frente a un uso futuro; la agregación diaria oculta picos horarios; y MAPE es inestable con demanda baja.

Recomiendo usar el pronóstico con bandas de seguridad y monitorear mensualmente errores por clima y estación. Como trabajo futuro, haría una validación temporal entrenando en 2011 y probando en 2012, incorporaría eventos y disponibilidad, y compararía Gradient Boosting con explicaciones SHAP.

La decisión más difícil fue tratar la multicolinealidad y los outliers sin perder información real. Lo haría diferente en una segunda versión usando validación temporal y datos horarios. En conclusión, el proyecto conecta EDA, PCA, clusters, modelos e interpretación en un flujo reproducible y sin fuga de información. Gracias.
