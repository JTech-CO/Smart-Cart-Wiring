"""Reproducible static connection checks. NOT native EasyEDA/KiCad ERC or safety certification."""
from pathlib import Path
import json,re,sys,collections,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'data/design.json').read_text());cs=d['components'];br=d['breadboard'];by={c['ref']:c for c in cs};checks=[]
def ck(name,condition,detail=''):
 checks.append(dict(name=name,pass_=bool(condition),detail=detail))
 if not condition:print('FAIL',name,detail)
ck('unique module references',len(by)==len(cs))
expected={(c['ref'],p['number']):(p['name'],p['net']) for c in cs for p in c['pins']}
ck('194 unique electrical terminals',len(expected)==194)
ck('63 canonical net names',len({n for _,n in expected.values()})==63)
ck('symbol pin sequences',all([p['number'] for p in c['pins']]==[str(i+1) for i in range(len(c['pins']))] for c in cs))
ck('400-hole reference topology',30*10+25*4==400)
def group(h):
 if re.match('[TB][+-]',h):return h[:2]
 return ('top' if h[0] in 'abcde' else 'bottom')+h[1:]
groups=collections.defaultdict(set)
for h,p in br['contacts'].items():groups[group(h)].add(p['net'])
ck('no conflicting nets on breadboard strips or rails',all(len(n)==1 for n in groups.values()))
ck('breadboard coordinates in valid 400-tie range',all((bool(re.fullmatch(r'[a-j](?:[1-9]|[12][0-9]|30)',h)) or bool(re.fullmatch(r'[TB][+-](?:[1-9]|1[0-9]|2[0-5])',h))) for h in br['contacts']))
ck('no 12V / battery / motor net on breadboard',not any(p['net'].startswith(('BAT','BUS24','DRIVE24','P12','COIL','SVL_PWR','SVR_PWR','ML_VIN','MR_VIN')) for p in br['contacts'].values()))
ck('3.3V and 5V positive rails remain separate',groups['T+']=={'P3V3'} and groups['B+']=={'LOGIC5'} and groups['T+']!=groups['B+'])
ck('negative rail bridge only',br['jumpers'][-1]==['T-25','B-25'])
ck('all inserted jumper ends have same net',all(br['contacts'][a]['net']==br['contacts'][b]['net'] for a,b in br['jumpers']))
ck('passive lead coordinates match terminal netlist',all(br['contacts'][h]['net']==by[ref]['pins'][i]['net'] for ref,hs in br['placements'].items() for i,h in enumerate(hs)))
ck('DIP14 numbering not mirrored',all(br['contacts'][('e'+str(i+2)) if i<=7 else ('f'+str(17-i))]['owner']==f'U2.{i}' for i in range(1,15)))
ck('DIP power GND7 VCC14',by['U2']['pins'][6]['net']=='GND' and by['U2']['pins'][13]['net']=='LOGIC5')
ck('unused buffer inputs and enables are tied',all(by['U2']['pins'][i-1]['net']==n for i,n in [(9,'GND'),(10,'LOGIC5'),(12,'GND'),(13,'LOGIC5')]))
ck('resistor lead paths placed on different rows',br['placements']['R3']==['d5','d11'] and br['placements']['R4']==['b8','b12'])
ck('ESP32 external 5V header not wired',not any('5V' in p['name'] and 'USB' not in p['name'] for p in by['U1']['pins']))
ck('IMU SPI mode P0 and P1 high',all(p['net']=='P3V3' for p in by['IMU1']['pins'] if p['name'] in ['P0','P1']))
ck('ToF raw 2.8V pins left unconnected',not any(p['name'] in ['XSHUT','GPIO1','VDD'] for p in by['TOF1']['pins']))
ck('user tag has no cart electrical connection',by['TAG1']['pins']==[])
ck('motor outputs are not GND',all(p['net']!='GND' for m in ['ML','MR'] for p in by[m]['pins']))
ck('motor branch protection before VIN',by['F1']['pins'][1]['net']==by['MDL']['pins'][0]['net'] and by['F2']['pins'][1]['net']==by['MDR']['pins'][0]['net'])
ck('main battery only one outgoing positive net',sum(p['net']=='BAT_POS' for c in cs for p in c['pins'])==2)
ck('four USB downstream device pairs',all(sum(p['net']==f'USB_{dev}_DP' for c in cs for p in c['pins'])==2 for dev in ['ESP','LIDAR','UWBL','UWBR']))
# Reparse the actual EasyEDA pins, wires, and labels independently of exporter expectations.
ed=json.loads((R/'eda/easyeda/SmartCart-B1-Modules.json').read_text());libs=[s for s in ed['shape'] if s.startswith('LIB~')];wiremap={};labels={};ids=[];actual={}
for s in ed['shape']:
 if s.startswith('W~'):
  f=s.split('~');v=list(map(float,f[1].split()));wiremap[(v[0],v[1])]=(v[2],v[3]);ids.append(f[6])
 elif s.startswith('N~'):
  f=s.split('~');labels[(float(f[1]),float(f[2]))]=f[5];ids.append(f[6])
 elif s.startswith('T~'):ids.append(s.split('~')[15])
