"""
Quick Sort Simulator  |  DAA CIA 3(b)
A step-by-step visual simulator built with Streamlit.
Run locally:  streamlit run app.py
"""
import random
import time

import streamlit as st

st.set_page_config(page_title="Quick Sort Simulator", layout="wide")

# ----------------------------------------------------------------------------
# 1. COLOURS AND STYLE
# ----------------------------------------------------------------------------
C = {
    "unchecked": "#EEDFC0",   # inside the current sub-array, not looked at yet
    "small": "#E3A5AE",       # small zone: numbers <= pivot (dusty rose)
    "big": "#F6D57A",         # big zone: numbers > pivot (butter yellow)
    "cur": "#4A5A7A",         # the number being checked right now (slate)
    "pivot": "#A63A50",       # the pivot (deep raspberry)
    "done": "#A9CBA4",        # in its final sorted position (sage)
    "faded": "#F8EEDC",       # outside the current sub-array
}
LEGEND = [("unchecked", "Not checked yet"), ("small", "Small zone (less than or equal to pivot)"),
          ("big", "Big zone (greater than pivot)"), ("cur", "Pointer i or j / number being checked"),
          ("pivot", "Pivot"), ("done", "Final sorted position")]

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, button, input { font-family: 'Poppins', sans-serif !important; }
.stApp { background: linear-gradient(170deg, #FFF3C4 0%, #FFF8E6 45%, #FCE6E8 100%); background-attachment: fixed; }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #FFEDB0, #F9D9DD); border-right: 1px solid #F0D6A0; }

/* ---- force readable text everywhere (works even if the browser is in dark mode) ---- */
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span,
[data-testid="stWidgetLabel"] *, [data-testid="stCaptionContainer"] *, [data-testid="stProgress"] p,
[data-testid="stExpander"] summary *, [data-testid="stExpander"] p, [data-testid="stExpander"] li,
[data-testid="stExpander"] td, [data-testid="stExpander"] th, [data-testid="stAlert"] * { color: #4B2E35 !important; }
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] * { color: #7A5A62 !important; }
input, textarea { background: #FFFFFF !important; color: #4B2E35 !important; -webkit-text-fill-color: #4B2E35 !important; }
[data-baseweb="input"], [data-baseweb="base-input"], [data-baseweb="select"] > div {
    background: #FFFFFF !important; color: #4B2E35 !important; border-radius: 12px !important; border-color: #EBCFD3 !important; }
[data-baseweb="select"] * { color: #4B2E35 !important; }
[data-baseweb="select"] svg { fill: #4B2E35 !important; }
[data-baseweb="popover"] *, [data-baseweb="menu"] * { background: #FFFFFF !important; color: #4B2E35 !important; }
[data-baseweb="menu"] li:hover, [data-baseweb="menu"] li:hover * { background: #FDEBEC !important; }
[data-testid="stExpander"] table { background: transparent !important; }
[data-testid="stExpander"] th, [data-testid="stExpander"] td { border-color: #EBCFD3 !important; background: transparent !important; }
[data-testid="stSlider"] [role="slider"] { background: #C0697A !important; }
[data-testid="stSlider"] [data-testid="stTickBarMin"], [data-testid="stSlider"] [data-testid="stTickBarMax"] { color: #7A5A62 !important; }

.block-container { padding-top: 2rem; max-width: 1100px; }
.hero { background: linear-gradient(120deg, #FFE59A 0%, #FDD3D4 60%, #F4C2CA 100%); border-radius: 24px; padding: 24px 28px;
        margin-bottom: 18px; box-shadow: 0 10px 30px rgba(190, 110, 125, .18); }
.hero h1 { margin: 0; font-size: 2.1rem; color: #4B2E35; font-weight: 700; }
.hero p { margin: 4px 0 0; color: #7A4F58; }
.steps3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-bottom: 18px; }
.steps3 div { background: rgba(255,255,255,.78); border-radius: 18px; padding: 14px 16px; color: #6E4F57; font-size: .9rem;
              box-shadow: 0 6px 18px rgba(190, 110, 125, .12); }
.steps3 b { display: block; color: #4B2E35; margin-bottom: 3px; }
.steps3 span { display: inline-block; border-radius: 50%; width: 24px; height: 24px; text-align: center; line-height: 24px;
               font-size: .78rem; margin-right: 8px; color: #4B2E35; font-weight: 700; }
.steps3 div:nth-child(1) span { background: #F6D57A; }
.steps3 div:nth-child(2) span { background: #E3A5AE; }
.steps3 div:nth-child(3) span { background: #A9CBA4; }
.card { background: rgba(255,255,255,.85); border-radius: 22px; padding: 18px 20px; margin-bottom: 16px;
        box-shadow: 0 10px 28px rgba(190, 110, 125, .14); color: #4B2E35; }
.card h3 { margin: 0 0 10px; font-size: .78rem; letter-spacing: .1em; text-transform: uppercase; color: #B07A85; }
.phase { display: inline-block; background: #B5616F; color: #fff; border-radius: 999px; padding: 4px 14px;
         font-size: .78rem; font-weight: 600; margin-bottom: 10px; }
.say { background: rgba(255,255,255,.92); border-radius: 18px; padding: 16px 20px; font-size: 1.08rem; color: #4B2E35;
       min-height: 92px; border-left: 8px solid #F6D57A; box-shadow: 0 8px 22px rgba(190, 110, 125, .14); }
.sub { font-size: .9rem; color: #8A6A70; margin-bottom: 4px; }
.stage { display: flex; align-items: flex-end; gap: 7px; height: 270px; padding-top: 26px; }
.bar { flex: 1; min-width: 18px; border-radius: 12px 12px 5px 5px; position: relative; transition: all .3s; }
.bar::after { content: ""; position: absolute; inset: 0; border-radius: inherit;
              background: linear-gradient(180deg, rgba(255,255,255,.45), rgba(255,255,255,0) 60%); pointer-events: none; }
.bar b { position: absolute; top: -22px; left: 0; right: 0; text-align: center; font-size: .82rem; color: #4B2E35; font-weight: 600; }
.idx { display: flex; gap: 7px; margin-top: 6px; }
.idx div { flex: 1; min-width: 18px; text-align: center; font-size: .72rem; color: #A88990; min-height: 34px; line-height: 1.3; }
.idx div b { font-size: .68rem; }
.legend { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 10px; font-size: .8rem; color: #6E4F57; }
.legend i { display: inline-block; width: 13px; height: 13px; border-radius: 5px; margin-right: 6px; vertical-align: -2px; }
.stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.stat { background: rgba(255,255,255,.88); border-radius: 18px; padding: 10px 16px; box-shadow: 0 6px 18px rgba(190, 110, 125, .12); }
.stat span { display: block; font-size: .72rem; color: #B07A85; text-transform: uppercase; letter-spacing: .08em; }
.stat b { font-size: 1.5rem; color: #4B2E35; }
.code { font-family: 'Courier New', monospace; font-size: .84rem; line-height: 1.75; }
.code div { padding: 1px 10px; border-radius: 8px; white-space: pre; color: #7A5A62; }
.code div.on { background: #FFE9A6; font-weight: 700; color: #4B2E35; }
.stk { display: flex; flex-direction: column-reverse; gap: 6px; }
.stk div { background: #FDF0F1; border-radius: 10px; padding: 4px 12px; font-family: 'Courier New', monospace; font-size: .84rem; color: #6E4F57; }
.stk div:last-child { background: #F9D3D9; color: #7A2338; font-weight: 700; }
.note { font-size: .8rem; color: #8A6A70; margin-top: 8px; }
div.stButton > button { border-radius: 999px; border: none; background: rgba(255,255,255,.95) !important; color: #4B2E35 !important;
                        font-weight: 600; width: 100%; box-shadow: 0 4px 12px rgba(190, 110, 125, .18); }
div.stButton > button p, div.stButton > button span { color: inherit !important; }
div.stButton > button:hover { background: #FFFFFF !important; color: #B5616F !important; box-shadow: 0 6px 16px rgba(190, 110, 125, .28); }
div.stButton > button[kind="primary"] { background: linear-gradient(120deg, #CC8090, #B5616F) !important; color: #FFFFFF !important; }
div.stButton > button[kind="primary"]:hover { color: #FFFFFF !important; }
[data-testid="stExpander"] { background: rgba(255,255,255,.75); border-radius: 16px; border: none; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# 2. ALGORITHM  (records a snapshot after every step so we can play and rewind)
# ----------------------------------------------------------------------------
PSEUDO = [
    "QuickSort(A, lo, hi):",
    "  if lo < hi:",
    "    p = Partition(A, lo, hi)",
    "    QuickSort(A, lo, p - 1)",
    "    QuickSort(A, p + 1, hi)",
    "Partition(A, lo, hi):",
    "  pivot = A[lo];  i = lo + 1;  j = hi",
    "  while i <= j:",
    "    move i right while A[i] <= pivot",
    "    move j left while A[j] >= pivot",
    "    if i < j:  swap(A[i], A[j]);  i++;  j--",
    "  swap(A[lo], A[j]);  return j",
]


def build_steps(arr, mode):
    a = list(arr)
    steps, stack, done = [], [], set()
    n_ = {"cmp": 0, "swp": 0}
    rng = lambda x, y: set(range(x, y))

    def snap(phase, msg, line=0, lo=None, hi=None, piv=None, cur=None, small=(), big=(), sw=(), ptrs=None):
        sub = ""
        if lo is not None and lo <= hi:
            sub = "Working on: " + ", ".join(str(v) for v in a[lo:hi + 1]) + f"   (positions {lo} to {hi})"
        steps.append(dict(a=list(a), lo=lo, hi=hi, piv=piv, cur=cur, small=set(small), big=set(big),
                          sw=list(sw), done=set(done), cmp=n_["cmp"], swp=n_["swp"], stack=list(stack),
                          line=line, phase=phase, msg=msg, sub=sub, ptrs=dict(ptrs or {})))

    def pick(lo, hi):
        if mode == "First element":
            return lo
        if mode == "Middle element":
            return (lo + hi) // 2
        if mode == "Random element":
            return random.randint(lo, hi)
        if mode == "Median of three":
            m = (lo + hi) // 2
            return sorted([lo, m, hi], key=lambda k: a[k])[1]
        return hi

    def hoare(lo, hi):
        p0 = pick(lo, hi)
        if p0 != lo:
            a[p0], a[lo] = a[lo], a[p0]
            n_["swp"] += 1
            snap("Choose the pivot",
                 f"Strategy: {mode.lower()}. The pivot is {a[lo]}. It is swapped to the first position ({lo}) "
                 f"so it stays out of the way while the pointers move.", 6, lo, hi, piv=lo, sw=(p0, lo))
        else:
            snap("Choose the pivot", f"The pivot is the first number, {a[lo]}.", 6, lo, hi, piv=lo)
        pivot, i, j = a[lo], lo + 1, hi

        def pt():
            return {i: "i,j"} if i == j else {i: "i", j: "j"}

        def sn(phase, msg, line):
            snap(phase, msg, line, lo, hi, piv=lo, small=rng(lo + 1, i), big=rng(j + 1, hi + 1), ptrs=pt())

        sn("Get ready to scan",
           f"The pivot {pivot} stays at the left end. i starts at index {i} and moves right. "
           f"j starts at index {j} and moves left.", 6)
        while i <= j:
            while i <= j:
                n_["cmp"] += 1
                if a[i] <= pivot:
                    sn("Move i", f"{a[i]} is less than or equal to the pivot {pivot}, so i moves right.", 8)
                    i += 1
                else:
                    sn("i stops", f"{a[i]} is greater than the pivot {pivot}, so i stops here.", 8)
                    break
            while i <= j:
                n_["cmp"] += 1
                if a[j] >= pivot:
                    sn("Move j", f"{a[j]} is greater than or equal to the pivot {pivot}, so j moves left.", 9)
                    j -= 1
                else:
                    sn("j stops", f"{a[j]} is smaller than the pivot {pivot}, so j stops here.", 9)
                    break
            if i < j:
                x, y = a[i], a[j]
                a[i], a[j] = y, x
                n_["swp"] += 1
                snap("Swap", f"{x} is on the left but belongs on the right, and {y} is the opposite. Swap them.",
                     10, lo, hi, piv=lo, small=rng(lo + 1, i + 1), big=rng(j, hi + 1), sw=(i, j))
                i += 1
                j -= 1
        sn("Pointers cross", f"i (index {i}) is now to the right of j (index {j}), so the scan is over.", 7)
        p, old = j, a[j]
        if p != lo:
            a[lo], a[p] = a[p], a[lo]
            n_["swp"] += 1
        done.add(p)
        msg = (f"The pivot {pivot} swaps with data[j], which is {old}. It is now in its final sorted position, "
               f"with smaller numbers on its left and larger ones on its right." if p != lo else
               f"j came all the way back to the pivot, so the pivot swaps with itself. {pivot} is now in its "
               f"final sorted position and no number in this part is smaller than it.")
        snap("Place the pivot", msg, 11, lo, hi, piv=p, small=rng(lo, p), big=rng(p + 1, hi + 1),
             sw=(lo, p) if p != lo else ())
        return p

    def qs(lo, hi):
        stack.append(f"QuickSort({lo}, {hi})")
        if lo < hi:
            snap("Current sub-array",
                 f"We now sort positions {lo} to {hi}, which holds {hi - lo + 1} numbers.", 1, lo, hi)
            p = hoare(lo, hi)
            snap("Sort the left side",
                 f"Repeat the whole process on the left side (positions {lo} to {p - 1})."
                 + (" It is empty, so there is nothing to do." if p - 1 < lo else ""), 3, lo, hi)
            qs(lo, p - 1)
            snap("Sort the right side",
                 f"Left side finished. Now repeat on the right side (positions {p + 1} to {hi})."
                 + (" It is empty, so there is nothing to do." if p + 1 > hi else ""), 4, lo, hi)
            qs(p + 1, hi)
        elif lo == hi:
            done.add(lo)
            snap("Single number", f"Only one number ({a[lo]}) is left here, so it is already sorted.", 1, lo, hi)
        stack.pop()

    snap("Start", "This is the starting array. Press Play, or use Next to go one step at a time.")
    qs(0, len(a) - 1)
    done.update(range(len(a)))
    snap("Finished", f"The array is sorted. It took {n_['cmp']} comparisons and {n_['swp']} swaps.")
    return steps


# ----------------------------------------------------------------------------
# 3. DRAWING HELPERS
# ----------------------------------------------------------------------------
def bars_html(s):
    a = s["a"]
    mn, mx = min(min(a), 0), max(max(a), 1)
    bars, idx = [], []
    for k, v in enumerate(a):
        in_range = s["lo"] is not None and s["lo"] <= k <= s["hi"]
        tag = ""
        ptr = s.get("ptrs", {}).get(k)
        if k == s["piv"] and k not in s["done"]:
            col, tag = C["pivot"], "pivot" + (f",{ptr}" if ptr else "")
        elif k in s["done"]:
            col = C["done"]
            tag = "pivot" if k == s["piv"] else ""
        elif ptr:
            col, tag = C["cur"], ptr
        elif k == s["cur"]:
            col, tag = C["cur"], "checking"
        elif k in s["small"]:
            col = C["small"]
        elif k in s["big"]:
            col = C["big"]
        elif in_range:
            col = C["unchecked"]
        else:
            col = C["faded"]
        ring = "box-shadow:0 0 0 3px #4B2E35;" if k in s["sw"] else ""
        h = 12 + (v - mn) / (mx - mn or 1) * 88
        bars.append(f'<div class="bar" style="height:{h:.0f}%;background:{col};{ring}"><b>{v}</b></div>')
        tag_html = f'<br><b style="color:{col if col != C["faded"] else "#A88990"}">{tag}</b>' if tag else ""
        idx.append(f"<div>{k}{tag_html}</div>")
    legend = "".join(f'<span><i style="background:{C[k]}"></i>{t}</span>' for k, t in LEGEND)
    return (f'<div class="sub">{s["sub"] or "&nbsp;"}</div><div class="stage">{"".join(bars)}</div>'
            f'<div class="idx">{"".join(idx)}</div><div class="legend">{legend}</div>'
            f'<div class="note">A dark outline means the two numbers were just swapped. Numbers under the bars are positions.</div>')


def code_html(line):
    lines = PSEUDO
    rows = "".join(f'<div class="{"on" if k == line else ""}">{t.replace("<", "&lt;")}</div>'
                   for k, t in enumerate(lines))
    return f'<div class="code">{rows}</div>'


def stack_html(stack):
    if not stack:
        return '<div class="stk"><div>(empty)</div></div>'
    return '<div class="stk">' + "".join(f"<div>{t}</div>" for t in stack) + "</div>"


# ----------------------------------------------------------------------------
# 4. STATE + SIDEBAR
# ----------------------------------------------------------------------------
if "inp" not in st.session_state:
    st.session_state.inp = "35, 12, 43, 8, 27, 19, 50"
    st.session_state.idx = 0
    st.session_state.sig = None
    st.session_state.arr = [35, 12, 43, 8, 27, 19, 50]


def random_array():
    st.session_state.inp = ", ".join(str(random.randint(1, 99)) for _ in range(random.randint(8, 12)))


def go(delta=None, to=None):
    n = len(st.session_state.steps)
    if to is not None:
        st.session_state.idx = to if to >= 0 else n - 1
    else:
        st.session_state.idx = max(0, min(n - 1, st.session_state.idx + delta))


with st.sidebar:
    st.markdown("### Setup")
    st.text_input("Numbers to sort (separate with commas, then press Enter)", key="inp")
    st.button("Random numbers", on_click=random_array)
    mode = st.selectbox("Pivot strategy", ["First element", "Last element", "Middle element",
                                           "Random element", "Median of three"])
    speed = st.slider("Play speed (1 = slowest)", 1, 10, 2)
    st.caption("Tip: enter 1, 2, 3, 4, 5, 6, 7, 8 with the first-element strategy to see the worst case. "
               "Then switch to median of three and compare the recursion depth.")

try:
    parsed = [int(x) for x in st.session_state.inp.replace(",", " ").split()]
    if not 2 <= len(parsed) <= 20:
        raise ValueError
    st.session_state.arr = parsed
except ValueError:
    st.sidebar.error("Please enter 2 to 20 whole numbers.")

sig = (tuple(st.session_state.arr), mode)
if sig != st.session_state.sig:
    st.session_state.steps = build_steps(st.session_state.arr, mode)
    st.session_state.sig = sig
    st.session_state.idx = 0
steps = st.session_state.steps

# ----------------------------------------------------------------------------
# 5. PAGE
# ----------------------------------------------------------------------------
st.markdown('<div class="hero"><h1>Quick Sort Simulator</h1>'
            '<p>See how Quick Sort arranges numbers, one small step at a time.</p></div>'
            '<div class="steps3">'
            '<div><b><span>1</span>Pick a pivot</b>Choose one number to compare everything against.</div>'
            '<div><b><span>2</span>Split into small and big</b>Numbers less than or equal to the pivot go left, the rest go right. The pivot lands in its final spot.</div>'
            '<div><b><span>3</span>Repeat on each side</b>Do the same on the left group and the right group until every number is placed.</div>'
            '</div>', unsafe_allow_html=True)

phase_ph = st.empty()
say = st.empty()
st.write("")
viz = st.empty()
c1, c2, c3, c4, c5 = st.columns(5)
c1.button("Reset", on_click=go, kwargs=dict(to=0))
c2.button("Back", on_click=go, kwargs=dict(delta=-1))
play = c3.button("Play", type="primary")
c4.button("Next", on_click=go, kwargs=dict(delta=1))
c5.button("End", on_click=go, kwargs=dict(to=-1))
st.caption("Press any button while playing to pause.")
prog = st.empty()
stats = st.empty()
st.write("")
left, right = st.columns([3, 2])
code_ph, stack_ph = left.empty(), right.empty()


def draw(k):
    s = steps[k]
    say.markdown(f'<div class="phase">{s["phase"]}</div><div class="say">{s["msg"]}</div>', unsafe_allow_html=True)
    viz.markdown(f'<div class="card">{bars_html(s)}</div>', unsafe_allow_html=True)
    prog.progress(k / (len(steps) - 1), text=f"Step {k} of {len(steps) - 1}")
    stats.markdown(
        '<div class="stats">'
        f'<div class="stat"><span>Comparisons</span><b>{s["cmp"]}</b></div>'
        f'<div class="stat"><span>Swaps</span><b>{s["swp"]}</b></div>'
        f'<div class="stat"><span>Recursion depth</span><b>{len(s["stack"])}</b></div></div>',
        unsafe_allow_html=True)
    code_ph.markdown(
        f'<div class="card"><h3>Pseudocode</h3>{code_html(s["line"])}'
        '<div class="note">The highlighted line is the one being executed. '
        'i moves right looking for a number greater than the pivot. '
        'j moves left looking for a number smaller than the pivot.</div></div>',
        unsafe_allow_html=True)
    stack_ph.markdown(
        f'<div class="card"><h3>Recursion call stack</h3>{stack_html(s["stack"])}'
        '<div class="note">Each line is a QuickSort call that is still waiting to finish. '
        'The top one (red) is the call running now.</div></div>', unsafe_allow_html=True)


draw(st.session_state.idx)

if play:
    if st.session_state.idx >= len(steps) - 1:
        st.session_state.idx = 0
    for k in range(st.session_state.idx, len(steps)):
        st.session_state.idx = k
        draw(k)
        time.sleep(2.6 - speed * 0.22)

with st.expander("Complexity"):
    st.markdown("""
| Case | Time | When it happens |
|---|---|---|
| Best | O(n log n) | The pivot splits the numbers into two nearly equal halves |
| Average | O(n log n) | Typical, mixed-up input |
| Worst | O(n²) | Already sorted input with a first or last pivot (very uneven splits) |

Space: O(log n) on average for the recursion stack. Quick Sort sorts in place and is not stable.
""")
with st.expander("Why the pivot choice matters"):
    st.markdown("""
The pivot decides how even each split is. If the pivot is always the smallest or largest number, one side
is empty and the other side holds almost everything, so the recursion goes about n levels deep. A pivot near
the middle value keeps the recursion about log n levels deep. This is why median of three and random pivots
exist. Watch the Recursion depth counter to see the difference.
""")