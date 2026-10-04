"""Binary Search Simulator: an interactive, step-by-step Streamlit app."""
import math
import random
import time

import pandas as pd
import streamlit as st

# ---------- Page setup ----------
st.set_page_config(page_title="Binary Search Simulator", page_icon="🔍", layout="wide")

INK, MUTE = "#3B3550", "#7A7391"
LAV, BLUSH, MINT, BUTTER, SKY = "#EFEAFB", "#FDEBF1", "#E5F4EC", "#FFF4D9", "#E4F0FB"
ACC, ROSE, FOUND = "#8B7FD1", "#E58FA8", "#6FC29A"

st.markdown(
    f"""
<style>
h1, h2, h3 {{ font-family: Georgia, serif !important; font-weight: normal !important; color: {INK}; }}
.hero {{ background: linear-gradient(135deg,{LAV} 0%,{BLUSH} 55%,{BUTTER} 100%);
        border-radius: 24px; padding: 34px 36px; margin-bottom: 18px; }}
.hero h1 {{ margin: 0 0 6px 0; font-size: 44px; }}
.hero p {{ margin: 0; color: {MUTE}; font-size: 17px; }}
.card {{ background: #fff; border: 1px solid #E6E0F5; border-radius: 18px; padding: 20px 22px; margin: 10px 0; }}
.explain {{ border-radius: 16px; padding: 16px 20px; margin: 12px 0; font-size: 16px; line-height: 1.7; color: {INK}; }}
.chip {{ display:inline-block; border-radius: 999px; padding: 4px 14px; margin-right: 8px; font-size: 14px;
        background:{LAV}; color:{INK}; }}
.chip b {{ color:{ACC}; }}
div[data-testid="stMetric"] {{ background:#fff; border:1px solid #E6E0F5; border-radius:16px; padding:12px 16px; }}
.stButton > button {{ border-radius: 12px; }}
</style>
""",
    unsafe_allow_html=True,
)


# ---------- Core algorithm: record every step ----------
def build_steps(data, target):
    """Run binary search and return one record per frame of the animation."""
    n = len(data)
    low, high = 0, n - 1
    steps = [dict(low=low, high=high, mid=None, kind="start",
                  msg=f"We are looking for <b>{target}</b>. We begin with the whole list, so every box is still possible.")]
    while low <= high:
        mid = low + (high - low) // 2
        v = data[mid]
        if v == target:
            steps.append(dict(low=low, high=high, mid=mid, kind="found",
                              msg=f"Check the middle box: it holds <b>{v}</b>. That is our target, so we found it at position <b>{mid}</b>!"))
            return steps
        if v < target:
            steps.append(dict(low=low, high=high, mid=mid, kind="less",
                              msg=f"Check the middle box: it holds <b>{v}</b>. {v} is smaller than {target}, so {target} must be on the <b>right</b>. Throw away the middle box and everything to its left."))
            low = mid + 1
        else:
            steps.append(dict(low=low, high=high, mid=mid, kind="greater",
                              msg=f"Check the middle box: it holds <b>{v}</b>. {v} is bigger than {target}, so {target} must be on the <b>left</b>. Throw away the middle box and everything to its right."))
            high = mid - 1
    steps.append(dict(low=low, high=high, mid=None, kind="missing",
                      msg=f"No boxes are left to check, so <b>{target}</b> is not in this list."))
    return steps


# ---------- State and callbacks ----------
def new_random():
    size = st.session_state.size
    st.session_state.rand_arr = sorted(random.sample(range(1, 100), size))
    st.session_state.target = random.choice(st.session_state.rand_arr)
    st.session_state.playing = False


def pick_existing():
    arr = st.session_state.cur_arr
    st.session_state.target = random.choice(arr)


def pick_missing():
    arr = set(st.session_state.cur_arr)
    pool = [x for x in range(1, 100) if x not in arr]
    st.session_state.target = random.choice(pool)


def stop():
    st.session_state.playing = False


