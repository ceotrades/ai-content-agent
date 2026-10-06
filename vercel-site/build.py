# Rebuilds index.html from a folder of exported collections.
# Usage: put the export under ./export/<collection>/<DOC-ID>.json, then: python3 build.py
import json, os, re, datetime
EX=os.environ.get('EXPORT_DIR','./export')
D={}
for col in sorted(os.listdir(EX)):
    p=os.path.join(EX,col)
    if not os.path.isdir(p): continue
    D[col]={}
    for f in sorted(os.listdir(p)):
        if not f.endswith('.json'): continue
        did=f[:-5]
        D[col][did]=json.load(open(os.path.join(p,f)))
D['requests']={}
counts={k:len(v) for k,v in D.items()}
print(counts)

html=open(os.environ.get('SOURCE_HTML','./control-room.html')).read()
# strip the title tag (goes in head) and keep the rest as body content
m=re.match(r'\s*<title>(.*?)</title>\s*', html, re.S)
title=m.group(1).strip() if m else 'ceotalks23 Control Room'
body=html[m.end():] if m else html
# move the two preconnects + font stylesheet into head
headlinks=[]
def grab(pat):
    global body
    out=[]
    for mm in re.finditer(pat, body):
        out.append(mm.group(0))
    body=re.sub(pat,'',body)
    return out
headlinks+=grab(r'<link rel="preconnect"[^>]*>')
headlinks+=grab(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>')

data=json.dumps(D, separators=(',',':'), ensure_ascii=False).replace('</','<\\/')
built=datetime.date.today().isoformat()

shim = """
window.__SNAPSHOT__=true;
window.__D=%s;
window.claude={use:async function(n){
  if(n!=="db") return null;
  var D=window.__D;
  function snap(c,i){return {id:i,exists:!!(D[c]&&D[c][i]),data:function(){return D[c]&&D[c][i]},metadata:{}};}
  function noop(){return Promise.resolve();}
  function coll(c){
    var o={};
    o.limit=function(){return o};
    o.orderBy=function(){return o};
    o.where=function(){return o};
    o.onSnapshot=function(f){setTimeout(function(){f({docs:Object.keys(D[c]||{}).map(function(i){return snap(c,i)}),size:Object.keys(D[c]||{}).length,empty:!Object.keys(D[c]||{}).length,docChanges:function(){return[]}})},30);return function(){}};
    o.add=noop; o.doc=function(i){return docRef(c,i)};
    return o;
  }
  function docRef(c,i){return {onSnapshot:function(f){setTimeout(function(){f(snap(c,i))},30);return function(){}},get:function(){return Promise.resolve(snap(c,i))},update:noop,set:noop,delete:noop};}
  return {doc:function(p){var a=String(p).split("/");return docRef(a[0],a[1])},collection:coll};
}};
var OK={close:1,open:1,ideaFilter:1,ideaSort:1,gotoScript:1,selScript:1,copy:1,cancelEdit:1,research:1,stop:1};
function block(){
  var r=document.getElementById("toastRoot");
  if(r){ r.innerHTML='<div class="toast">Read-only showcase copy. The live control room is where the buttons work.</div>';
    clearTimeout(window.__bt); window.__bt=setTimeout(function(){r.innerHTML=""},3200); }
}
document.addEventListener("click",function(e){
  var el=e.target.closest && e.target.closest("[data-act]");
  if(!el) return;
  if(OK[el.dataset.act]) return;
  e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); block();
},true);
document.addEventListener("change",function(e){
  if(e.target && e.target.type==="file"){ e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); e.target.value=""; block(); }
},true);
document.addEventListener("submit",function(e){ e.preventDefault(); e.stopPropagation(); e.stopImmediatePropagation(); block(); },true);
""" % data

banner = """
<style>
#snapbar{position:relative;z-index:50;display:flex;flex-wrap:wrap;gap:10px;align-items:center;
  background:var(--yellow);color:#15161A;border-bottom:2px solid var(--rule);
  padding:9px 16px;font-family:var(--body);font-size:13px;font-weight:600;line-height:1.35}
#snapbar b{font-family:var(--display);font-weight:400;letter-spacing:.01em;text-transform:uppercase;font-size:12px}
#snapbar span{font-weight:500}
#snapbar .sb-a{color:inherit;text-decoration:none;border-bottom:1.5px solid #15161A;font-weight:700;white-space:nowrap}
#snapbar .sb-a:hover{background:#15161A;color:var(--yellow);border-color:#15161A}
#snapbar .sb-x{margin-left:auto;background:transparent;border:1.5px solid #15161A;border-radius:0;
  font:inherit;font-size:12px;padding:3px 9px;cursor:pointer;color:inherit}
#snapbar .sb-x:hover{background:#15161A;color:var(--yellow)}
@media(max-width:600px){#snapbar{font-size:12px;padding:8px 14px}}
</style>
<div id="snapbar"><b>Showcase snapshot</b><span>Real data from the live system, frozen %s. The buttons and the AI drafting tools only work in the live copy.</span><a class="sb-a" href="https://www.tiktok.com/@ceotalks23" target="_blank" rel="noopener">The account &rarr;</a><button class="sb-x" onclick="this.parentNode.remove()">Hide</button></div>
""" % built

out = ('<!doctype html>\n<html lang="en-GB">\n<head>\n<meta charset="utf-8">\n'
 '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
 '<meta name="color-scheme" content="light dark">\n'
 '<title>%s</title>\n'
 '<meta name="description" content="A three-agent TikTok content intelligence system: outlier research, script drafting and weekly performance grading. Read-only snapshot of the live control room.">\n'
 '<meta property="og:title" content="%s">\n'
 '<meta property="og:description" content="Three AI agents that research outliers, draft scripts and grade performance for a TikTok account. Read-only snapshot.">\n'
 '<meta property="og:type" content="website">\n'
 '%s\n</head>\n<body>\n<script>%s</script>\n%s\n%s\n</body>\n</html>\n'
) % (title, title, '\n'.join(headlinks), shim, banner, body)

open('./index.html','w').write(out)
print('index.html', len(out), 'bytes')
