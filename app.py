"""Binary Search Simulator (Divide and Conquer, recursive) - midnight theme.

Sidebar  : simple explanation + settings.
Main page: array -> step explanation -> Next/Back/Auto-play -> pseudocode + call stack -> complexity.
"""
import json
import math
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Binary Search | Divide & Conquer", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown(
    """
<style>
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.stApp {
  background:
    radial-gradient(circle at 15% 0%, rgba(139,124,255,.28) 0, transparent 40%),
    radial-gradient(circle at 95% 15%, rgba(255,122,168,.18) 0, transparent 38%),
    radial-gradient(circle at 50% 100%, rgba(94,230,216,.12) 0, transparent 45%),
    #0E0B1F;
  color: #ECE9FF;
}
[data-testid="stSidebar"] { background: #130F2B; border-right: 1px solid rgba(255,255,255,.08); }
[data-testid="stSidebar"] h2 { font-family: 'Segoe UI', system-ui, sans-serif; font-weight: 700; color: #fff; font-size: 20px; letter-spacing: .3px; }
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span { color: #CFCAF0; }
[data-testid="stSidebar"] input { background: #1E1942 !important; color: #fff !important; }
.stButton > button { border-radius: 12px; background: #221C48; color: #fff; border: 1px solid rgba(255,255,255,.14); }
.stButton > button:hover { border-color: #8B7CFF; color: #fff; }
[data-testid="stExpander"] { background: rgba(255,255,255,.04); border: 1px solid rgba(255,255,255,.1); border-radius: 14px; }
.block-container { max-width: 980px; padding-top: 2rem; }
.tag { display:inline-block; font-size:12px; letter-spacing:2px; color:#5EE6D8; border:1px solid rgba(94,230,216,.4);
       border-radius:999px; padding:3px 14px; margin-bottom:10px; }
.title { font-family:'Segoe UI',system-ui,sans-serif; font-weight:800; font-size:46px; line-height:1.1; margin:0;
         background:linear-gradient(90deg,#B9AEFF 0%,#FF9EC0 55%,#FFD38A 100%); -webkit-background-clip:text;
         background-clip:text; color:transparent; }
.sub { color:#9A94C4; font-size:16px; margin:8px 0 18px 0; }
.step-box { background:rgba(255,255,255,.05); border:1px solid rgba(255,255,255,.09); border-radius:14px;
            padding:11px 14px; margin-bottom:8px; color:#DAD6F5; font-size:14.5px; line-height:1.5; }
.step-box b { color:#FFC66B; }
</style>
<div class="tag">DIVIDE &amp; CONQUER</div>
<div class="title">Binary Search</div>
<div class="sub">Watch a recursive function cut a sorted list in half, call after call.</div>
""",
    unsafe_allow_html=True,
)


# ---------- helpers ----------
def new_random():
    st.session_state.rand_arr = sorted(random.sample(range(1, 100), st.session_state.size))
    st.session_state.target = random.choice(st.session_state.rand_arr)


def pick_in_list():
    st.session_state.target = random.choice(st.session_state.cur_arr)


def pick_not_in_list():
    taken = set(st.session_state.cur_arr)
    st.session_state.target = random.choice([x for x in range(1, 100) if x not in taken])


if "rand_arr" not in st.session_state:
    st.session_state.size = 10
    st.session_state.rand_arr = sorted(random.sample(range(1, 100), 10))
    st.session_state.target = random.choice(st.session_state.rand_arr)

# ---------- Sidebar ----------
with st.sidebar:
    st.header("How it works")
    st.markdown(
        """
<div class="step-box"><b>1. Divide.</b> Look at the middle number of the sorted list.</div>
<div class="step-box"><b>2. Conquer.</b> If the middle is smaller than your number, search the right half. If bigger, search the left half.</div>
<div class="step-box"><b>3. Repeat.</b> The function calls itself on the smaller half, until the number is found or no numbers are left.</div>
""",
        unsafe_allow_html=True,
    )

    st.header("Settings")
    with st.expander("Use my own numbers"):
        raw = st.text_input("Numbers with commas", placeholder="3, 8, 15, 22, 40",
                            help="We sort them for you.")
    arr = st.session_state.rand_arr
    if raw.strip():
        try:
            parsed = sorted(int(x) for x in raw.replace(" ", ",").split(",") if x.strip())
            if not 1 <= len(parsed) <= 14:
                raise ValueError
            arr = parsed
        except ValueError:
            st.error("Type 1 to 14 whole numbers, like 3, 8, 15.")
    st.session_state.cur_arr = arr

    st.number_input("Number to find", min_value=0, max_value=999, step=1, key="target")
    target = int(st.session_state.target)
    st.caption("This number is in the list." if target in arr else "This number is not in the list.")
    b1, b2 = st.columns(2)
    b1.button("In list", on_click=pick_in_list, use_container_width=True)
    b2.button("Not in list", on_click=pick_not_in_list, use_container_width=True)

    if not raw.strip():
        st.slider("How many numbers", 5, 14, key="size", on_change=new_random)
        st.button("New list", on_click=new_random, use_container_width=True)
    speed = st.select_slider("Auto-play speed", ["Slow", "Normal", "Fast"], value="Normal")