def go_next():
    st.session_state.playing = False
    st.session_state.step = min(st.session_state.step + 1, st.session_state.last)


def go_back():
    st.session_state.playing = False
    st.session_state.step = max(st.session_state.step - 1, 0)


def go_reset():
    st.session_state.playing = False
    st.session_state.step = 0


def start_play():
    if st.session_state.step >= st.session_state.last:
        st.session_state.step = 0
    st.session_state.playing = True


if "rand_arr" not in st.session_state:
    st.session_state.size = 12
    st.session_state.rand_arr = sorted(random.sample(range(1, 100), 12))
    st.session_state.target = random.choice(st.session_state.rand_arr)
    st.session_state.step = 0
    st.session_state.playing = False

# ---------- Sidebar: data and target ----------
with st.sidebar:
    st.header("Setup")
    source = st.radio("List of numbers", ["Random", "Custom"], horizontal=True, on_change=stop)
    if source == "Random":
        st.slider("How many numbers", 5, 30, key="size", on_change=new_random)
        st.button("New random list", on_click=new_random, width="stretch")
        arr = st.session_state.rand_arr
    else:
        raw = st.text_input("Numbers (comma separated)", "4, 9, 15, 21, 28, 34, 41, 57, 63, 79",
                            help="They are sorted for you, because binary search needs sorted data.")
        try:
            parsed = sorted(int(x) for x in raw.replace(" ", ",").split(",") if x.strip() != "")
            if not 1 <= len(parsed) <= 40:
                raise ValueError
            arr = parsed
        except ValueError:
            st.error("Enter between 1 and 40 whole numbers, e.g. 3, 8, 15.")
            arr = st.session_state.rand_arr
    st.session_state.cur_arr = arr

    st.number_input("Number to find", step=1, key="target", on_change=stop)
    c1, c2 = st.columns(2)
    c1.button("One in the list", on_click=pick_existing, width="stretch", help="Pick a number that is in the list")
    c2.button("One not in the list", on_click=pick_missing, width="stretch", help="Pick a number that is not in the list")

    st.header("Playback")
    delay = st.slider("Speed (seconds per step)", 0.2, 2.0, 0.9, 0.1)

target = int(st.session_state.target)
steps = build_steps(arr, target)
st.session_state.last = len(steps) - 1

# Reset the walkthrough whenever the data or the target changes.
sig = (tuple(arr), target)
if st.session_state.get("sig") != sig:
    st.session_state.sig = sig
    st.session_state.step = 0
    st.session_state.playing = False

# Advance autoplay (done before the step slider is created).
if st.session_state.playing:
    if st.session_state.step < st.session_state.last:
        st.session_state.step += 1
    if st.session_state.step >= st.session_state.last:
        st.session_state.playing = False
        finished_now = True
    else:
        finished_now = False
else:
    finished_now = False

st.session_state.step = min(st.session_state.step, st.session_state.last)
cur = steps[st.session_state.step]

# ---------- Header ----------
st.markdown(
    '<div class="hero"><h1>Binary Search Simulator</h1>'
    "<p>Pick a number to find. Each step checks the middle box and throws away half of the list. Press Play or go step by step.</p></div>",
    unsafe_allow_html=True,
)

# ---------- Controls ----------
b1, b2, b3, b4 = st.columns(4)
b1.button("⏮ Reset", on_click=go_reset, width="stretch")
b2.button("◀ Back", on_click=go_back, width="stretch", disabled=st.session_state.step == 0)
b3.button("Next ▶", on_click=go_next, width="stretch",
          disabled=st.session_state.step >= st.session_state.last)
if st.session_state.playing:
    b4.button("⏸ Pause", on_click=stop, width="stretch", type="primary")
else:
    b4.button("▶ Play", on_click=start_play, width="stretch", type="primary")
st.slider("Step", 0, st.session_state.last, key="step", on_change=stop)

