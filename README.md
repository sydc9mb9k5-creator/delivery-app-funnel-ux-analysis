# 배달특급 Funnel & UX Analysis
## Delivery App Funnel & UX Analysis — Synthetic Data

배달 앱의 사용자 여정을 **진입 → 탐색 → 장바구니 → 구매완료** 퍼널로 구조화하고,  
10,000명의 가상 사용자 로그를 활용해 핵심 이탈 구간을 진단한 개인 분석 프로젝트입니다.

퍼널 분석에서 끝나지 않고 **이벤트 로그 설계 → 가상 데이터 생성 → 병목 분석 → A/B 시나리오 비교 → UX 개선안 → Streamlit 대시보드**까지 연결했습니다.

> **Data Notice**  
> 본 프로젝트는 실제 배달특급 고객 데이터나 실제 운영 A/B 테스트 결과가 아닌 **synthetic data(가상 데이터)** 기반의 분석 연습 프로젝트입니다.  
> A/B 그룹의 차이 역시 코드에서 설정한 전환 확률을 바탕으로 생성한 시뮬레이션 결과입니다.

---

## Project Goal

> 사용자가 구매까지 도달하는 과정에서 **어디에서 가장 많이 이탈하는지** 파악하고,  
> 퍼널 병목을 줄이기 위한 UX 개선 가설을 데이터로 검토할 수 있을까?

분석을 위해 사용자 행동을 네 단계로 정의했습니다.

1. **진입** — App Opened
2. **탐색** — Home Viewed
3. **장바구니** — Cart Interacted
4. **구매완료** — Purchase Completed

---

## My Work

본 프로젝트는 로그 설계부터 분석, 시각화, 대시보드와 개선 리포트까지 직접 구성한 개인 프로젝트입니다.

### 1. Event Taxonomy Design

앱 사용자의 행동을 분석할 수 있도록 이벤트 로그 체계를 설계했습니다.

- Funnel Stage
- Event Category
- Event Name
- Business Question
- Trigger / Event Description
- Property Type
- Property Name
- Sample Values
- Platform

진입·탐색·장바구니·구매뿐 아니라 위치 권한, 주소 입력, 검색, 리뷰, 쿠폰, 결제수단, 오류 등  
추후 서비스 분석으로 확장할 수 있는 이벤트와 속성을 함께 정의했습니다.

### 2. Synthetic Log Generation

Python으로 10,000명의 가상 사용자를 생성하고 A/B UI 그룹과 지역을 할당했습니다.

- A: 기존 UI
- B: 선탐색을 허용한 개선 UI
- 사용자 지역: 도심권 / 외곽 주거지

그룹과 지역에 따라 단계별 전환 확률을 다르게 설정하여 가상 이벤트 로그를 생성했습니다.

### 3. Funnel Analysis

생성된 로그를 기준으로 단계별 고유 사용자 수를 집계했습니다.

| Funnel Stage | Users | Previous-step Drop-off |
| --- | ---: | ---: |
| App Opened | 10,000 | - |
| Home Viewed | 3,942 | 60.6% |
| Cart Interacted | 1,186 | 69.9% |
| Purchase Completed | 491 | 58.6% |

**전체 구매 전환율은 약 4.9%**였으며, 가장 큰 병목은 진입→탐색과 탐색→장바구니 구간에서 나타났습니다.

### 4. A/B Scenario Comparison

초기 진입 마찰을 줄인 UI 시나리오를 가정해 두 그룹을 비교했습니다.

| Group | App Opened | Home Viewed | Entry → Explore |
| --- | ---: | ---: | ---: |
| A — Existing UI | 5,076 | 1,017 | **20.0%** |
| B — Improved UI | 4,924 | 2,925 | **59.4%** |

B 그룹의 탐색 진입률은 A 그룹보다 **39.4%p 높게 생성**되었습니다.

> 이 수치는 실제 서비스 실험의 인과 효과가 아니라,  
> 개선 UI가 더 높은 탐색 전환을 만든다는 **가정으로 생성한 데이터의 시뮬레이션 결과**입니다.

### 5. UX Improvement Proposal

분석 결과를 바탕으로 다음 개선 방향을 제안했습니다.

**선탐색 중심 온보딩**
- 앱 진입 직후 상세 주소 입력을 강제하지 않음
- 위치 권한을 이용해 임시 지역을 설정하고 음식점·메뉴 탐색을 먼저 허용
- 상세 주소는 주문 단계에서 입력

**탐색 효율 개선**
- 홈 화면의 정보 과밀도를 줄이고 핵심 탐색 기능을 전면 배치
- ‘1인분’, ‘오늘의 할인’ 등 빠르게 선택할 수 있는 퀵 필터 제안

---

## Event Taxonomy

`data/event_taxonomy.xlsx`에는 실제 서비스 분석을 가정한 이벤트 로그 설계가 정리되어 있습니다.

대표 이벤트:

- `app_opened`
- `location_permission_requested`
- `address_detail_entered`
- `home_viewed`
- `home_content_clicked`
- `search_interacted`
- `store_interacted`
- `cart_interacted`
- `order_initiated`
- `purchase_completed`
- `order_status_changed`
- `error_encountered`
- `review_written`

각 이벤트에는 분석 목적과 Trigger, Property까지 함께 정의했습니다.

---

## Visualization

Plotly를 활용해 메인 퍼널과 A/B 그룹 비교 퍼널을 시각화했습니다.

- `notebooks/plotly_visualization.ipynb`
- 생성 결과물: `funnel_chart.html`, `ab_test_funnel.html`

---

## Streamlit Dashboard

`app/app.py`에서는 프로젝트 결과를 대시보드 형태로 확인할 수 있습니다.

구성:

- 핵심 지표 요약
- 메인 퍼널
- A/B 그룹별 퍼널
- 주요 병목 진단
- UX 개선 전략
- 원본 이벤트 로그 조회

### Run locally

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

---

## Repository Files

### `data/event_taxonomy.xlsx`
배달 앱 이벤트 및 Property를 정의한 **로그 설계서**입니다.

### `data/delivery_app_logs.csv`
10,000명의 가상 사용자 행동으로 생성한 **synthetic event log**입니다.

### `notebooks/funnel_analysis.ipynb`
가상 사용자 생성, 퍼널 집계, 세그먼트 분석 및 통계 검정을 수행한 메인 분석 노트북입니다.

### `notebooks/plotly_visualization.ipynb`
메인 퍼널과 A/B 비교 퍼널을 Plotly로 시각화하는 노트북입니다.

### `app/app.py`
퍼널 분석 결과와 UX 개선안을 보여주는 Streamlit 대시보드입니다.

### `report/funnel_ux_report.pdf`
문제 정의, 병목 분석, A/B 시나리오, UX 개선안을 정리한 최종 리포트입니다.

---

## Tools

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Seaborn
- Plotly
- Streamlit

---

## Repository Structure

```text
delivery-app-funnel-ux-analysis/
│
├── README.md
├── requirements.txt
│
├── data/
│   ├── event_taxonomy.xlsx
│   └── delivery_app_logs.csv
│
├── notebooks/
│   ├── funnel_analysis.ipynb
│   └── plotly_visualization.ipynb
│
├── app/
│   └── app.py
│
└── report/
    └── funnel_ux_report.pdf
```

---

## Project Type

- **Personal Data Analysis Project**
- Synthetic Data / Simulation
- Funnel Analysis
- Product & UX Analytics

> The project demonstrates an end-to-end workflow from event taxonomy design and synthetic data generation  
> to funnel diagnosis, scenario-based A/B comparison, UX recommendations, and dashboard implementation.
