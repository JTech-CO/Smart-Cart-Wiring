# 스마트카트 모듈 배선도 B1

[English](README.md) | [한국어](README-KR.md)

배터리·퓨즈·단자대·DC-DC 컨버터·모터 드라이버·제어보드·센서·브레드보드를 함께 보는 정적 웹앱입니다. 이전 PCB 신호 허브를 모듈과 점퍼 하네스 방식으로 재구성했습니다. PCB 레이아웃, 추종 시뮬레이터, 주행 제어 화면은 없습니다.

## 실행

`index.html`을 브라우저로 엽니다. 모든 CSS·JS·도면·다운로드 파일이 로컬에 있어 인터넷/CDN/빌드/로그인이 필요하지 않습니다. 로컬 서버 사용 시 다음 명령을 실행합니다.

```sh
python -m http.server 8000
```

GitHub Pages에는 폴더 구조 전체를 유지해서 배치합니다. 기존 Smart-Cart의 3D 뷰어를 보존하려면 이 패키지를 별도 `wiring/` 디렉터리에 추가합니다. 저장소에는 자동으로 커밋·푸시하지 않았습니다.

## 화면

전체 배선 / 전원·구동 / 제어·센서 / 브레드보드 네 시트입니다. 부품 선택 시 실제 단자명·연결 네트·부품별 조건을 확인합니다. 브레드보드 접점을 선택하면 삽입 리드와 같은 도체의 다른 접점을 확인합니다. 드래그 이동, 휠·핀치 확대, 화면 맞춤, PDF·SVG·EasyEDA 다운로드만 제공합니다.

## 도면과 원본

- `downloads/Smart-Cart-Wiring-B1.pdf`: A3 가로 도면·삽입 위치·단자표·BOM·가져오기 안내.
- `assets/drawings/`: 네 시트의 벡터 SVG 원본.
- `eda/easyeda/SmartCart-B1-Modules.json`: EasyEDA Standard 회로도. Pro에서는 **Import EasyEDA(Standard)**로 가져옵니다.
- `eda/kicad/`: 캐시 라이브러리를 포함한 KiCad 5.1 계열 legacy 회로도 원본.
- `data/terminal-netlist.csv`: 44개 전기 심볼, 194개 단자, 63개 네트.
- `data/breadboard-contacts.csv`: 400접점 브레드보드의 사용 접점 84개.
- `docs/`: 조립·가져오기·출처 문서.
- `tests/`: 정적 검사와 브라우저 검사 기록.

## 반드시 구분할 것

웹/PDF는 재질과 외형을 재구성한 비축척 모듈 배선도입니다. 이미지에 그려진 헤더 위치를 실제 구매품의 핀 위치로 간주하면 안 됩니다. 실제 핀 이름·J2/J3 표·EDA 네트·브레드보드 접점표를 우선합니다. 케이블 개요에서는 USB와 GPIO 여러 가닥을 묶어 표시합니다.

브레드보드는 저전류 로직과 센서만 사용하며, 12V·배터리·모터·서보 전력은 통과하지 않습니다. 레일은 각 줄 25개 접점을 왼쪽부터 세는 독립 번호입니다. 실물 레일 분할과 중앙 홈 절연은 무전원 도통 검사로 확인해야 합니다. 주행용에는 납땜 하네스·잠금 커넥터·고정/절연이 필요합니다.

퓨즈의 * 값, 배터리/BMS, 컨버터, USB 허브, 접촉기, 모터 전류·회생·제동, 조향 기구는 미확정 항목입니다. 이 파일을 제작 승인이나 안전 인증으로 간주하지 않습니다. EasyEDA Pro 실제 가져오기 및 KiCad 자체 ERC도 미실행이며, 제공 정적 검사와 별개입니다. Gerber·PCB·실장 좌표는 포함하지 않습니다.

## 재생성

```sh
python tools/design.py
python tools/render.py
python tools/export_eda.py
python tests/validate_design.py
```

PDF 재생성은 `tools/build_documents.py` 및 `tools/build_pdf.py`를 사용합니다. PDF 생성에는 Playwright와 Chromium이 필요하지만 웹앱 실행에는 필요하지 않습니다.
