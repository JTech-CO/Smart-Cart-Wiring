"""Deterministic, textured SVG harness drawings. No raster text, no external assets."""
from pathlib import Path
import json, math, html
from design import ROOT,MODEL,C,BP,placements,jumpers,byref,signalrows
E=lambda x:html.escape(str(x),quote=True)
COL={'24':'#da4439','12':'#df8a18','5':'#ba397c','3':'#7d50b7','gnd':'#273443','sig':'#168b83','usb':'#3374b8','pwm':'#738622'}
def netcolor(n):
 if n=='GND':return COL['gnd']
 if n=='P3V3':return COL['3']
 if n in ['P12','COIL12','COIL_FUSED','LATCH_IN'] or n.endswith('_PWR'):return COL['12']
 if n in ['P5','OPI5','HUB5','LOGIC5'] or n.endswith('_5'):return COL['5']
 if n.startswith(('BAT','BUS24','DRIVE24','DC12_IN','DC5_IN')) or n.endswith('_VIN'):return COL['24']
 if 'PWM' in n or 'SERVO' in n:return COL['pwm']
 return COL['sig']
DEFS='''<defs>
<linearGradient id="metal" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#f4f6f5"/><stop offset=".19" stop-color="#b3bdc2"/><stop offset=".45" stop-color="#e7ecee"/><stop offset=".7" stop-color="#7e8b94"/><stop offset="1" stop-color="#cad1d4"/></linearGradient>
<linearGradient id="dark" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#3b464e"/><stop offset=".38" stop-color="#202a31"/><stop offset="1" stop-color="#10191f"/></linearGradient>
<linearGradient id="fin" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#7e8992"/><stop offset=".2" stop-color="#303b44"/><stop offset=".7" stop-color="#121c24"/><stop offset="1" stop-color="#65727c"/></linearGradient>
<linearGradient id="pcb" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#257664"/><stop offset="1" stop-color="#104a40"/></linearGradient>
<linearGradient id="bluepcb" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#296c97"/><stop offset="1" stop-color="#123c60"/></linearGradient>
<linearGradient id="gold" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f5dc8b"/><stop offset=".5" stop-color="#af883e"/><stop offset="1" stop-color="#e8bf64"/></linearGradient>
<linearGradient id="plastic" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset="1" stop-color="#dfe4e4"/></linearGradient>
<linearGradient id="glass" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#f9fcfc" stop-opacity=".82"/><stop offset=".5" stop-color="#d6e7eb" stop-opacity=".25"/><stop offset="1" stop-color="#91a8b1" stop-opacity=".7"/></linearGradient>
<radialGradient id="redbutton" cx=".32" cy=".26"><stop stop-color="#ff7970"/><stop offset=".52" stop-color="#dc302c"/><stop offset="1" stop-color="#8d191e"/></radialGradient>
<radialGradient id="lens" cx=".4" cy=".35"><stop stop-color="#586f79"/><stop offset=".3" stop-color="#202e38"/><stop offset="1" stop-color="#0a1015"/></radialGradient>
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".8" fill="#c9d1d7"/></pattern>
<pattern id="brushed" width="8" height="8" patternUnits="userSpaceOnUse"><path d="M0 1H8M0 4H8M0 6H8" stroke="#fff" stroke-width=".6" opacity=".12"/></pattern>
<pattern id="rubber" width="7" height="7" patternUnits="userSpaceOnUse"><path d="M0 0L7 7M-3 4L3 10" stroke="#73808a" stroke-width=".5" opacity=".25"/></pattern>
<filter id="shadow" x="-25%" y="-25%" width="150%" height="165%"><feGaussianBlur in="SourceAlpha" stdDeviation="4"/><feOffset dx="1" dy="5"/><feComponentTransfer><feFuncA type="linear" slope="0.19"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="tinyshadow" x="-20%" y="-30%" width="140%" height="170%"><feGaussianBlur in="SourceAlpha" stdDeviation="1.4"/><feOffset dx="0" dy="2"/><feComponentTransfer><feFuncA type="linear" slope="0.24"/></feComponentTransfer><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>'''
def text(x,y,s,size=17,fill='#263747',weight=400,anchor='start',extra=''):
 return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}" {extra}>{E(s)}</text>'
def rect(x,y,w,h,fill,stroke='none',r=0,extra=''):
 return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" {extra}/>'
def screw(x,y,r=5):
 return f'<circle cx="{x}" cy="{y}" r="{r+1}" fill="#303d46"/><circle cx="{x}" cy="{y}" r="{r}" fill="url(#metal)"/><path d="M{x-r*.65} {y}h{r*1.3}M{x} {y-r*.65}v{r*1.3}" stroke="#52616b" stroke-width="1.2"/>'
def chip(x,y,w,h,label=''):
 s=''
 for k in range(3,int(w)-2,8):
  s+=rect(x+k,y-4,3,5,'#b9c4c7')+rect(x+k,y+h-1,3,5,'#b9c4c7')
 for k in range(4,int(h)-2,8):s+=rect(x-4,y+k,5,3,'#b9c4c7')+rect(x+w-1,y+k,5,3,'#b9c4c7')
 s+=rect(x,y,w,h,'url(#dark)','#172830',2)+rect(x+1,y+1,w-2,h-2,'url(#rubber)',r=2)
 if label:s+=text(x+w/2,y+h/2+3,label,7,'#b5c0c3',500,'middle')
 return s

