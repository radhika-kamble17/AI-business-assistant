import os
import google.generativeai as genai


def get_gemini_model():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key.startswith("your_"):
        raise ValueError(
            "GEMINI_API_KEY is required and must be set in .env"
        )

    genai.configure(api_key=api_key)

    model_name = os.getenv("GEMINI_MODEL", "models/gemini-pro")
    return genai.GenerativeModel(model_name)


def ask_gemini(prompt: str) -> str:

    model = get_gemini_model()

    if not prompt:
        return "Please enter a question for the AI assistant."

    wrapped_prompt = (
        "You are a helpful business assistant. Answer the user's question clearly and professionally, "
        "in a concise and direct manner. If the question is unclear, ask for clarification. "
        f"Question: {prompt}"
    )

    try:

        response = model.generate_content(
            wrapped_prompt,
            generation_config={
                "temperature": 0.25,
                "max_output_tokens": 600,
            }
        )

    except Exception as error:

        raise RuntimeError(
            f"Gemini request failed: {error}"
        ) from error

    try:
        return response.text or "Sorry, AI could not generate response."

    except Exception:
        return "Sorry, AI could not generate response."