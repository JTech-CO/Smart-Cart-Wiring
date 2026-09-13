"""Canonical harness model. All exports are derived from these terminal/net assignments.
This is a module-level design, not a PCB or a safety certification.
"""
from pathlib import Path
import json,csv
ROOT=Path(__file__).resolve().parents[1]
C=[]
def add(ref,name,kind,pins,notes='',spec='',status='reference',page='power'):
    C.append(dict(ref=ref,name=name,kind=kind,pins=[dict(number=str(i+1),name=p,net=n) for i,(p,n) in enumerate(pins)],notes=notes,spec=spec,status=status,page=page))
def two(ref,name,kind,n1,n2,spec='',notes='',status='candidate',page='power'):
    add(ref,name,kind,[('1',n1),('2',n2)],notes,spec,status,page)
add('BT1','LiFePO4 배터리','battery',[('+','BAT_POS'),('-','GND')], '기존 도면의 24V 108Ah를 유지. 실제 모델·BMS 정격 미확정. 8S라면 공칭 25.6V, 충전 상한은 제조사 확인.','24V class / 108Ah','candidate')
two('F0','메인 퓨즈','fuse','BAT_POS','BAT_FUSED','60A *','배터리 + 가까이 설치. 60A는 검토값. DC 전압·차단용량·전선 보호 협조 확정 전 통전 금지.')
two('S0','메인 차단 스위치','switch','BAT_FUSED','BUS24','DC disconnect','전류 정격과 DC 부하 차단 능력 확인. 배터리 -는 외부 공통 0V 버스로 연결.')
add('X24','배터리 전원 분배','bus',[('IN','BUS24'),('K1','BUS24'),('F3','BUS24'),('F4','BUS24')],'절연 커버가 있는 양극 전용 버스. 음극 버스와 물리적으로 분리.','24V class','candidate')
add('X0','공통 0V 분배','groundbus',[(str(i),'GND') for i in range(1,13)],'비절연 DC-DC 기준. 모터·서보 귀환은 이 버스로 직접 연결. 브레드보드를 대전류 귀환 경로로 사용하지 않음.','0V / star return','candidate')
add('K1','구동 전원 접촉기','contactor',[('L1','BUS24'),('T1','DRIVE24'),('A1','COIL12'),('A2','GND'),('13','LATCH_IN'),('14','COIL12')], '12V 코일과 별도 NO 보조접점이 필요. DC 주접점 정격은 최종 선정. E-stop은 구동전원 차단이며 제동 보장은 아님.','12V coil / DC main contacts','candidate')
two('F1','좌측 모터 입력 퓨즈','fuse','DRIVE24','ML_VIN','25A *')
two('F2','우측 모터 입력 퓨즈','fuse','DRIVE24','MR_VIN','25A *')
for s in ['L','R']:
 add('MD'+s,('좌측' if s=='L' else '우측')+' 모터 드라이버','driver',[('VIN',f'M{s}_VIN'),('GND','GND'),('OUTA',f'M{s}_A'),('OUTB',f'M{s}_B'),('RX',f'M{s}_RX'),('TX',f'M{s}_TX')], 'Pololu G2 SMC 24v19를 조건부 기준으로 사용. 정상 권장 상한 34V. 19A 연속값은 조건부이며 스톨·열·회생은 별도 검증. 포함 단자대는 제조사 15~16A 안내가 있어 25A 보호분기에는 그대로 승인하지 않음. UART timeout, safe-start 설정 필요.','SMC G2 24v19 / UART','conditional')
 add('M'+s,('좌측' if s=='L' else '우측')+' 감속모터','motor',[('A',f'M{s}_A'),('B',f'M{s}_B')], '24V 250W 브러시드 DC 감속모터 가정. 극성은 바퀴를 띄운 상태에서 확인. 스톨 전류 미확정.','24V / 250W','candidate')
