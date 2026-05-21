# 📊 TIMA 스타일 주도주 모니터링

한국 주식 시장의 실시간 주도주 테마를 모니터링하는 Streamlit 애플리케이션입니다.

## ✨ 기능

- 🚀 **실시간 테마 조회**: Naver Finance에서 상승률 상위 4개 테마 자동 추출
- 📈 **주식 정보**: 각 테마별 주도주 3개 표시 (가격, 변동률, 거래대금)
- 📱 **모바일 최적화**: 모든 기기에서 완벽한 반응형 디자인
- 🔄 **자동 업데이트**: 60초마다 캐시 갱신
- 💰 **거래대금 정보**: pykrx를 통한 실시간 거래대금 데이터

## 🚀 설치 및 실행

### 로컬 설치

```bash
# 1. 저장소 클론
git clone https://github.com/baekjongil86-crypto/tima-theme-monitor.git
cd tima-theme-monitor

# 2. 필요 패키지 설치
pip install -r requirements.txt

# 3. 앱 실행
streamlit run app.py
```

### Streamlit Cloud 배포

1. [Streamlit Cloud](https://streamlit.io/cloud)에 로그인
2. "New app" → GitHub 저장소 선택
3. Repository: `baekjongil86-crypto/tima-theme-monitor`
4. Main file path: `app.py`
5. Deploy!

## 📋 요구사항

- Python 3.8+
- streamlit
- requests
- beautifulsoup4
- pandas
- pykrx

## 🎯 주요 특징

### 모바일 최적화
- ✅ 반응형 레이아웃
- ✅ 터치 친화적 UI
- ✅ 최적화된 글씨 크기
- ✅ 자동 사이드바 숨김

### 실시간 데이터
- 📡 Naver Finance 실시간 스크래핑
- 💾 60초 캐시로 성능 최적화
- 🔍 거래대금 자동 조회
- ⏰ 장외 시간 에러 처리

## 📝 사용 방법

1. 앱 실행 시 상위 4개 상승 테마가 자동으로 표시됩니다.
2. 각 테마 카드에서 주도주 정보를 확인할 수 있습니다.
3. 🔄 새로고침 버튼으로 수동 업데이트 가능합니다.
4. 60초마다 자동으로 데이터가 갱신됩니다.

## ⚠️ 주의사항

- 평일 09:00~15:30 장시간에만 정상 동작합니다.
- 웹 스크래핑 기반이므로 Naver Finance 레이아웃 변경 시 수정 필요할 수 있습니다.
- 과도한 요청 시 IP 제한될 수 있으니 주의하세요.

## 📧 지원

문제가 발생하면 GitHub Issues에 등록해주세요.

---

**Last Updated**: 2026-05-21
