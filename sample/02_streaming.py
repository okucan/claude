"""
02_streaming.py - 스트리밍 응답

긴 응답이나 실시간 출력이 필요할 때 스트리밍을 사용합니다.
토큰이 생성되는 즉시 출력됩니다.
"""

import anthropic

client = anthropic.Anthropic()

print("Claude가 글을 씁니다...\n")

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "파이썬의 매력을 소개하는 짧은 에세이를 써줘."}
    ]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# 스트림 완료 후 최종 메시지 정보 가져오기
final = stream.get_final_message()
print(f"\n\n--- 사용 토큰: 입력 {final.usage.input_tokens}, 출력 {final.usage.output_tokens} ---")
