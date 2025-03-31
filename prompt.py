from dataclasses import dataclass
import yaml
from typing import List

@dataclass
class PromptTest:
    vars: dict
    asserts: List[dict]

@dataclass
class Prompt:
    description: str
    prompt: str
    providers: List[str]
    tests: List[PromptTest]

def load_prompt_from_yaml(file_path: str) -> Prompt:
    with open(file_path, 'r') as f:
        data = yaml.safe_load(f)
    
    # Convert nested test data to PromptTest objects
    tests = [
        PromptTest(
            vars=test_case["vars"],
            asserts=test_case["asserts"]
        )
        for test_case in data["tests"]
    ]
    
    return Prompt(
        description=data["description"],
        prompt=data["prompts"],
        providers=data["providers"],
        tests=tests
    )