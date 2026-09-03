import os
import streamlit as st
from dotenv import load_dotenv
from anthropic import Anthropic
from datetime import datetime


load_dotenv()


client = Anthropic(
    base_url=os.getenv("ANTHROPIC_BASE_URL"),
    api_key=os.getenv("ANTHROPIC_API_KEY")
)


def ask_ai(prompt):
    res = client.messages.create(
        model="claude-haiku", max_tokens=1024,
        messages=[{"role":"user","content":prompt}]
    )
    return res.content[0].text


def get_zodiac_sign(month, day):
    """생년월일로부터 별자리를 반환합니다."""
    zodiac_signs = [
        ("양자리", (3, 21), (4, 19)),
        ("황소자리", (4, 20), (5, 20)),
        ("쌍둥이자리", (5, 21), (6, 20)),
        ("게자리", (6, 21), (7, 22)),
        ("사자자리", (7, 23), (8, 22)),
        ("처녀자리", (8, 23), (9, 22)),
        ("천칭자리", (9, 23), (10, 22)),
        ("전갈자리", (10, 23), (11, 21)),
        ("궁수자리", (11, 22), (12, 21)),
        ("염소자리", (12, 22), (1, 19)),
        ("물병자리", (1, 20), (2, 18)),
        ("물고기자리", (2, 19), (3, 20)),
    ]

    date = (month, day)
    for sign, start, end in zodiac_signs:
        if start <= date <= end:
            return sign
    return "양자리"


def generate_fortune(name, birth_date, zodiac):
    """AI를 사용하여 오늘의 운세를 생성합니다."""
    prompt = f"""당신은 전문 점술가입니다. 다음 사람의 오늘의 운세를 생성해주세요:

이름: {name}
생년월일: {birth_date}
별자리: {zodiac}

다음 조건을 반드시 따르세요:
1. 40-50줄의 상세한 운세를 작성하세요
2. 반드시 부정적이고 경고적인 내용으로만 작성하세요
3. 일과, 사랑, 건강, 재정, 운의 측면에서 각각 어려움이 있을 것임을 암시하세요
4. 주의와 조심을 강조하세요
5. 한국어로 작성하세요

{name}님({birth_date}, {zodiac})의 오늘의 운세:"""

    return ask_ai(prompt)


def main():
    st.set_page_config(page_title="나의 운세 & 별자리 앱", page_icon="🔮", layout="centered")

    st.title("🔮 나의 운세 & 별자리 앱")
    st.write("당신의 운명을 확인해보세요...")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("이름", placeholder="예: 김지은", key="name_input")

    with col2:
        birth_date = st.date_input(
            "생년월일",
            value=datetime(2000, 1, 1),
            min_value=datetime(1900, 1, 1),
            max_value=datetime(2099, 12, 31),
            key="date_input"
        )

    if birth_date:
        zodiac = get_zodiac_sign(birth_date.month, birth_date.day)
        st.info(f"당신의 별자리: **{zodiac}**")
    else:
        zodiac = None

    st.divider()

    if st.button("운세보기 🔮", use_container_width=True, type="primary"):
        if not name:
            st.error("이름을 입력해주세요!")
        elif not birth_date:
            st.error("생년월일을 선택해주세요!")
        else:
            with st.spinner("운세를 불러오는 중..."):
                fortune = generate_fortune(
                    name,
                    birth_date.strftime("%Y년 %m월 %d일"),
                    zodiac
                )

                st.divider()
                st.subheader(f"{name}님의 오늘의 운세")
                st.markdown(fortune, unsafe_allow_html=True)


if __name__ == "__main__":
    main()