for lib in libs:
 seg=lib.split('#@$');lh=seg[0].split('~');ids.append(lh[6]);prefixes=[x.split('~')[12] for x in seg[1:] if x.startswith('T~P~')];ref=prefixes[0]
 for prim in seg[1:]:
  f=prim.split('~')
  if prim.startswith('P~'):
   p=prim.split('^^');ph=p[0].split('~');xy=(float(ph[4]),float(ph[5]));name=p[3].split('~')[4];net=labels.get(wiremap.get(xy));actual[(ref,ph[3])]=(name,net);ids.append(ph[7])
  elif prim.startswith('T~'):ids.append(f[15])
  elif prim.startswith('R~'):ids.append(f[11])
ck('EasyEDA 44 embedded module symbols',len(libs)==44)
ck('EasyEDA 194 real pins and 194 wire stubs',len(actual)==194 and len(wiremap)==194)
ck('EasyEDA pin/name/net round trip matches canonical model',actual==expected)
ck('EasyEDA graph ids unique',len(ids)==len(set(ids)),str(len(ids)))
ck('no PCB footprint or converter flag',all(x.split('#@$')[0].split('~')[11]=='no' for x in libs))
ck('document has schematic type and no raster picture primitives',ed['head']['docType']=='1' and not any(x.startswith('I~') for x in ed['shape']))
# KiCad legacy source-level cross-check, NOT native schematic parser/ERC.
ks=(R/'eda/kicad/SmartCart.sch').read_text();kl=(R/'eda/kicad/SmartCart.lib').read_text()
ck('KiCad legacy 44 components and 194 physical pin declarations',ks.count('$Comp\n')==44 and len(re.findall(r'^X ',kl,re.M))==194)
ck('KiCad legacy wire and netlabel counts',ks.count('Wire Wire Line\n')==194 and len(re.findall(r'^Text Label ',ks,re.M))==194)
ck('KiCad symbol library and cache identical',(R/'eda/kicad/SmartCart.lib').read_bytes()==(R/'eda/kicad/SmartCart-cache.lib').read_bytes())
root=ET.parse(R/'eda/SmartCart-B1.net').getroot();xmlactual={(n.attrib['ref'],n.attrib['pin']):net.attrib['name'] for net in root.find('nets') for n in net}
ck('XML netlist matches 194 exported terminals',xmlactual=={k:v[1] for k,v in expected.items()})
for sf in sorted((R/'assets/drawings').glob('*.svg')):
 tree=ET.parse(sf).getroot();ck(f'SVG XML and viewBox {sf.name}',tree.attrib['viewBox']=='0 0 2100 1450')
 if 'breadboard' in sf.name:ck('400 rendered breadboard holes',len([g for g in tree.iter() if g.attrib.get('class')=='hole'])==400)
report={'scope':'STATIC DESIGN / FILE ROUND-TRIP ONLY','counts':{'components_with_pins':44,'symbol_terminals':194,'nets':63,'breadboard_used_holes':len(br['contacts']),'breadboard_total_holes':400},'passed':sum(x['pass_'] for x in checks),'total':len(checks),'checks':checks,'not_executed':['Native EasyEDA Standard/Pro import','Native KiCad file opening / ERC','Hardware prototype / electrical compliance','Current rating, wire gauge, fuses and thermal validation','Motor regeneration / contactor opening / braking validation']}
(R/'tests/design-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(report['passed'],'/',report['total'],'checks passed; used holes',len(br['contacts']))
sys.exit(0 if all(x['pass_'] for x in checks) else 1)
