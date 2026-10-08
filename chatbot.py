import config 

from providers import ask_openai, ask_gemini, ask_ollama

def model_name():

  if config.PROVIDER == "openai":
    return config.OPENAI_MODEL
  if config.PROVIDER == "gemini":
    return config.GEMINI_MODEL
  if config.PROVIDER == "ollama":
    return config.OLLAMA_MODEL


# -- SETUP for checking missing things 

def check_setup():
  """Return helpful message if something is missing in .env otherwise None."""

  if config.PROVIDER not in ("openai","gemini","ollama"):
    return (
      "LLM_PROVIDER is '" + config.PROVIDER +"'.\n"
      "Please set LLM_PROVIDER to openai, gemini or ollama in the .env file."
    )

  if config.PROVIDER == "openai" and not config.OPENAI_API_KEY:
    return "OPENAI_API_KEY is missing.\nPlease add your OpenAI API key to the .env"

  if config.PROVIDER == "gemini" and not config.GEMINI_API_KEY:
      return "GEMINI_API_KEY is missing.\nPlease add your Gemini API key to the .env"

  if not model_name():
    return (
      "The model name for "+ config.PROVIDER + " is missing.\n"
      "Please set "+ config.PROVIDER.upper() + "_MODEL in the .env file."
    )


# -- Asking LLM --- 

def ask_llm(message):

  if config.PROVIDER == "openai":
    return ask_openai(message)
  elif config.PROVIDER == "gemini":
    return ask_gemini(message)
  else:
    return ask_ollama(message)


# main ----

def main():

  problem = check_setup()

  if problem:
    print(f"Error: {problem}")
    return

  print("="*40)
  print("     SIMPLE CLI CHATBOT")
  print("="*40)
  print("\nProvider:",config.PROVIDER)
  print("Model:",model_name())

  while True:

    message = input("\nYou: ").strip()

    if message in ("quit","stop"):
      print("GoodBye!!")
      break

    if not message:
      continue

    try:
      print(f"\nAssistant: {ask_llm(message)}")
    except Exception as e:
      print(f"Sorry, the request failed: {e}")


if __name__ == "__main__":
  main()