# EasyEDA Pro / KiCad 가져오기

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
