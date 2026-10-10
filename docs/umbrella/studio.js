import * as THREE from './vendor/three.module.min.js';

const $ = (id) => document.getElementById(id);
const canvas = $('render');
const stage = $('stage');
const clamp = THREE.MathUtils.clamp;
const TAU = Math.PI * 2;
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const state = { free: false, rotating: false, theme: 'day', preset: 'outside', ready: false };
const orbit = { az: .68, el: .48, distance: 1.97, target: new THREE.Vector3(0, .21, 0) };
let renderer, scene, camera, floor, contact, model, keyLight, fillLight, rimLight, environment;
let needsRender = true, transition = null, lastTime = 0, toastTimer;
const pointers = new Map();
const keys = new Set();
const presets = {
  outside: { az: .68, el: .48, distance: 1.97, target: [0, .21, 0] },
  inside: { az: .3, el: -1.05, distance: 1.95, target: [0, .42, 0] },
  top: { az: 0, el: 1.54, distance: 2.05, target: [0, .46, 0] },
  detail: { az: .5, el: .08, distance: .52, target: [0, -.10, 0] },
};

function notify(message) {
  $('toast').textContent = message;
  $('toast').classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => $('toast').classList.remove('show'), 3000);
}
function fail(message) {
  $('loading').classList.add('done');
  $('fallback').hidden = false;
  $('fallback-message').textContent = message;
  document.querySelectorAll('button').forEach(b => b.disabled = true);
}
function mesh(geometry, material, parent = model) {
  const m = new THREE.Mesh(geometry, material);
  m.castShadow = true;
  m.receiveShadow = true;
  parent.add(m);
  return m;
}
function tube(points, radius, material, segments = 48) {
  return mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points), segments, radius, 6, false), material);
}
function link(a, b, radius, material) {
  const d = b.clone().sub(a);
  const m = mesh(new THREE.CylinderGeometry(radius, radius, d.length(), 10), material);
  m.position.copy(a).add(b).multiplyScalar(.5);
  m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), d.normalize());
  return m;
}
function surface(k, t, f, underside = false) {
  const angle = Math.PI / 2 + (k + f - .5) * TAU / 8;
  // The hem is pulled inward between the ribs, with a slight fabric sag.
  const scallop = 1 - .035 * Math.sin(Math.PI * f) ** 2 * t ** 7;
  const r = .48 * t * scallop;
  const y = .42 + .16 * (1 - t * t) - .013 * Math.sin(Math.PI * f) * t ** 1.7;
  return new THREE.Vector3(r * Math.cos(angle), y - (underside ? .0018 : 0), r * Math.sin(angle));
}
function panelGeometry(k, inside = false) {
  const positions = [], uvs = [], indices = [];
  const rings = 44, steps = 28;
  for (let j = 0; j <= rings; j++) {
    const t = Math.max(.001, j / rings);
    for (let i = 0; i <= steps; i++) {
      const f = i / steps;
      const p = surface(k, t, f, inside);
      positions.push(p.x, p.y, p.z);
      // Flat, triangular print coordinates preserve letter shapes across tapered gores.
      uvs.push(.5 + (inside ? 1 : -1) * (f - .5) * t, 1 - t);
    }
  }
  for (let j = 0; j < rings; j++) for (let i = 0; i < steps; i++) {
    const a = j * (steps + 1) + i, b = a + steps + 1;
    if (inside) indices.push(a, b, a + 1, b, b + 1, a + 1);
    else indices.push(a, a + 1, b, b, a + 1, b + 1);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
  g.setAttribute('uv', new THREE.Float32BufferAttribute(uvs, 2));
  g.setIndex(indices);
  g.computeVertexNormals();
  return g;
}
function fabricTexture() {
  const c = document.createElement('canvas'); c.width = c.height = 128;
  const ctx = c.getContext('2d');
  const pixels = ctx.createImageData(128, 128);
  for (let y = 0; y < 128; y++) for (let x = 0; x < 128; x++) {
    const v = 120 + ((x % 4 < 2) !== (y % 4 < 2) ? 25 : -25);
    const i = (y * 128 + x) * 4;
    pixels.data.set([v, v, v, 255], i);
  }
  ctx.putImageData(pixels, 0, 0);
  const t = new THREE.CanvasTexture(c);
  t.wrapS = t.wrapT = THREE.RepeatWrapping;
  t.repeat.set(10, 14);
  return t;
}
function makeEnvironment() {
  const c = document.createElement('canvas'); c.width = 512; c.height = 256;
  const x = c.getContext('2d');
  const g = x.createLinearGradient(0, 0, 0, 256);
  g.addColorStop(0, '#faf6ed'); g.addColorStop(.5, '#b5b6be'); g.addColorStop(1, '#525461');
  x.fillStyle = g; x.fillRect(0, 0, 512, 256);
  x.fillStyle = '#ffffff'; x.fillRect(75, 45, 75, 95); x.fillRect(350, 55, 40, 100);
  const t = new THREE.CanvasTexture(c); t.mapping = THREE.EquirectangularReflectionMapping; t.colorSpace = THREE.SRGBColorSpace;
  const pmrem = new THREE.PMREMGenerator(renderer);
  const result = pmrem.fromEquirectangular(t);
  t.dispose(); pmrem.dispose();
  return result;
}
async function buildModel() {
  const loader = new THREE.TextureLoader();
  const urls = [...Array.from({length:4}, (_,i) => `assets/out-${i}.png`), ...Array.from({length:8}, (_,i) => `assets/in-${i}.png`)];
  const textures = await Promise.all(urls.map(url => loader.loadAsync(url)));
  textures.forEach(t => { t.colorSpace = THREE.SRGBColorSpace; t.anisotropy = Math.min(8, renderer.capabilities.getMaxAnisotropy()); });
  const fabric = fabricTexture();
  for (let k = 0; k < 8; k++) {
    const outer = new THREE.MeshPhysicalMaterial({ map: textures[k % 4], roughness: .76, metalness: 0, bumpMap: fabric, bumpScale: .00024, sheen: .12, sheenRoughness: .8, sheenColor: new THREE.Color('#eaa9af'), envMapIntensity: .24 });
    const inner = new THREE.MeshStandardMaterial({ map: textures[4+k], roughness: .95, bumpMap: fabric, bumpScale: .00018, envMapIntensity: .22 });
    mesh(panelGeometry(k), outer);
    mesh(panelGeometry(k, true), inner);
  }
  const rib = new THREE.MeshStandardMaterial({color:'#56606b', roughness:.78, metalness:.12});
  const support = new THREE.MeshStandardMaterial({color:'#727984', roughness:.68, metalness:.2});
  const runnerY = .355;
  const seam = new THREE.MeshStandardMaterial({color:'#bf4b5d', roughness:.9});
  const hem = new THREE.MeshStandardMaterial({color:'#d66b79', roughness:.9});
  const metal = new THREE.MeshStandardMaterial({color:'#6b727b', roughness:.26, metalness:.87, envMapIntensity:.8});
  const ink = new THREE.MeshStandardMaterial({color:'#162238', roughness:.62, metalness:.08});
  for (let k = 0; k < 8; k++) {
    const upper = [], lower = [], edge = [];
    for (let j = 0; j <= 40; j++) {
      const p = surface(k, j/40, 0);
      upper.push(p.clone().add(new THREE.Vector3(0,.0007,0)));
      lower.push(p.clone().add(new THREE.Vector3(0,-.0034,0)));
      edge.push(surface(k, 1, j/40));
    }
    tube(upper, .0008, seam);
    tube(lower, .0014, rib);
    tube(edge, .0018, hem);
    const anchor = surface(k, .60, 0, true).add(new THREE.Vector3(0,-.0048,0));
    link(new THREE.Vector3(0,runnerY,0), anchor, .00115, support);
    const end = mesh(new THREE.CapsuleGeometry(.003, .008, 4, 10), ink);
    end.position.copy(surface(k,1,0));
    const a = Math.PI/2 + (k-.5)*TAU/8;
    end.rotation.z = Math.PI/2; end.rotation.y = -a;
    const joint = mesh(new THREE.SphereGeometry(.0028, 10, 8), support); joint.position.copy(anchor);
  }
  // Three telescoping shaft sections and the runner beneath the rib supports.
  for (const [radius, length, y] of [[.006,.24,.44],[.0068,.19,.225],[.0077,.17,.045]]) {
    mesh(new THREE.CylinderGeometry(radius,radius,length,24),metal).position.y=y;
  }
  mesh(new THREE.CylinderGeometry(.011,.010,.032,24),ink).position.y=runnerY;
  mesh(new THREE.CylinderGeometry(.009,.009,.013,24),metal).position.y=-.005;
  mesh(new THREE.CapsuleGeometry(.022,.105,8,32),ink).position.y=-.10;
  const gripSeam = mesh(new THREE.TorusGeometry(.0221,.0006,6,40),rib); gripSeam.rotation.x=Math.PI/2; gripSeam.position.y=-.146;
  const button = mesh(new THREE.CapsuleGeometry(.009,.008,6,16),metal); button.position.set(0,-.067,.020); button.scale.z=.30;
  const buttonInset = mesh(new THREE.CapsuleGeometry(.0067,.006,6,16),ink); buttonInset.position.set(0,-.067,.023); buttonInset.scale.z=.2;
  mesh(new THREE.CapsuleGeometry(.0055,.024,5,16),ink).position.y=.597;
  const loop = [];
  for(let i=0;i<=48;i++){const t=i/48*TAU;loop.push(new THREE.Vector3(.017*Math.sin(t),-.195+.029*Math.cos(t),.004*Math.sin(2*t)));}
  tube(loop,.0015,ink);
  model.rotation.y = 0;
}
function makeFloor() {
  floor = new THREE.Group(); scene.add(floor);
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(200,200),new THREE.ShadowMaterial({color:'#746455',opacity:.035}));
  shadow.rotation.x = -Math.PI/2; shadow.position.y=-.265; shadow.receiveShadow=true; shadow.visible=false; floor.add(shadow);
  const c=document.createElement('canvas');c.width=c.height=128;
  const x=c.getContext('2d'),g=x.createRadialGradient(64,64,5,64,64,64);g.addColorStop(0,'rgba(65,52,43,.16)');g.addColorStop(.4,'rgba(65,52,43,.08)');g.addColorStop(1,'rgba(65,52,43,0)');x.fillStyle=g;x.fillRect(0,0,128,128);
  contact=new THREE.Mesh(new THREE.PlaneGeometry(.65,.65),new THREE.MeshBasicMaterial({map:new THREE.CanvasTexture(c),transparent:true,depthWrite:false}));
  contact.rotation.x=-Math.PI/2;contact.position.y=-.264;floor.add(contact);
}
function updateCamera() {
  const c = Math.cos(orbit.el);
  camera.position.set(orbit.target.x + orbit.distance*c*Math.sin(orbit.az),orbit.target.y+orbit.distance*Math.sin(orbit.el),orbit.target.z+orbit.distance*c*Math.cos(orbit.az));
  camera.lookAt(orbit.target);
  floor.visible = !state.free && orbit.el > -.08 && orbit.target.y > -.2;
  needsRender = true;
}
function resize() {
  if(!renderer)return;
  const w=stage.clientWidth,h=stage.clientHeight;
  if(!w||!h)return;
  renderer.setPixelRatio(Math.min(devicePixelRatio||1,2));renderer.setSize(w,h,false);
  camera.aspect=w/h;
  camera.fov=2*Math.atan(Math.tan(18*Math.PI/180)/Math.min(1,camera.aspect/.95))*180/Math.PI;
  camera.updateProjectionMatrix();needsRender=true;
}
function autoRotate(enabled) {
  state.rotating=enabled;
  $('rotate').setAttribute('aria-checked',String(enabled));
}
function preset(name, immediate=false) {
  const p=presets[name];state.preset=name;autoRotate(false);
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===name)));
  const dest={az:p.az,el:p.el,distance:p.distance,target:new THREE.Vector3(...p.target)};
  // Take the short way around the canopy when changing views.
  while(dest.az-orbit.az>Math.PI)dest.az-=TAU;
  while(dest.az-orbit.az< -Math.PI)dest.az+=TAU;
  if(immediate||reducedMotion){Object.assign(orbit,dest);transition=null;updateCamera();}
  else transition={start:performance.now(),from:{...orbit,target:orbit.target.clone()},to:dest};
}
function freeMode(enabled) {
  state.free=enabled;document.body.classList.toggle('free-mode',enabled);
  transition=null;keys.clear();autoRotate(false);
  if(!enabled)preset(state.preset,true);
  resize();updateCamera();
  if(enabled)canvas.focus({preventScroll:true});else $('enter-free').focus({preventScroll:true});
}
function lighting(theme) {
  state.theme=theme;document.body.dataset.theme=theme;
  document.querySelectorAll('[data-light]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.light===theme)));
  const night=theme==='night';
  keyLight.color.set(night?'#e0e8ff':'#fff1df');keyLight.intensity=night?1.65:2.0;
  fillLight.color.set(night?'#a6befa':'#eef3ff');fillLight.intensity=night?.65:.65;
  rimLight.color.set(night?'#ecbdca':'#fff3e8');rimLight.intensity=night?1.4:1.1;
  scene.environmentIntensity=night?.36:.45;
  needsRender=true;
}
function pan(dx,dy) {
  camera.updateMatrixWorld();
  const right=new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld,0);
  const up=new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld,1);
  const scale=2*orbit.distance*Math.tan(camera.fov*Math.PI/360)/Math.max(stage.clientHeight,1);
  orbit.target.addScaledVector(right,-dx*scale).addScaledVector(up,dy*scale);
  updateCamera();
}
function bindInputs() {
  canvas.addEventListener('contextmenu',e=>e.preventDefault());
  canvas.addEventListener('pointerdown',e=>{transition=null;autoRotate(false);canvas.focus({preventScroll:true});canvas.setPointerCapture(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY,button:e.button});});
  canvas.addEventListener('pointermove',e=>{
    const old=pointers.get(e.pointerId);if(!old)return;
    const before=[...pointers.values()];
    const dx=e.clientX-old.x,dy=e.clientY-old.y;
    pointers.set(e.pointerId,{x:e.clientX,y:e.clientY,button:old.button});
    if(pointers.size===2){
      const after=[...pointers.values()];
      const d0=Math.hypot(before[0].x-before[1].x,before[0].y-before[1].y);
      const d1=Math.hypot(after[0].x-after[1].x,after[0].y-after[1].y);
      if(d0>0&&d1>0)orbit.distance=clamp(orbit.distance*d0/d1,.12,8);
      pan(dx/2,dy/2);
    }else if(pointers.size===1){
      if(old.button===2||e.shiftKey)pan(dx,dy);
      else{orbit.az-=dx*.006;orbit.el=clamp(orbit.el+dy*.006,-Math.PI/2+.01,Math.PI/2-.01);}
    }
    updateCamera();
  });
  const release=e=>pointers.delete(e.pointerId);
  canvas.addEventListener('pointerup',release);canvas.addEventListener('pointercancel',release);canvas.addEventListener('lostpointercapture',release);
  canvas.addEventListener('wheel',e=>{e.preventDefault();transition=null;autoRotate(false);orbit.distance=clamp(orbit.distance*Math.exp(clamp(e.deltaY,-150,150)*.0012),.12,8);updateCamera();},{passive:false});
  addEventListener('keydown',e=>{
    if(e.key==='Escape'&&state.free){freeMode(false);return;}
    if(document.activeElement!==canvas)return;
    const key=e.key.toLowerCase();
    if(['w','a','s','d','q','e','arrowleft','arrowright','arrowup','arrowdown','shift','r','+','-','='].includes(key)){
      e.preventDefault();transition=null;autoRotate(false);
      if(key==='r')preset(state.free?'outside':state.preset);
      else keys.add(key);
    }
  });
  addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));
  addEventListener('blur',()=>{keys.clear();pointers.clear();});
  canvas.addEventListener('blur',()=>keys.clear());
  document.addEventListener('visibilitychange',()=>{keys.clear();lastTime=performance.now();});
  document.querySelectorAll('[data-view]').forEach(b=>b.addEventListener('click',()=>preset(b.dataset.view)));
  document.querySelectorAll('[data-light]').forEach(b=>b.addEventListener('click',()=>lighting(b.dataset.light)));
  $('rotate').addEventListener('click',()=>{transition=null;autoRotate(!state.rotating);});
  $('reset').addEventListener('click',()=>preset(state.preset));
  $('free-reset').addEventListener('click',()=>{preset('outside');canvas.focus({preventScroll:true});});
  $('enter-free').addEventListener('click',()=>freeMode(true));$('exit-free').addEventListener('click',()=>freeMode(false));
  $('fullscreen').addEventListener('click',async()=>{
    try{if(document.fullscreenElement)await document.exitFullscreen();else{freeMode(true);if(stage.requestFullscreen)await stage.requestFullscreen();}}catch{notify('Free cam is ready. Browser fullscreen is unavailable.');}
  });
  document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement&&state.free)freeMode(false);resize();});
  $('exit-free').addEventListener('click',()=>{if(document.fullscreenElement)document.exitFullscreen().catch(()=>{});});
  $('save').addEventListener('click',()=>{
    // Render the current framing on a solid studio background for a clean, portable PNG.
    const background=scene.background;scene.background=new THREE.Color(state.theme==='night'?'#151d2a':'#f4f1ec');renderer.render(scene,camera);
    canvas.toBlob(blob=>{if(!blob){notify('Could not save the image. Try again.');return;}const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`RainBorrow-${state.preset}.png`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);notify('View saved as a PNG.');},'image/png');
    scene.background=background;needsRender=true;
  });
  canvas.addEventListener('webglcontextlost',e=>{e.preventDefault();fail('The graphics connection was interrupted. Reload this page to restart the 3D viewer.');});
}
function frame(now) {
  requestAnimationFrame(frame);
  if(document.hidden)return;
  const dt=Math.min((now-lastTime)/1000,.05);lastTime=now;
  if(transition){const t=clamp((now-transition.start)/750,0,1),e=t*t*(3-2*t);for(const key of ['az','el','distance'])orbit[key]=THREE.MathUtils.lerp(transition.from[key],transition.to[key],e);orbit.target.lerpVectors(transition.from.target,transition.to.target,e);updateCamera();if(t===1)transition=null;}
  if(state.rotating){orbit.az+=dt*.17;updateCamera();}
  if(keys.size){
    camera.updateMatrixWorld();
    const speed=dt*orbit.distance*(keys.has('shift')?1.5:.45);
    const right=new THREE.Vector3().setFromMatrixColumn(camera.matrixWorld,0),forward=camera.getWorldDirection(new THREE.Vector3());
    orbit.target.addScaledVector(right,((keys.has('d')?1:0)-(keys.has('a')?1:0))*speed);
    orbit.target.addScaledVector(forward,((keys.has('w')?1:0)-(keys.has('s')?1:0))*speed);
    orbit.target.y+=((keys.has('e')?1:0)-(keys.has('q')?1:0))*speed;
    orbit.az+=((keys.has('arrowleft')?1:0)-(keys.has('arrowright')?1:0))*dt;
    orbit.el=clamp(orbit.el+((keys.has('arrowup')?1:0)-(keys.has('arrowdown')?1:0))*dt,-1.56,1.56);
    if(keys.has('+')||keys.has('='))orbit.distance=clamp(orbit.distance*Math.exp(-dt),.12,8);
    if(keys.has('-'))orbit.distance=clamp(orbit.distance*Math.exp(dt),.12,8);
    updateCamera();
  }
  if(needsRender){renderer.render(scene,camera);needsRender=false;}
}
async function init() {
  document.querySelectorAll('button').forEach(b=>b.disabled=true);
  try{
    renderer=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true,preserveDrawingBuffer:true,powerPreference:'high-performance'});
    renderer.setClearColor(0x000000,0);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.92;
    renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
    scene=new THREE.Scene();camera=new THREE.PerspectiveCamera(36,1,.008,100);
    environment=makeEnvironment();scene.environment=environment.texture;
    scene.add(new THREE.HemisphereLight(0xffffff,0xc5b7a4,.55));
    keyLight=new THREE.DirectionalLight(0xfff1df,2.7);keyLight.position.set(-1.8,5,2);keyLight.castShadow=true;keyLight.shadow.mapSize.set(2048,2048);keyLight.shadow.camera.left=-1.5;keyLight.shadow.camera.right=1.5;keyLight.shadow.camera.top=1.5;keyLight.shadow.camera.bottom=-1.5;keyLight.shadow.camera.near=.1;keyLight.shadow.camera.far=10;keyLight.shadow.bias=-.0003;keyLight.shadow.normalBias=.008;scene.add(keyLight);
    fillLight=new THREE.DirectionalLight(0xeef3ff,1.5);fillLight.position.set(2,-1,2);scene.add(fillLight);
    rimLight=new THREE.DirectionalLight(0xfff3e8,1.9);rimLight.position.set(0,2,-3);scene.add(rimLight);
    const undersideLight=new THREE.DirectionalLight(0xfff4e5,1.0);undersideLight.position.set(0,-3,1);scene.add(undersideLight);
    model=new THREE.Group();scene.add(model);makeFloor();
    await buildModel();lighting('day');preset('outside',true);resize();
    bindInputs();new ResizeObserver(resize).observe(stage);
    renderer.render(scene,camera);
    state.ready=true;$('loading').classList.add('done');document.querySelectorAll('button').forEach(b=>b.disabled=false);
    if(new URLSearchParams(location.search).get('view')==='free')freeMode(true);
    requestAnimationFrame(frame);
    window.__studio={state,orbit,renderer,scene,camera,preset,freeMode};
  }catch(error){console.error('Umbrella studio:',error);fail('The 3D view could not load. Try reloading or opening a browser with WebGL enabled.');}
}
init();