def art(kind,label='',ref=''):
 """All art uses a 300x190 coordinate system; normalized silhouettes, not CAD dimensions."""
 s=''
 if kind=='battery':
  s+=rect(14,34,272,142,'url(#dark)','#0b1821',11)+rect(14,34,272,142,'url(#rubber)',r=11)
  s+=f'<path d="M14 34L38 12H267L286 34Z" fill="#45515a" stroke="#263743"/>'
  for i in range(5):s+=rect(75,18+i*2.5,150,1,'#6b777f',r=1)
  s+=rect(44,65,214,77,'#e8eced',r=3)+rect(44,65,214,22,'#172c38',r=3)
  s+=text(57,81,'LiFePO4  /  BATTERY',13,'#f3f7f8',700)+text(57,118,'24V  108Ah',27,'#183d4d',750)+text(57,134,'BMS • FUSED OUTPUT',9,'#6c7d84',500)
  for x,c in [(51,'#db493d'),(249,'#172a36')]:
   s+=f'<ellipse cx="{x}" cy="30" rx="18" ry="8" fill="{c}"/>'+rect(x-9,10,18,20,'url(#gold)',r=3)+screw(x,13,7)
  s+=text(52,55,'+',18,'#e35044',800,'middle')+text(249,55,'−',18,'#b0bcc3',800,'middle')
 elif kind=='fuse':
  s+=rect(9,52,282,84,'#37444c',r=10)+rect(12,46,276,80,'url(#glass)','#93a4af',10)
  s+=rect(35,80,230,25,'url(#gold)','#92733b',3)
  s+=rect(105,64,90,51,'#29343b','#c3ccd0',4)+text(150,98,label or 'FUSE',26,'#fff',800,'middle')
  for x in [49,251]:s+=screw(x,93,15)
  s+=f'<path d="M28 57H271" stroke="#fff" opacity=".85" stroke-width="3"/>'
 elif kind in ['switch','estop','start']:
  s+=rect(51,10,198,170,'#28353f','#111f27',12)+rect(60,19,180,150,'url(#rubber)',r=8)
  for x in [69,231]:
   for y in [28,155]:s+=screw(x,y,6)
  if kind=='switch':
   s+=f'<circle cx="150" cy="95" r="60" fill="url(#redbutton)" stroke="#8e3028" stroke-width="3"/>'
   s+=rect(113,54,74,83,'#f75c46','#c83529',10)+text(150,45,'ON',10,'#fff',700,'middle')+text(220,113,'OFF',10,'#fff',700,'middle')
  else:
   s+=f'<circle cx="150" cy="95" r="61" fill="#eac42b"/>'
   s+=f'<circle cx="150" cy="94" r="47" fill="'+('url(#redbutton)' if kind=='estop' else '#1f9a73')+'" stroke="#183a36" stroke-width="2"/>'
   s+=text(150,101,'STOP' if kind=='estop' else 'START',18,'#fff',750,'middle')
 elif kind in ['bus','groundbus']:
  s+=rect(4,53,292,79,'url(#dark)',r=9)+rect(14,61,272,51,'url(#gold)' if kind=='bus' else 'url(#metal)',r=4)
  for x in [33,80,126,172,219,266]:s+=screw(x,86,12)
  s+=text(150,151,'POSITIVE BUS' if kind=='bus' else 'COMMON 0V BUS',14,'#5d6d76',700,'middle')
 elif kind=='converter':
  s+=rect(17,22,266,145,'#253440','#101f2d',5)
  s+=rect(18,22,264,145,'url(#brushed)',r=5)
  for i in range(17):s+=rect(24+i*15,20,10,149,'url(#fin)','#162530',2)
  s+=rect(70,62,160,57,'#15212a','#71808b',3)+text(150,81,'DC / DC',13,'#e0e9ef',700,'middle')+text(150,107,label,20,'#f1f5f7',800,'middle')
  for x in [29,271]:
   for y in [33,154]:s+=screw(x,y,5)
  s+=rect(31,172,79,14,'#298777',r=2)+rect(188,172,79,14,'#298777',r=2)
  for x in [49,91,207,249]:s+=screw(x,178,4)
 elif kind in ['driver','opi','imu','tof','uwb','adapter','esp32','buffer']:
  if kind=='buffer':
   for i in range(7):s+=rect(25+i*36,24,13,32,'url(#metal)')+rect(25+i*36,135,13,32,'url(#metal)')
   s+=rect(17,46,266,98,'url(#dark)','#051922',8)+f'<path d="M17 80Q43 94 17 108" fill="#101820" stroke="#52616c"/>'
   s+=text(156,100,'SN74AHCT125N',20,'#b7c3c9',700,'middle')+f'<circle cx="33" cy="63" r="5" fill="#61717d"/>'
   return s
  pcbfill='url(#bluepcb)' if kind=='opi' else 'url(#pcb)'
  if kind in ['esp32','uwb']:pcbfill='#18282b'
  s+=rect(12,12,276,166,pcbfill,'#164c47',7)
  for x,y in [(23,23),(277,23),(23,167),(277,167)]:
   s+=f'<circle cx="{x}" cy="{y}" r="7" fill="url(#gold)"/><circle cx="{x}" cy="{y}" r="3.5" fill="#eff3f5"/>'
  for i in range(13):
   x=36+(i*29)%227;y=34+(i*23)%109
   s+=f'<path d="M{x} {y}h15l6 6v18h14" fill="none" stroke="#68b799" stroke-width="1" opacity=".37"/>'
   s+=rect(x+2,y+6,5,9,'#ceb477','#7a8e8d',1)+rect(x+1,y+6,7,2,'#c3d1cd')
  if kind=='opi':
   s+=chip(106,68,59,59,'A733')+chip(178,72,31,48,'RAM')
   for y in [38,87]:s+=rect(241,y,51,41,'url(#metal)','#5c788b',3)+rect(251,y+9,42,17,'#21384e')
   s+=rect(38,124,55,46,'url(#metal)','#798893',3)+rect(43,132,45,27,'#263640')
   s+=rect(52,5,39,28,'url(#metal)','#688291',4)+rect(59,6,25,10,'#233d4d',r=4)
   for i in range(20):
    for j in [0,1]:s+=rect(48+i*8,25+j*9,5,5,'url(#gold)','#9f783a')
   s+=text(108,160,'Orange Pi 4 Pro',10,'#e8f4fa',700)
  elif kind=='esp32':
   s+=rect(104,23,99,99,'url(#metal)','#839d9d',3)+rect(104,23,99,99,'url(#brushed)',r=3)
   s+=text(154,64,'ESPRESSIF',12,'#364e59',700,'middle')+text(154,84,'WROOM-32E',12,'#364e59',700,'middle')
   s+=chip(73,126,30,30,'USB')+rect(129,153,48,34,'url(#metal)','#71838d',3)+rect(137,174,32,12,'#162832',r=3)
   for i in range(19):
    for x in [37,258]:s+=rect(x,27+i*7.3,6,5,'url(#gold)')
   s+=rect(58,139,10,14,'#a6b3b4',r=2)+rect(222,139,10,14,'#a6b3b4',r=2)
  elif kind=='uwb':
   s+=rect(77,34,148,55,'url(#metal)','#8e9c9e',3)+text(151,58,'BU04',21,'#566d71',750,'middle')+text(151,78,'Ai-Thinker',10,'#5a737a',500,'middle')
   s+=chip(123,112,53,45,'STM32')
   for x in [82,218]:s+=f'<circle cx="{x}" cy="22" r="8" fill="url(#gold)"/><circle cx="{x}" cy="22" r="3" fill="#202f34"/>'
   for x,t in [(72,'USB'),(201,'TTL')]:s+=rect(x,157,35,27,'url(#metal)','#829da2',3)+text(x+17,149,t,8,'#d4e0df',700,'middle')
   for i in range(15):
    for x in [39,256]:s+=rect(x,43+i*7.5,5,4,'url(#gold)')
  elif kind=='imu':
   s+=chip(110,57,74,69,'BNO085')
   for i,t in enumerate(['VIN','GND','SCL','SDA','DI','CS','INT','RST']):
    x=41+i*29;s+=f'<circle cx="{x}" cy="150" r="6" fill="url(#gold)"/><circle cx="{x}" cy="150" r="2.6" fill="#162a2a"/>'+text(x,137,t,7,'#e5f0eb',500,'middle')
   s+=text(154,33,'9-DOF  /  SPI',13,'#dceee6',700,'middle')
  elif kind=='tof':
   s+=rect(100,49,96,72,'#142334','#57717c',5)+rect(108,56,38,56,'#263947',r=4)+rect(152,56,34,56,'#544360',r=3)
   s+=f'<circle cx="169" cy="81" r="10" fill="#191623"/>'+text(150,139,'VL53L1X',15,'#e8f2e9',700,'middle')
   for i in range(7):s+=f'<circle cx="{49+i*33}" cy="160" r="5.5" fill="url(#gold)"/>'
  elif kind=='driver':
   s+=rect(113,21,95,47,'#222e39',r=4)
   for k in range(7):s+=rect(116+k*13,22,8,45,'url(#fin)',r=1)
   s+=chip(121,87,44,41,'SMC G2')
   for x in [51,93,214,256]:
    s+=rect(x-15,139,31,33,'#328a65','#154e3a',2)+screw(x,149,7)
   for x in [34,64]:s+=f'<circle cx="{x}" cy="61" r="16" fill="#556c78"/><circle cx="{x}" cy="59" r="13" fill="url(#metal)"/><path d="M{x-8} 59h16" stroke="#7b8e95"/>'
   s+=text(188,88,'24v19',13,'#e6f6ed',750)
   for i in range(7):s+=rect(21,86+i*6,5,4,'url(#gold)')
  else:
   s+=chip(123,66,52,50,'USB UART')+rect(27,48,65,96,'url(#metal)','#7b939b',3)
   for i in range(4):s+=rect(256,59+i*20,22,11,'url(#gold)')
 elif kind=='motor':
  s+=rect(33,71,55,66,'url(#metal)','#637683',5)+f'<ellipse cx="88" cy="103" rx="20" ry="46" fill="#8fa0aa"/>'
  s+=rect(84,53,152,98,'url(#dark)','#132a38',9)+rect(84,53,152,98,'url(#rubber)',r=9)
  s+=f'<ellipse cx="89" cy="102" rx="21" ry="48" fill="url(#metal)" stroke="#647d8d"/><ellipse cx="235" cy="102" rx="14" ry="46" fill="#152731"/>'
  s+=rect(8,96,75,14,'url(#metal)','#718895',3)+rect(6,99,13,8,'#bbcad1',r=1)
  s+=rect(112,73,90,56,'#c5cfd2',r=2)+text(157,93,'24V DC',14,'#254351',750,'middle')+text(157,116,'250W',20,'#254351',800,'middle')
  s+=f'<path d="M245 87h32v-20" fill="none" stroke="#c75242" stroke-width="7"/><path d="M245 119h39v29" fill="none" stroke="#293c4a" stroke-width="7"/>'
  for y in [66,140]:s+=screw(99,y,5)
 elif kind=='servo':
  s+=rect(52,50,211,117,'url(#dark)','#182b3b',6)+rect(43,57,23,19,'url(#metal)',r=2)+rect(255,57,28,19,'url(#metal)',r=2)
  s+=f'<path d="M52 50L77 19H249L263 50Z" fill="url(#metal)" stroke="#67808b"/>'
  s+=f'<ellipse cx="116" cy="33" rx="38" ry="19" fill="#bbc8cf" stroke="#627884"/><circle cx="116" cy="31" r="13" fill="url(#gold)"/>'
  s+=rect(95,29,93,10,'url(#metal)','#647b88',4)+screw(116,31,6)+screw(174,34,3)
  s+=rect(84,83,146,51,'#b2396c',r=2)+text(157,103,'RDS51150',16,'#fff',700,'middle')+text(157,123,'12V / STEERING',11,'#fde5ee',600,'middle')
  for y,c in [(141,'#de5144'),(149,'#263b48'),(157,'#bf8f27')]:s+=f'<path d="M58 {y}H19v20" fill="none" stroke="{c}" stroke-width="5"/>'
 elif kind=='lidar':
  s+=f'<ellipse cx="150" cy="150" rx="93" ry="26" fill="#1b2b36"/><path d="M57 73V149Q149 194 243 149V73Z" fill="url(#dark)" stroke="#101f29"/>'
  s+=f'<ellipse cx="150" cy="75" rx="93" ry="43" fill="#2d3b45" stroke="#111f29" stroke-width="3"/><ellipse cx="150" cy="65" rx="80" ry="34" fill="url(#dark)"/><ellipse cx="150" cy="65" rx="32" ry="17" fill="#354753" stroke="#647783"/>'
  s+=rect(167,106,54,24,'url(#lens)','#2f4656',6)+rect(67,110,31,9,'#0a131b',r=3)
  s+=text(142,65,'SLAMTEC',9,'#98abb8',500,'middle')+text(129,145,'C1',13,'#c0d0d9',650,'middle')
 elif kind=='hub':
  s+=rect(15,32,270,127,'url(#dark)','#142837',10)+rect(23,39,254,108,'url(#brushed)',r=8)
  for i in range(4):s+=rect(32+i*61,120,46,31,'url(#metal)','#6b8394',2)+rect(37+i*61,128,36,14,'#174263',r=1)+text(55+i*61,114,str(i+1),10,'#a8bac8',600,'middle')
  s+=text(150,70,'POWERED USB HUB',17,'#cedce5',700,'middle')+text(150,91,'5V IN · NO BACKFEED',11,'#93a8b7',600,'middle')
 elif kind=='contactor':
  s+=rect(60,24,180,148,'url(#dark)','#152a38',10)+rect(67,30,166,65,'#566d7a',r=6)
  for x in [98,202]:s+=rect(x-13,14,26,32,'url(#gold)',r=3)+screw(x,27,10)
  s+=rect(78,108,144,43,'#dce5e9',r=2)+text(150,126,'DC CONTACTOR',12,'#344e5d',700,'middle')+text(150,142,'12V COIL  /  K1',11,'#344e5d',600,'middle')
  for x in [45,255]:s+=rect(x-7,114,14,33,'url(#gold)',r=2)
 elif kind in ['resistor','capacitor','suppressor']:
  if kind=='resistor':
   s+=f'<path d="M18 96H282" stroke="#c1c9c8" stroke-width="5"/>'+rect(92,75,116,43,'#c5c2aa','#7d8e92',12)
   for x,c in [(105,'#875333'),(124,'#263d48'),(146,'#b53430'),(187,'#b99441')]:s+=rect(x,77,7,39,c)
   s+=text(150,143,label,15,'#516974',650,'middle')
  elif kind=='capacitor':
   s+=f'<path d="M121 112V169M177 112V169" stroke="#a0b1ba" stroke-width="5"/>'+rect(102,53,95,76,'#d5a345','#a67328',13)+text(150,96,'104',23,'#775028',700,'middle')
  else:s+=f'<path d="M22 99H280" stroke="#95a5ad" stroke-width="5"/>'+rect(82,76,138,46,'url(#dark)',r=7)+text(150,105,'COIL TVS',14,'#cad6dc',700,'middle')
 elif kind=='tag':
  s+=rect(68,16,164,158,'url(#plastic)','#94a9b5',18)+f'<circle cx="150" cy="46" r="8" fill="#d0dce3" stroke="#92a7b3"/>'
  s+=rect(88,76,124,68,'#164350',r=8)+text(150,103,'UWB TAG',18,'#e8f4f6',700,'middle')+text(150,125,'LOCAL BATTERY',9,'#bdd6dd',500,'middle')
 elif kind=='breadboard':
  s+=rect(3,7,294,175,'url(#plastic)','#a8bbc4',8)+rect(10,89,280,10,'#c9d3d7',r=2)
  for y in [19,31,156,168]:
   s+=f'<path d="M12 {y}H288" stroke="'+('#b04659' if y in [19,156] else '#5986a6')+'" stroke-width="1"/>'
  for col in range(30):
   x=12+col*9.5
   for y in [46,54,62,70,78,109,117,125,133,141]:s+=rect(x,y,3.4,3.4,'#6b7d89',r=.7)
  s+=rect(35,81,67,33,'url(#dark)',r=3)+text(69,101,'AHCT125',7,'#b5c6ce',500,'middle')
  for a,b,c in [(130,18,'#8f56b8'),(170,145,'#40876e'),(230,157,'#b93d83')]:s+=f'<path d="M{a} 62V{b}H{a+35}V120" fill="none" stroke="{c}" stroke-width="2.8"/>'
 return s

