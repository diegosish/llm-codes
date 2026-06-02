from click import prompt
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_google_genai import ChatGoogleGenerativeAI
import json

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)

def preprocess_text(text):
    return text.strip()[:500]

preprocessor = RunnableLambda(preprocess_text)

def generate_summary(text):
    prompt = f"Resume en una sola oración: {text}"
    response = llm.invoke(prompt)
    return response.content 

summary_branch = RunnableLambda(generate_summary)

def analyze_sentiment(text):
    prompt = f"""Analiza el sentimiento de este texto.
    Responde únicamente en formato JSON sin markdown, sin backticks:
    {{"sentimiento": "positivo/negativo/neutral", "razon": "explicación breve"}}
    Texto: {text}"""
    
    response = llm.invoke(prompt)
    
    try:
        # Limpiar backticks de markdown
        content = response.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        return json.loads(content)
    except json.JSONDecodeError:
        return {"sentimiento": "no se pudo analizar", "razon": "error de parseo"}
sentiment_branch = RunnableLambda(analyze_sentiment)

def merge_results(data):
    return {
        "resume": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merger = RunnableLambda(merge_results)
parallel_analysis = RunnableParallel({
    "resumen": summary_branch,
    "sentimiento_data": sentiment_branch
})

chain = preprocessor | parallel_analysis | merger

review = ["Este producto me ha salido muy malo, no sirve absolutamente para nada, no lo recomiendo a nadie",
          "El producto es bueno, lo recomiendo",
          "Cumple su función normal, no es nada especial pero tampoco es malo"
          ]
result = chain.batch(review)
print(result)
