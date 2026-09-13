"""EasyEDA Standard JSON (import path into Pro) and KiCad 5.1 legacy schematic.
Self-contained module symbols, actual electrical pins/wires/net labels. No PCB footprints.
"""
from pathlib import Path
import json,uuid,re,zipfile,html
from design import ROOT,C,MODEL
U=lambda s:uuid.uuid5(uuid.NAMESPACE_URL,'smartcart-b1/'+s).hex
counter=0
def gid():
 global counter
 counter+=1;return 'gge'+str(counter)
def asc(s):
 return s.replace('Ω','ohm').replace('→','->').replace('≥','>=').replace('·','/').replace('−','-').replace('³','3').replace('²','2')
def T(kind,x,y,value,size=9):
 return f'T~{kind}~{x}~{y}~0~#18384c~Arial~{size}pt~~~~comment~{asc(value)}~1~start~{gid()}~0~'
def P(number,name,x,y,side):
 length=20 if side=='left' else -20;tx=x+24 if side=='left' else x-24;anchor='start' if side=='left' else 'end';rot=180 if side=='left' else 0
 return f'P~show~0~{number}~{x}~{y}~{rot}~{gid()}~0^^{x}~{y}^^M {x} {y} h {length}~#537080^^1~{tx}~{y+2}~0~{asc(name)}~{anchor}~Arial~5pt~#274b62^^1~{x+length/2}~{y-3}~0~{number}~middle~Arial~5pt~#567786^^0~{x+length}~{y}^^0~M {x+length} {y}'
# Category columns keep power on the left, host/sensors central, breadboard components on right.
groups=[[],[],[],[],[],[]]
for c in C:
 if not c['pins']:continue
 r=c['ref']
 idx=0 if r in ['BT1','F0','S0','X24','X0','K1','F1','F2'] else 1 if r in ['MDL','MDR','ML','MR','F3','F4','DC1','DC2'] else 2 if c['page']=='power' else 3 if r in ['OP1','H1','U1'] else 4 if c['page']=='signal' else 5
 groups[idx].append(c)
