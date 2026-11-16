"""Step-by-step animations of the two standard loops over a 2-D list, for COMP 141.

In a notebook:

    from grid_animations import *
    grid = [[1, 3, 5, 7], [2, 4, 6, 8], [5, 10, 15, 20]]
    animate_row_loop(grid)
    animate_col_loop(grid)
"""

import json
import uuid

from IPython.display import HTML, display

__all__ = ["animate_row_loop", "animate_col_loop"]


ROW_LOOP_CODE = [
    "for row in range(0, len(grid)):",
    "    for col in range(0, len(grid[0])):",
    "        print(grid[row][col])",
]

COL_LOOP_CODE = [
    "for col in range(0, len(grid[0])):",
    "    for row in range(0, len(grid)):",
    "        print(grid[row][col])",
]


def _frames(grid, by_rows):
    """Builds the frames for the row-by-row loop (by_rows=True) or the
    column-by-column loop (by_rows=False)."""
    num_rows = len(grid)
    num_cols = len(grid[0])
    order = [[None] * num_cols for _ in range(num_rows)]
    output = []
    frames = []
    state = {"row": "", "col": "", "count": 0}

    def add(line, caption, band=None, cur=None):
        value = ""
        if cur is not None:
            value = str(grid[cur[0]][cur[1]])
        if by_rows:
            names = [["row", state["row"]], ["col", state["col"]]]
        else:
            names = [["col", state["col"]], ["row", state["row"]]]
        frames.append({
            "line": line,
            "vars": names + [["grid[row][col]", value]],
            "band": band,
            "cur": cur,
            "order": [list(r) for r in order],
            "output": list(output),
            "caption": caption,
        })

    def visit(row, col):
        value = grid[row][col]
        if by_rows:
            both = "row is " + str(row) + " and col is " + str(col)
        else:
            both = "col is " + str(col) + " and row is " + str(row)
        add(1, both + ", so grid[row][col] is grid["
            + str(row) + "][" + str(col) + "], which is " + str(value) + ".",
            band=row if by_rows else col, cur=[row, col])
        state["count"] += 1
        order[row][col] = state["count"]
        output.append(str(value))
        add(2, "Print grid[" + str(row) + "][" + str(col) + "], which is " + str(value) + ".",
            band=row if by_rows else col, cur=[row, col])

    if by_rows:
        for row in range(0, num_rows):
            state["row"] = str(row)
            if row == 0:
                caption = "row is 0. The inner loop will go across row 0, one column at a time."
            else:
                caption = ("The inner loop is done with row " + str(row - 1) + ", so row is now "
                           + str(row) + ". The inner loop starts over at col 0.")
            add(0, caption, band=row)
            for col in range(0, num_cols):
                state["col"] = str(col)
                visit(row, col)
        add(None, "Both loops are done. We visited all " + str(num_rows * num_cols)
            + " items row by row: all of row 0, then all of row 1, and so on.")
    else:
        for col in range(0, num_cols):
            state["col"] = str(col)
            if col == 0:
                caption = "col is 0. The inner loop will go down column 0, one row at a time."
            else:
                caption = ("The inner loop is done with column " + str(col - 1) + ", so col is now "
                           + str(col) + ". The inner loop starts over at row 0.")
            add(0, caption, band=col)
            for row in range(0, num_rows):
                state["row"] = str(row)
                visit(row, col)
        add(None, "Both loops are done. We visited all " + str(num_rows * num_cols)
            + " items column by column: all of column 0, then all of column 1, and so on.")
    return frames


def animate_row_loop(grid, seconds=1.0):
    """Animate the row-by-row loop over grid, one line at a time."""
    _show(ROW_LOOP_CODE, grid, True, _frames(grid, True), seconds)


def animate_col_loop(grid, seconds=1.0):
    """Animate the column-by-column loop over grid, one line at a time."""
    _show(COL_LOOP_CODE, grid, False, _frames(grid, False), seconds)