# ---------- Metrics ----------
n = len(arr)
done_steps = steps[: st.session_state.step + 1]
comparisons = sum(1 for s in done_steps if s["mid"] is not None)
m1, m2 = st.columns(2)
m1.metric("Numbers in the list", n)
m2.metric("Boxes checked so far", comparisons)

# ---------- Array visual ----------
low, high, mid, kind = cur["low"], cur["high"], cur["mid"], cur["kind"]
cells = []
for i, v in enumerate(arr):
    in_range = low <= i <= high
    if kind == "found" and i == mid:
        style = f"background:{FOUND};border:2px solid {FOUND};color:#fff;font-weight:bold;transform:translateY(-6px)"
    elif i == mid:
        style = f"background:{ACC};border:2px solid {ACC};color:#fff;font-weight:bold;transform:translateY(-6px)"
    elif in_range:
        style = f"background:#fff;border:2px solid #D9D2F0;color:{INK}"
    else:
        style = "background:#F5F2FA;border:2px dashed #DDD7EC;color:#BDB5D3"
    tags = []
    if in_range and i == low:
        tags.append("start")
    if i == mid:
        tags.append("middle")
    if in_range and i == high:
        tags.append("end")
    label = "/".join(tags) or "&nbsp;"
    cells.append(
        f'<div style="text-align:center;min-width:52px">'
        f'<div style="width:52px;height:52px;line-height:48px;border-radius:14px;font-family:Georgia,serif;'
        f'font-size:19px;transition:all .3s;{style}">{v}</div>'
        f'<div style="font-size:11px;color:#B3ABCB;line-height:18px">{i}</div>'
        f'<div style="height:18px;font-size:12px;font-weight:bold;color:{ROSE};white-space:nowrap">{label}</div></div>'
    )
legend = "".join(
    f'<span style="margin-right:16px"><span style="display:inline-block;width:13px;height:13px;border-radius:4px;'
    f'background:{bg};border:1px solid {bd};vertical-align:-2px;margin-right:6px"></span>{t}</span>'
    for bg, bd, t in [(ACC, ACC, "Middle (being checked)"), ("#fff", "#D9D2F0", "Still possible"),
                      ("#F5F2FA", "#DDD7EC", "Thrown away"), (FOUND, FOUND, "Found")]
)
st.markdown(
    f'<div class="card"><div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding-top:10px">{"".join(cells)}</div>'
    f'<div style="font-size:13px;color:{MUTE};margin-top:12px;text-align:center">{legend}</div></div>',
    unsafe_allow_html=True,
)

# ---------- Explanation ----------
bg = {"start": SKY, "less": LAV, "greater": BLUSH, "found": MINT, "missing": BUTTER}[kind]
chips = f'<span class="chip">Looking for <b>{target}</b></span>'
if kind not in ("start", "missing"):
    chips += f'<span class="chip">Middle box <b>{mid}</b></span>'
st.markdown(
    f'<div class="explain" style="background:{bg}"><div style="margin-bottom:8px">{chips}</div>{cur["msg"]}</div>',
    unsafe_allow_html=True,
)
if kind in ("found", "missing") and st.session_state.step == st.session_state.last:
    if kind == "found":
        st.success(f"Found it after checking only {comparisons} box(es). Checking one by one from the left would have taken {arr.index(target) + 1}.")
    else:
        st.info(f"We checked {comparisons} box(es) and ruled out the whole list.")

# ---------- Step history ----------
with st.expander("See every step so far"):
    log = pd.DataFrame([{
        "Step": str(i),
        "Middle box": "-" if x["mid"] is None else str(x["mid"]),
        "Value there": "-" if x["mid"] is None else str(arr[x["mid"]]),
        "What happened": {"start": "Started", "less": "Too small, go right", "greater": "Too big, go left",
                          "found": "Found it", "missing": "Not in the list"}[x["kind"]],
    } for i, x in enumerate(done_steps)])
    st.dataframe(log, hide_index=True, width="stretch")

# ---------- Autoplay loop ----------
if st.session_state.playing:
    time.sleep(delay)
    st.rerun()