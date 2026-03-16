"""
05_structured_output.py - 구조화된 출력 (Structured Output)

Pydantic 모델로 JSON 응답 형식을 강제합니다.
client.messages.parse()를 사용하면 자동으로 검증됩니다.
"""

import anthropic
from pydantic import BaseModel
from typing import List


client = anthropic.Anthropic()


# 원하는 응답 구조를 Pydantic 모델로 정의
class Recipe(BaseModel):
    name: str
    ingredients: List[str]
    steps: List[str]
    cooking_time_minutes: int
    difficulty: str  # "쉬움", "보통", "어려움"


class RecipeList(BaseModel):
    recipes: List[Recipe]
    tip: str


# messages.parse() 사용 - 자동으로 스키마 적용 및 검증
response = client.messages.parse(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=[
        {
            "role": "user",
            "content": "초보자도 만들 수 있는 한국 요리 레시피 2개를 알려줘."
        }
    ],
    output_format=RecipeList,
)

# parsed_output은 RecipeList 인스턴스
result = response.parsed_output

if result:
    for i, recipe in enumerate(result.recipes, 1):
        print(f"\n{'='*40}")
        print(f"[레시피 {i}] {recipe.name}")
        print(f"난이도: {recipe.difficulty} | 조리시간: {recipe.cooking_time_minutes}분")
        print("\n재료:")
        for ingredient in recipe.ingredients:
            print(f"  - {ingredient}")
        print("\n조리법:")
        for j, step in enumerate(recipe.steps, 1):
            print(f"  {j}. {step}")

    print(f"\n{'='*40}")
    print(f"팁: {result.tip}")
else:
    print("파싱 실패")