two('F3','12V 컨버터 입력 퓨즈','fuse','BUS24','DC12_IN','15A *')
two('F4','5V 컨버터 입력 퓨즈','fuse','BUS24','DC5_IN','5A *')
add('DC1','조향 전원 컨버터','converter',[('IN+','DC12_IN'),('IN-','GND'),('OUT+','P12'),('OUT-','GND')], '입력은 배터리 완충 및 과도전압을 허용해야 함. 12V 20A 연속 출력, 방열 및 동시 서보 스톨 확인. 비절연형 기준.','24V class → 12V / 20A','candidate')
add('DC2','제어 전원 컨버터','converter',[('IN+','DC5_IN'),('IN-','GND'),('OUT+','P5'),('OUT-','GND')], '입력 범위·출력 과전압 보호·연속 출력 사양 확인. 5V는 부하 단자에서 측정. 비절연형 기준.','24V class → 5V / 10A','candidate')
for s,f in [('L','F5'),('R','F6')]:
 two(f,('좌측' if s=='L' else '우측')+' 서보 퓨즈','fuse','P12',f'SV{s}_PWR','10A *')
 add('SV'+s,('좌측' if s=='L' else '우측')+' 조향 서보','servo',[('V+',f'SV{s}_PWR'),('GND','GND'),('PWM',f'SERVO_{s}')], 'RDS51150 12V형 조건부. 실제 선 색·순서·피드백 선 유무·5V PWM 허용 여부 확인. 기존 저장소는 자유 캐스터 차동 구동이므로 조향 링크를 확정하기 전 장착 구동 금지.','RDS51150 / 12V','conditional')
two('F7','Orange Pi 출력 퓨즈','fuse','P5','OPI5','4A *')
two('F8','USB 허브 출력 퓨즈','fuse','P5','HUB5','4A *')
two('F9','접촉기 코일 퓨즈','fuse','P12','COIL_FUSED','1A *')
two('F10','브레드보드 5V 분기','fuse','P5','LOGIC5','0.5A *','5V는 AHCT 버퍼에만 공급. 서보·SBC 전원은 브레드보드를 통과하지 않음.')
two('S1','비상정지 버튼','estop','COIL_FUSED','LATCH_IN','NC / twist reset','래칭 NC 접점. 해제만으로 재출발하지 않으며 S2를 다시 눌러야 접촉기가 유지됨.')
two('S2','수동 재무장 버튼','start','LATCH_IN','COIL12','momentary NO','K1 NO 보조접점 13-14와 병렬. 이것은 단일 채널 기능 회로이며 인증된 안전 회로가 아님.')
two('Z1','코일 서지 억제 모듈','suppressor','COIL12','GND','K1 지정품','코일 전압·클램프·접촉기 해제시간에 맞는 제조사 지정 억제기. 임의 플라이백 다이오드로 대체 금지.')
add('OP1','Orange Pi 4 Pro','opi',[('PWR+','OPI5'),('PWR-GND','GND'),('HOST_VBUS','HOST5'),('HOST_D-','HOST_DM'),('HOST_D+','HOST_DP'),('HOST_GND','GND')], '전원용 Type-C 5V 입력 사용. 호스트 USB는 외부 전원 허브의 upstream에 연결. 보드의 USB 포트 전류 한도로 전체 센서를 급전하지 않음.','5V Type-C / high-level control','reference','signal')
hp=[('DC+','HUB5'),('DC-','GND'),('UP_VBUS_SENSE','HOST5'),('UP_D-','HOST_DM'),('UP_D+','HOST_DP'),('UP_GND','GND')]
for i,dev in enumerate(['ESP','LIDAR','UWBL','UWBR'],1):
 hp.extend([(f'P{i}_VBUS',f'USB_{dev}_5'),(f'P{i}_D-',f'USB_{dev}_DM'),(f'P{i}_D+',f'USB_{dev}_DP'),(f'P{i}_GND','GND')])