class Sheet:
 def __init__(self,name,num,sub):
  self.name=name;self.num=num;self.sub=sub;self.parts=[];self.wires=[];self.anchors={};self.items=[];self.background=[]
 def add(self,s):self.parts.append(s)
 def zone(self,x,y,w,h,n,title):
  self.add(rect(x,y,w,h,'#fff','#d7e1e6',12)+rect(x+1,y+1,w-2,49,'#f1f5f7',r=11)+text(x+20,y+33,n,15,'#3c8590',750)+text(x+55,y+33,title,19,'#294552',700))
 def comp(self,ref,x,y,w=230,h=146,sub=None,small=False):
  c=byref[ref];label=c['spec'].split(' / ')[0]
  if c['kind']=='converter':label='12V / 20A' if ref=='DC1' else '5V / 10A'
  body=f'<g class="component" data-ref="{ref}" role="button" tabindex="0" aria-label="{E(c["name"])}">'
  body+=rect(x-7,y-7,w+14,h+65,'none','none',10,extra='class="selection-frame"')
  body+=f'<g transform="translate({x},{y}) scale({w/300},{h/190})" filter="url(#shadow)">{art(c["kind"],label,ref)}</g>'
  body+=text(x+w/2,y+h+25,f'{ref}  {c["name"]}',17 if not small else 15,'#1c3b4b',700,'middle')
  body+=text(x+w/2,y+h+47,sub if sub is not None else c['spec'],14,'#627b88',500,'middle')+'</g>'
  self.add(body);self.items.append(ref)
  for side,pt in [('l',(x,y+h/2)),('r',(x+w,y+h/2)),('t',(x+w/2,y)),('b',(x+w/2,y+h))]:self.anchors[ref+'.'+side]=pt
  return self
 def port(self,key,x,y,label,net=None,anchor='start'):
  self.anchors[key]=(x,y);col=netcolor(net) if net else '#637887'
  self.add(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="{col}" stroke-width="2"/>'+text(x+(10 if anchor=='start' else -10),y-9,label,13,col,650,anchor))
 def cable(self,start,end,color=None,label='',via=None,nets=None,width=5,labelpos=None,dash=False):
  a=self.anchors.get(start,start);b=self.anchors.get(end,end)
  pts=[a]+(via or [])+[b]
  if not via:
   mx=(a[0]+b[0])/2;pts=[a,(mx,a[1]),(mx,b[1]),b]
  d='M'+' L'.join(f'{round(x,2)},{round(y,2)}' for x,y in pts)
  color=color or netcolor((nets or [''])[0]);ns=' '.join(nets or [])
  s=f'<g class="wire" data-nets="{E(ns)}"><title>{E(label or ns)}</title>'
  s+=f'<path d="{d}" fill="none" stroke="#fbfcfd" stroke-width="{width+7}" stroke-linecap="round" stroke-linejoin="round"/>'
  s+=f'<path d="{d}" fill="none" stroke="#132c3a" stroke-opacity=".22" stroke-width="{width+2}" transform="translate(0,1.5)" stroke-linecap="round" stroke-linejoin="round"/>'
  s+=f'<path class="wire-line" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" '+('stroke-dasharray="9 9"' if dash else '')+'/>'
  if not dash:s+=f'<path d="{d}" fill="none" stroke="#fff" opacity=".25" stroke-width="{max(.8,width*.16)}" transform="translate(0,-1)" stroke-linecap="round" stroke-linejoin="round"/>'
  s+='</g>';self.wires.append(s)
  if label:
   q=labelpos or pts[len(pts)//2];tw=len(label)*7.3+18
   self.add(rect(q[0]-tw/2,q[1]-25,tw,23,'#fff',r=5)+text(q[0],q[1]-9,label,13,color,650,'middle'))
 def note(self,x,y,lines,title='',w=650):
  h=30+len(lines)*26+(24 if title else 0)
  self.add(rect(x,y,w,h,'#f7f4ec','#e0d6bd',8))
  if title:self.add(text(x+16,y+28,title,17,'#8c622a',700))
  for i,line in enumerate(lines):self.add(text(x+16,y+28+(26 if title else 0)+i*26,line,15,'#685c46'))
 def svg(self):
  content=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2100 1450" width="2100" height="1450" aria-label="{E(self.name)}">{DEFS}<style>text{{font-family:"Noto Sans CJK KR","Malgun Gothic",Arial,sans-serif}} .component{{cursor:pointer}} .component:hover .selection-frame,.component.selected .selection-frame{{stroke:#238e98;stroke-width:2;fill:#2c8e9810}} .wire.dim{{opacity:.13}} .wire.selected .wire-line{{filter:drop-shadow(0px 0px 3px #2699a4)}} </style>'
  content+=rect(0,0,2100,1450,'#f9fbfc')+rect(0,153,2100,1230,'url(#dots)')
  content+=text(55,51,'SMART CART  /  MODULE WIRING',15,'#44717f',750)+text(55,97,self.name,34,'#163645',750)+text(55,128,self.sub,16,'#667e8c')
  content+=text(2045,54,'B1  ·  2026.09.13',15,'#597684',650,'end')+text(2045,86,'MODULES + BREADBOARD',13,'#758994',550,'end')
  content+=f'<path d="M55 151H2045" stroke="#b9cad2"/>'
  # Drawing zones must be behind wires; component art and callouts in front.
  zones=[];others=[]
  for s in self.parts:
   (zones if s.startswith('<rect') and ('#d7e1e6' in s) else others).append(s)
  content+=''.join(self.background)+''.join(zones)+''.join(self.wires)+''.join(others)
  content+=f'<path d="M55 1386H2045" stroke="#c0cfd6"/>'
  content+=text(55,1415,'B1 조건부 설계  |  외형 비축척 · 실물 단자표 우선  |  * 퓨즈값은 부하·전선·차단용량 검토 후 확정',14,'#657b88')
  content+=text(2045,1415,f'SC-WIR-{self.num:02d}   /   {self.num:02d}',14,'#365c70',700,'end')+'</svg>'
  return content

# ------------------------- OVERVIEW ----------------------------
def overview():
 s=Sheet('스마트카트 모듈 배선도',1,'외형을 재구성한 케이블 개요. 굵은 신호선은 다심 케이블 묶음이며 실제 접속은 단자표·상세 시트를 우선합니다.')
 s.zone(50,180,590,1155,'01','전원 분배')
 s.zone(680,180,735,1155,'02','구동 · 컴퓨팅')
 s.zone(1455,180,595,1155,'03','센서 · 조향')
 for args in [('BT1',80,270,240,160),('F0',410,263,150,96),('S0',426,389,125,105),('X24',97,537,425,74),('DC1',88,718,228,144),('DC2',372,718,228,144),('K1',102,1000,195,123),('X0',92,1203,457,63),('MDL',725,281,217,137),('MDR',1129,281,217,137),('ML',720,506,220,139),('MR',1126,506,220,139),('OP1',735,803,247,157),('H1',1097,813,229,145),('U1',740,1095,195,124),('BB1',1020,1090,346,157),('LD1',1480,264,215,150),('UWL',1721,260,135,153),('UWR',1881,260,135,153),('TAG1',1773,512,176,113),('A1',1500,526,159,95),('IMU1',1505,774,177,116),('TOF1',1812,774,174,116),('SVL',1485,1052,234,148),('SVR',1795,1052,234,148)]:s.comp(*args,small=args[0] in ['UWL','UWR','A1'])
 # Power overview: cable bundles are explicitly distinguished from single conductors.
 s.cable((121,281),'F0.l',COL['24'],'BAT +',via=[(121,246),(365,246),(365,311)],nets=['BAT_POS'],width=8,labelpos=(353,308))
 s.cable('F0.b','S0.t',COL['24'],nets=['BAT_FUSED'],via=[(485,373),(488,373)],width=7)
 s.cable('S0.b','X24.r',COL['24'],nets=['BUS24'],via=[(574,494),(574,574)],width=7)
 s.cable('X24.l','DC1.t',COL['24'],'F3 → IN',via=[(66,574),(66,674),(202,674)],nets=['BUS24','DC12_IN'],width=7,labelpos=(145,673))
 s.cable('X24.r','DC2.t',COL['24'],'F4 → IN',via=[(615,574),(615,674),(486,674)],nets=['BUS24','DC5_IN'],width=7,labelpos=(521,673))
 s.cable('X24.l','K1.t',COL['24'],'구동 분기',via=[(65,574),(65,966),(199,966)],nets=['BUS24'],width=7,labelpos=(156,965))
 s.cable('K1.r','MDL.l',COL['24'],'F1 / 25A *',via=[(656,1061),(656,349)],nets=['DRIVE24','ML_VIN'],width=7,labelpos=(722,240))
 s.cable('K1.r','MDR.r',COL['24'],'F2 / 25A *',via=[(665,1061),(665,248),(1393,248),(1393,349)],nets=['DRIVE24','MR_VIN'],width=7,labelpos=(1180,249))
 for a,b,via,n in [((880,389),(923,555),[(880,423),(970,423),(970,555)],'ML_A'),((910,389),(928,614),[(910,439),(988,439),(988,614)],'ML_B'),((1284,389),(1329,555),[(1284,423),(1375,423),(1375,555)],'MR_A'),((1314,389),(1334,614),[(1314,439),(1390,439),(1390,614)],'MR_B')]:s.cable(a,b,COL['sig'],via=via,nets=[n],width=4)
 s.add(text(975,504,'A / B',13,COL['sig'],650))
 s.add(text(1330,504,'A / B',13,COL['sig'],650))
 s.cable('DC2.r','OP1.l',COL['5'],'5V / F7',via=[(655,790),(655,881)],nets=['P5','OPI5'],width=6,labelpos=(700,789))
 s.cable('DC2.r','H1.t',COL['5'],'5V / F8',via=[(655,790),(655,761),(1211,761)],nets=['P5','HUB5'],width=6,labelpos=(1120,761))
 s.cable('OP1.r','H1.l',COL['usb'],'USB upstream',nets=['HOST_DM','HOST_DP','HOST5','GND'],width=7,labelpos=(1040,847))
 s.cable('H1.b','U1.t',COL['usb'],'USB power + data',via=[(1211,1015),(838,1015)],nets=['USB_ESP_5','USB_ESP_DM','USB_ESP_DP','GND'],width=7,labelpos=(1095,1015))
 s.cable('H1.r','A1.l',COL['usb'],'USB → UART',via=[(1432,886),(1432,574)],nets=['USB_LIDAR_5','USB_LIDAR_DM','USB_LIDAR_DP'],width=6,labelpos=(1485,467))
 s.cable('A1.t','LD1.b',COL['sig'],'5V + UART',via=[(1579,494),(1587,494)],nets=['USB_LIDAR_5','GND','LIDAR_TX','LIDAR_RX'],width=6,labelpos=(1590,496))
 for ref,x,n in [('UWL',1704,'UWBL'),('UWR',2033,'UWBR')]:
  s.cable('H1.r',ref+'.b',COL['usb'],'USB (거리 데이터)',via=[(1439,886),(1439,690),(x,690),(x,471),(s.anchors[ref+'.b'][0],471)],nets=[f'USB_{n}_5',f'USB_{n}_DM',f'USB_{n}_DP','GND'],width=6,labelpos=(1770 if ref=='UWL' else 1947,706))
 s.cable('U1.r','BB1.l',COL['sig'],'GPIO',nets=['IMU_SCK','IMU_MOSI','IMU_MISO','TOF_SDA','TOF_SCL'],width=6,labelpos=(977,1150))
 s.cable('BB1.t','IMU1.b',COL['sig'],'SPI · 3.3V',via=[(1193,1028),(1534,1028),(1534,947),(1593,947)],nets=['IMU_SCK','IMU_MOSI','IMU_MISO','IMU_CS','IMU_INT','IMU_RST','P3V3','GND'],width=6,labelpos=(1524,978))
 s.cable('BB1.t','TOF1.b',COL['sig'],'I²C · 3.3V',via=[(1208,1012),(1889,1012),(1889,948),(1899,948)],nets=['TOF_SDA','TOF_SCL','P3V3','GND'],width=6,labelpos=(1870,978))
 s.cable('U1.l','MDL.l',COL['sig'],'UART L',via=[(700,1157),(700,454),(714,454),(714,350)],nets=['ESP_L_TX','ML_RX','ML_TX','GND'],width=4,labelpos=(756,724))
 s.cable('U1.l','MDR.r',COL['sig'],'UART R',via=[(691,1157),(691,712),(1404,712),(1404,350)],nets=['ESP_R_TX','MR_RX','MR_TX','GND'],width=4,labelpos=(1264,747))
 for ref,x,net in [('SVL',1602,'SVL_PWR'),('SVR',1912,'SVR_PWR')]:
  s.cable('DC1.b',ref+'.b',COL['12'],'12V / F5·F6',via=[(202,926),(340,926),(340,1307),(x,1307)],nets=['P12',net,'GND'],width=7,labelpos=(x-20,1307))
  s.cable('BB1.r',ref+'.l',COL['pwm'],'5V PWM',via=[(1431,1168),(1431,1279),(x-160,1279),(x-160,1126)],nets=['SERVO_L' if ref=='SVL' else 'SERVO_R'],width=4,labelpos=(x-58,1267))
 s.cable((279,281),'X0.l',COL['gnd'],via=[(333,281),(333,1181),(72,1181),(72,1234)],nets=['GND'],width=6)
 s.add(text(1861,515,'무선 / 독립 전원',14,'#587987',650,'middle'))
 s.note(349,1024,['K1 제어·비상정지는','전원·구동 시트 참조.','GND는 X0로 귀환.'],w=262)
 s.add(text(105,1312,'대전류는 브레드보드 통과 금지',15,'#8b5c30',650))
 return s

# -------------------------- POWER ------------------------------
def power():
 s=Sheet('전원 분배 · 구동 · 수동 재무장',2,'전압별 단자와 보호 장치를 분리한 기능 배선도. 단일 채널 정지 회로는 안전 인증 회로가 아님.')
 # Main high-current row.
 for args in [('BT1',62,213,256,173),('F0',369,232,180,114),('S0',602,209,184,154),('X24',852,236,287,91),('K1',1223,216,215,145),('F1',1530,230,144,91),('F2',1530,693,144,91),('MDL',1735,209,219,139),('MDR',1735,670,219,139),('ML',1728,445,235,145),('MR',1728,894,235,145),('F3',374,577,171,108),('DC1',635,553,281,178),('F4',374,868,171,108),('DC2',635,845,281,178)]:s.comp(*args)
 # Defined terminal positions, presented as endpoint callouts (not guessed photo pin positions).
 ports=[('B+',106,225,'+', 'BAT_POS'),('B-',275,225,'−','GND'),('F0i',378,289,'IN','BAT_POS'),('F0o',540,289,'OUT','BAT_FUSED'),('S0i',614,286,'IN','BAT_FUSED'),('S0o',774,286,'OUT','BUS24'),('BUSi',870,280,'BUS24','BUS24'),('BUSo',1121,280,'BUS24','BUS24'),('K1i',1250,249,'L1','BUS24'),('K1o',1408,249,'T1','DRIVE24'),('F1i',1534,276,'IN','DRIVE24'),('F1o',1670,276,'OUT','ML_VIN'),('F2i',1534,738,'IN','DRIVE24'),('F2o',1670,738,'OUT','MR_VIN'),('Lvin',1744,253,'VIN','ML_VIN'),('Lg',1744,318,'GND','GND'),('La',1812,334,'OUTA','ML_A'),('Lb',1890,334,'OUTB','ML_B'),('LM_a',1945,496,'A','ML_A'),('LM_b',1950,558,'B','ML_B'),('Rvin',1744,714,'VIN','MR_VIN'),('Rg',1744,778,'GND','GND'),('Ra',1812,795,'OUTA','MR_A'),('Rb',1890,795,'OUTB','MR_B'),('RM_a',1945,945,'A','MR_A'),('RM_b',1950,1007,'B','MR_B')]
 for p in ports:s.port(*p)
 for a,b,n in [('F0o','S0i','BAT_FUSED'),('S0o','BUSi','BUS24'),('BUSo','K1i','BUS24'),('K1o','F1i','DRIVE24'),('F1o','Lvin','ML_VIN'),('F2o','Rvin','MR_VIN')]:s.cable(a,b,nets=[n],width=7)
 s.cable('B+','F0i',nets=['BAT_POS'],via=[(106,183),(349,183),(349,289)],width=7)
 s.cable('K1o','F2i',nets=['DRIVE24'],via=[(1482,249),(1482,738)],width=7)
 for a,b,n,x in [('La','LM_a','ML_A',1980),('Lb','LM_b','ML_B',2001),('Ra','RM_a','MR_A',1980),('Rb','RM_b','MR_B',2001)]:
  ap=s.anchors[a];bp=s.anchors[b];s.cable(a,b,nets=[n],via=[(ap[0],ap[1]+8),(x,ap[1]+8),(x,bp[1])],width=5)
 # Grounds: outside of components and motor outputs, one star bus only.
 s.port('Gstar',148,1139,'X0  공통 0V (음극 버스)', 'GND')
 s.add(rect(137,1132,1858,16,'url(#metal)','#617581',4))
 for x in [148,570,617,958,991,1040,1620,1690,1976]:s.add(screw(x,1140,6))
 s.cable('B-','Gstar',nets=['GND'],via=[(333,225),(333,1109),(148,1109)],width=8)
 s.cable('Lg',(1690,1140),nets=['GND'],via=[(1690,318)],width=6)
 s.cable('Rg',(1976,1140),nets=['GND'],via=[(2019,778),(2019,1140)],width=6)
 for d,f,y,ins,out in [('DC1','F3',642,'DC12_IN','P12'),('DC2','F4',934,'DC5_IN','P5')]:
  yy=613 if d=='DC1' else 905
  s.port(f+'i',380,yy,'IN','BUS24');s.port(f+'o',538,yy,'OUT',ins)
  s.port(d+'i',650,yy,'IN+',ins);s.port(d+'g',650,yy+76,'IN−','GND')
  s.port(d+'o',902,yy,'OUT+',out);s.port(d+'og',902,yy+76,'OUT−','GND')
  s.cable('BUSi',f+'i',nets=['BUS24'],via=[(826,280),(826,477),(350,477),(350,yy)],width=6)
  s.cable(f+'o',d+'i',nets=[ins],width=6)
  s.cable(d+'g',(617 if d=='DC1' else 570,1140),nets=['GND'],via=[(617 if d=='DC1' else 570,yy+76)],width=5)
  s.cable(d+'og',(958 if d=='DC1' else 991,1140),nets=['GND'],via=[(958 if d=='DC1' else 991,yy+76)],width=5)
  x=1065;endpoint=(x,yy)
  s.cable(d+'o',endpoint,nets=[out],width=7)
  s.port('OUT_'+out,*endpoint,('12V → F5/F6/서보 + F9/코일' if out=='P12' else '5V → F7/OP1 + F8/H1 + F10/BB1'),out)
 s.note(69,519,['모터 퓨즈는 드라이버 VIN 앞에 설치.','모터 A/B 어느 쪽도 GND가 아님.','BTS7960 직접 연결은 제외.','24v19도 스톨·열·회생 검증 필요.'],title='구동 전력부',w=263)
 s.note(1083,936,['12V/5V 출력 개별 퓨즈 및 부하는','제어·센서 시트의 연결표에 수록.','모든 귀환은 공통 0V. 전압의 +끼리 합치지 않음.'],title='전원 네트 분리',w=535)
 s.comp('S1',1033,451,146,103,sub='NC 접점 · 하단 회로 참조',small=True)
 s.comp('S2',1290,451,146,103,sub='NO 접점 · 하단 회로 참조',small=True)
 # Self-holding contactor control strip. Wires stop at component terminals.
 s.background.append(rect(57,1184,1985,179,'#fff','#cbd9e0',9))
 s.add(text(75,1210,'접촉기 코일 / 12V 정전압 측',18,'#345969',750))
 y=1242
 for a,b,n in [((100,y),(238,y),'P12'),((328,y),(418,y),'COIL_FUSED'),((562,y),(786,y),'LATCH_IN'),((939,y),(1162,y),'COIL12'),((1319,y),(1480,y),'GND')]:s.cable(a,b,nets=[n],width=4)
 s.add(rect(238,1230,90,24,'#fff','#657d89',3)+text(283,1278,'F9  1A *',14,'#435e6c',650,'middle'))
 s.add(f'<path d="M418 {y}h38m58 0h48M456 {y}l58 -12v12" fill="none" stroke="#ba473e" stroke-width="3"/>'+text(491,1278,'S1 NC 비상정지',14,'#435e6c',650,'middle'))
 s.add(f'<path d="M786 {y}h34m75 0h44M820 {y-13}h75M857 {y-22}v9" fill="none" stroke="#3b697b" stroke-width="3"/>'+text(864,1278,'S2 NO 재무장',14,'#435e6c',650,'middle'))
 s.cable((733,y),(798,1318),nets=['LATCH_IN'],via=[(733,1318)],width=3)
 s.cable((928,1318),(1004,y),nets=['COIL12'],via=[(1004,1318)],width=3)
 s.add(f'<path d="M798 1318h36m52 0h42M834 1318l52 -12" fill="none" stroke="#3b697b" stroke-width="2.5"/>'+text(866,1348,'K1 보조 NO 13-14',13,'#526f7c',600,'middle'))
 for x in [733,1004]:s.add(f'<circle cx="{x}" cy="{y}" r="4" fill="{COL['12']}"/>')
 s.add(rect(1162,1224,157,36,'#fff','#667e8a',3)+text(1240,1248,'K1 12V COIL',15,'#31586b',650,'middle'))
 s.add(text(1147,1220,'A1',12,COL['12'],650)+text(1323,1220,'A2',12,COL['gnd'],650))
 s.cable((1105,y),(1162,1310),nets=['COIL12'],via=[(1105,1310)],width=3)
 s.cable((1319,1310),(1375,y),nets=['GND'],via=[(1375,1310)],width=3)
 s.add(rect(1162,1296,157,28,'url(#dark)',r=4)+text(1240,1315,'Z1 K1 지정 억제기',12,'#fff',600,'middle'))
 s.port('P12COIL',100,y,'P12','P12');s.port('GCOIL',1480,y,'X0 / GND','GND')
 s.add(text(1555,1228,'동작: S1 복귀 → S2 누름 → K1 자기유지',15,'#576f7d',600))
 s.add(text(1555,1257,'S1 누름 → 코일 OFF / 구동 전원 차단',15,'#576f7d',600))
 s.add(text(1555,1286,'서보 전원 유지 / 제동 기능 별도',15,'#98652f',650))
 s.add(text(1555,1315,'단일 고장 안전성·접촉기 해제시간 미검증',14,'#98652f',600))

 return s

# ------------------------ CONTROL ------------------------------
def control():
 s=Sheet('제어보드 · USB 센서 · 조향 전원',3,'모든 USB는 완성 케이블을 사용. 브레드보드는 소신호만 담당하며 고전류 장치에는 별도 전원을 분배.')
 s.zone(50,181,488,1155,'01','12V 조향 분기')
 s.zone(567,181,945,1155,'02','5V 컴퓨팅 · 제어')
 s.zone(1541,181,509,1155,'03','USB 센서')
 for a in [('DC1',96,269,205,130),('F5',96,506,146,93),('F6',332,506,146,93),('SVL',136,751,252,160),('SVR',136,1034,252,160),('DC2',610,269,219,139),('F7',884,281,158,100),('F8',1260,281,158,100),('OP1',650,560,290,183),('H1',1099,543,310,196),('U1',638,965,229,146),('BB1',1025,977,397,181),('F10',1209,843,142,90),('LD1',1602,266,211,164),('A1',1819,301,175,102),('UWL',1598,623,176,180),('UWR',1809,623,176,180),('IMU1',1567,1034,187,124),('TOF1',1814,1034,187,124)]:s.comp(*a,small=a[0] in ['F7','F8','F10'])
 s.cable('DC1.b','F5.t',COL['12'],'12V',via=[(198,461),(169,461)],nets=['P12'],width=6,labelpos=(203,461))
 s.cable('DC1.b','F6.t',COL['12'],via=[(198,461),(405,461)],nets=['P12'],width=6)
 s.cable('F5.b','SVL.t',COL['12'],'F5 → V+',via=[(169,699),(262,699)],nets=['SVL_PWR'],width=6,labelpos=(229,699))
 s.cable('F6.b','SVR.t',COL['12'],'F6 → V+',via=[(477,552),(504,552),(504,994),(262,994)],nets=['SVR_PWR'],width=6,labelpos=(404,994))
 s.cable('DC2.r','F7.l',COL['5'],nets=['P5'],width=6)
 s.cable('DC2.r','F8.l',COL['5'],'5V 분배',via=[(850,339),(850,246),(1218,246),(1218,331)],nets=['P5'],width=6,labelpos=(1061,246))
 s.cable('F7.b','OP1.t',COL['5'],'F7 → Type-C 5V / GND',via=[(963,499),(795,499)],nets=['OPI5','GND'],width=6,labelpos=(906,499))
 s.cable('F8.b','H1.t',COL['5'],'F8 → 5V / GND',via=[(1339,491),(1254,491)],nets=['HUB5','GND'],width=6,labelpos=(1344,491))
 s.cable('OP1.r','H1.l',COL['usb'],'upstream',nets=['HOST_DM','HOST_DP','HOST5','GND'],width=7,labelpos=(1019,629))
 usb=[('U1.t',[(1010,640),(1010,909),(752,909)],'ESP'),('A1.b',[(1490,641),(1490,484),(1906,484)],'LIDAR'),('UWL.t',[(1497,654),(1497,554),(1686,554)],'UWBL'),('UWR.t',[(1504,672),(1504,571),(1897,571)],'UWBR')]
 for target,via,n in usb:s.cable('H1.r',target,COL['usb'],via=via,nets=[f'USB_{n}_5',f'USB_{n}_DM',f'USB_{n}_DP','GND'],width=6)
 s.cable('A1.l','LD1.r',COL['sig'],'5V + TX/RX',nets=['LIDAR_RX','LIDAR_TX','USB_LIDAR_5','GND'],width=5,labelpos=(1831,454))
 s.cable('DC2.b','F10.l',COL['5'],'로직 분기',via=[(719,466),(586,466),(586,881)],nets=['P5'],width=5,labelpos=(1019,881))
 s.cable('F10.b','BB1.t',COL['5'],'5V / buffer only',via=[(1280,956),(1223,956)],nets=['LOGIC5'],width=5,labelpos=(1360,995))
 s.cable('U1.r','BB1.l',COL['sig'],'GPIO + 3V3 / GND',nets=['P3V3','GND','IMU_SCK','IMU_MOSI','IMU_MISO','TOF_SDA','TOF_SCL','PWM_L_3V3','PWM_R_3V3'],width=6,labelpos=(947,1038))
 s.cable('BB1.r','IMU1.l',COL['sig'],'SPI',via=[(1482,1067),(1482,1096)],nets=['P3V3','GND','IMU_SCK','IMU_MOSI','IMU_MISO','IMU_CS','IMU_INT','IMU_RST'],width=5,labelpos=(1490,1011))
 s.cable('BB1.r','TOF1.b',COL['sig'],'I²C',via=[(1490,1067),(1490,1257),(1908,1257)],nets=['P3V3','GND','TOF_SDA','TOF_SCL'],width=5,labelpos=(1895,1257))
 for target,n,yy in [('SVL.r','SERVO_L',1259),('SVR.r','SERVO_R',1280)]:s.cable('BB1.b',target,COL['pwm'],'5V PWM',via=[(1223,yy),(554,yy),(554,s.anchors[target][1])],nets=[n],width=4,labelpos=(562,yy))
 # Named star return, never through the breadboard.
 s.port('G',110,1290,'X0 / GND', 'GND')
 for ref,y in [('SVL',831),('SVR',1114)]:s.cable((136,y),'G',COL['gnd'],via=[(78,y),(78,1290)],nets=['GND'],width=6)
 s.note(628,752,['ESP32: USB만 급전. 5V 헤더 미연결.','UWB: USB 거리 데이터 포트 사용, TTL 포트와 구분.'],w=787)
 s.note(1571,874,['IMU는 Adafruit #4754 / SPI.','ToF는 Pololu #3415 / 3.3V VIN.','서보는 기구·입력 레벨 검증 후 활성화.'],w=447)
 return s

# ------------------------ BREADBOARD ---------------------------
def breadboard():
 s=Sheet('브레드보드 실제 접점 배선',4,'400접점: 본체 30열 × 10행 + 전원 레일 25접점 × 4줄. 레일 번호는 본체 열 번호와 별도로 왼쪽부터 셉니다.')
 # Large BB physical positions, generous contact pitch and rails.
 bx=382;by=482;pitch=44;bbwidth=30*pitch+100;bbh=526
 def xy(h):
  if h.startswith(('T+','T-','B+','B-')):
   row=h[:2];n=int(h[2:]);yy={'T+':by+44,'T-':by+83,'B+':by+436,'B-':by+479}[row]
  else:
   row=h[0];n=int(h[1:]);yy=by+140+'abcde'.index(row)*29 if row in 'abcde' else by+303+'fghij'.index(row)*29
  gap=(n-1)//5 if h.startswith(('T+','T-','B+','B-')) else 0
  return bx+68+(n-1+gap)*pitch,yy
 # BB backing first, explicit zones don't go over traces.
 s.add(rect(bx,by,bbwidth,bbh,'url(#plastic)','#a4b6c0',15,extra='filter="url(#shadow)"'))
 s.add(rect(bx+18,by+268,bbwidth-36,23,'#c7d3d9','#b6c5cc',4))
 for row,col in [('T+',COL['3']),('T-',COL['gnd']),('B+',COL['5']),('B-',COL['gnd'])]:
  y=xy(row+'1')[1];s.add(f'<path d="M{bx+35} {y-15}H{bx+bbwidth-28}" stroke="{col}" stroke-width="2"/>')
  s.add(text(bx+16,y+4,'+' if '+' in row else '−',18,col,700))
 for row in 'abcdefghij':s.add(text(bx+22,xy(row+'1')[1]+6,row,18,'#6d808a',650))
 for n in range(1,31):
  x=xy('a'+str(n))[0];s.add(text(x,by+119,str(n),14,'#657984',550,'middle'))
  for row in ['T+','T-','a','b','c','d','e','f','g','h','i','j','B+','B-']:
   if len(row)==2 and n>25:continue
   h=row+str(n);px,py=xy(h);d=BP.get(h);c=netcolor(d['net']) if d else '#7e8d94'
   s.add(f'<g class="hole" data-hole="{h}" data-net="{E(d["net"] if d else "")}"><title>{E(h+": "+(d["owner"]+" / "+d["net"] if d else "미사용"))}</title><rect x="{px-6}" y="{py-6}" width="12" height="12" rx="2" fill="#b9c7ce"/><rect x="{px-4.5}" y="{py-4.5}" width="9" height="9" rx="1" fill="#51626e"/>'+(f'<circle cx="{px}" cy="{py}" r="8" fill="none" stroke="{c}" stroke-width="2"/>' if d else '')+'</g>')
 s.add(text(bx+35,by+25,'3.3V 레일 / 접점은 각 줄 1~25번',16,COL['3'],700)+text(bx+875,by+415,'5V AHCT 버퍼 전용 레일',16,COL['5'],700))
 # Put breadboard wires and part bodies ABOVE the contacts; use direct vector paths.
 def localwire(a,b,net,mid=None,width=4):
  p=xy(a);q=xy(b);pts=[p]+(mid or [])+[q];d='M'+' L'.join(f'{x},{y}' for x,y in pts);co=netcolor(net)
  return f'<g class="wire" data-nets="{net}"><title>{a} → {b} / {net}</title><path d="{d}" fill="none" stroke="#fff" stroke-width="{width+3}" stroke-linecap="round"/><path class="wire-line" d="{d}" fill="none" stroke="{co}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/></g>'
 for i,(a,b) in enumerate(jumpers):s.add(localwire(a,b,BP[a]['net']))
 # DIP leads accurately map top e3...e9 to pins 1...7, bottom f3...f9 to 14...8.
 ux=xy('e3')[0]-18;uy=xy('e3')[1]+11;uw=6*pitch+36;uh=xy('f3')[1]-xy('e3')[1]-22
 body=f'<g class="component" data-ref="U2" tabindex="0"><title>U2 / SN74AHCT125N</title>'
 for pin in range(1,15):
  hole=('e'+str(pin+2)) if pin<=7 else ('f'+str(17-pin));px,py=xy(hole)
  dest=uy if pin<=7 else uy+uh
  body+=f'<path d="M{px} {py}V{dest}" stroke="#8c9ba5" stroke-width="9"/>'+text(px,py+(-11 if pin<=7 else 22),str(pin),12,'#536c7a',650,'middle')
 body+=rect(ux,uy,uw,uh,'url(#dark)','#172d3b',4)+f'<path d="M{ux} {uy+4}Q{ux+20} {uy+uh/2} {ux} {uy+uh-4}" fill="#0c1720"/>'+text(ux+uw/2,uy+uh/2+5,'SN74AHCT125N',13,'#cdd9df',650,'middle')+'</g>'
 s.add(body)
 # Axial resistor bodies placed on their real two contact coordinates.
 for ref,(a,b) in placements.items():
  p=xy(a);q=xy(b);cx=(p[0]+q[0])/2;cy=(p[1]+q[1])/2;ang=math.degrees(math.atan2(q[1]-p[1],q[0]-p[0]));co=byref[ref]['spec'].split(' / ')[0]
  bdy=f'<g class="component" data-ref="{ref}" tabindex="0"><title>{ref}: {a} - {b}</title><path d="M{p[0]} {p[1]}L{q[0]} {q[1]}" stroke="#617984" stroke-width="4"/>'
  if ref=='C1':bdy+=rect(cx-12,cy-18,24,36,'#d5a449','#9a7437',4)+text(cx+20,cy+5,'C1 104',12,'#697e88',600)
  else:
   bdy+=f'<g transform="translate({cx},{cy}) rotate({ang})">'+rect(-23,-8,46,16,'#bfcdc6','#7d9498',7)
   colors=['#7b432c','#172933','#bc2828','#bc963b'] if ref in ['R1','R2'] else ['#bd352d','#bc362a','#704629','#b99440'] if ref in ['R3','R4'] else ['#78462f','#1d313d','#e89835','#b58a32']
   for xx,cc in zip([-16,-6,5,16],colors):bdy+=rect(xx,-7,3,14,cc)
   bdy+='</g>'+text(cx+14,cy-13,ref+' '+co,12,'#3f6375',700)
  s.add(bdy+'</g>')
 # Perimeter terminal patch panels: silkscreen references rather than fabricated board pin placement.
 # Real ESP32 module image plus small terminal name rails.
 s.comp('U1',80,184,248,148,sub='USB 급전 / 5V 헤더 NC')
 s.comp('IMU1',1422,222,231,146,sub='P0 = P1 = 3.3V / SPI')
 s.comp('TOF1',1786,229,219,139,sub='VIN 3.3V / 보조 핀 NC')
 # Functions are grouped; each endpoint label contains the verified actual DevKit header id.
 left_targets=[('U1.IO13','a4','IO13 · J2.15'),('U1.IO14','a7','IO14 · J2.12'),('U1.IO17','a13','IO17 · J3.11'),('U1.IO16','a14','IO16 · J3.12'),('U1.IO25','a15','IO25 · J2.9'),('U1.IO26','a16','IO26 · J2.10')]
 for i,(own,h,lab) in enumerate(left_targets):
  yy=551+i*60;x1=340;p=xy(h);co=netcolor(BP[h]['net']);route=416+i*17
  s.add(text(85,yy+5,lab,17,'#335a6d',650)+f'<circle cx="{x1}" cy="{yy}" r="5" fill="{co}"/>')
  # fanout runs above a-row at separate lanes
  d=f'M{x1},{yy} L{bx-20-i*9},{yy} L{bx-20-i*9},{route} L{p[0]},{route} L{p[0]},{p[1]}'
  s.add(f'<g class="wire" data-nets="{BP[h]["net"]}"><path d="{d}" fill="none" stroke="#fff" stroke-width="6"/><path class="wire-line" d="{d}" fill="none" stroke="{co}" stroke-width="3"/></g>')
 # Signal fanouts for IMU and ToF sit above board, actual names located at connector lane.
 for i,(col,net,gpio,pin) in enumerate(signalrows):
  p=xy('a'+str(col));q=xy('c'+str(col));sx=1442+i*72 if i<6 else 1853+(i-6)*80
  # Draw sensor from c-hole vertically to short label; ESP a-hole connection listed in label.
  label_y=428 if i%2==0 else 456
  s.add(f'<g class="wire" data-nets="{net}"><path class="wire-line" d="M{q[0]} {q[1]} L{q[0]+13} {q[1]} V{label_y+9}" fill="none" stroke="{COL["sig"]}" stroke-width="3"/></g>')
  s.add(rect(p[0]-27,label_y-17,54,23,'#e8f3f2','#98bebc',3)+text(p[0],label_y,pin,12,'#376c78',700,'middle'))
  s.add(text(p[0],by+135,gpio,10,'#536b78',650,'middle'))
 # Explicit power ports and short leads; external +3.3 and +5 stay isolated.
 for h,title,x,y in [('T+1','U1 3V3 → T+1',76,421),('T-1','U1 GND → T−1',76,453),('B+1','F10 5V → B+1',84,1026),('B-1','X0 GND → B−1',84,1058)]:
  p=xy(h);s.add(text(x,y,title,16,netcolor(BP[h]['net']),650))
  s.add(f'<path d="M{x+244} {y-6}H{bx-15}V{p[1]}H{p[0]}" fill="none" stroke="{netcolor(BP[h]["net"])}" stroke-width="4"/>')
 # Each connection not drawn as a long line is named at the contact and exhaustively in the table.
 s.note(66,1149,['R1: e13-f13 (1kΩ)  /  R2: e15-f15 (1kΩ)','R3: d5-d11 (220Ω)  /  R4: b8-b12 (220Ω)','R5: b4-T−4 (10kΩ)  /  R6: b7-T−7 (10kΩ)'],title='저항의 실제 삽입 위치',w=620)
 s.note(718,1149,['좌 드라이버 RX: j13, TX: c14 / 우 RX: j15, TX: c16','좌 서보 PWM: c11 / 우 서보 PWM: c12 (5V 버퍼 후)','IMU / ToF 전원 및 GPIO 접점은 접점표와 함께 연결.'],title='출력 · 모듈 하네스',w=736)
 s.note(1484,1149,['두 −레일만 T−25-B−25으로 연결.','3.3V +레일과 5V +레일은 연결 금지.','센서·GPIO만. 12V·24V 인입 금지.'],title='통전 전 실물 도통 검사',w=558)
 s.add(text(450,1104,'상부: a-e 공통 / 하부: f-j 공통  ·  핀 1은 U2 좌측 상단(e3)  ·  브레드보드는 실험용, 주행 전 납땜 하네스로 이전',16,'#5b7481',600))
 # store exact geometry for inspection and hole-to-net selection.
 s.xy=xy
 return s

def build():
 sheets=[overview(),power(),control(),breadboard()]
 data=[]
 for i,s in enumerate(sheets,1):
  name=f'{i:02d}-'+['overview','power','control','breadboard'][i-1]
  svg=s.svg();(ROOT/'assets/drawings'/f'{name}.svg').write_text(svg)
  data.append({'id':name,'title':s.name,'short':['전체 배선','전원·구동','제어·센서','브레드보드'][i-1],'svg':svg,'refs':s.items})
 (ROOT/'js/drawings.js').write_text('window.CART_DRAWINGS = '+json.dumps(data,ensure_ascii=False)+';\n')
 (ROOT/'js/design.js').write_text('window.CART_DESIGN = '+json.dumps(MODEL,ensure_ascii=False)+';\n')
 return data
if __name__=='__main__':build()
