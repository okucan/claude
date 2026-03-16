"""
01_basic.py — 기본 메시지 요청
가장 간단한 Claude API 사용 예시입니다.

실행: python 01_basic.py
"""

import anthropic

client = anthropic.Anthropic()  # ANTHROPIC_API_KEY 환경변수 사용


def basic_request():
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {"role": "user", "content": "파이썬으로 피보나치 수열을 구하는 함수를 짜줘"}
        ],
    )

    # response.content는 블록 리스트 — .type으로 구분
    for block in response.content:
        if block.type == "text":
            print(block.text)

    print(f"\n--- 사용 토큰: 입력 {response.usage.input_tokens} / 출력 {response.usage.output_tokens} ---")


def with_system_prompt():
    print("\n[시스템 프롬프트 예시]")
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=512,
        system="당신은 한 줄로만 답하는 짧은 답변 전문가입니다.",
        messages=[
            {"role": "user", "content": "파이썬이 뭔가요?"}
        ],
    )
    for block in response.content:
        if block.type == "text":
            print(block.text)


if __name__ == "__main__":
    basic_request()
    with_system_prompt()