add('H1','외부 전원 USB 허브','hub',hp,'5V 외부 입력, 포트별 전류 제한, upstream VBUS 역급전 방지 제품 필요. USB 케이블은 완성품 사용. USB D±를 브레드보드에 배선하지 않음.','4 downstream / powered USB','candidate','signal')
epins=[('USB_VBUS','USB_ESP_5'),('USB_D-','USB_ESP_DM'),('USB_D+','USB_ESP_DP'),('USB_GND','GND'),('J2.1 / 3V3','P3V3'),('J2.14 / GND','GND'),('J3.11 / IO17','ESP_L_TX'),('J3.12 / IO16','ML_TX'),('J2.9 / IO25','ESP_R_TX'),('J2.10 / IO26','MR_TX'),('J3.9 / IO18','IMU_SCK'),('J3.2 / IO23','IMU_MOSI'),('J3.8 / IO19','IMU_MISO'),('J2.11 / IO27','IMU_CS'),('J2.5 / IO34','IMU_INT'),('J2.7 / IO32','IMU_RST'),('J3.6 / IO21','TOF_SDA'),('J3.3 / IO22','TOF_SCL'),('J2.15 / IO13','PWM_L_3V3'),('J2.12 / IO14','PWM_R_3V3')]
add('U1','ESP32-DevKitC V4','esp32',epins,'ESP32-WROOM-32E 기준. USB만 급전하고 5V 헤더는 미연결. GPIO16/17은 WROVER에 재사용 불가. 외부 보드로 배치하여 브레드보드 접점을 가리지 않음.','WROOM-32E / USB power only','reference','signal')
ad=[('USB_VBUS','USB_LIDAR_5'),('USB_D-','USB_LIDAR_DM'),('USB_D+','USB_LIDAR_DP'),('USB_GND','GND'),('5V_OUT','USB_LIDAR_5'),('GND_OUT','GND'),('TX_3V3','LIDAR_RX'),('RX_3V3','LIDAR_TX')]
add('A1','LiDAR USB 어댑터','adapter',ad,'C1용 정품 USB-UART 어댑터와 지정 케이블 사용. TX는 센서 RX, RX는 센서 TX로 교차.','SLAMTEC C1 adapter','reference','signal')
add('LD1','2D LiDAR','lidar',[('5V','USB_LIDAR_5'),('GND','GND'),('TX','LIDAR_TX'),('RX','LIDAR_RX')],'RPLIDAR C1. 5V 전원과 3.3V UART를 구분. 센서 입력 4.8~5.2V 범위 검증.','SLAMTEC RPLIDAR C1','reference','signal')
for s in ['L','R']:
 add('UW'+s,('좌측' if s=='L' else '우측')+' UWB 베이스','uwb',[('USB_VBUS',f'USB_UWB{s}_5'),('USB_D-',f'USB_UWB{s}_DM'),('USB_D+',f'USB_UWB{s}_DP'),('USB_GND','GND')], 'BU04-Kit의 USB(거리 데이터) Type-C 포트 사용. TTL/AT 포트와 혼동하지 않음. bare BU04 및 별도 Follow Package는 동일 핀맵으로 간주하지 않음. 2베이스+1태그 동시 측정 펌웨어는 별도 설정.','Ai-Thinker BU04-Kit','reference','signal')
add('TAG1','사용자 휴대 태그','tag',[], '독립 배터리로 동작. 카트 배터리와 유선 연결하지 않음. 베이스와 태그의 역할 및 ID는 펌웨어에서 설정.','UWB tag / independent power','conditional','signal')
add('IMU1','관성 센서','imu',[('VIN','P3V3'),('GND','GND'),('SCL / SCK','IMU_SCK'),('DI / MOSI','IMU_MOSI'),('SDA / MISO','IMU_MISO'),('CS','IMU_CS'),('INT','IMU_INT'),('RST','IMU_RST'),('P0','P3V3'),('P1','P3V3')], 'Adafruit BNO085 #4754 기준. P0/P1 모두 HIGH로 SPI 설정. 3Vo는 출력이므로 외부 전원과 병렬 연결하지 않음. INT/RST 포함.','BNO085 / SPI','reference','signal')
add('TOF1','근거리 거리 센서','tof',[('VIN','P3V3'),('GND','GND'),('SDA','TOF_SDA'),('SCL','TOF_SCL')], 'Pololu VL53L1X carrier #3415 기준. XSHUT, GPIO1, VDD는 미연결. 보드의 I2C 풀업 사용. XSHUT을 추가할 때는 2.8V 측 제약 확인.','VL53L1X / I2C 0x29','reference','signal')
for ref,n1,n2,val in [('R1','ESP_L_TX','ML_RX','1kΩ'),('R2','ESP_R_TX','MR_RX','1kΩ'),('R3','PWM_L_5V','SERVO_L','220Ω'),('R4','PWM_R_5V','SERVO_R','220Ω'),('R5','PWM_L_3V3','GND','10kΩ'),('R6','PWM_R_3V3','GND','10kΩ')]:
 two(ref,ref+' '+val,'resistor',n1,n2,val+' / 0.25W','', 'reference','breadboard')
