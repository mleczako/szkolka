import os
import json
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()
open_ai_endpoint = os.getenv("OPEN_AI_ENDPOINT")
open_ai_key = os.getenv("OPEN_AI_KEY")
embedding_model = os.getenv("EMBEDDING_MODEL")
search_url = os.getenv("SEARCH_ENDPOINT")
search_key = os.getenv("SEARCH_KEY")
index_name = os.getenv("INDEX_NAME")  

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=open_ai_endpoint,
    api_key=open_ai_key
)

query_text = "Jakie hotele oferuje Margie’s Travel w Dubaju?"


vector_rag_params = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_url,
                "index_name": index_name,
                "authentication": {
                    "type": "api_key",
                    "key": search_key,
                },
                "query_type": "vector",
                "embedding_dependency": {
                    "type": "deployment_name",
                    "deployment_name": embedding_model,
                },
            }
        }
    ]
}

semantic_rag_params = {
    "data_sources": [
        {
            "type": "azure_search",
            "parameters": {
                "endpoint": search_url,
                "index_name": index_name,
                "authentication": {
                    "type": "api_key",
                    "key": search_key,
                },
                "query_type": "simple",
            }
        }
    ]
}

messages = [{"role": "user", "content": query_text}]
chat_model = os.getenv("CHAT_MODEL")

vector_response = client.chat.completions.create(
    model=chat_model,
    messages=messages,
    extra_body=vector_rag_params
)

semantic_response = client.chat.completions.create(
    model=chat_model,
    messages=messages,
    extra_body=semantic_rag_params
)


vector_result = vector_response.choices[0].message.content
semantic_result = semantic_response.choices[0].message.content

notebook_data = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["## Zapytanie: Jakie hotele oferuje Margie’s Travel w Dubaju?\n"]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": ["# Wektorowe wyszukiwanie\n", f"result_vector = {json.dumps(vector_result, indent=2)}"],
            "execution_count": None,
            "outputs": []
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": ["# Semantyczne wyszukiwanie\n", f"result_semantic = {json.dumps(semantic_result, indent=2)}"],
            "execution_count": None,
            "outputs": []
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}

os.makedirs("notebooks", exist_ok=True)
with open("notebooks/queries.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook_data, f, ensure_ascii=False, indent=2)

print(" Zapisano wyniki zapytań do notebooks/queries.ipynb")
