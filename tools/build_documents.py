"""Build documentation and the matching A3 drawing/terminal PDF print source."""
from pathlib import Path
import json,html,math
from design import ROOT,MODEL,C,BP,placements,jumpers,byref,SOURCES
E=lambda s:html.escape(str(s))
readme='''# Smart Cart Module Wiring Studio B1

[한국어](README-KR.md) | [English](README.md)

A module-level wiring viewer for the user-following smart cart. This is NOT a PCB layout or a cart-control application. The project contains original textured vector illustrations, an accurate reference breadboard contact map, terminal data, and editable electrical schematic exports.

## Use
Open `index.html`. All assets are local, with no build step, CDN, login, backend, or device-control API. Alternatively, run `python -m http.server 8000` in this folder. For GitHub Pages, copy the entire folder contents to a chosen deployment directory. To preserve the existing Smart-Cart viewer, add this package under a separate `wiring/` directory instead of overwriting its root files.

## Files
- `assets/drawings/`: four editable SVG drawing sheets.
- `downloads/Smart-Cart-Wiring-B1.pdf`: A3 landscape drawing and assembly-reference set.
- `eda/easyeda/SmartCart-B1-Modules.json`: self-contained EasyEDA Standard schematic; import into Pro using Import EasyEDA(Standard).
- `eda/kicad/`: KiCad 5.1-compatible legacy schematic/library source, not a modern PCB project.
- `data/`: module BOM, terminal netlist and breadboard contacts.
- `tools/`: reproducible model/export/render generators.
- `tests/`: static and browser checks and reports.

## Scope
The reference uses 44 wired module symbols, 194 schematic terminals and 63 net names. A 400-tie breadboard uses 300 strip contacts and 100 rail contacts. Rails are numbered separately from the numbered strip columns, from left to right, 1 to 25.

The first three drawings use named functional terminals and cable bundles; their pictorial geometry is not a mechanical drawing or exact purchased-board pin placement. Follow physical terminal names and the contact tables, not illustrative silkscreen positions. Components with unknown specifications and fuse ratings marked * are conditional. This is a bench prototype reference, not a release-approved vehicle harness.

EasyEDA Standard JSON uses real symbols, pins, wires and net labels, not an imported picture. Native EasyEDA Pro conversion and native KiCad ERC have NOT been executed. Check the import against the supplied 194-terminal CSV before any hardware work. No Gerber, PCB, pick-and-place or footprint package is supplied.

See `docs/ASSEMBLY-KR.md`, `docs/EASYEDA-IMPORT-KR.md`, `docs/SOURCES.md` and `tests/design-report.json`.
'''
(ROOT/'README.md').write_text(readme)
(ROOT/'README-KR.md').write_text('''# 스마트카트 모듈 배선도 B1

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
''')
assembly='''# B1 모듈 조립 참조 및 미확정 항목

## 설계 기준과 출처

Smart-Cart 저장소 main의 `2b4b8fea6909e4f76b4a52b02c5075c3f478097b`를 참조했습니다. 해당 저장소는 사진 기반 절차적 WebGL 뷰어이며 전장 회로나 FreeCAD 치수 원본이 아닙니다. 코드나 기존 이미지의 라이선스를 새로 지정하거나 그대로 가져오지 않았습니다. 본 도면의 외형 재구성 역시 실측·제품 CAD가 아닙니다.

원래 카트의 후륜 차동 구동·전륜 자유 캐스터와 조향 서보 2개 요구를 구분합니다. 두 서보는 보존했으나 조향 링크·조향 끝점·차동 구동과의 운동학을 정하기 전에는 동력 조향을 활성화하지 않습니다.

## 배선 기준

전력 하네스는 BAT+, BUS24, DRIVE24, P12, P5, GND로 구분합니다. 전원 -의 공통화와 서로 다른 +전원 합선은 다릅니다. 컨버터는 비절연형을 가정했으며 다른 제품 사용 시 공통 접지/통신 기준을 다시 검토합니다. 모터 A/B는 H브리지 출력이라 어느 쪽도 상시 GND가 아닙니다.

SBC·서보·모터 전류는 브레드보드를 거치지 않습니다. 각 귀환은 X0의 적절한 전력 분기로 보내며 신호 점퍼를 대전류 귀환으로 이용하지 않습니다. 그림의 케이블 굵기는 시각 구분이고 AWG 선정값이 아닙니다. 길이, 주위 온도, 번들링, 단자 전류, 전압 강하, 퓨즈 시간-전류 곡선과 단락 차단용량을 확보한 뒤 도체 단면을 확정합니다.

## 전원과 정지

BT1은 기존 24V 클래스 108Ah 요구입니다. 배터리 실모델·직렬 수·BMS 방전/충전 허용 전류·충전 상한은 미확정입니다. 8S LiFePO4로 구성하면 공칭 25.6V이며 최대 충전 전압은 배터리 제조사에 따라 확인해야 합니다. 용량 Ah를 허용 방전 A로 취급하지 않습니다.

BTS7960의 정상 입력 전압 범위(5.5~27.5V)는 완충 8S 배터리와 여유가 부족하므로 기본 구성에서 제외했습니다. SMC G2 24v19는 조건부 참조이며, 실제 연속 전류·스톨·방열·재생 제동 검증이 필요합니다. 제조사의 포함 단자대 15~16A 안내 때문에 25A 퓨즈가 적힌 분기를 해당 단자대에 그대로 승인하지 않았습니다. 적합한 고전류 접속 또는 드라이버 변경이 필요합니다. [S02, S11]

DC1: 12V/20A, DC2: 5V/10A는 목표 출력입니다. 입력 허용 범위가 완충 및 과도전압을 포함해야 하고, 연속 출력 열조건·단락·과전압 보호·부하 급변 응답은 실모델로 확인해야 합니다. 12V 서보 2개의 지속 스톨을 퓨즈만으로 보호할 수는 없습니다.

K1은 12V 코일과 독립 NO 보조접점이 있는 DC 접촉기를 가정합니다. P12→F9→S1 NC→(S2 NO || K1 13-14)→A1, A2→GND가 자기유지 기능 회로입니다. Z1은 K1 지정 코일 억제기입니다. S1 복귀만으로 코일을 재여자하지 않지만, 단일 접점 용착·배선 단락까지 안전을 보장하는 인증 회로가 아닙니다. 전원 차단은 제동이 아니며 조향 전원은 유지됩니다. K1 개방/배터리 완충/BMS 차단 시 회생 에너지 처리와 별도 브레이크를 반드시 설계해야 합니다.

## 제어·센서

ESP32-DevKitC V4 WROOM-32E는 허브 USB로만 급전합니다. 5V 헤더와 다른 USB 전원을 추가 병렬 급전하지 않습니다. J2/J3 번호는 Espressif V4 보드의 표 기준이며 다른 DevKit·WROVER·클론은 회로/핀맵을 다시 확인합니다. [S03]

Orange Pi는 외부 5V 전원 입력을 사용합니다. 외부 전원 4포트 허브는 upstream 역급전 방지와 포트별 전류 조건이 있는 제품이어야 합니다. 4포트는 ESP32, C1 어댑터, UWB L, UWB R에 각각 할당합니다. USB D±는 완성 케이블로 배선하고 브레드보드를 통과하지 않습니다. C1의 기동 전류와 허브 포트 한도·케이블 손실을 시험합니다.

BU04-Kit의 USB/거리 데이터 포트와 TTL/AT 포트는 다릅니다. 여기서는 USB 거리 데이터 포트를 연결합니다. bare BU04나 다른 Follow Package를 동일 회로로 간주하지 않습니다. 사용자 태그는 별도 배터리입니다. 2개 베이스와 1개 태그의 동시 측정/동기화/ID는 해당 펌웨어에서 검증해야 합니다. [S06]

IMU는 Adafruit BNO085 #4754 SPI 기준입니다. VIN 3.3V, P0/P1 HIGH, SCL=SCK, DI=MOSI, SDA=MISO, CS/INT/RST 사용. 3Vo 출력은 외부 전원에 연결하지 않습니다. ToF는 Pololu #3415의 VIN 3.3V·I2C 기준이고 XSHUT/GPIO1/VDD는 NC입니다. 두 제품의 자체 레귤레이터 출력과 입력을 혼동하지 않습니다. [S04, S05]

서보 PWM은 SN74AHCT125N 5V 버퍼를 통해 공급합니다. GPIO13/14에 10kΩ 풀다운을 두고, 버퍼 출력에 220Ω 직렬 저항을 둡니다. DIP 8/11번 출력은 NC, 9/12번 입력은 GND, 10/13번 /OE는 5V입니다. 제조사 핀 표와 실제 패키지 노치 방향을 확인합니다. RDS51150 실제 모델의 5V PWM 허용/선 순서/피드백선과 기구 끝점은 미확정입니다. [S07]

UART 직렬 저항은 TX에 1kΩ이며 완전한 전원 분리/역급전 방지 소자가 아닙니다. 드라이버 또는 ESP32 전원이 없는 상태의 통신선 전압과 역급전, 명령 timeout 및 safe-start를 실측 검증합니다.

## 브레드보드 위치 규칙

400접점 기준: 본체 30열×10행=300개, 전원 레일 25개×4줄=100개. 상부 T+/T-, 하부 B+/B- 레일은 각각 왼쪽부터 1~25번으로 세며 본체 열 번호와 혼용하지 않습니다. 실제 구매 브레드보드의 레일 개수·분할·배치는 무전원 도통 검사로 확인합니다.

T+는 ESP32 3.3V, B+는 F10에서 오는 5V 버퍼 전원입니다. T-25와 B-25만 공통 음극 점퍼로 연결합니다. IC U2는 e3~e9 / f3~f9에 걸치며 1번=e3, 7번=e9, 8번=f9, 14번=f3입니다. `data/breadboard-contacts.csv`가 84개 사용 접점과 연결 리드의 전체 목록입니다. 저항의 긴 다리를 서로 접촉시키지 말고 노출 구간을 절연/정리합니다.

## 첫 통전 전

1. 배터리를 분리하고 모든 전원 레일의 극성, 분배 블록의 도통, 각 퓨즈 전단/후단과 스위치 우회선 부재를 확인합니다.
2. 전류 제한 전원으로 DC-DC를 단독 시험하고, 센서/USB/ESP32를 한 모듈씩 연결하여 전압과 발열을 확인합니다.
3. 모터를 바퀴가 안전하게 뜬 상태에서 제한 전류로 시험합니다. 스톨을 손으로 강제로 만들지 않습니다.
4. 조향 끝점과 링크를 검증한 후 서보를 시험합니다. 두 서보가 서로 맞서는 토크를 지속하지 않게 합니다.
5. 비상정지, 통신 끊김, 제어보드 재부팅, 태그 상실, 명령 timeout, 수동 재무장을 시험합니다. 탑승 시험이나 경사로 시험은 별도 기계/제동 검토 전 실시하지 않습니다.

정적 연결 검사는 전력 정격이나 고장 시 안전성을 검증하는 시험이 아닙니다. 이 파일은 조건부 벤치 설계이므로 전장 담당자의 제작 승인과 실측 검증이 필요합니다.
'''
(ROOT/'docs/ASSEMBLY-KR.md').write_text(assembly)
importdoc='''# EasyEDA Pro / KiCad 가져오기

## EasyEDA Pro

1. Pro 편집기를 열고 **File → Import → EasyEDA(Standard)** 가져오기를 선택합니다. UI 언어/버전에 따라 메뉴 위치가 다를 수 있습니다.
2. `eda/easyeda/SmartCart-B1-Modules.json`을 선택하거나 `downloads/Smart-Cart-B1-EDA.zip`을 선택합니다. 이 ZIP은 해당 JSON 한 개만 포함합니다.
3. 이 파일은 EasyEDA **Standard 형식**입니다. **Import EasyEDA(Professional)**이나 Gerber 업로드를 선택하지 않습니다.
4. 생성된 회로도에서 44개 심볼과 194개 핀을 확인합니다. 같은 이름의 네트 라벨이 연결되며 63개 네트가 있습니다. 2개 NC 네트(NC_U2_8, NC_U2_11)는 각각 버퍼의 사용하지 않는 출력 하나만 포함합니다.
5. `data/terminal-netlist.csv`와 실제 단자명·핀 번호·네트 이름을 대조합니다. 모듈 심볼의 번호는 1..N 인덱스이며 실제 물리 핀은 핀 이름에 적힌 J2/J3 및 모듈 단자명을 따릅니다.

심볼·핀·배선·네트 라벨을 포함하는 실제 전기적 문서이며 단순 이미지 삽입물이 아닙니다. 패키지/풋프린트와 PCB는 의도적으로 비어 있습니다. 부품 내부 회로까지 복제한 것은 아니며 완성 모듈/허브/USB 케이블은 외부 어셈블리로 표현했습니다. USB 차동 라우팅이나 PCB 제조용 회로를 대신하지 않습니다.

웹/PDF의 금속·플라스틱·회로보드 텍스처와 브레드보드 렌더링은 SVG입니다. 그것이 EasyEDA에서 동일한 사실적 배치로 자동 변환되는 것은 아닙니다. EasyEDA에서는 대응하는 모듈형 전기 심볼 회로를 편집합니다.

## 검증 범위

공개 Standard JSON 문서 형식에 따라 생성했으며, JSON/심볼/핀/배선/라벨을 독립 재해석해 194개 단자의 모델 일치 여부를 검사했습니다. EasyEDA Pro 실제 가져오기와 변환 후 ERC는 실행하지 않았습니다. 공식 안내도 변환 시 도형·글꼴·핀 속성에 차이가 생길 수 있음을 명시합니다. 정상 가져오기/도면 일치 확인 전 제조·통전용으로 승인하지 않습니다.

## KiCad 보조 원본

`eda/kicad/SmartCart.pro`, `.sch`, `.lib`, `SmartCart-cache.lib`, `sym-lib-table`을 같은 폴더에 둡니다. KiCad 5.1 legacy 문법으로 생성한 회로도 원본입니다. KiCad 최신 버전에서는 legacy 변환 절차가 필요할 수 있습니다. EasyEDA의 KiCad 가져오기를 사용하려면 먼저 KiCad에서 열고 프로젝트 아카이브를 생성한 뒤 변환하는 방식을 권장합니다. 여기서는 KiCad 자체 파일 열기/ERC와 그 아카이브 생성까지 수행하지 않았습니다.

## 출처

- EasyEDA Pro Standard JSON/ZIP 가져오기: https://prodocs.easyeda.com/en/import-export/import-easyeda/
- EasyEDA Standard 문서 포맷: https://docs.easyeda.com/en/DocumentFormat/EasyEDA-Format-Standard/index.html
- EasyEDA Pro KiCad 가져오기: https://prodocs.easyeda.com/en/import-export/import-kicad/
'''
(ROOT/'docs/EASYEDA-IMPORT-KR.md').write_text(importdoc)
(ROOT/'docs/SOURCES.md').write_text('# Primary sources / 기본 참조\n\n검토일: 2026-09-13. 정확한 구매품 사양은 해당 제조사의 구매 모델 문서로 재확인합니다.\n\n'+'\n\n'.join(f'## {a} | {b}\n\n{c}' for a,b,c in SOURCES)+'\n\nRDS51150, 배터리/BMS, DC-DC, 허브, 접촉기는 정확한 구매 SKU가 없어 조건부 항목으로 표기했습니다.\n')
(ROOT/'docs/CHANGELOG.md').write_text('''# B1 변경 사항

PCB 신호 허브/제조 패키지를 모듈·퓨즈·단자대·브레드보드 참조로 교체했습니다. 추종 시뮬레이션·전력 예산 UI·체크리스트 편집·PCB 레이어·고급 대시보드를 제거했습니다. 400접점의 전원 레일은 본체와 별도로 25개씩 번호를 매겼습니다. GPIO13/14 서보 신호를 AHCT 5V 버퍼로 처리하고 조향 서보 2개는 기계 구조 검증이 필요한 조건부로 보존했습니다. UWB 2개는 BU04-Kit USB 거리 데이터 포트, 사용자 태그는 별도 전원입니다. 별도의 구매 회로/키트에는 동일 핀맵을 적용하지 않습니다.

B1은 Smart-Cart 저장소를 참조한 별도 정적 웹앱 패키지입니다. 원본 저장소를 변경하지 않았고 원본의 라이선스를 새로 부여하지 않았습니다. PCB 제조 파일이나 안전 인증은 포함하지 않습니다.
''')
# Print source. Identical SVG drawings followed by exhaustive assembly tables.
pages=[]
for i,p in enumerate(sorted((ROOT/'assets/drawings').glob('*.svg')),1):
 svg=p.read_text();svg=svg.replace('id="',f'id="p{i}-').replace('url(#',f'url(#p{i}-')
 pages.append('<section class="page drawing">'+svg+'</section>')