up=[('1 / 1OE','GND'),('2 / 1A','PWM_L_3V3'),('3 / 1Y','PWM_L_5V'),('4 / 2OE','GND'),('5 / 2A','PWM_R_3V3'),('6 / 2Y','PWM_R_5V'),('7 / GND','GND'),('8 / 3Y','NC_U2_8'),('9 / 3A','GND'),('10 / 3OE','LOGIC5'),('11 / 4Y','NC_U2_11'),('12 / 4A','GND'),('13 / 4OE','LOGIC5'),('14 / VCC','LOGIC5')]
add('U2','서보 PWM 레벨 버퍼','buffer',up,'SN74AHCT125N DIP-14. 5V 전원, 3.3V TTL 입력. 미사용 출력 8/11번은 NC, 미사용 입력은 GND, 해당 OE는 5V. 핀1 표시 방향 확인.','SN74AHCT125N / DIP-14','reference','breadboard')
two('C1','버퍼 디커플링','capacitor','LOGIC5','GND','100nF / ≥16V','U2 14-7번 전원 가까이.','reference','breadboard')
add('BB1','400 tie-point 브레드보드','breadboard',[],'300개 본체 접점(30열 × 10행)과 100개 전원 레일 접점(25개 × 4줄). 레일은 각 줄 왼쪽부터 별도로 1~25번. a-e / f-j는 독립 5접점 스트립. 상부 +레일은 3.3V, 하부 +레일은 5V. 두 -레일만 공통. 모든 레일은 실물 도통 확인. 센서·로직 실험용이며 주행 차량에는 납땜/잠금 커넥터로 이전.','3.3V sensors + 5V buffer ONLY','reference','breadboard')
# Breadboard physical locations. Each numbered a-e / f-j strip is one node.
BP={}
def put(h,net,owner):
 if h in BP: raise ValueError(f'contact collision {h}')
 BP[h]={'net':net,'owner':owner}
# IC occupies e3-e9 and f9-f3; do not mirror DIP-14 numbering.
for pin in range(1,15):
 h='e'+str(pin+2) if pin<=7 else 'f'+str(17-pin)
 put(h,up[pin-1][1],f'U2.{pin}')
for h,net,owner in [('a13','ESP_L_TX','U1.IO17'),('a14','ML_TX','U1.IO16'),('a15','ESP_R_TX','U1.IO25'),('a16','MR_TX','U1.IO26'),('c14','ML_TX','MDL.TX'),('c16','MR_TX','MDR.TX'),('j13','ML_RX','MDL.RX'),('j15','MR_RX','MDR.RX'),('a4','PWM_L_3V3','U1.IO13'),('a7','PWM_R_3V3','U1.IO14'),('c11','SERVO_L','SVL.PWM'),('c12','SERVO_R','SVR.PWM')]: put(h,net,owner)
placements={
'R1':('e13','f13'),'R2':('e15','f15'),
'R3':('d5','d11'),'R4':('b8','b12'),
'R5':('b4','T-4'),'R6':('b7','T-7'),
'C1':('j3','B-3')}
byref={c['ref']:c for c in C}
for ref,hs in placements.items():
 for i,h in enumerate(hs): put(h,byref[ref]['pins'][i]['net'],f'{ref}.{i+1}')
signalrows=[(20,'IMU_SCK','IO18','SCL'),(21,'IMU_MOSI','IO23','DI'),(22,'IMU_MISO','IO19','SDA'),(23,'IMU_CS','IO27','CS'),(24,'IMU_INT','IO34','INT'),(25,'IMU_RST','IO32','RST'),(27,'TOF_SDA','IO21','SDA'),(28,'TOF_SCL','IO22','SCL')]
for col,net,gpio,sensorpin in signalrows:
 put(f'a{col}',net,'U1.'+gpio)
 put(f'c{col}',net,('IMU1.' if col<26 else 'TOF1.')+sensorpin)
