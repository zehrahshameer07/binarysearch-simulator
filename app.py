"""Binary Search Simulator: pastel, animated, easy to follow.

Settings live in the sidebar. The animated walkthrough runs in the browser
inside one iframe, so Next / Back / Auto-play are instant.
"""
import json
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Binary Search Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

INK, MUTE = "#3F3A5A", "#8A839F"

st.markdown(
    f"""
<style>
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent; }}
.stApp {{ background: linear-gradient(160deg,#F6F2FF 0%,#FFF1F6 55%,#FFF8E8 100%); }}
[data-testid="stSidebar"] {{ background: linear-gradient(180deg,#EFE9FF 0%,#FDEBF3 100%); }}
[data-testid="stSidebar"] h2 {{ font-family: Georgia, serif; font-weight: normal; color: {INK}; font-size: 24px; }}
.block-container {{ max-width: 860px; padding-top: 2.2rem; }}
.title {{ font-family: Georgia, serif; font-size: 40px; color: {INK}; margin: 0; line-height: 1.15; }}
.sub {{ color: {MUTE}; font-size: 16px; margin: 4px 0 18px 0; }}
.stButton > button {{ border-radius: 12px; }}
</style>
<div class="title">Binary Search</div>
<div class="sub">A sorted list is cut in half at every step, until the number is found.</div>
""",
    unsafe_allow_html=True,
)


# ---------- Sidebar: all settings live here ----------
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

with st.sidebar:
    st.header("Settings")

    with st.expander("Use my own numbers"):
        raw = st.text_input("Type numbers with commas", placeholder="3, 8, 15, 22, 40",
                            help="We sort them for you. Binary search needs a sorted list.")
    arr = st.session_state.rand_arr
    if raw.strip():
        try:
            parsed = sorted(int(x) for x in raw.replace(" ", ",").split(",") if x.strip())
            if not 1 <= len(parsed) <= 14:
                raise ValueError
            arr = parsed
        except ValueError:
            st.error("Please type 1 to 14 whole numbers, like 3, 8, 15.")
    st.session_state.cur_arr = arr

    st.number_input("Number to find", min_value=0, max_value=999, step=1, key="target")
    target = int(st.session_state.target)
    st.caption("This number is in the list." if target in arr else "This number is not in the list.")
    b1, b2 = st.columns(2)
    b1.button("In list", on_click=pick_in_list, width="stretch", help="Pick a number that is in the list")
    b2.button("Not in list", on_click=pick_not_in_list, width="stretch", help="Pick a number that is not in the list")

    st.divider()
    if not raw.strip():
        st.slider("How many numbers", 5, 14, key="size", on_change=new_random)
        st.button("New list", on_click=new_random, width="stretch")
    speed = st.select_slider("Auto-play speed", ["Slow", "Normal", "Fast"], value="Normal")

delay = {"Slow": 2400, "Normal": 1500, "Fast": 800}[speed]