# ---------------------------------------------------------------------------
# The player
# ---------------------------------------------------------------------------

_STYLE = """
.ga-player { font-family: Menlo, Consolas, "DejaVu Sans Mono", monospace;
  background: #ffffff; color: #1a1a1a; border: 1px solid #d0d0d0;
  border-radius: 8px; padding: 16px; max-width: 100%; box-sizing: border-box; }
.ga-player * { box-sizing: border-box; }
.ga-top { display: flex; flex-wrap: wrap; gap: 24px; align-items: flex-start; }
.ga-code { font-size: 16px; line-height: 1.6; }
.ga-line { white-space: pre; padding: 0 8px; border-radius: 4px; border-left: 4px solid transparent; }
.ga-line.current { background: #fff3b0; border-left-color: #f0b400; }
/* ".ga-player" in front so these beat JupyterLab's own table styles */
.ga-player .ga-vars { border-collapse: collapse; font-size: 16px; margin: 0; }
.ga-player .ga-vars td { padding: 4px 10px; border: none; border-bottom: 1px solid #eee;
  font-family: inherit; font-size: 16px; }
.ga-player .ga-vars td:first-child { color: #555; text-align: right; }
.ga-player .ga-vars td:last-child { font-weight: bold; min-width: 4em; text-align: left; }
.ga-player .ga-vars td.changed { background: #fff3b0; }
.ga-middle { display: flex; flex-wrap: wrap; gap: 32px; align-items: flex-start; margin-top: 8px; }
.ga-middle > div { min-width: 0; }
.ga-gridwrap { max-width: 100%; overflow-x: auto; padding: 10px 10px 4px 0; }
.ga-grid { display: inline-grid; gap: 6px; align-items: center; justify-items: center; font-size: 18px; }
.ga-label { color: #444; font-size: 15px; white-space: pre; padding: 2px 6px; border-radius: 4px; }
.ga-label.band { background: #fff3b0; color: #1a1a1a; font-weight: bold; }
.ga-cell { position: relative; background: #5b9bd5; color: #fff; font-weight: bold;
  width: 3.2em; height: 2.4em; display: flex; align-items: center; justify-content: center;
  border: 3px solid transparent; border-radius: 4px; transition: transform 0.2s; }
.ga-cell.band { box-shadow: 0 0 0 4px #ffe08a; }
.ga-cell.current { border-color: #ed7d31; transform: translateY(-3px); }
.ga-badge { position: absolute; top: -9px; right: -9px; background: #19a149; color: #fff;
  font-size: 12px; min-width: 20px; height: 20px; line-height: 20px; border-radius: 10px;
  text-align: center; padding: 0 4px; }
.ga-out { min-width: 7em; }
.ga-out-title { font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 14px;
  color: #555; margin-bottom: 4px; }
.ga-out-box { background: #f6f6f6; border: 1px solid #ddd; border-radius: 4px; padding: 6px 10px;
  font-size: 15px; line-height: 1.35; white-space: pre; height: 15em; overflow-y: auto; }
.ga-caption { margin-top: 12px; font-family: -apple-system, "Segoe UI", Roboto, sans-serif;
  font-size: 17px; min-height: 1.6em; }
.ga-controls { margin-top: 12px; display: flex; flex-wrap: wrap; gap: 8px; align-items: center;
  font-family: -apple-system, "Segoe UI", Roboto, sans-serif; font-size: 14px; }
.ga-controls button { font-size: 14px; padding: 4px 12px; border: 1px solid #aaa;
  border-radius: 4px; background: #f4f4f4; color: #1a1a1a; cursor: pointer; }
.ga-controls button:hover { background: #e6e6e6; }
.ga-controls select { font-size: 14px; }
.ga-step { color: #555; margin-left: 6px; }
"""

