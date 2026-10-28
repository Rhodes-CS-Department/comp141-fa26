"""Step-by-step animations of the basic string loop, for COMP 141.

In a notebook:

    from string_animations import *
    animate_count_upper("BanANA")
    animate_keep_capitals("BanANA")
    animate_double_chars("BanANA")
"""

import html
import json
import uuid

from IPython.display import HTML, display

__all__ = ["animate_count_upper", "animate_keep_capitals", "animate_double_chars"]


def _q(s):
    """Show a string the way Python would, in double quotes."""
    if '"' in s:
        return "'" + s + "'"
    return '"' + s + '"'


# ---------------------------------------------------------------------------
# Counting
# ---------------------------------------------------------------------------

COUNT_UPPER_CODE = [
    "def count_upper(string):",
    "    count = 0",
    "    for idx in range(0, len(string)):",
    "        if string[idx].isupper():",
    "            count += 1",
    "    return count",
]


def _count_upper_frames(string):
    frames = []
    marks = [None] * len(string)
    count = 0

    def add(line, idx, caption, result=None):
        ch = _q(string[idx]) if idx is not None else ""
        frames.append({
            "line": line,
            "idx": idx,
            "vars": [["idx", "" if idx is None else str(idx)],
                     ["string[idx]", ch],
                     ["count", str(count)]],
            "marks": list(marks),
            "result": result,
            "caption": caption,
        })

    add(1, None, "Start the count at 0.")
    for idx in range(0, len(string)):
        ch = string[idx]
        add(2, idx, "idx is " + str(idx) + ", so string[idx] is " + _q(ch) + ".")
        if ch.isupper():
            add(3, idx, "Is " + _q(ch) + " uppercase? Yes!")
            count += 1
            marks[idx] = ["+1", "yes"]
            add(4, idx, "Add 1 to count. count is now " + str(count) + ".")
        else:
            marks[idx] = ["+0", "no"]
            add(3, idx, "Is " + _q(ch) + " uppercase? No, so skip count += 1. "
                        "count stays " + str(count) + ".")
    add(5, None, "The loop is done, so return count, which is " + str(count) + ".",
        result="= " + str(count))
    return frames


def animate_count_upper(string, seconds=1.2):
    """Animate count_upper(string) one line at a time."""
    _show(COUNT_UPPER_CODE, {1: "init", 4: "update"}, string,
          "count = 0", _count_upper_frames(string), seconds)


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

KEEP_CAPITALS_CODE = [
    "def keep_capitals(string):",
    '    answer = ""',
    "    for idx in range(0, len(string)):",
    "        if string[idx].isupper():",
    "            answer = answer + string[idx]",
    "    return answer",
]


def _keep_capitals_frames(string):
    frames = []
    marks = [None] * len(string)
    answer = ""

    def add(line, idx, caption, result=None):
        ch = _q(string[idx]) if idx is not None else ""
        frames.append({
            "line": line,
            "idx": idx,
            "vars": [["idx", "" if idx is None else str(idx)],
                     ["string[idx]", ch],
                     ["answer", _q(answer)]],
            "marks": list(marks),
            "result": result,
            "caption": caption,
        })

    add(1, None, 'Start answer as the empty string, "".')
    for idx in range(0, len(string)):
        ch = string[idx]
        add(2, idx, "idx is " + str(idx) + ", so string[idx] is " + _q(ch) + ".")
        if ch.isupper():
            add(3, idx, "Is " + _q(ch) + " uppercase? Yes, so keep it!")
            answer = answer + ch
            marks[idx] = ["+ " + _q(ch), "yes"]
            add(4, idx, "Add " + _q(ch) + " to the end of answer. answer is now " + _q(answer) + ".")
        else:
            marks[idx] = ['+ ""', "no"]
            add(3, idx, "Is " + _q(ch) + " uppercase? No, so skip it. "
                        "answer stays " + _q(answer) + ".")
    add(5, None, "The loop is done, so return answer, which is " + _q(answer) + ".",
        result="= " + _q(answer))
    return frames


def animate_keep_capitals(string, seconds=1.2):
    """Animate keep_capitals(string) one line at a time."""
    _show(KEEP_CAPITALS_CODE, {1: "init", 4: "update"}, string,
          'answer = ""', _keep_capitals_frames(string), seconds)


# ---------------------------------------------------------------------------
# Transforming
# ---------------------------------------------------------------------------

DOUBLE_CHARS_CODE = [
    "def double_chars(string):",
    '    answer = ""',
    "    for idx in range(0, len(string)):",
    "        answer = answer + string[idx] + string[idx]",
    "    return answer",
]


