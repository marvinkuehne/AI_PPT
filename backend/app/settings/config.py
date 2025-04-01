# config

# Configurating the AI APIs
import os

AI_CONFIG = {
    "openai": {
        "api_key": os.getenv("OPENAI_API_KEY", "your-openai-key"),
        "model": "gpt-4o"
    },
    # "deepseek": {
    #     "api_key": os.getenv("DEEPSEEK_API_KEY", "your-deepseek-key"),
    #     "model": "deepseek-coder-6.7b"
    # },
    # "anthropic": {
    #     "api_key": os.getenv("ANTHROPIC_API_KEY", "your-anthropic-key"),
    #     "model": "claude-3-opus"
    # }
}