layouts=[]
for col,cs in enumerate(groups):
 y=130
 for c in cs:
  h=max(90,((len(c['pins'])+1)//2)*18+46);x=180+col*650
  layouts.append((c,x,y,h));y+=h+95
maxh=max(y+h for _,x,y,h in layouts)+100
shapes=[T('L',35,35,'SMART CART B1 / MODULE + BREADBOARD ELECTRICAL SCHEMATIC',18),T('L',35,65,'No PCB. Same-name net labels are connected. Confirm all physical pin names against purchased modules.',10),T('L',35,89,'* Fuse ratings and power components are provisional. USB cables and powered hub are black-box assemblies.',10)]
# Conventional SVG preview for offline verification of the symbolic export.
sv=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4020 {maxh+50}" width="4020" height="{maxh+50}"><rect width="4020" height="{maxh+50}" fill="white"/><g font-family="Arial,sans-serif">']
sv.append('<text x="35" y="40" font-size="23" fill="#173c4b">SMART CART B1 / Electrical module schematic</text>')
expected=[]
for c,x,y,h in layouts:
 ref=c['ref'];w=220;cy=y+h/2;half=(len(c['pins'])+1)//2
 subs=[T('P',x+8,y+17,ref,10),T('N',x+8,y+32,c['spec'],7)]
 subs.append(f'R~{x}~{y}~~~{w}~{h}~#385c70~1~0~#f4f9fb~{gid()}~0~')
 # Draw rectangle first so it does not cover the reference/value text.
 subs=subs[-1:]+subs[:-1]
 sv.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f4f9fb" stroke="#355c70"/><text x="{x+8}" y="{y+17}" font-size="13" fill="#173c4b">{ref}</text><text x="{x+8}" y="{y+32}" font-size="8" fill="#37596c">{html.escape(asc(c["spec"]))}</text>')
 outside=[]
 for i,p in enumerate(c['pins']):
  side='left' if i<half else 'right';row=i if i<half else i-half;py=y+49+row*18;px=x-20 if side=='left' else x+w+20
  subs.append(P(p['number'],p['name'],px,py,side))
  endx=px-103 if side=='left' else px+103
  outside.append(f'W~{px} {py} {endx} {py}~#008800~1~0~none~{gid()}~0')
  anchor='end' if side=='left' else 'start';textx=endx-3 if side=='left' else endx+3
  outside.append(f'N~{endx}~{py}~0~#174c72~{p["net"]}~{gid()}~{anchor}~{textx}~{py-3}~Arial~6pt~0')
  expected.append({'ref':ref,'pin':p['number'],'name':p['name'],'net':p['net'],'xy':[px,py]})
  sv.append(f'<path d="M{px+(20 if side=="left" else -20)} {py}H{endx}" fill="none" stroke="#318472"/><text x="{textx}" y="{py-3}" text-anchor="{anchor}" font-size="8" fill="#155471">{p["net"]}</text>')
  tx=px+24 if side=='left' else px-24
  sv.append(f'<text x="{tx}" y="{py+2}" text-anchor="'+('start' if side=='left' else 'end')+f'" font-size="7" fill="#335361">{html.escape(asc(p["name"]))}</text>')
 libheader=f'LIB~{x+w/2}~{cy}~package``Contributor`SmartCart`spicePre`U`spiceSymbolName`{ref}`nameAlias`Value`~0~0~{gid()}~~{U(ref)}~0~~no~yes'
 shapes.append(libheader+'#@$'+'#@$'.join(subs));shapes.extend(outside)
sv.append('</g></svg>')
eda={'head':{'docType':'1','editorVersion':'6.5.51','newgId':True,'c_para':{'name':'SmartCart-B1-Modules'},'x':0,'y':0,'uuid':U('schematic')},'canvas':f'CA~4020~{maxh+50}~#FFFFFF~yes~#D5DFE5~5~4020~{maxh+50}~line~5~pixel~5~0~0','shape':shapes,'BBox':{'x':0,'y':0,'width':4020,'height':maxh+50},'colors':{}}
(ROOT/'eda/easyeda/SmartCart-B1-Modules.json').write_text(json.dumps(eda,ensure_ascii=False,indent=2))
(ROOT/'eda/SmartCart-B1-symbolic.svg').write_text(''.join(sv))
(ROOT/'eda/expected-terminals.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2))
# KiCad 5.1 / legacy: one self-contained cached library and a 6-column A0 schematic.
lib=['EESchema-LIBRARY Version 2.4','#encoding utf-8']
sch=['EESchema Schematic File Version 4','LIBS:SmartCart-cache','EELAYER 29 0','EELAYER END','$Descr A0 46811 33110','encoding utf-8','Sheet 1 1','Title "Smart Cart B1 - Module wiring, no PCB"','Date "2026-09-13"','Rev "B1"','Comp "Smart-Cart capstone"','Comment1 "Reference pins are module terminals; footprints intentionally unassigned."','Comment2 "Fuse ratings provisional; external power and braking require validation."','Comment3 "See breadboard-contacts.csv for physical tie points."','Comment4 "Single-channel contactor circuit is not safety-certified."','$EndDescr']
for c,x,y,h in layouts:
 ref=c['ref'];symbol='Module_'+ref;xc=round((x+110)*10);yc=round((y+h/2)*10);hh=round(h*5);half=(len(c['pins'])+1)//2
 lib+=['#','# '+symbol,'#',f'DEF {symbol} U 0 20 Y Y 1 F N',f'F0 "U" 0 {hh+150} 50 H V C CNN',f'F1 "{asc(c["spec"])}" 0 {hh+75} 45 H V C CNN','DRAW',f'S -1100 {hh} 1100 {-hh} 0 1 10 f']
 sch+=['$Comp',f'L SmartCart:{symbol} {ref}',f'U 1 1 {U(ref)[:8].upper()}',f'P {xc} {yc}',f'F 0 "{ref}" H {xc} {yc-hh-180} 60 0000 C CNN',f'F 1 "{asc(c["spec"])}" H {xc} {yc-hh-80} 45 0000 C CNN',f'F 2 "" H {xc} {yc} 50 0001 C CNN',f'F 3 "" H {xc} {yc} 50 0001 C CNN',f'\t1 {xc} {yc}','\t1 0 0 -1','$EndComp']
 for i,p in enumerate(c['pins']):
  side='left' if i<half else 'right';row=i if i<half else i-half;py=round((y+49+row*18)*10);lx=-1300 if side=='left' else 1300;ly=yc-py;ori='R' if side=='left' else 'L'
  pn=asc(p['name']).replace(' ','_').replace('/','_')
  lib.append(f'X {pn} {p["number"]} {lx} {ly} 200 {ori} 38 38 1 1 P')
  px=xc+lx;end=px+(-1030 if side=='left' else 1030)
  sch+=['Wire Wire Line',f'\t{px} {py} {end} {py}',f'Text Label {end} {py} 0 40 ~ 0',p['net']]
 lib+=['ENDDRAW','ENDDEF']
lib+=['#','#End Library'];sch+=['$EndSCHEMATC']
kdir=ROOT/'eda/kicad';(kdir/'SmartCart.sch').write_text('\n'.join(sch)+'\n');(kdir/'SmartCart-cache.lib').write_text('\n'.join(lib)+'\n');(kdir/'SmartCart.lib').write_text('\n'.join(lib)+'\n')
(kdir/'sym-lib-table').write_text('(sym_lib_table\n (lib (name SmartCart)(type Legacy)(uri ${KIPRJMOD}/SmartCart.lib)(options "")(descr "Self-contained Smart Cart module terminals"))\n)\n')
(kdir/'SmartCart.pro').write_text('update=2026-09-13\nversion=1\nlast_client=eeschema\n[eeschema]\nversion=1\nLibDir=\n[eeschema/libraries]\nLibName1=SmartCart\n')
# Generic XML terminal netlist, deliberately not SPICE (boards are external assemblies).
from xml.etree.ElementTree import Element,SubElement,ElementTree
ex=Element('export',version='D');de=SubElement(ex,'design');SubElement(de,'source').text='SmartCart.sch';SubElement(de,'date').text='2026-09-13';SubElement(de,'tool').text='SmartCart B1 generator'
cs=SubElement(ex,'components')
for c in C:
 if not c['pins']:continue
 comp=SubElement(cs,'comp',ref=c['ref']);SubElement(comp,'value').text=asc(c['spec']);SubElement(comp,'footprint').text='';SubElement(comp,'libsource',lib='SmartCart',part='Module_'+c['ref'],description=c['name'])
ns=SubElement(ex,'nets');nets={}
for p in expected:nets.setdefault(p['net'],[]).append(p)
for i,(name,ps) in enumerate(sorted(nets.items()),1):
 n=SubElement(ns,'net',code=str(i),name=name)
 for p in ps:SubElement(n,'node',ref=p['ref'],pin=p['pin'])
ElementTree(ex).write(ROOT/'eda/SmartCart-B1.net',encoding='utf-8',xml_declaration=True)
print('EDA files written:',len(layouts),'symbols,',len(expected),'pins,',len(nets),'nets')