def _double_chars_frames(string):
    frames = []
    marks = [None] * len(string)
    answer = ""

    def add(line, idx, caption, result=None):
        ch = _q(string[idx]) if idx is not None else ""
        frames.append({
            "line": line,
            "idx": idx,
            "vars": [["idx", "" if idx is None else str(idx)],
                     ["string[idx]", ch],
                     ["answer", _q(answer)]],
            "marks": list(marks),
            "result": result,
            "caption": caption,
        })

    add(1, None, 'Start answer as the empty string, "".')
    for idx in range(0, len(string)):
        ch = string[idx]
        add(2, idx, "idx is " + str(idx) + ", so string[idx] is " + _q(ch) + ".")
        answer = answer + ch + ch
        marks[idx] = ["+ " + _q(ch + ch), "yes"]
        add(3, idx, "Add " + _q(ch) + " twice to the end of answer. answer is now " + _q(answer) + ".")
    add(4, None, "The loop is done, so return answer, which is " + _q(answer) + ".",
        result="= " + _q(answer))
    return frames


def animate_double_chars(string, seconds=1.2):
    """Animate double_chars(string) one line at a time."""
    _show(DOUBLE_CHARS_CODE, {1: "init", 3: "update"}, string,
          'answer = ""', _double_chars_frames(string), seconds)


# ---------------------------------------------------------------------------
# The player (shared by all the animations)
# ---------------------------------------------------------------------------

_STYLE = """
.sa-player { font-family: Menlo, Consolas, "DejaVu Sans Mono", monospace;
  background: #ffffff; color: #1a1a1a; border: 1px solid #d0d0d0;
  border-radius: 8px; padding: 16px; max-width: 100%; box-sizing: border-box; }
.sa-player * { box-sizing: border-box; }
.sa-top { display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start; }
.sa-code { font-size: 16px; line-height: 1.6; }
.sa-line { white-space: pre; padding: 0 8px; border-radius: 4px; border-left: 4px solid transparent; }
.sa-line.init { color: #d41f1f; }
.sa-line.update { color: #19a149; }
.sa-line.current { background: #fff3b0; border-left-color: #f0b400; }
/* ".sa-player" in front so these beat JupyterLab's own table styles */
.sa-player .sa-vars { border-collapse: collapse; font-size: 16px; margin: 0; }
.sa-player .sa-vars td { padding: 4px 10px; border: none; border-bottom: 1px solid #eee;
  font-family: inherit; font-size: 16px; }
.sa-player .sa-vars td:first-child { color: #555; text-align: right; }
.sa-player .sa-vars td:last-child { font-weight: bold; min-width: 4em; text-align: left; }
.sa-player .sa-vars td.changed { background: #fff3b0; }
.sa-strip { position: relative; overflow-x: auto; margin-top: 18px; padding-bottom: 4px; }
.sa-grid { display: inline-grid; column-gap: 4px; row-gap: 2px; align-items: center;
  justify-items: center; font-size: 18px; }
.sa-index { color: #444; }
.sa-box { background: #5b9bd5; color: #fff; font-weight: bold; padding: 6px 8px;
  min-width: 2.6em; text-align: center; white-space: pre; border: 3px solid transparent;
  border-radius: 3px; transition: transform 0.2s; }
.sa-box.current { border-color: #ed7d31; transform: translateY(-3px); }
.sa-arrow { color: #ed7d31; font-size: 34px; line-height: 1; height: 38px; font-weight: bold; }
.sa-mark { font-weight: bold; height: 1.5em; white-space: pre; }
.sa-mark.yes { color: #19a149; }
.sa-mark.no { color: #888; }
.sa-label { color: #d41f1f; font-weight: bold; white-space: pre; justify-self: end; padding-right: 6px; }
.sa-result { font-weight: bold; white-space: pre; justify-self: start; padding-left: 6px; }
.sa-caption { margin-top: 12px; font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 17px; min-height: 1.6em; }
.sa-controls { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 14px; }
.sa-controls button { font-size: 14px; padding: 4px 12px; border: 1px solid #aaa;
  border-radius: 4px; background: #f4f4f4; color: #1a1a1a; cursor: pointer; }
.sa-controls button:hover { background: #e6e6e6; }
.sa-controls select { font-size: 14px; }
.sa-step { color: #555; margin-left: 6px; }
"""

