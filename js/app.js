/* Offline, dependency-free SVG drawing viewer. Does not simulate or control a cart. */
'use strict';
(() => {
  const data = window.CART_DESIGN;
  const sheets = window.CART_DRAWINGS;
  const byRef = new Map(data.components.map(c => [c.ref, c]));
  const stage = document.getElementById('stage');
  const host = document.getElementById('svg-host');
  const tabs = document.getElementById('sheet-tabs');
  const inspector = document.getElementById('inspector');
  const content = document.getElementById('inspect-content');
  let current = 0, svg, selected = null;
  const initial = {x:30,y:168,w:2040,h:1198};
  let view = {...initial};
  const pointers = new Map();
  let drag = null, pinch = null, moved = false;
  const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const netMembers = net => data.components.flatMap(c => c.pins.filter(p => p.net === net).map(p => ({ref:c.ref,name:p.name})));
  function applyView(){
    svg.setAttribute('viewBox', `${view.x} ${view.y} ${view.w} ${view.h}`);
    document.getElementById('zoom-value').textContent = `${Math.round(initial.w/view.w*100)}%`;
  }
  function fit(){ view={...initial}; applyView(); }
  function stagePoint(clientX,clientY){
    const point = svg.createSVGPoint(); point.x=clientX; point.y=clientY;
    return point.matrixTransform(svg.getScreenCTM().inverse());
  }
  function zoom(factor,clientX,clientY){
    const target = Math.min(initial.w*2.5,Math.max(initial.w/5.5,view.w/factor));
    const p = clientX === undefined ? {x:view.x+view.w/2,y:view.y+view.h/2} : stagePoint(clientX,clientY);
    const f=target/view.w;
    view={x:p.x-(p.x-view.x)*f,y:p.y-(p.y-view.y)*f,w:target,h:view.h*f};applyView();
  }
  function clearSelection(){
    selected=null;inspector.hidden=true;
    svg.querySelectorAll('.component,.wire').forEach(el=>el.classList.remove('selected','dim'));
  }
  function highlight(nets,ref){
    svg.querySelectorAll('.component').forEach(el=>el.classList.toggle('selected',el.dataset.ref===ref));
    const set=new Set(nets);
    svg.querySelectorAll('.wire').forEach(el=>{
      const match=(el.dataset.nets||'').split(' ').some(n=>set.has(n));
      el.classList.toggle('selected',match);el.classList.toggle('dim',set.size>0&&!match);
    });
  }
  function inspectComponent(ref){
    const c=byRef.get(ref);if(!c)return;
    selected=ref;highlight(c.pins.map(p=>p.net),ref);
    document.getElementById('inspect-label').textContent='COMPONENT / TERMINALS';
    const status={reference:'기준 모듈',candidate:'실제 모델·정격 확정 필요',conditional:'적합성 검증 후 사용'}[c.status]||c.status;
    content.innerHTML=`<div class="inspect-ref">${esc(c.ref)}</div><h1 class="inspect-title">${esc(c.name)}</h1><p class="inspect-spec">${esc(c.spec)}</p><span class="tag-status ${esc(c.status)}">${esc(status)}</span><p class="inspect-note">${esc(c.notes)}</p>`;
    if(c.pins.length)content.innerHTML+=`<table class="pin-table"><thead><tr><th>실제 단자명</th><th>연결 네트</th></tr></thead><tbody>${c.pins.map(p=>`<tr data-net="${esc(p.net)}"><td>${esc(p.name)}</td><td>${esc(p.net)}</td></tr>`).join('')}</tbody></table>`;
    else if(ref==='BB1')content.innerHTML+='<p class="inspect-note">브레드보드 시트에서 접점을 선택하면 홀 번호와 연결 네트를 확인할 수 있습니다.</p>';
    content.querySelectorAll('[data-net]').forEach(row=>row.addEventListener('click',()=>inspectNet(row.dataset.net)));
    inspector.hidden=false;inspector.scrollTop=0;
  }
  function inspectNet(net){
    if(!net)return;highlight([net]);selected=net;
    document.getElementById('inspect-label').textContent='NET / CONNECTIONS';
    const members=netMembers(net);
    content.innerHTML=`<div class="inspect-ref">NET</div><h1 class="inspect-title">${esc(net)}</h1><p class="inspect-note">같은 이름의 네트에 속한 단자입니다. 퓨즈·저항·스위치 양단은 서로 다른 네트로 구분합니다.</p><table class="pin-table"><thead><tr><th>부품</th><th>단자</th></tr></thead><tbody>${members.map(m=>`<tr data-ref="${esc(m.ref)}"><td>${esc(m.ref)}</td><td>${esc(m.name)}</td></tr>`).join('')}</tbody></table>`;
    content.querySelectorAll('[data-ref]').forEach(el=>el.addEventListener('click',()=>inspectComponent(el.dataset.ref)));
    inspector.hidden=false;inspector.scrollTop=0;
  }
  function inspectHole(hole){
    const d=data.breadboard.contacts[hole];
    document.getElementById('inspect-label').textContent='BREADBOARD / TIE POINT';
    if(d)highlight([d.net]);else highlight([]);
    const rail=/^[TB][+-]/.test(hole);const row=hole[0];const num=Number(hole.replace(/[^0-9]/g,''));
    const group=rail?`${hole.slice(0,2)} 레일 1-25`:`${'abcde'.includes(row)?'a-e':'f-j'} ${num}번 스트립`;
    content.innerHTML=`<div class="inspect-ref">${esc(hole)}</div><h1 class="inspect-title">${esc(group)}</h1><p class="inspect-spec">${esc(d?.net||'미사용 접점')}</p><p class="inspect-note">${esc(d?.owner||'이 접점에는 부품 리드나 점퍼가 지정되지 않았습니다.')}<br>실물 브레드보드의 레일 분할 여부를 무전원 도통 검사로 확인하세요.</p>`;
    const peers=Object.entries(data.breadboard.contacts).filter(([h])=>rail?h.startsWith(hole.slice(0,2)):Number(h.replace(/[^0-9]/g,''))===num&&!/^[TB]/.test(h)&&'abcde'.includes(h[0])==='abcde'.includes(row));
    content.innerHTML+=`<table class="pin-table"><thead><tr><th>같은 도체의 접점</th><th>삽입 리드</th></tr></thead><tbody>${peers.map(([h,v])=>`<tr><td>${esc(h)}</td><td>${esc(v.owner)}</td></tr>`).join('')}</tbody></table>`;
    inspector.hidden=false;inspector.scrollTop=0;
  }
  function showSheet(index){
    current=index;host.innerHTML=sheets[index].svg;svg=host.querySelector('svg');svg.removeAttribute('width');svg.removeAttribute('height');svg.setAttribute('preserveAspectRatio','xMidYMin meet');
    tabs.querySelectorAll('.tab').forEach((t,i)=>t.setAttribute('aria-selected',String(i===index)));
    clearSelection();fit();
    document.getElementById('status-text').textContent=index===3?'상부 + 3.3V / 하부 + 5V · 두 −레일만 공통':'외형 비축척 · 브레드보드는 소신호 실험용 · * 퓨즈값 검토 필요';
  }
  sheets.forEach((s,i)=>{
    const b=document.createElement('button');b.className='tab';b.setAttribute('role','tab');b.setAttribute('aria-selected','false');b.innerHTML=`<span class="tab-number">0${i+1}</span>${esc(s.short)}`;b.addEventListener('click',()=>showSheet(i));tabs.append(b);
  });
  stage.addEventListener('wheel',ev=>{ev.preventDefault();zoom(Math.exp(-ev.deltaY*.0014),ev.clientX,ev.clientY);},{passive:false});
  stage.addEventListener('pointerdown',ev=>{
    if(ev.button!==0)return;stage.setPointerCapture(ev.pointerId);pointers.set(ev.pointerId,{x:ev.clientX,y:ev.clientY});moved=false;
    if(pointers.size===1){drag={point:stagePoint(ev.clientX,ev.clientY),view:{...view},x:ev.clientX,y:ev.clientY,target:ev.target};stage.classList.add('panning');}
    else if(pointers.size===2){const p=[...pointers.values()];pinch={distance:Math.hypot(p[1].x-p[0].x,p[1].y-p[0].y)};drag=null;moved=true;}
  });
  stage.addEventListener('pointermove',ev=>{
    if(!pointers.has(ev.pointerId))return;pointers.set(ev.pointerId,{x:ev.clientX,y:ev.clientY});
    if(pointers.size===2&&pinch){const p=[...pointers.values()];const dist=Math.hypot(p[1].x-p[0].x,p[1].y-p[0].y);zoom(dist/Math.max(1,pinch.distance),(p[1].x+p[0].x)/2,(p[1].y+p[0].y)/2);pinch.distance=dist;moved=true;}
    else if(drag){
      if(Math.hypot(ev.clientX-drag.x,ev.clientY-drag.y)>4)moved=true;
      const p=stagePoint(ev.clientX,ev.clientY);view.x+=drag.point.x-p.x;view.y+=drag.point.y-p.y;applyView();
    }
  });
  stage.addEventListener('pointerup',ev=>{
    const target=drag?.target;
    if(!moved&&target){const hole=target.closest('.hole');const component=target.closest('.component');const wire=target.closest('.wire');if(hole)inspectHole(hole.dataset.hole);else if(component)inspectComponent(component.dataset.ref);else if(wire){const nets=(wire.dataset.nets||'').split(' ').filter(Boolean);if(nets.length)inspectNet(nets[0]);}else clearSelection();}
    pointers.delete(ev.pointerId);drag=null;pinch=null;stage.classList.remove('panning');
  });
  stage.addEventListener('pointercancel',ev=>{pointers.delete(ev.pointerId);drag=null;pinch=null;stage.classList.remove('panning');});
  stage.addEventListener('keydown',ev=>{const c=ev.target.closest('.component');if(c&&['Enter',' '].includes(ev.key)){ev.preventDefault();inspectComponent(c.dataset.ref);}});
  document.getElementById('zoom-in').addEventListener('click',()=>zoom(1.3));document.getElementById('zoom-out').addEventListener('click',()=>zoom(1/1.3));document.getElementById('fit').addEventListener('click',fit);document.getElementById('close-inspector').addEventListener('click',clearSelection);
  document.addEventListener('keydown',ev=>{if(['INPUT','TEXTAREA'].includes(ev.target.tagName))return;if(ev.key==='Escape')clearSelection();if(ev.key==='0')fit();if(ev.key==='+')zoom(1.2);if(ev.key==='-')zoom(1/1.2);});
  document.getElementById('save-svg').addEventListener('click',()=>{const blob=new Blob([sheets[current].svg],{type:'image/svg+xml;charset=utf-8'});downloadBlob(blob,`Smart-Cart-${sheets[current].id}.svg`);});
  function downloadBlob(blob,name){const a=document.createElement('a');const url=URL.createObjectURL(blob);a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),3000);}
  if(window.CART_EMBEDDED_DOWNLOADS){document.querySelectorAll('[data-download]').forEach(a=>{a.addEventListener('click',ev=>{ev.preventDefault();const d=window.CART_EMBEDDED_DOWNLOADS[a.dataset.download];const bytes=Uint8Array.from(atob(d.base64),c=>c.charCodeAt(0));downloadBlob(new Blob([bytes],{type:d.type}),d.name);});});}
  showSheet(0);
  // Read-only diagnostics for smoke tests; no device-control API is exposed.
  window.CartWiringViewer={getState:()=>({sheet:current,view:{...view},selected}),select:inspectComponent,showSheet};
})();
