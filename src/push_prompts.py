"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header, validate_prompt_structure

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    """
    Faz push do prompt otimizado para o LangSmith Hub (PÚBLICO).

    Args:
        prompt_name: Nome do prompt "nimbo/bug_to_user_story_v2"
        prompt_data: Dados do prompt

    Returns:
        True se sucesso, False caso contrário
    """
    prompt = ChatPromptTemplate([
        ("system", prompt_data.get("system_prompt", "")),
        ("user", prompt_data.get("user_prompt", ""))
    ])
    try:
        hub.push(
            prompt_name,
            prompt,
            new_repo_is_public=True,
            tags=prompt_data.get("tags", []),
            new_repo_description=prompt_data.get("description", "")
        )
        return True
    except Exception as e:
        print(f"Erro ao fazer push do prompt: {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    """
    Valida estrutura básica de um prompt (versão simplificada).

    Args:
        prompt_data: Dados do prompt

    Returns:
        (is_valid, errors) - Tupla com status e lista de erros
    """
    return validate_prompt_structure(prompt_data)

def main():
    """Função principal"""
    has_required_vars = check_env_vars([
        'LANGSMITH_ENDPOINT',
        'LANGSMITH_API_KEY',
    ])
    if not has_required_vars:
        print_section_header("Variáveis de ambiente necessárias não estão definidas. Verifique o .env.")
        return 1

    prompt_data = load_yaml("prompts/bug_to_user_story_v2.yml")
    prompt_names = prompt_data.keys()

    successfull_report: dict[str, bool] = {}

    for prompt_name in prompt_names:
        print_section_header(f"Validando prompt: {prompt_name}")
        isValid, errors = validate_prompt(prompt_data[prompt_name])

        if not isValid:
            print_section_header("Erros de validação encontrados:")
            for error in errors:
                print(f"   - {error}")
            print("\nCorrija os erros antes de fazer push do prompt.")
            return 1

        print_section_header(f"Fazendo push do prompt: {prompt_name}")
        successfull_report[prompt_name] = push_prompt_to_langsmith(prompt_name, prompt_data[prompt_name])

    print_section_header("Resumo do push:")
    for prompt_name, success in successfull_report.items():
        status = "Sucesso" if success else "Falha"
        print(f"   - {prompt_name}: {status}")

if __name__ == "__main__":
    sys.exit(main())
