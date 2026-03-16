#!/bin/bash
# 모든 샘플 순서대로 실행 (비대화형 샘플만)

echo "환경 설정 중..."
cd "$(dirname "$0")"
pip install -q -r requirements.txt

echo ""
echo "========================================"
echo "01. 기본 메시지 요청"
echo "========================================"
python 01_basic.py

echo ""
echo "========================================"
echo "02. 스트리밍"
echo "========================================"
python 02_streaming.py

echo ""
echo "========================================"
echo "04. 툴 사용"
echo "========================================"
python 04_tool_use.py

echo ""
echo "========================================"
echo "05. 구조화된 출력"
echo "========================================"
python 05_structured_output.py

echo ""
echo "========================================"
echo "06. Extended Thinking"
echo "========================================"
python 06_thinking.py

echo ""
echo "=== 완료! ==="
echo "대화형 샘플(03_conversation.py)은 직접 실행하세요: python 03_conversation.py"
