import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# 1. 페이지 기본 설정
st.set_page_config(page_title="배달특급 퍼널 분석", layout="wide")

# 2. 데이터 로드 및 전처리
DATA_PATH = Path(__file__).resolve().parents[1] / 'data' / 'delivery_app_logs.csv'
df = pd.read_csv(DATA_PATH)
if 'user_region' in df.columns:
    df = df.drop(columns=['user_region'])

# 3. 차트 생성 함수 모음
def get_funnel_chart(data):
    step_order = ['1_app_opened', '2_home_viewed', '3_cart_interacted', '4_purchase_completed']
    step_labels = ['1. 진입', '2. 탐색', '3. 장바구니', '4. 구매완료']
    funnel_counts = [data[data['step'] == s]['user_id'].nunique() for s in step_order]
    custom_colors = ['#AECDF8', '#679DF5', '#1D68F2', '#0F3B99']
    
    fig = go.Figure(go.Funnel(
        y=step_labels,
        x=funnel_counts,
        textinfo="value+percent initial",
        marker=dict(color=custom_colors)
    ))
    fig.update_layout(title="<b>메인 퍼널 이탈 현황</b>", template="plotly_white")
    return fig

def get_ab_test_funnel_chart(data):
    step_order = ['1_app_opened', '2_home_viewed', '3_cart_interacted', '4_purchase_completed']
    step_labels = ['1. 진입', '2. 탐색', '3. 장바구니', '4. 구매완료']
    
    group_a = data[data['ui_group'] == 'A(기존 UI)'].groupby('step')['user_id'].nunique().reindex(step_order)
    group_b = data[data['ui_group'] == 'B(개선 UI)'].groupby('step')['user_id'].nunique().reindex(step_order)

    fig = go.Figure()
    fig.add_trace(go.Funnel(name='A (기존 UI - 주소 강제)', y=step_labels, x=group_a.values, textinfo="value+percent initial", marker=dict(color="#B0BEC5")))
    fig.add_trace(go.Funnel(name='B (개선 UI - 선탐색 허용)', y=step_labels, x=group_b.values, textinfo="value+percent initial", marker=dict(color="#1D68F2")))
    
    fig.update_layout(title="<b>A/B 테스트 그룹별 퍼널 전환 비교 (초기 진입 마찰 검증)</b>", template="plotly_white")
    return fig

# --- 4. 대시보드 화면 구성 ---

# 좌측 사이드바 구성
with st.sidebar:
    st.title("배달특급 프로젝트")
    st.markdown("데이터 분석가 **양재희**")
    st.divider()
    st.info("**프로젝트 목적**\n\n초기 진입 이탈(60%) 원인 진단 및 A/B 테스트 기반 UX 전략 도출")

# 메인 타이틀
st.title("배달특급 퍼널 분석 및 UX 개선 대시보드")
st.markdown("초기 진입 단계의 대규모 이탈 원인을 분석하고, 데이터 기반의 UX 개선 전략을 제안합니다.")

# 핵심 지표 하이라이트
st.subheader("핵심 지표 요약")
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="A그룹(기존 UI) 진입률", value="20.0%", delta="60% 이탈", delta_color="inverse")
    with col2:
        st.metric(label="B그룹(선탐색 UI) 진입률", value="59.4%", delta="39.4%p 상승")
    with col3:
        st.metric(label="B그룹 최종 구매 전환율", value="8.7%", delta="기존 대비 상승")

# 탭(Tabs) 분할
st.subheader("데이터 분석 및 인사이트")
tab1, tab2, tab3 = st.tabs(["퍼널 비교 시각화", "서비스 개선 리포트", "원본 데이터 조회"])

# 첫 번째 탭: 시각화
with tab1:
    col_left, col_right = st.columns(2)
    with col_left:
        st.plotly_chart(get_funnel_chart(df), use_container_width=True)
    with col_right:
        st.plotly_chart(get_ab_test_funnel_chart(df), use_container_width=True)

# 두 번째 탭: 서비스 개선 리포트
with tab2:
    st.markdown("### 배달특급 퍼널 분석 및 UX 개선 요약 리포트")
    
    # [행 1] 좌측: 1. 주요 병목 구간 진단 / 우측: 2. A/B 테스트 검증 결과
    row1_col1, row1_col2 = st.columns(2)
    
    with row1_col1:
        st.markdown("#### 1. 주요 병목 구간 진단 및 연쇄 구조")
        st.markdown("""
        * **1단계 (진입 - 탐색) | 이탈률 60%**
          * 원인: 앱 실행 직후 상세 주소 입력 강제로 인한 초기 진입 마찰 발생
        * **2단계 (탐색 - 장바구니) | 이탈률 70%**
          * 원인: 15분할 롤링 배너의 비효율적 동선 및 맞춤 필터 부재로 인한 탐색 피로도 급증
        * **인과적 연쇄 구조**
          * 1단계 마찰로 유입 파이프라인 자체가 붕괴된 상태이며, 겨우 진입한 유저마저 2단계의 복잡한 UI를 만나 이탈하는 연쇄적 결함 발생. 따라서 1단계 기초 공사 후 2단계 리텐션 보완이 필수적임.
        """)

    with row1_col2:
        st.markdown("#### 2. A/B 테스트 검증 결과")
        st.markdown("""
        * **검증 대상:** 초기 진입 마찰 해소 (선탐색 허용)
        * **성과:** 진입률 **20.0%에서 59.4%로 39.4%p 상승**
        * **시사점:** 주소 입력을 뒤로 미루는 온보딩 구조가 초기 이탈 방어의 핵심 기반임을 입증
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # [행 2] 좌측: 3. 서비스 개선 전략 / 우측: 4. 기대 효과
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        st.markdown("#### 3. 서비스 개선 전략 및 제안 (논리 분리)")
        st.markdown("""
        * **[실험 검증 완료] 전략 A: 선탐색 중심 온보딩 개편**
          * 내용: 회원가입 및 상세 주소 입력을 결제 단계로 유예하고, 위치 권한 기반 동 단위 임시 설정으로 즉각적인 음식 탐색 보장 (쿠팡이츠 벤치마킹)
          * 근거: A/B 테스트를 통해 진입률 상승 효과가 정량적으로 검증됨
        * **[데이터 기반 추가 제안] 전략 B: 직관적 퀵 필터 배치**
          * 내용: 2단계 탐색 이탈(70%)을 방어하기 위해, 효율 낮은 롤링 배너를 축소하고 '1인분', '오늘의 할인' 필터를 홈 최상단에 고정하여 동선 단축
          * 근거: 퍼널 데이터에서 확인된 탐색 피로도 해결을 위한 후속 조치
        """)

    with row2_col2:
        st.markdown("#### 4. 기대 효과")
        st.markdown("""
        * 검증된 온보딩 개편을 통한 대규모 유입 확보와 퀵 필터를 통한 탐색 효율 극대화를 결합하여 최종 구매 전환율 및 거래액(GMV) 증대 견인
        """)

# 세 번째 탭: 원본 데이터
with tab3:
    st.dataframe(df, use_container_width=True)