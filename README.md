# LLM-Codes 🤖

Contenidos y códigos sobre Large Language Models (LLMs) usando LangChain y Google Gemini.

---

## 📄 sentiment_analysis_langchain.py

Script que implementa un pipeline de **análisis de sentimiento y resumen automático** de reseñas de productos usando LangChain y el modelo Gemini de Google.

### ¿Qué hace?

El script procesa una lista de textos y para cada uno ejecuta en paralelo dos tareas:

- **Resumen**: genera una oración que resume el texto recibido.
- **Análisis de sentimiento**: clasifica el texto como `positivo`, `negativo` o `neutral`, junto con una breve explicación.

Finalmente combina ambos resultados en un único objeto de salida por cada texto.

### Arquitectura de la cadena

```
texto → preprocessor → (summary_branch ∥ sentiment_branch) → merger → resultado
```

Utiliza los siguientes componentes de LangChain:

- `RunnableLambda`: envuelve funciones Python como pasos de la cadena.
- `RunnableParallel`: ejecuta resumen y sentimiento al mismo tiempo.
- `chain.batch()`: procesa múltiples textos en una sola llamada.

### Requisitos

```bash
pip install langchain-core langchain-google-genai
```

También necesitas configurar tu API Key de Google Generative AI:

```bash
export GOOGLE_API_KEY="tu_api_key_aqui"
```

### Uso

```python
python sentiment_analysis_langchain.py
```

### Ejemplo de salida

```python
[
  {
    "resume": "El usuario tuvo una mala experiencia con el producto y no lo recomienda.",
    "sentimiento": "negativo",
    "razon": "El texto expresa insatisfacción total con el producto."
  },
  {
    "resume": "El producto es bueno y el usuario lo recomienda.",
    "sentimiento": "positivo",
    "razon": "El texto muestra conformidad y recomendación del producto."
  },
  {
    "resume": "El producto cumple su función de manera ordinaria sin destacar.",
    "sentimiento": "neutral",
    "razon": "El texto no expresa ni satisfacción ni insatisfacción marcada."
  }
]
```

---

## 📌 Tecnologías usadas

- [LangChain](https://www.langchain.com/)
- [Google Gemini (gemini-3.5-flash)](https://ai.google.dev/)
- Python 3.10+

## 📝 Licencia

MIT