_TEMPLATE = """
<div class="ga-player" id="__ID__">
<style>__STYLE__</style>
<div class="ga-body"><p>Run this cell to see the animation.</p></div>
</div>
<script>
(function () {
  var data = __DATA__;
  var root = document.getElementById("__ID__");
  if (!root) { return; }
  var body = root.querySelector(".ga-body");
  var numRows = data.grid.length, numCols = data.grid[0].length;

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) { e.className = cls; }
    if (text !== undefined) { e.textContent = text; }
    return e;
  }

  body.innerHTML = "";
  var top = el("div", "ga-top");
  var code = el("div", "ga-code");
  var lines = data.code.map(function (text) {
    var line = el("div", "ga-line", text);
    code.appendChild(line);
    return line;
  });
  var vars = el("table", "ga-vars");
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

  var middle = el("div", "ga-middle");
  var grid = el("div", "ga-grid");
  grid.style.gridTemplateColumns = "auto repeat(" + numCols + ", auto)";
  function put(e, row, col) {
    e.style.gridRow = row;
    e.style.gridColumn = col;
    grid.appendChild(e);
    return e;
  }
  var colLabels = [], rowLabels = [], cells = [], badges = [];
  for (var c = 0; c < numCols; c++) {
    colLabels.push(put(el("div", "ga-label", "col " + c), 1, c + 2));
  }
  for (var r = 0; r < numRows; r++) {
    rowLabels.push(put(el("div", "ga-label", "row " + r), r + 2, 1));
    cells.push([]);
    badges.push([]);
    for (var c = 0; c < numCols; c++) {
      var cell = put(el("div", "ga-cell", String(data.grid[r][c])), r + 2, c + 2);
      var badge = el("span", "ga-badge", "");
      cell.appendChild(badge);
      cells[r].push(cell);
      badges[r].push(badge);
    }
  }
  var gridWrap = el("div", "ga-gridwrap");
  gridWrap.appendChild(grid);
  middle.appendChild(gridWrap);
  var out = el("div", "ga-out");
  out.appendChild(el("div", "ga-out-title", "Output:"));
  var outBox = el("div", "ga-out-box", "");
  out.appendChild(outBox);
  middle.appendChild(out);
  body.appendChild(middle);

  var caption = el("div", "ga-caption");
  body.appendChild(caption);

  var controls = el("div", "ga-controls");
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
  var stepLabel = el("span", "ga-step", "");
  [restartBtn, backBtn, playBtn, nextBtn, speed, stepLabel].forEach(function (x) {
    controls.appendChild(x);
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
    for (var r = 0; r < numRows; r++) {
      rowLabels[r].classList.toggle("band", data.byRows && f.band === r);
      for (var c = 0; c < numCols; c++) {
        var inBand = f.band !== null && (data.byRows ? f.band === r : f.band === c);
        cells[r][c].classList.toggle("band", inBand);
        cells[r][c].classList.toggle("current", f.cur !== null && f.cur[0] === r && f.cur[1] === c);
        var n = f.order[r][c];
        badges[r][c].textContent = n === null ? "" : String(n);
        badges[r][c].style.display = n === null ? "none" : "inline-block";
      }
    }
    for (var c = 0; c < numCols; c++) {
      colLabels[c].classList.toggle("band", !data.byRows && f.band === c);
    }
    outBox.textContent = f.output.join("\\n");
    outBox.scrollTop = outBox.scrollHeight;
    caption.textContent = f.caption;
    stepLabel.textContent = "Step " + (step + 1) + " of " + data.frames.length;
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


def _player_html(code, grid, by_rows, frames, seconds):
    data = {
        "code": code,
        "grid": grid,
        "byRows": by_rows,
        "frames": frames,
        "seconds": seconds,
    }
    # "</" inside a script tag would end it early
    data_json = json.dumps(data).replace("</", "<\\/")
    return (_TEMPLATE.replace("__ID__", "ga-" + uuid.uuid4().hex)
                     .replace("__STYLE__", _STYLE)
                     .replace("__DATA__", data_json))


def _show(code, grid, by_rows, frames, seconds):
    display(HTML(_player_html(code, grid, by_rows, frames, seconds)))
