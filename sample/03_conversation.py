"""
03_conversation.py - 멀티턴 대화

Claude API는 무상태(stateless)이므로 매 요청마다 전체 대화 히스토리를 전송합니다.
"""

import anthropic

client = anthropic.Anthropic()


def chat(messages: list, user_input: str) -> str:
    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        system="당신은 파이썬 튜터입니다. 친절하고 간결하게 설명해주세요.",
        messages=messages
    )

    assistant_reply = next(
        (b.text for b in response.content if b.type == "text"), ""
    )
    messages.append({"role": "assistant", "content": assistant_reply})
    return assistant_reply


def main():
    messages = []

    print("=== Python 튜터와 대화하기 (종료: 'q') ===\n")

    while True:
        user_input = input("나: ").strip()
        if user_input.lower() == "q":
            break
        if not user_input:
            continue

        reply = chat(messages, user_input)
        print(f"\nClaude: {reply}\n")


if __name__ == "__main__":
    main()
