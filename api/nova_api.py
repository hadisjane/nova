import aiohttp
import json
from core.config import MODE_PROMPTS, DEFAULT_MODE, create_ssl_context
from core.memory import user_memories, UserMemory
from utils.text_processing import apply_all_filters as process_reply

# Updated to use the latest Groq API endpoint and model
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL_NAME = "meta-llama/llama-4-scout-17b-16e-instruct"  # Latest Groq model

async def ask_grok(api_key, prompt, mode, user_id):
    """Отправляет запрос к API Groq и возвращает обработанный ответ"""
    system_prompt = MODE_PROMPTS.get(mode, MODE_PROMPTS[DEFAULT_MODE])
    
    # Получаем или создаём память пользователя
    if user_id not in user_memories:
        user_memories[user_id] = UserMemory()
    
    memory = user_memories[user_id]
    
    # Добавляем новое сообщение пользователя
    memory.add_message("USER", prompt)
    
    # Получаем контекст для модели
    context = memory.get_context()
    
    # Выводим отладочную информацию о контексте
    print("\n[DEBUG] Текущий контекст:")
    for i, msg in enumerate(context):
        role = msg.get('role', 'UNKNOWN')
        content = msg.get('content', '')
        print(f"[{i}] {role}: {content[:100]}{'...' if len(content) > 100 else ''}")
    
    # Подготавливаем историю чата для Grok
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add message history with proper role mapping
    for msg in context:
        role = msg.get("role", "").upper()
        content = msg.get("content", "").strip()
        
        if not content:  # Skip empty messages
            continue
            
        # Map roles to what the API expects
        if role in ["USER"]:
            messages.append({"role": "user", "content": content})
        elif role in ["CHATBOT", "NOVA"]:
            messages.append({"role": "assistant", "content": content})
        elif role == "SYSTEM":
            messages.append({"role": "system", "content": content})
        # Skip any messages with unknown roles
    
    # Добавляем текущий промпт
    messages.append({"role": "user", "content": prompt})
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 4000,
        "top_p": 0.9,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
        "stop": None
    }

    ssl_context = create_ssl_context()
    conn = aiohttp.TCPConnector(ssl=ssl_context)

    async with aiohttp.ClientSession(connector=conn) as session:
        try:
            async with session.post(GROQ_API_URL, headers=headers, json=payload, ssl=ssl_context) as response:
                if response.status == 200:
                    result = await response.json()
                    reply = result['choices'][0]['message']['content'].strip()
                    
                    # Обрабатываем ответ через все фильтры (но без ограничений)
                    reply = process_reply(reply)
                    
                    # Добавляем ответ бота в память
                    memory.add_message("NOVA", reply)
                    
                    # Уменьшаем важность старых сообщений
                    for i in range(len(memory.importance)):
                        memory.importance[i] *= 0.99  # Постепенное забывание
                    
                    return reply
                else:
                    error_text = await response.text()
                    print(f"[ERROR] Groq API error {response.status}: {error_text}")
                    return "Произошла ошибка при обработке запроса"
        except aiohttp.ClientError as e:
            print(f"[ERROR] Groq API request failed: {str(e)}")
            return "Проблема с подключением к серверу, попробуйте позже"
        except Exception as e:
            print(f"[UNEXPECTED ERROR] {str(e)}")
            return "Произошла непредвиденная ошибка"