def table(head,rows,cls=''):
 return f'<table class="{cls}"><thead><tr>'+''.join('<th>'+E(h)+'</th>' for h in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+E(v)+'</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table>'
def pg(title,sub,body):
 no=len(pages)+1
 pages.append(f'<section class="page appendix"><header><div class="eyebrow">SMART CART / MODULE WIRING <span>B1 · 2026.09.13</span></div><h1>{E(title)}</h1><p>{E(sub)}</p></header><article>{body}</article><footer>조건부 벤치 설계 · 실제 구매품/퓨즈/전력/제동 검증 필요<span>SC-WIR-B1 / {no:02d}</span></footer></section>')
def box(title,txt):return '<div class="box"><h2>'+E(title)+'</h2><p>'+E(txt)+'</p></div>'
# Sheet 5: principal assembly maps
pinrows=[]
for p in byref['U1']['pins'][4:]:
 hs=[h for h,d in BP.items() if d['net']==p['net'] and d['owner'].startswith('U1.')]
 pinrows.append([p['name'],p['net'],', '.join(hs)])
passiverows=[[ref,byref[ref]['spec'],a+' ↔ '+b] for ref,(a,b) in placements.items()]
jumprows=[[f'JMP{i+1}',a+' ↔ '+b,BP[a]['net']] for i,(a,b) in enumerate(jumpers)]
body='<div class="cols"><div><h2>ESP32 실제 헤더 → 브레드보드</h2>'+table(['DevKitC V4 단자','연결 네트','삽입 위치'],pinrows)
body+=box('보드 및 전원 조건 [S03]','ESP32-WROOM-32E / DevKitC V4 기준. USB로만 급전하며 5V 헤더는 연결하지 않습니다. WROVER·클론은 이 표를 그대로 적용하지 않습니다. USB D±는 완성 케이블로 허브에 연결합니다.')
body+=box('IMU / ToF 조건 [S04, S05]','IMU는 Adafruit #4754: P0/P1=3.3V, SCL=SCK, DI=MOSI, SDA=MISO. 3Vo는 NC. ToF는 Pololu #3415: VIN=3.3V; XSHUT/GPIO1/VDD는 NC. GPIO34는 입력 전용 INT에 사용합니다.')+'</div><div><h2>저항 / 디커플링 실제 삽입</h2>'+table(['부품','사양','두 접점'],passiverows)+'<h2>전원·접지 점퍼</h2>'+table(['점퍼','두 접점','네트'],jumprows)
body+=box('U2 DIP14 방향 [S07]','상부 e3~e9는 1~7번, 하부 f3~f9는 14~8번입니다. 핀 1은 왼쪽 위 e3. 핀 7 GND, 핀 14 5V. 미사용 출력 8/11은 NC. 레일 번호는 본체 열 번호와 다릅니다.')+'</div></div>'
pg('조립 단자표 · ESP32 / 브레드보드','J2/J3는 보드의 실제 헤더 번호. 렌더링된 보드 그림의 헤더 위치를 핀 배치도로 대신하지 않습니다.',body)
# All 84 contacts, 42 rows per side.
contacts=[[h,v['net'],v['owner']] for h,v in BP.items()]
body='<div class="cols">'+''.join('<div>'+table(['접점','네트','삽입 리드'],contacts[i:i+42],'compact mono')+'</div>' for i in range(0,len(contacts),42))+'</div>'
body+=box('400접점의 해석','본체 30열×10행=300개, 전원 레일 25개×4줄=100개입니다. T/B는 상/하부 레일이며 +/− 각 줄을 왼쪽부터 1~25번으로 셉니다. 같은 열 a-e / f-j는 각각 공통. 모든 레일의 실제 연속성은 도통 검사를 실시합니다.')
pg('브레드보드 사용 접점 전체 목록','사용 접점 84개. 같은 홀에 두 리드를 중복 지정하지 않았습니다. 주행용에는 잠금 커넥터/납땜 하네스로 이전합니다.',body)
# Full canonical terminal list, 97 per page / two columns.
terminals=[[c['ref'],p['name'],p['net']] for c in C for p in c['pins']]
for part in range(2):
 rows=terminals[part*97:(part+1)*97]
 body='<div class="cols">'+''.join('<div>'+table(['부품','실제 단자명','네트'],rows[i:i+49],'compact mono')+'</div>' for i in range(0,len(rows),49))+'</div>'
 pg('모듈 전기 연결표 '+str(part+1)+' / 2','전체 194단자 / 63네트. 동일 네트명은 연결되며, 퓨즈·저항·접점 양단은 서로 다른 네트로 구분합니다.',body)
# BOM and open engineering requirements.
status={'reference':'기준품','candidate':'정격/모델 확인','conditional':'조건부'}
bom=[[c['ref'],c['name'],c['spec'],status[c['status']]] for c in C]
body='<div class="cols">'+''.join('<div>'+table(['부품','구성 요소','사양 / 목표','상태'],bom[i:i+23],'bom')+'</div>' for i in range(0,len(bom),23))+'</div>'
body+=box('퓨즈·전력부 제작 보류 조건','* 표시는 확정 정격이 아닙니다. 배터리/BMS, 스톨·회생, DC-DC 연속 출력, 전선·커넥터, 퓨즈 차단용량/시간곡선, 접촉기 DC 정격, 별도 브레이크를 검토합니다. 24v19 포함 단자대는 25A 분기에 그대로 승인하지 않습니다. [S02, S11]')
pg('부품 목록 · 조건부 항목','부품 위치별 46개 항목. 배터리 전압과 전류가 흐르는 하네스를 브레드보드에 연결하지 않습니다.',body)
# EDA and references compact and clear.
body='<div class="cols"><div><h2>EasyEDA Pro 가져오기 [S08, S09]</h2><p class="lead">File → Import → EasyEDA(Standard)</p><p>SmartCart-B1-Modules.json 또는 이 JSON만 들어 있는 Smart-Cart-B1-EDA.zip을 선택합니다. Pro 자체 파일 가져오기나 Gerber 업로드가 아닙니다.</p><p>44개 모듈 심볼 / 194개 전기 핀 / 63개 네트를 포함합니다. 심볼의 핀 번호 1..N은 문서 인덱스이며, 실제 핀은 단자명에 적힌 J2/J3 및 제품 핀 표를 따릅니다. NC_U2_8 / NC_U2_11은 개별 미사용 출력입니다.</p><p>웹/PDF의 사실적 외형은 SVG 표현입니다. EasyEDA에는 대응하는 모듈형 전기 심볼을 가져오며 텍스처나 브레드보드 사진 배치가 자동 변환되지는 않습니다. 풋프린트·PCB·Gerber는 없습니다.</p>'
body+=box('검증 범위','정적 JSON/SVG/네트리스트 재해석 및 브라우저 렌더링을 검사했습니다. EasyEDA Pro 실제 가져오기, KiCad 네이티브 ERC, 제조사 검토, 실물 조립·통전·주행·고장 시험은 미실행입니다. 변환 후 반드시 단자 CSV와 대조합니다.')
body+=box('정지·조향','S1 NC와 S2 NO / K1 보조접점은 기능상 수동 재무장 회로입니다. 단일 고장 안전 인증이나 기계적 제동이 아닙니다. 두 서보는 별도 조향 링크·끝점·PWM 전압 검증 후 활성화합니다. 기존 저장소는 차동 구동·자유 캐스터 뷰어입니다.')
body+=box('키캣 보조 원본 [S10]','eda/kicad에 legacy .sch/.lib/.pro 및 cache를 포함했습니다. 최신 KiCad에서 변환/검증 후 사용하고, EasyEDA로 넘길 때는 KiCad 프로젝트 아카이브를 사용하는 경로를 확인합니다. 네이티브 열기 시험을 수행했다고 주장하지 않습니다.')+'</div><div><h2>기본 자료 / Primary sources</h2>'
for sid,title,url in SOURCES:body+=f'<div class="source"><b>{E(sid)} · {E(title)}</b><a href="{E(url)}">{E(url)}</a></div>'
body+='</div></div>'
pg('EDA 편집 · 검증 범위 · 참조 자료','공식 자료와 실제 구매 부품의 모델/리비전을 함께 확인해야 합니다. 자료 검토일 2026-09-13.',body)
css='''@page{size:A3 landscape;margin:8mm}*{box-sizing:border-box}body{margin:0;font-family:"Noto Sans CJK KR","Malgun Gothic",Arial,sans-serif;color:#244656;-webkit-print-color-adjust:exact;print-color-adjust:exact}.page{width:404mm;height:281mm;position:relative;break-after:page;overflow:hidden;background:#fff}.page:last-child{break-after:auto}.drawing svg{display:block;width:100%;height:100%}.appendix{padding:7mm 8mm 9mm}header{height:30mm;border-bottom:.25mm solid #bacbd3;margin-bottom:5mm}.eyebrow{font-size:9pt;font-weight:700;color:#528291}.eyebrow span{float:right}h1{font-size:24pt;font-weight:750;line-height:1.2;margin:3mm 0 2mm}header p{font-size:10pt;margin:0;color:#64818e}.cols{display:grid;grid-template-columns:1fr 1fr;gap:8mm}h2{font-size:12pt;margin:1mm 0 2mm;color:#235d6e}p{font-size:10pt;line-height:1.55;margin:2mm 0 4mm}.lead{font-size:14pt;font-weight:700;color:#16828d}.box{padding:3mm 4mm;border:.2mm solid #d3dfdf;background:#f3f7f7;border-radius:1.3mm;margin-top:4mm}.box p{font-size:9.5pt;margin:0;line-height:1.6}.box h2{font-size:10.5pt;margin:0 0 1mm}table{width:100%;border-collapse:collapse;table-layout:auto;font-size:9pt;line-height:1.3}th{text-align:left;background:#e8f0f3;color:#3c6474;padding:1.4mm 1.7mm;font-size:8.5pt}td{border-bottom:.15mm solid #dce5e9;padding:1.3mm 1.7mm;vertical-align:top}tr:nth-child(even)td{background:#f8fafb}.compact{font-size:8.8pt;line-height:1.15}.compact th{padding:1.3mm 1.1mm}.compact td{padding:.15mm 1.1mm;white-space:nowrap}.mono td:last-child{font-family:Arial,sans-serif;font-size:8.4pt}.bom{font-size:8.6pt}.bom td{padding:1.35mm 1.5mm}.bom th{white-space:nowrap}.source{margin-bottom:3mm;font-size:9pt;line-height:1.3}.source b{display:block;color:#2e5666;font-size:9pt;margin-bottom:1mm}.source a{display:block;color:#5a7684;font-size:8pt;overflow-wrap:anywhere;text-decoration:none}footer{position:absolute;bottom:4mm;left:8mm;right:8mm;border-top:.2mm solid #c2d0d8;padding-top:2mm;color:#77909b;font-size:8pt}footer span{float:right}'''
(ROOT/'docs/print.html').write_text('<!doctype html><html lang="ko"><meta charset="utf-8"><title>Smart Cart Wiring B1 | A3 Drawings</title><style>'+css+'</style><body>'+''.join(pages)+'</body></html>')
print('Print pages:',len(pages),'components',len(C))
