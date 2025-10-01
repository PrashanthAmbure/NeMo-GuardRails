import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails
from colorama import Fore, Back, Style, init
init()  # Initialize colorama

# Fix for running async code in some environments
nest_asyncio.apply()

load_dotenv()

async def run_nim_validation():
    # --- 1. Load the Guardrails Configuration ---
    if not os.path.isdir("config"):
        print("Error: 'config' folder not found. Please create it with config.yml and rails.co.")
        return

    print("Loading NeMo Guardrails configuration with NIM...")
    # NeMo Guardrails automatically uses the LangChain integration
    # based on the settings in config.yml
    config = RailsConfig.from_path("./config")
    rails = LLMRails(config)

    response = await rails.generate_async(prompt='hi')
    explain(rails, response)


    response = await rails.generate_async(prompt='is president biased?')
    explain(rails, response)

def explain(rails, response):
    info = rails.explain()

    print(f"{Fore.RED}{Style.BRIGHT}=== COLANG HISTORY ==={Style.RESET_ALL}")
    print(info.colang_history)

    print(f"{Fore.MAGENTA}{Style.BRIGHT}=== LLM CALLS SUMMARY ==={Style.RESET_ALL}")
    info.print_llm_calls_summary()

    print(f"\n{Fore.BLUE}{Style.BRIGHT}=== PROMPT ==={Style.RESET_ALL}")
    print(f"{Fore.CYAN}{info.llm_calls[0].prompt}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}{Style.BRIGHT}=== COMPLETION ==={Style.RESET_ALL}")
    print(f"{Fore.GREEN}{info.llm_calls[0].completion}{Style.RESET_ALL}")

    print(f"\n{Fore.YELLOW}{Style.BRIGHT}=== FINAL ANSWER ==={Style.RESET_ALL}")
    print(response)

    print(f"{Fore.YELLOW}{'-' * 50}{Style.RESET_ALL}")

if __name__ == "__main__":
    asyncio.run(run_nim_validation())