_TEMPLATE = """
<div class="sa-player" id="__ID__">
<style>__STYLE__</style>
<div class="sa-body"><p>Run this cell to see the animation.</p></div>
</div>
<script>
(function () {
  var data = __DATA__;
  var root = document.getElementById("__ID__");
  if (!root) { return; }
  var body = root.querySelector(".sa-body");
  var n = data.string.length;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (text !== undefined) { e.textContent = text; }
    return e;
  }

  body.innerHTML = "";
  var top = el("div", "sa-top");
  var code = el("div", "sa-code");
  var lines = data.code.map(function (text, i) {
    var line = el("div", "sa-line " + (data.lineClasses[i] || ""), text);
    code.appendChild(line);
    return line;
  });
  var vars = el("table", "sa-vars");
  var varCells = data.frames[0].vars.map(function (v) {
    var tr = el("tr");
    tr.appendChild(el("td", "", v[0]));
    var td = el("td");
    tr.appendChild(td);
    vars.appendChild(tr);
    return td;
  });
  top.appendChild(code);
  top.appendChild(vars);
  body.appendChild(top);

  var strip = el("div", "sa-strip");
  var grid = el("div", "sa-grid");
  grid.style.gridTemplateColumns = "auto repeat(" + n + ", auto) auto";
  function put(e, row, col) {
    e.style.gridRow = row;
    e.style.gridColumn = col;
    grid.appendChild(e);
    return e;
  }
  var boxes = [], arrows = [], marks = [];
  for (var i = 0; i < n; i++) {
    put(el("div", "sa-index", String(i)), 1, i + 2);
    boxes.push(put(el("div", "sa-box", JSON.stringify(data.string[i])), 2, i + 2));
    arrows.push(put(el("div", "sa-arrow", ""), 3, i + 2));
    marks.push(put(el("div", "sa-mark", ""), 4, i + 2));
  }
  put(el("div", "sa-label", data.label), 4, 1);
  var result = put(el("div", "sa-result", ""), 4, n + 2);
  strip.appendChild(grid);
  body.appendChild(strip);

  var caption = el("div", "sa-caption");
  body.appendChild(caption);

  var controls = el("div", "sa-controls");
  var restartBtn = el("button", "", "Restart");
  var backBtn = el("button", "", "\\u25c0 Back");
  var playBtn = el("button", "", "\\u25b6 Play");
  var nextBtn = el("button", "", "Next \\u25b6");
  var speed = el("select");
  [["Slow", 2.0], ["Normal", 1.0], ["Fast", 0.5]].forEach(function (s) {
    var o = el("option", "", s[0]);
    o.value = s[1];
    if (s[1] === 1.0) { o.selected = true; }
    speed.appendChild(o);
  });
  var stepLabel = el("span", "sa-step", "");
  [restartBtn, backBtn, playBtn, nextBtn, speed, stepLabel].forEach(function (c) {
    controls.appendChild(c);
  });
  body.appendChild(controls);

  var step = 0, timer = null;

  function show(k) {
    step = Math.max(0, Math.min(k, data.frames.length - 1));
    var f = data.frames[step];
    var prev = step > 0 ? data.frames[step - 1] : null;
    lines.forEach(function (line, i) { line.classList.toggle("current", i === f.line); });
    f.vars.forEach(function (v, i) {
      varCells[i].textContent = v[1];
      varCells[i].classList.toggle("changed", prev !== null && prev.vars[i][1] !== v[1] && v[1] !== "");
    });
    for (var i = 0; i < n; i++) {
      boxes[i].classList.toggle("current", i === f.idx);
      arrows[i].textContent = (i === f.idx) ? "\\u2193" : "";
      var m = f.marks[i];
      marks[i].textContent = m ? m[0] : "";
      marks[i].className = "sa-mark" + (m ? " " + m[1] : "");
    }
    result.textContent = f.result || "";
    caption.textContent = f.caption;
    stepLabel.textContent = "Step " + (step + 1) + " of " + data.frames.length;
    if (f.idx !== null) {
      // keep the current box visible by scrolling the strip sideways, not the page
      var b = boxes[f.idx];
      if (b.offsetLeft < strip.scrollLeft) {
        strip.scrollLeft = b.offsetLeft - 40;
      } else if (b.offsetLeft + b.offsetWidth > strip.scrollLeft + strip.clientWidth) {
        strip.scrollLeft = b.offsetLeft + b.offsetWidth - strip.clientWidth + 40;
      }
    }
  }

  function stop() {
    if (timer !== null) { clearInterval(timer); timer = null; }
    playBtn.textContent = "\\u25b6 Play";
  }
  function play() {
    if (step === data.frames.length - 1) { show(0); }
    playBtn.textContent = "\\u23f8 Pause";
    timer = setInterval(function () {
      if (step >= data.frames.length - 1) { stop(); } else { show(step + 1); }
    }, data.seconds * 1000 * Number(speed.value));
  }

  restartBtn.onclick = function () { stop(); show(0); };
  backBtn.onclick = function () { stop(); show(step - 1); };
  nextBtn.onclick = function () { stop(); show(step + 1); };
  playBtn.onclick = function () { if (timer === null) { play(); } else { stop(); } };
  speed.onchange = function () { if (timer !== null) { stop(); play(); } };

  show(0);
})();
</script>
"""


def _player_html(code, line_classes, string, label, frames, seconds):
    data = {
        "code": code,
        "lineClasses": [line_classes.get(i, "") for i in range(len(code))],
        "string": string,
        "label": label,
        "frames": frames,
        "seconds": seconds,
    }
    # "</" inside a script tag would end it early
    data_json = json.dumps(data).replace("</", "<\\/")
    return (_TEMPLATE.replace("__ID__", "sa-" + uuid.uuid4().hex)
                     .replace("__STYLE__", _STYLE)
                     .replace("__DATA__", data_json))


def _show(code, line_classes, string, label, frames, seconds):
    display(HTML(_player_html(code, line_classes, string, label, frames, seconds)))
