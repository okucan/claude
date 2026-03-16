"""
04_tool_use.py - 툴 사용 (Tool Use)

Claude가 외부 함수를 호출할 수 있게 합니다.
Tool Runner를 사용하면 루프를 자동으로 처리합니다.
"""

import anthropic
from anthropic import beta_tool
import json

client = anthropic.Anthropic()


# --- 방법 1: Tool Runner (권장) ---
# @beta_tool 데코레이터로 함수를 도구로 등록합니다.

@beta_tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """지정된 위치의 현재 날씨를 가져옵니다.

    Args:
        location: 도시 이름, 예: 서울, 부산
        unit: 온도 단위 ("celsius" 또는 "fahrenheit")
    """
    # 실제로는 날씨 API를 호출하겠지만 여기선 가상 데이터 반환
    weather_data = {
        "서울": {"temp": 15, "condition": "맑음"},
        "부산": {"temp": 18, "condition": "흐림"},
        "제주": {"temp": 20, "condition": "비"},
    }
    data = weather_data.get(location, {"temp": 17, "condition": "알 수 없음"})
    temp = data["temp"] if unit == "celsius" else data["temp"] * 9 / 5 + 32
    unit_str = "°C" if unit == "celsius" else "°F"
    return f"{location}의 현재 날씨: {data['condition']}, 기온 {temp}{unit_str}"


@beta_tool
def calculate(expression: str) -> str:
    """수학 표현식을 계산합니다.

    Args:
        expression: 계산할 수식, 예: "2 + 3 * 4"
    """
    try:
        # eval 대신 실제 환경에서는 안전한 파서를 사용하세요
        result = eval(expression, {"__builtins__": {}}, {})
        return f"{expression} = {result}"
    except Exception as e:
        return f"계산 오류: {e}"


print("=== Tool Runner 방식 ===")
runner = client.beta.messages.tool_runner(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[get_weather, calculate],
    messages=[
        {"role": "user", "content": "서울과 부산의 날씨를 알려주고, 15 * 7 + 3을 계산해줘."}
    ]
)

for message in runner:
    for block in message.content:
        if hasattr(block, "text"):
            print(block.text)


# --- 방법 2: 수동 루프 ---
print("\n=== 수동 루프 방식 ===")

tools_def = [
    {
        "name": "get_weather",
        "description": "지정된 위치의 현재 날씨를 가져옵니다.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "도시 이름"},
            },
            "required": ["location"]
        }
    }
]

messages = [{"role": "user", "content": "제주의 날씨는 어때?"}]

while True:
    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
        tools=tools_def,
        messages=messages
    )

    if response.stop_reason == "end_turn":
        for block in response.content:
            if block.type == "text":
                print(block.text)
        break

    # tool_use 처리
    tool_results = []
    messages.append({"role": "assistant", "content": response.content})

    for block in response.content:
        if block.type == "tool_use":
            print(f"[도구 호출] {block.name}({json.dumps(block.input, ensure_ascii=False)})")
            # get_weather 함수 직접 호출
            result = get_weather(**block.input)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

    messages.append({"role": "user", "content": tool_results})
