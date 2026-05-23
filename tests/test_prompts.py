"""
Testes automatizados para validação de prompts.
"""
import pytest
import yaml
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

def load_prompts(file_path: str):
    """Carrega prompts do arquivo YAML."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

class TestPrompts:
    def test_prompt_has_system_prompt(self):
        """Verifica se o campo 'system_prompt' existe e não está vazio."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        system_prompt = prompt_data.get("system_prompt", "").strip()
        assert system_prompt, "O campo 'system_prompt' está ausente ou vazio."

    def test_prompt_has_role_definition(self):
        """Verifica se o prompt define uma persona (ex: "Você é um Product Manager")."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        system_prompt = prompt_data.get("system_prompt", "").strip()
        assert "você é" in system_prompt.lower(), "O 'system_prompt' deve definir uma persona (ex: 'Você é um Product Manager')."

    def test_prompt_mentions_format(self):
        """Verifica se o prompt exige formato Markdown ou User Story padrão."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        system_prompt = prompt_data.get("system_prompt", "").strip()
        assert "markdown" in system_prompt.lower() or "user story" in system_prompt.lower(), "O 'system_prompt' deve mencionar o formato Markdown ou User Story padrão."

    def test_prompt_has_few_shot_examples(self):
        """Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot)."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        system_prompt = prompt_data.get("system_prompt", "").strip()
        assert "exemplo" in system_prompt.lower() or "example" in system_prompt.lower(), "O 'system_prompt' deve conter exemplos de entrada/saída (técnica Few-shot)."

    def test_prompt_no_todos(self):
        """Garante que você não esqueceu nenhum `[TODO]` no texto."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        system_prompt = prompt_data.get("system_prompt", "").strip()
        assert "[TODO]" not in system_prompt, "O 'system_prompt' contém '[TODO]', revise o texto para remover placeholders."

    def test_minimum_techniques(self):
        """Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas."""
        prompt_data = load_prompts("prompts/bug_to_user_story_v2.yml")['bug_to_user_story_v2']
        techniques = prompt_data.get("techniques_applied", [])
        assert len(techniques) >= 2, "O prompt deve listar pelo menos 2 técnicas."

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])