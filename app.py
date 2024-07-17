from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import openai

app = FastAPI()

# your uvicorn server addr, default is http://localhost:4999
openai.api_base = "http://localhost:4999/v1"  # Используем HTTP
openai.api_key = "not needed for a local LLM"

# Set up the model name
model = "gpt4all-j-v1.3-groovy"

@app.get("/", response_class=HTMLResponse)
async def get_chat():
    with open("templates/index.html", "r") as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.post("/chat", response_class=JSONResponse)
async def post_chat(request: Request):
    form = await request.form()
    message = form["message"]
    print("Received message:", message)  # Отладочное сообщение

    # Формируем тело запроса
    payload = {
        "prompt": f"\n### Instruction:\nТы – нейросетевой помощник, который обладает следующими характеристиками и стилем общения:Ты демонстрируешь высокий уровень знаний и умений в своей области.Твой тон вежливый, уважительный и доброжелательный.Твой стиль общения четкий, ясный и лаконичный. Ты избегает использования сложных терминов без необходимости.Ты быстро реагируешь на запросы и обеспечиваешь конструктивные и полезные ответы.Ты умеешь использовать умеренный и уместный юмор, чтобы разрядить обстановку или сделать общение более приятным.Ты обладаешь глубокими знаниями в области технологий, умеешь решать технические проблемы и предоставлять подробные инструкции.Ты эффективно находишь и предоставляешь актуальную и достоверную информацию по запросу пользователя.Ты умеешь анализировать информацию и предоставлять четкие и логически обоснованные ответы.Ты всегда предоставляешь точную и достоверную информацию.Ты способен адаптироваться к стилю общения и предпочтениям пользователя.\n### Text:\n{message}\n### Response:\n",
        "max_tokens": 5000,
        "temperature": 0.8,
        "top_p": 0.90,
        "n": 1,
        "echo": False,
        "stream": False
    }

    # Make the API request
    try:
        response = openai.Completion.create(
            model=model,
            **payload
        )
    except Exception as e:
        print("Error during API request:", e)  # Отладочное сообщение
        return JSONResponse(content={"error": str(e)}, status_code=500)

    # Extract the generated completion and clean it
    generated_text = response.choices[0].text.strip()
    clean_response = generated_text.split("### Response:\n")[-1].strip()
    print("Generated response:", clean_response)  # Отладочное сообщение

    return JSONResponse(content={"response": clean_response})

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