delay = {"Slow": 2600, "Normal": 1700, "Fast": 900}[speed]
max_calls = int(math.log2(len(arr))) + 2

# ---------- Simulator ----------
SIMULATOR = r"""
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{--ink:#ECE9FF;--mute:#9A94C4;--line:rgba(255,255,255,.1);--vio:#8B7CFF;--cyan:#5EE6D8;--pink:#FF7AA8;--amber:#FFC66B;--size:56px;}
*{box-sizing:border-box}
body{margin:0;padding:2px;font-family:'Segoe UI',system-ui,Helvetica,Arial,sans-serif;color:var(--ink);background:transparent}
.app{background:linear-gradient(160deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border:1px solid var(--line);
 border-radius:28px;padding:24px;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.goal{font-size:17px;color:var(--mute)}
.goal b{display:inline-block;margin-left:10px;background:linear-gradient(135deg,#8B7CFF,#C06BFF);color:#fff;border-radius:14px;
 padding:3px 18px;font-size:26px;box-shadow:0 0 22px rgba(139,124,255,.55)}
.step{font-size:13px;color:var(--mute);border:1px solid var(--line);border-radius:999px;padding:4px 14px}

.stage{padding:26px 4px 0;overflow-x:auto}
.row{display:flex;justify-content:center;gap:8px;min-width:min-content}
.col{display:flex;flex-direction:column;align-items:center;width:var(--size);flex:none}
.box{width:var(--size);height:var(--size);border-radius:16px;display:flex;align-items:center;justify-content:center;
 font-weight:700;font-size:calc(var(--size)*.38);background:#1A1536;color:var(--ink);border:2px solid #3A3270;transition:all .4s ease}
.col.out .box{background:transparent;border:2px dashed #2C2655;color:#4A4378;transform:scale(.84)}
.col.M .box{background:linear-gradient(135deg,#8B7CFF,#C06BFF);border-color:#C9BFFF;color:#fff;
 transform:translateY(-8px) scale(1.1);box-shadow:0 0 28px rgba(139,124,255,.75)}
.col.found .box{background:linear-gradient(135deg,#34D399,#5EE6D8);border-color:#B8FFF3;color:#07261F;
 box-shadow:0 0 30px rgba(94,230,216,.75)}
.idx{font-size:12px;color:#6B64A0;margin-top:8px}
.ptrs{display:flex;flex-direction:column;align-items:center;gap:3px;margin-top:3px;min-height:56px}
.ptr{font-size:13px;font-weight:700;border-radius:8px;width:28px;text-align:center;padding:1px 0;color:#0E0B1F}
.ptr.L{background:var(--cyan)}.ptr.M{background:var(--amber)}.ptr.R{background:var(--pink)}
.legend{text-align:center;font-size:13px;color:var(--mute)}
.legend span{display:inline-block;border-radius:6px;padding:0 7px;margin:0 4px 0 14px;font-weight:700;color:#0E0B1F}

.status{border-radius:20px;padding:16px 20px;margin:16px 0;text-align:center;transition:all .3s;border:1px solid}
.main{font-size:22px;font-weight:600;line-height:1.5}
.n{display:inline-block;background:rgba(255,255,255,.14);border-radius:10px;padding:0 11px;font-weight:700;margin:0 2px}
.hint{margin-top:3px;font-size:15px;color:#C4BFE6}

.controls{display:flex;flex-wrap:wrap;gap:10px;justify-content:center;margin-bottom:24px}
.btn{font-family:inherit;font-size:16px;border:1px solid rgba(255,255,255,.16);background:rgba(255,255,255,.06);color:var(--ink);
 border-radius:14px;height:48px;padding:0 22px;cursor:pointer;transition:all .15s}
.btn:hover:not(:disabled){border-color:var(--vio);background:rgba(139,124,255,.18)}
.btn:disabled{opacity:.35;cursor:not-allowed}
.btn.big{background:linear-gradient(135deg,#8B7CFF,#C06BFF);border-color:transparent;color:#fff;font-weight:700;font-size:18px;
 min-width:140px;box-shadow:0 8px 22px rgba(139,124,255,.5)}
.btn.big:hover:not(:disabled){transform:translateY(-1px)}

.panels{display:grid;grid-template-columns:1.2fr 1fr;gap:14px}
@media(max-width:700px){.panels{grid-template-columns:1fr}}
.card{border-radius:18px;padding:14px 16px}
.card h4{margin:0 0 10px;font-size:12px;letter-spacing:1.5px;font-weight:700;color:var(--mute)}
.code{background:#08061A;border:1px solid var(--line);font-family:Consolas,'Courier New',monospace;font-size:13.5px;line-height:1.85;color:#DAD6F5}
.ln{display:block;padding:0 8px;border-radius:6px;white-space:pre;border-left:3px solid transparent}
.ln i{color:#585087;font-style:normal;display:inline-block;width:22px}
.ln.on{background:rgba(255,198,107,.15);border-left-color:var(--amber);color:#fff}
.kw{color:#FF9EC0}.fn{color:#7FD6FF}
.stack{background:rgba(255,255,255,.04);border:1px solid var(--line)}
.frame{border-radius:10px;padding:7px 12px;margin-bottom:6px;font-size:13.5px;background:rgba(255,255,255,.06);
 border:1px solid var(--line);font-family:Consolas,monospace}
.frame.top{background:linear-gradient(135deg,#8B7CFF,#C06BFF);border-color:transparent;color:#fff;box-shadow:0 0 18px rgba(139,124,255,.45)}
.empty{color:var(--mute);font-size:14px}
.cx{margin-top:16px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.cx div{border:1px solid rgba(94,230,216,.35);background:rgba(94,230,216,.08);border-radius:999px;padding:6px 16px;font-size:14px;color:#BFF6EF}
.cx b{color:#fff}
</style></head><body>
<div class="app">
 <div class="top"><div class="goal">Looking for<b id="goal"></b></div><div class="step" id="step"></div></div>
 <div class="stage"><div class="row" id="row"></div></div>
 <div class="legend"><span style="background:#5EE6D8">L</span>left end
  <span style="background:#FFC66B">M</span>middle
  <span style="background:#FF7AA8">R</span>right end</div>
 <div class="status" id="status"></div>
 <div class="controls">
  <button class="btn" id="reset">Start over</button>
  <button class="btn" id="back">Back</button>
  <button class="btn big" id="next">Next</button>
  <button class="btn" id="auto">Auto-play</button>
 </div>
 <div class="panels">
  <div class="card code"><h4>PSEUDOCODE</h4><div id="code"></div></div>
  <div class="card stack"><h4>CALL STACK (top = running now)</h4><div id="stack"></div></div>
 </div>
 <div class="cx"><div>Time: <b>O(log n)</b></div><div>Space: <b>O(log n)</b> recursion stack, at most __MAXC__ calls here</div></div>
</div>
<script>
const $=id=>document.getElementById(id);
const arr=__DATA__,T=__TARGET__,DELAY=__DELAY__;
const CODE=[
 '<span class="fn">BinarySearch</span>(A, low, high, key)',
 '  <span class="kw">if</span> low &gt; high: <span class="kw">return</span> -1',
 '  mid = (low + high) / 2',
 '  <span class="kw">if</span> A[mid] == key: <span class="kw">return</span> mid',
 '  <span class="kw">else if</span> A[mid] &lt; key:\n      <span class="kw">return</span> <span class="fn">BinarySearch</span>(A, mid+1, high, key)',
 '  <span class="kw">else</span>:\n      <span class="kw">return</span> <span class="fn">BinarySearch</span>(A, low, mid-1, key)',
];
const frames=[{k:'start',low:0,high:arr.length-1,mid:null,ln:-1,stack:[]}];
function bs(low,high,stack){
 const st=[...stack,[low,high]];
 frames.push({k:'call',low,high,mid:null,ln:0,stack:st});
 if(low>high){frames.push({k:'base',low,high,mid:null,ln:1,stack:st});return -1;}
 const mid=low+((high-low)>>1);
 frames.push({k:'mid',low,high,mid,ln:2,stack:st});
 if(arr[mid]===T){frames.push({k:'found',low,high,mid,ln:3,stack:st});return mid;}
 if(arr[mid]<T){frames.push({k:'right',low,high,mid,ln:4,stack:st});return bs(mid+1,high,st);}
 frames.push({k:'left',low,high,mid,ln:5,stack:st});return bs(low,mid-1,st);
}
const result=bs(0,arr.length-1,[]);
frames.push({k:'done',low:0,high:-1,mid:null,ln:-1,stack:[],res:result});
const LAST=frames.length-1;let i=0,timer=null;
$('goal').textContent=T;
$('code').innerHTML=CODE.map((c,n)=>`<span class="ln" id="ln${n}"><i>${n+1}</i>${c}</span>`).join('');
function fit(){const W=$('row').parentElement.clientWidth||640,N=arr.length;
 const s=Math.floor((W-12-(N-1)*8)/N);
 document.documentElement.style.setProperty('--size',Math.max(32,Math.min(68,s))+'px');}
const nb=x=>`<span class="n">${x}</span>`;
const TONE={start:'94,160,255',call:'94,160,255',base:'154,148,196',mid:'255,198,107',right:'139,124,255',left:'255,122,168',found:'94,230,216',doneok:'94,230,216',donenf:'154,148,196'};
function render(){
 const f=frames[i],empty=f.low>f.high;
 $('row').innerHTML=arr.map((v,k)=>{
  const inr=k>=f.low&&k<=f.high,isM=f.mid===k;
  const c='col'+(inr?'':' out')+(isM?' M':'')+(f.k==='found'&&isM?' found':'');
  let p='';
  if(!empty&&f.k!=='done'){
   if(k===f.low)p+='<div class="ptr L">L</div>';
   if(isM)p+='<div class="ptr M">M</div>';
   if(k===f.high)p+='<div class="ptr R">R</div>';}
  return `<div class="${c}"><div class="box">${v}</div><div class="idx">${k}</div><div class="ptrs">${p}</div></div>`;
 }).join('');
 const v=f.mid===null?null:arr[f.mid];let tone,main,hint;
 if(f.k==='start'){tone=TONE.start;main=`We want to find ${nb(T)}`;hint='The list is sorted. Press Next to make the first function call.';}
 else if(f.k==='call'){tone=TONE.call;main=`Call BinarySearch for positions ${nb(f.low)} to ${nb(f.high)}`;hint=f.stack.length===1?'This is the first call.':`This is recursive call number ${f.stack.length}. The list is now smaller.`;}
 else if(f.k==='base'){tone=TONE.base;main=`No numbers left. Return ${nb(-1)}`;hint=`So ${T} is not in the list.`;}
 else if(f.k==='mid'){tone=TONE.mid;main=`Divide: the middle is ${nb(v)}`;hint=`Position (${f.low} + ${f.high}) / 2 = ${f.mid}. Now compare ${v} with ${T}.`;}
 else if(f.k==='right'){tone=TONE.right;main=`${nb(v)} is smaller than ${nb(T)}`;hint=`So ${T} must be on the right. Conquer the right half only.`;}
 else if(f.k==='left'){tone=TONE.left;main=`${nb(v)} is bigger than ${nb(T)}`;hint=`So ${T} must be on the left. Conquer the left half only.`;}
 else if(f.k==='found'){tone=TONE.found;main=`Found it! ${nb(T)} is at position ${nb(f.mid)}`;hint=`It took ${f.stack.length} call${f.stack.length===1?'':'s'}. Checking one by one would take ${arr.indexOf(T)+1}.`;}
 else{tone=f.res>=0?TONE.doneok:TONE.donenf;main=f.res>=0?`Done. The answer is position ${nb(f.res)}`:`Done. The answer is ${nb(-1)} (not found)`;hint='All calls have returned and the stack is empty.';}
 const s=$('status');s.style.background=`rgba(${tone},.14)`;s.style.borderColor=`rgba(${tone},.45)`;
 s.innerHTML=`<div class="main">${main}</div><div class="hint">${hint}</div>`;
 for(let n=0;n<CODE.length;n++)$('ln'+n).className='ln'+(f.ln===n?' on':'');
 $('stack').innerHTML=f.stack.length?[...f.stack].reverse().map((s,n)=>
   `<div class="frame${n===0?' top':''}">BinarySearch(low=${s[0]}, high=${s[1]})</div>`).join('')
   :'<div class="empty">Empty</div>';
 $('step').textContent=`Step ${i} of ${LAST}`;
 $('back').disabled=i===0;$('reset').disabled=i===0&&!timer;$('next').disabled=i===LAST;
 $('auto').textContent=timer?'Pause':(i===LAST?'Play again':'Auto-play');
}
function stop(){if(timer){clearInterval(timer);timer=null;}}
function go(d){stop();i=Math.min(LAST,Math.max(0,i+d));render();}
function play(){if(timer){stop();render();return;}
 if(i===LAST)i=0;
 timer=setInterval(()=>{if(i<LAST)i++;if(i>=LAST)stop();render();},DELAY);render();}
$('next').onclick=()=>go(1);$('back').onclick=()=>go(-1);
$('reset').onclick=()=>{stop();i=0;render();};$('auto').onclick=play;
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1);});
window.addEventListener('resize',fit);
fit();render();
</script></body></html>
"""

html = (
    SIMULATOR.replace("__DATA__", json.dumps(arr))
    .replace("__TARGET__", str(target))
    .replace("__DELAY__", str(delay))
    .replace("__MAXC__", str(max_calls))
)
if hasattr(st, "iframe"):
    st.iframe(html, height=900)
else:
    components.html(html, height=900, scrolling=True)