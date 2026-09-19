import streamlit as st
import re
from pypinyin import pinyin, Style
from korean_romanizer.romanizer import Romanizer

# 页面基础配置
st.set_page_config(page_title="汉字拼音 / 韩语罗马音速查", page_icon="🔤", layout="centered")

st.title("汉字拼音 / 韩语罗马音速查")
st.caption("输入中文➡输出拼音，输入韩文➡输出罗马音")

# 韩国常用姓氏与高频音节习惯拼写法映射
CUSTOM_KOREAN_MAP = {
    "김": "kim",
    "박": "park",
    "이": "lee",
    "최": "choi",
    "정": "jung",
    "강": "kang",
    "조": "cho",
    "윤": "yoon",
    "장": "jang",
    "임": "lim",
    "한": "han",
    "오": "oh",
    "신": "shin",
    "권": "kwon",
    "황": "hwang",
    "안": "ahn",
    "송": "song",
    "전": "jeon",
    "홍": "hong",
    "유": "yoo",
    "고": "ko",
    "문": "moon",
    "양": "yang",
    "손": "son",
    "배": "bae",
    "백": "baek",
    "허": "huh",
    "노": "noh",
    "심": "shim",
    "하": "ha",
    "곽": "kwak",
    "성": "sung",
    "차": "cha",
    "주": "joo",
    "우": "woo",
    "구": "koo",
    "신": "shin",
    "임": "lim",
    "나": "na",
    "민": "min",
    "현": "hyun",
    "원": "won",
}

def has_hangul(text: str) -> bool:
    """检查是否包含韩文字符"""
    return bool(re.search(r'[\uac00-\ud7a3\u1100-\u11ff\u3130-\u318f]', text))

def has_chinese(text: str) -> bool:
    """检查是否包含汉字"""
    return bool(re.search(r'[\u4e00-\u9fa5]', text))

def romanize_korean_spaced(text: str) -> str:
    """逐字转为罗马音并用空格隔开，优先采用常用习惯拼写"""
    result = []
    for char in text:
        if char in CUSTOM_KOREAN_MAP:
            result.append(CUSTOM_KOREAN_MAP[char])
        elif re.search(r'[\uac00-\ud7a3]', char):
            result.append(Romanizer(char).romanize())
        elif char.strip():
            result.append(char)
    return " ".join(result)

# 单一输入框
query = st.text_input("请输入汉字或韩语：", placeholder="例如：韩鑫哲 或 한흠철").strip()

if query:
    is_ko = has_hangul(query)
    is_zh = has_chinese(query)

    with st.container(border=True):
        if is_ko:
            romanized_result = romanize_korean_spaced(query)
            st.subheader(f"韩语原文：{query}")
            st.markdown(f"**官方罗马读音：** `{romanized_result}`")

        elif is_zh:
            py_list = pinyin(query, style=Style.TONE)
            pinyin_result = " ".join([item[0] for item in py_list])

            st.subheader(f"汉字原文：{query}")
            st.markdown(f"**标准汉语拼音：** `{pinyin_result}`")

        else:
            st.warning("未检测到汉字或韩文字符，请输入汉字或韩语文本。")