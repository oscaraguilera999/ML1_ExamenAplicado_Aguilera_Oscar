# ML1_ExamenAplicado_Aguilera_Oscar

**Autor:** Oscar Aguilera  
**Asignatura:** Machine Learning I  
**Tarea:** regresión de la demanda diaria de bicicletas compartidas.

## Dataset

Se utiliza `day.csv` del [Bike Sharing Dataset de UCI](https://archive.ics.uci.edu/dataset/275/bike+sharing+dataset): 731 días, 16 columnas originales y `cnt` como objetivo. La fuente declara datos de Capital Bikeshare de 2011-2012, tarea de regresión y licencia CC BY 4.0. Se excluyen identificadores y las variables `casual`/`registered`, porque suman exactamente `cnt` y producirían fuga de información.

## Metodología

1. EDA: nulos, IQR, distribución del objetivo, correlaciones y visualizaciones.
2. Split 80/20 antes de transformaciones (`random_state=42`).
3. `ColumnTransformer`: imputación, recorte IQR, estandarización, `OneHotEncoder` y `OrdinalEncoder`.
4. PCA y K-Means, con scree plot, codo y Silhouette Score.
5. Ridge y Random Forest con `GridSearchCV`, 5 folds y evaluación final en test.
6. Importancia, diez errores mayores y conclusiones ejecutivas.

## Resultado principal

| Modelo seleccionado | RMSE test | MAE test | R2 test | Observación |
|---|---:|---:|---:|---|
| Random Forest | 679.6695 | 441.6843 | 0.8848 | Mejor desempeño; presenta brecha train-test que debe monitorearse |

La tabla completa está en [`model_comparison.csv`](model_comparison.csv).

## Estructura

- `Oscar_Aguilera_ML1_Examen.ipynb`: notebook ejecutado.
- `data/`: copia del archivo original y descripción de UCI.
- `figures/`: todos los gráficos en PNG, 150 dpi.
- `model_comparison.csv`: métricas y tiempos por modelo.
- `test_predictions_and_errors.csv`: predicciones y análisis de errores.
- `VIDEO_SCRIPT.md`: texto exacto y pauta visual para el video (<8 min).
- `requirements.txt`: entorno congelado.

## Reproducir

```bash
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tools/execute_notebook.py Oscar_Aguilera_ML1_Examen.ipynb
```

## Video

**Enlace:** `https://drive.google.com/file/d/1TodfJpIgM4tfLx2xS-JRc5XWP6Mo8Ze4/view?usp=drive_link`

El guion completo está en `VIDEO_SCRIPT.md` y dura 8 minutos exactos.

## Declaración de uso de IA generativa

Se utilizó ChatGPT (OpenAI) como apoyo para estructurar el notebook, revisar código, mejorar redacción y verificar la cobertura de la rúbrica. Yo Oscar Aguilera revisé la lógica, ejecuté el análisis y soy el responsable de comprender, validar y presentar las decisiones y resultados. No se incorporó material ajeno sin referencia.

## Referencias

- Fanaee-T, H. (2013). *Bike Sharing* [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5W894
- Fanaee-T, H., & Gama, J. (2014). Event labeling combining ensemble detectors and background knowledge. *Progress in Artificial Intelligence, 2*, 113-127. https://doi.org/10.1007/s13748-013-0040-3
- Scikit-learn Developers. User Guide. https://scikit-learn.org/stable/user_guide.html
- Material docente de Machine Learning I, clases 1-10 (2026), proporcionado en el aula virtual.