# ---------- The simulator ----------
SIMULATOR = r"""
<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{
 --ink:#3F3A5A; --mute:#8A839F; --line:#E9E3F7;
 --lav:#EEE8FD; --blush:#FFE9F1; --butter:#FFF3D6; --mint:#DDF4EA; --sky:#E1EFFC;
 --acc:#9A8CE0; --accd:#8274D3; --rose:#F29BB6; --green:#7FD1AE; --blue:#8EC1F0;
 --size:56px;
}
*{box-sizing:border-box}
body{margin:0;padding:2px;font-family:'Trebuchet MS',Helvetica,Arial,sans-serif;color:var(--ink);background:transparent}
.app{background:rgba(255,255,255,.88);border:1px solid var(--line);border-radius:28px;padding:22px 22px 20px;
 box-shadow:0 14px 34px rgba(154,140,224,.16)}
.top{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}
.goal{font-size:18px;color:var(--mute)}
.goal b{display:inline-block;margin-left:8px;background:linear-gradient(135deg,#B3A7F0,#9A8CE0);color:#fff;border-radius:14px;
 padding:2px 16px;font-family:Georgia,serif;font-size:28px}
.step{font-size:14px;color:var(--mute);background:var(--lav);border-radius:999px;padding:4px 14px}

.stage{padding:22px 4px 6px;overflow-x:auto}
.row{display:flex;justify-content:center;gap:8px;min-width:min-content}
.col{display:flex;flex-direction:column;align-items:center;width:var(--size);flex:none}
.box{width:var(--size);height:var(--size);border-radius:18px;display:flex;align-items:center;justify-content:center;
 font-family:Georgia,serif;font-weight:bold;font-size:calc(var(--size)*.4);background:#fff;color:var(--ink);
 border:3px solid #DCD4F3;transition:all .5s ease;box-shadow:0 3px 8px rgba(154,140,224,.12)}
.col.L .box{border-color:var(--blue)}
.col.R .box{border-color:var(--rose)}
.col.out .box{background:#F5F2FA;border:2px dashed #E2DCF0;color:#C2BBD6;transform:scale(.82);box-shadow:none}
.col.M .box{background:linear-gradient(135deg,#B3A7F0,#9A8CE0);border-color:#9A8CE0;color:#fff;
 transform:translateY(-8px) scale(1.08);box-shadow:0 10px 20px rgba(154,140,224,.42)}
.col.M.out .box{background:#ECE8F8;color:#A59DC2;border:2px dashed #B3A7F0;box-shadow:none;transform:scale(.9)}
.col.found .box{background:linear-gradient(135deg,#A5E3C7,#7FD1AE);border-color:#7FD1AE;color:#fff;
 box-shadow:0 10px 20px rgba(127,209,174,.45)}
.idx{font-size:12px;color:#B8B1CC;margin-top:8px;height:16px}
.ptrs{display:flex;flex-direction:column;align-items:center;gap:3px;margin-top:3px;min-height:60px}
.ptr{font-size:13px;font-weight:bold;border-radius:9px;padding:2px 0;width:30px;text-align:center}
.ptr.L{background:#D9EBFC;color:#3B72AD}
.ptr.M{background:#9A8CE0;color:#fff}
.ptr.R{background:#FFDCE7;color:#B8506F}
.legend{text-align:center;font-size:13px;color:var(--mute);margin-top:6px}
.legend b{display:inline-block;width:22px;border-radius:7px;margin:0 3px 0 10px;font-size:12px}
.legend b.L{background:#D9EBFC;color:#3B72AD}.legend b.M{background:#9A8CE0;color:#fff}.legend b.R{background:#FFDCE7;color:#B8506F}

.status{border-radius:22px;padding:18px 22px;margin:20px 0 18px;text-align:center;transition:background .35s}
.main{font-size:24px;font-family:Georgia,serif;line-height:1.55}
.n{display:inline-block;background:#fff;border-radius:11px;padding:0 12px;font-weight:bold;margin:0 2px}
.hint{margin-top:2px;font-size:15px;color:var(--mute)}

.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:center}
.btn{font-family:inherit;font-size:16px;border:2px solid var(--line);background:#fff;color:var(--ink);border-radius:16px;
 height:52px;padding:0 24px;cursor:pointer;transition:all .15s}
.btn:hover:not(:disabled){border-color:var(--acc);transform:translateY(-1px)}
.btn:disabled{opacity:.4;cursor:not-allowed}
.btn.big{background:linear-gradient(135deg,#AFA2EE,#9A8CE0);border-color:#9A8CE0;color:#fff;font-weight:bold;font-size:18px;
 min-width:150px;box-shadow:0 8px 16px rgba(154,140,224,.35)}
.btn.icon{padding:0;width:52px;font-size:20px}
</style></head><body>
<div class="app">
 <div class="top"><div class="goal">Looking for<b id="goal"></b></div><div class="step" id="step"></div></div>
 <div class="stage"><div class="row" id="row"></div></div>
 <div class="legend"><b class="L">L</b>left end<b class="M">M</b>middle<b class="R">R</b>right end</div>
 <div class="status" id="status"></div>
 <div class="controls">
  <button class="btn" id="reset">Start over</button>
  <button class="btn" id="back">Back</button>
  <button class="btn big" id="next">Next</button>
  <button class="btn" id="auto">Auto-play</button>
 </div>
</div>
<script>
const $=id=>document.getElementById(id);
const arr=__DATA__,T=__TARGET__,DELAY=__DELAY__;
const frames=[];
(function(){let low=0,high=arr.length-1;frames.push({k:'start',low,high,mid:null});
 while(low<=high){const mid=low+((high-low)>>1),v=arr[mid];frames.push({k:'pick',low,high,mid});
  if(v===T){frames.push({k:'found',low,high,mid});break;}
  if(v<T){low=mid+1;frames.push({k:'right',low,high,mid});}
  else{high=mid-1;frames.push({k:'left',low,high,mid});}}
 if(frames[frames.length-1].k!=='found')frames.push({k:'missing',low,high,mid:null});})();
const LAST=frames.length-1;let i=0,timer=null;
$('goal').textContent=T;
function fit(){const W=$('row').parentElement.clientWidth||640,N=arr.length;
 const s=Math.floor((W-12-(N-1)*8)/N);
 document.documentElement.style.setProperty('--size',Math.max(32,Math.min(72,s))+'px');}
const nb=x=>`<span class="n">${x}</span>`;
function render(){
 const f=frames[i],inArr=k=>k>=0&&k<arr.length;
 $('row').innerHTML=arr.map((v,k)=>{
  const inr=k>=f.low&&k<=f.high,isM=f.mid===k;
  const c='col'+(inr?'':' out')+(isM?' M':'')+(inr&&k===f.low?' L':'')+(inr&&k===f.high?' R':'')+(f.k==='found'&&isM?' found':'');
  let p='';
  if(k===f.low&&inArr(f.low))p+='<div class="ptr L">L</div>';
  if(isM)p+='<div class="ptr M">M</div>';
  if(k===f.high&&inArr(f.high))p+='<div class="ptr R">R</div>';
  return `<div class="${c}"><div class="box">${v}</div><div class="idx">${k}</div><div class="ptrs">${p}</div></div>`;
 }).join('');
 const v=f.mid===null?null:arr[f.mid];let bg,main,hint;
 if(f.k==='start'){bg='var(--sky)';main=`We want to find ${nb(T)}.`;hint='The numbers are in order, from small to big. Press Next and we will start with the middle number.';}
 else if(f.k==='pick'){bg='var(--butter)';main=`The middle number is ${nb(v)}.`;hint=`Let's compare it with ${T}.`;}
 else if(f.k==='right'){bg='var(--lav)';main=`${nb(v)} is smaller than ${nb(T)}.`;hint=`The list goes from small to big, so ${T} must be on the right. We can ignore the left side.`;}
 else if(f.k==='left'){bg='var(--blush)';main=`${nb(v)} is bigger than ${nb(T)}.`;hint=`The list goes from small to big, so ${T} must be on the left. We can ignore the right side.`;}
 else if(f.k==='found'){bg='var(--mint)';main=`Found it! ${nb(T)} is at position ${f.mid}.`;
  const c=frames.slice(0,i+1).filter(x=>x.k==='pick').length;
  hint=`We only looked at ${c} number${c===1?'':'s'}. Looking one by one would take ${arr.indexOf(T)+1}.`;}
 else{bg='#F3F0F9';main=`${nb(T)} is not in the list.`;hint='We have run out of numbers to check, so it is not here.';}
 $('status').style.background=bg;$('status').innerHTML=`<div class="main">${main}</div><div class="hint">${hint}</div>`;
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
window.addEventListener('resize',()=>{fit();});
fit();render();
</script></body></html>
"""

html = (
    SIMULATOR.replace("__DATA__", json.dumps(arr))
    .replace("__TARGET__", str(target))
    .replace("__DELAY__", str(delay))
)
if hasattr(st, "iframe"):
    st.iframe(html, height=540)
else:  # older Streamlit versions
    components.html(html, height=540, scrolling=True)