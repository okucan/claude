"""
06_thinking.py - Extended Thinking (확장 사고)

Claude Opus 4.6에서 적응형 사고(adaptive thinking)를 사용합니다.
복잡한 문제에서 Claude의 내부 추론 과정을 볼 수 있습니다.
"""

import anthropic

client = anthropic.Anthropic()

print("Claude가 문제를 풀고 있습니다...\n")

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=16000,
    thinking={"type": "adaptive"},       # 적응형 사고 활성화 (Opus 4.6 권장)
    output_config={"effort": "high"},    # 사고 깊이: low / medium / high / max
    messages=[
        {
            "role": "user",
            "content": (
                "다음 논리 퍼즐을 풀어줘:\n"
                "5명(A, B, C, D, E)이 일렬로 서 있다.\n"
                "- A는 B 바로 앞에 있다.\n"
                "- C는 D와 E 사이에 있다.\n"
                "- B는 D 앞에 있다.\n"
                "- E는 맨 뒤에 있지 않다.\n"
                "순서를 구하고 단계별로 설명해줘."
            )
        }
    ]
)

for block in response.content:
    if block.type == "thinking":
        print(f"[내부 사고 과정]\n{block.thinking}\n")
        print("-" * 50)
    elif block.type == "text":
        print(f"[최종 답변]\n{block.text}")

print(f"\n--- 사용 토큰: 입력 {response.usage.input_tokens}, 출력 {response.usage.output_tokens} ---")