for h,net,owner in [('T+1','P3V3','U1.3V3'),('T-1','GND','U1.GND'),('B+1','LOGIC5','F10.OUT'),('B-1','GND','X0'),('T+20','P3V3','IMU1.VIN'),('T-20','GND','IMU1.GND'),('T+21','P3V3','IMU1.P0'),('T+22','P3V3','IMU1.P1'),('T+23','P3V3','TOF1.VIN'),('T-23','GND','TOF1.GND')]: put(h,net,owner)
# Supply jumpers use free contacts on the same electrical strip as each IC pin.
jumpers=[('b3','T-3'),('b6','T-6'),('b9','T-9'),('h3','B+3'),('h4','B+4'),('h5','B-5'),('h7','B+7'),('h8','B-8'),('T-25','B-25')]
for k,(a,b) in enumerate(jumpers,1):
 n='LOGIC5' if b.startswith('B+') else 'GND'
 put(a,n,f'JMP{k}.1');put(b,n,f'JMP{k}.2')
SOURCES=[
('S01','Smart-Cart repository / 2b4b8fea6909e4f76b4a52b02c5075c3f478097b','https://github.com/JTech-CO/Smart-Cart/tree/2b4b8fea6909e4f76b4a52b02c5075c3f478097b'),
('S02','Pololu G2 SMC user guide','https://www.pololu.com/docs/0J77/all'),
('S03','ESP32-DevKitC V4 power and J2/J3 pin tables','https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html'),
('S04','Adafruit BNO085 pinouts and SPI mode','https://learn.adafruit.com/adafruit-9-dof-orientation-imu-fusion-breakout-bno085/pinouts'),
('S05','Pololu VL53L1X carrier #3415','https://www.pololu.com/product/3415'),
('S06','Ai-Thinker BU04-Kit specification v1.1.0, p9 USB port','https://en.ai-thinker.com/Uploads/file/20241018/20241018150326_27432.pdf'),
('S07','TI SN74AHCT125 datasheet','https://www.ti.com/lit/ds/symlink/sn74ahct125.pdf'),
('S08','EasyEDA Standard document format','https://docs.easyeda.com/en/DocumentFormat/EasyEDA-Format-Standard/index.html'),
('S09','EasyEDA Pro import EasyEDA Standard JSON / ZIP','https://prodocs.easyeda.com/en/import-export/import-easyeda/'),
('S10','EasyEDA Pro KiCad 5.1 import','https://prodocs.easyeda.com/en/import-export/import-kicad/'),
('S11','Infineon BTS7960 operating voltage','https://www.infineon.com/dgdl/BTS7960_Datasheet.pdf'),
('S12','SLAMTEC C1 datasheet','https://d229kd5ey79jzj.cloudfront.net/3157/SLAMTEC_rplidar_datasheet_C1_v1.0_en.pdf')]
MODEL={'name':'Smart Cart Wiring Studio','revision':'B1','date':'2026-09-13','repo_commit':'2b4b8fea6909e4f76b4a52b02c5075c3f478097b','components':C,'breadboard':{'contacts':BP,'placements':placements,'jumpers':jumpers,'signalrows':signalrows},'sources':[dict(id=a,title=b,url=c) for a,b,c in SOURCES]}
def write():
 (ROOT/'data/design.json').write_text(json.dumps(MODEL,ensure_ascii=False,indent=2))
 with (ROOT/'data/terminal-netlist.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Reference','Device','SymbolPin','PhysicalTerminal','Net'])
  for c in C:
   for p in c['pins']:w.writerow([c['ref'],c['name'],p['number'],p['name'],p['net']])
 with (ROOT/'data/breadboard-contacts.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Hole','Net','ConnectedLead'])
  for h,d in BP.items():w.writerow([h,d['net'],d['owner']])
 with (ROOT/'data/BOM.csv').open('w',newline='',encoding='utf-8-sig') as f:
  w=csv.writer(f);w.writerow(['Reference','Description','Specification','Status','Notes'])
  for c in C:w.writerow([c['ref'],c['name'],c['spec'],c['status'],c['notes']])
if __name__=='__main__': write()
