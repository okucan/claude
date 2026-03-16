"""
01_basic.py - 기본 메시지 요청

가장 단순한 Claude API 사용법입니다.
ANTHROPIC_API_KEY 환경변수가 필요합니다.
"""

import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "파이썬으로 피보나치 수열을 구하는 함수를 작성해줘."}
    ]
)

# content는 ContentBlock 리스트입니다. type을 확인 후 접근하세요.
for block in response.content:
    if block.type == "text":
        print(block.text)

print(f"\n--- 사용 토큰: 입력 {response.usage.input_tokens}, 출력 {response.usage.output_tokens} ---")
