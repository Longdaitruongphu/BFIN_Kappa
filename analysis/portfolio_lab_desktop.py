"""Modern local desktop UI. All Tk operations stay on the main thread."""
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime
import json
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import numpy as np
import pandas as pd

import interactive_surplus_portfolio_lab as core
from portfolio_lab_scenarios import Settings, calculate, baseline_comparison, export_bundle
from portfolio_lab_charts import VIEWS, draw_figure, identity

BG = "#eef3f8"
NAVY = "#18334c"
TEAL = "#007f86"
GUIDE = core.ROOT / "advisory/2026-10-20/PORTFOLIO_LAB_USER_GUIDE_VI.md"

# UI percentages / bps are converted exactly once at the boundary.
FIELDS = [
    ("rf", "Forecast risk-free", "%", 100, "Lãi suất danh nghĩa cho dự báo/CAL/Sharpe; không thay RF lịch sử của FF3."),
    ("erp", "Market risk premium", "%", 100, "Lợi suất kỳ vọng thêm so với RF. 4.5% + RF 4% = thị trường kỳ vọng 8.5%."),
    ("smb", "SMB expected premium", "%", 100, "Phần bù small-minus-big; chỉ dùng khi chọn FF3. Blank = chưa quyết định."),
    ("hml", "HML expected premium", "%", 100, "Phần bù value-minus-growth; chỉ dùng khi chọn FF3. 0% là một giả định chủ động."),
    ("a", "Risk aversion A", "", 1, "A cao phạt variance mạnh hơn. A=4 là giả định làm việc, không phải chuẩn ngành."),
    ("inflation", "Planning inflation", "%", 100, "Đổi sức mua mục tiêu 2030; không tự thay lợi suất danh nghĩa hay tỷ trọng tối ưu."),
    ("vol_mult", "Volatility multiplier", "×", 1, "1.25 = độ lệch chuẩn tăng 25%; covariance tăng 1.25² = 1.5625 lần."),
    ("corr_stress", "Correlation stress", "%", 100, "0% giữ tương quan; 50% kéo nửa đường về +1; 100% đồng biến hoàn toàn."),
    ("shrink", "Diagonal shrinkage", "%", 100, "0% giữ matrix; 100% bỏ covariance chéo. Đây là sensitivity thủ công, không phải Ledoit–Wolf."),
    ("return_shift", "Return shift (all assets)", "pp", 100, "-2 = trừ 2 điểm % khỏi lợi suất năm kỳ vọng của mỗi tài sản; không phải cú sập tức thời."),
    ("cost", "Cost per dollar traded", "bps", 10000, "10 bps = 0.1% trên tổng tiền mua + bán mỗi lần rebalance; chỉ áp dụng kiểm chứng lịch sử."),
    ("asset_cap", "Optional max any asset", "%", 100, "Để trống = không giới hạn thêm. Bao gồm cả ETF; không phải rule đề bài."),
    ("stock_cap", "Optional direct-stock total", "%", 100, "Để trống = không giới hạn thêm; 0% chỉ cho ETF. Không cộng look-through cổ phiếu bên trong ETF."),
    ("real_goal", "2030 real goal", "$m", 1e-6, "8 = 8 triệu USD sức mua Dec-2022. Đổi mục tiêu là thử nghiệm, không sửa đề gốc."),
]


class Tip:
    def __init__(self, widget, text):
        self.widget, self.text, self.popup = widget, text, None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)
    def show(self, _=None):
        if self.popup: return
        self.popup = tk.Toplevel(self.widget)
        self.popup.wm_overrideredirect(True)
        self.popup.wm_geometry(f"+{self.widget.winfo_rootx()+12}+{self.widget.winfo_rooty()+25}")
        tk.Label(self.popup, text=self.text, wraplength=330, bg=NAVY, fg="white",
                 padx=12, pady=9, justify="left", font=("Segoe UI", 10)).pack()
    def hide(self, _=None):
        if self.popup: self.popup.destroy(); self.popup = None


def scroll_frame(parent):
    holder = ttk.Frame(parent)
    holder.pack(fill="both", expand=True)
    canvas = tk.Canvas(holder, bg="white", highlightthickness=0, width=330)
    bar = ttk.Scrollbar(holder, orient="vertical", command=canvas.yview)
    bar.pack(side="right", fill="y"); canvas.pack(side="left", fill="both", expand=True)
    frame = ttk.Frame(canvas, padding=12)
    window = canvas.create_window((0, 0), window=frame, anchor="nw")
    frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window, width=e.width))
    canvas.configure(yscrollcommand=bar.set)
    def wheel(event):
        canvas.yview_scroll(int(-event.delta / 120), "units")
    # Bind to descendants through the shared top-level event, only when pointer is within this pane.
    def scoped_wheel(event):
        if str(event.widget).startswith(str(holder)): wheel(event)
    parent.winfo_toplevel().bind("<MouseWheel>", scoped_wheel, add="+")
    return frame


class ModernPortfolioLab:
    def __init__(self, root, auto_start=True):
        import matplotlib
        matplotlib.use("TkAgg")
        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        self.root = root
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None; self.result = None; self.baseline = None; self.closed = False
        self.checks = {}; self.redraw_job = None
        root.title("Kappa | Portfolio Research Lab")
        root.geometry("1480x940"); root.minsize(1080, 720); root.configure(bg=BG)
        root.protocol("WM_DELETE_WINDOW", self.close)
        style = ttk.Style(root); style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10))
        style.configure("TFrame", background="white")
        style.configure("TLabel", background="white", foreground=NAVY)
        style.configure("TCheckbutton", background="white", padding=(2, 5))
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(12, 9))
        style.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", TEAL)])
        style.configure("TButton", padding=(9, 7), background="#e9f0f6", borderwidth=0)
        style.configure("Accent.TButton", foreground="white", background=TEAL, font=("Segoe UI", 10, "bold"))
        style.map("Accent.TButton", background=[("active", "#00666c"), ("disabled", "#8da8aa")])
        style.configure("Treeview", rowheight=29, font=("Segoe UI", 9), borderwidth=0)
        style.configure("Treeview.Heading", background="#e7eff6", foreground=NAVY, font=("Segoe UI", 9, "bold"))
        header = tk.Frame(root, bg=NAVY, height=70); header.pack(fill="x"); header.pack_propagate(False)
        tk.Label(header, text="KAPPA  /  PORTFOLIO LAB", fg="white", bg=NAVY,
                 font=("Segoe UI", 18, "bold")).pack(side="left", padx=22)
        tk.Label(header, text="DECISION 31 DEC 2022\nSCENARIOS ≠ APPROVED POLICY",
                 bg=NAVY, fg="#bdd4e6", justify="right", font=("Segoe UI", 9)).pack(side="right", padx=22)
        self.status = tk.StringVar(value="Ready")
        tk.Label(root, textvariable=self.status, bg=BG, fg="#425b71", anchor="w",
                 padx=16, pady=8, font=("Segoe UI", 9)).pack(side="bottom", fill="x")
        main = ttk.Panedwindow(root, orient="horizontal"); main.pack(fill="both", expand=True, padx=12, pady=12)
        self.sidebar = ttk.Frame(main, width=350); main.add(self.sidebar, weight=0)
        self.workspace = ttk.Frame(main); main.add(self.workspace, weight=1)
        root.after(50, lambda: main.sashpos(0, 350))
        ttk.Button(self.sidebar, text="Apply & recalculate", style="Accent.TButton", command=self.recalculate).pack(fill="x", padx=10, pady=10)
        self.progress = ttk.Progressbar(self.sidebar, mode="indeterminate"); self.progress.pack(fill="x", padx=10)
        self.controls = ttk.Notebook(self.sidebar); self.controls.pack(fill="both", expand=True, padx=4, pady=8)
        self.inputs = scroll_frame(self._control_tab("Inputs"))
        self.stress = scroll_frame(self._control_tab("Stress"))
        self.portfolios = scroll_frame(self._control_tab("Portfolios"))
        self.vars = {}; self.shock_vars = {}; self.custom_vars = {}
        self._build_inputs()
        self._build_stress()
        ttk.Label(self.portfolios, text="Only checked portfolios are drawn / exported.", wraplength=290).pack(anchor="w", pady=6)
        bar = ttk.Frame(self.portfolios); bar.pack(fill="x")
        for label, action in [("Core", self.select_core), ("All", lambda: self.select_all(True)), ("None", lambda: self.select_all(False))]:
            ttk.Button(bar, text=label, command=action).pack(side="left", padx=2)
        self.check_frame = ttk.Frame(self.portfolios); self.check_frame.pack(fill="both", expand=True, pady=8)
        self.cards = tk.StringVar(value="Loading local data…")
        self.card_label = tk.Label(self.workspace, textvariable=self.cards, bg="#eaf5f4", fg=NAVY, anchor="w",
                 justify="left", padx=15, pady=12, font=("Segoe UI", 10))
        self.card_label.pack(fill="x", padx=10, pady=10)
        self.workspace.bind("<Configure>", lambda e: self.card_label.configure(wraplength=max(e.width-60, 300)))
        toolbar = ttk.Frame(self.workspace); toolbar.pack(fill="x", padx=10)
        self.view = tk.StringVar(value=VIEWS[0])
        choices = ttk.Combobox(toolbar, textvariable=self.view, values=VIEWS + ["Scorecard", "Baseline comparison"],
                               state="readonly", width=23)
        choices.pack(side="left"); choices.bind("<<ComboboxSelected>>", lambda _: self.draw())
        self.details = tk.BooleanVar(value=True)
        ttk.Checkbutton(toolbar, text="Point labels", variable=self.details, command=self.draw).pack(side="left", padx=7)
        ttk.Button(toolbar, text="Pin baseline", command=self.pin).pack(side="left", padx=3)
        ttk.Button(toolbar, text="Export", command=self.export).pack(side="right")
        ttk.Button(toolbar, text="Guide VI", command=lambda: os.startfile(GUIDE)).pack(side="right", padx=3)
        self.content = ttk.Frame(self.workspace); self.content.pack(fill="both", expand=True, padx=8, pady=6)
        self.graph_frame = ttk.Frame(self.content)
        self.figure = Figure(figsize=(11, 7), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.navigation = NavigationToolbar2Tk(self.canvas, self.graph_frame, pack_toolbar=False)
        self.navigation.update(); self.navigation.pack(fill="x")
        self.canvas.mpl_connect("motion_notify_event", self.hover)
        self.points = []
        self.table_frame = ttk.Frame(self.content)
        self.table = ttk.Treeview(self.table_frame, show="headings")
        xs = ttk.Scrollbar(self.table_frame, orient="horizontal", command=self.table.xview)
        ys = ttk.Scrollbar(self.table_frame, orient="vertical", command=self.table.yview)
        self.table.configure(xscrollcommand=xs.set, yscrollcommand=ys.set)
        xs.pack(side="bottom", fill="x"); ys.pack(side="right", fill="y"); self.table.pack(fill="both", expand=True)
        self.reset()
        if auto_start: root.after(120, self.recalculate)

    def _control_tab(self, name):
        frame = ttk.Frame(self.controls); self.controls.add(frame, text=name); return frame

    def _combo(self, parent, name, value, choices, tip):
        ttk.Label(parent, text=name).pack(anchor="w", pady=(8, 3))
        var = tk.StringVar(value=value)
        widget = ttk.Combobox(parent, textvariable=var, values=choices, state="readonly")
        widget.pack(fill="x"); Tip(widget, tip); return var

    def _build_inputs(self):
        ttk.Label(self.inputs, text="Forecast & risk model", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        self.model = self._combo(self.inputs, "Expected-return model", "CAPM", ["CAPM", "FF3"],
                                "CAPM: thị trường. FF3: thêm size/value. Alpha dự báo luôn bằng 0.")
        self.risk = self._combo(self.inputs, "Common scoring covariance", "Sample", ["Sample", "Single-index"],
                               "Mọi danh mục trong bảng được chấm bằng cùng matrix này; tên Sample/Single-index chỉ matrix đã tạo tỷ trọng.")
        self.months = self._combo(self.inputs, "Training months ending Dec 2022", "96", ["60", "72", "84", "96"],
                                 "96 = Jan2015; 60 = Jan2018. Mọi beta/covariance đều được tính lại cùng cửa sổ.")
        self.frequency = self._combo(self.inputs, "Historical rebalance rule", "Annual", ["Annual", "Quarterly", "Monthly", "Buy and hold"],
                                    "Đổi lịch rebalance trong kiểm chứng lịch sử; không tự đưa turnover/cost vào hàm tối ưu.")
        for key, label, unit, scale, tip in FIELDS:
            row = ttk.Frame(self.inputs); row.pack(fill="x", pady=(9, 0))
            ttk.Label(row, text=label).pack(side="left")
            help_label = ttk.Label(row, text="  ⓘ", foreground=TEAL); help_label.pack(side="left"); Tip(help_label, tip)
            entry_row = ttk.Frame(self.inputs); entry_row.pack(fill="x", pady=(3, 0))
            var = tk.StringVar(); self.vars[key] = var
            entry = ttk.Entry(entry_row, textvariable=var, width=13); entry.pack(side="left"); Tip(entry, tip)
            ttk.Label(entry_row, text=unit, foreground="#68798b").pack(side="left", padx=8)
        ttk.Label(self.inputs, text="Long-only · 100% equity sleeve.\nExtra caps are optional, initially blank.\nHover over ⓘ for Vietnamese explanations.",
                  foreground="#62788d", wraplength=285).pack(anchor="w", pady=14)
        ttk.Button(self.inputs, text="Reset all inputs", command=self.reset).pack(fill="x", pady=4)
        ttk.Button(self.inputs, text="Load exported scenario JSON", command=self.load).pack(fill="x", pady=4)

    def _build_stress(self):
        ttk.Label(self.stress, text="Illustrative scenarios", font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(self.stress, text="Presets overwrite listed stress inputs. They are hypotheses, not forecasts or historical events.",
                  wraplength=285, foreground="#62788d").pack(anchor="w", pady=6)
        for title, preset in [("Baseline risk assumptions", "base"), ("Recession / risk-off", "recession"), ("Inflation pressure", "inflation")]:
            ttk.Button(self.stress, text=title, command=lambda p=preset: self.preset(p)).pack(fill="x", pady=3)
        ttk.Separator(self.stress).pack(fill="x", pady=12)
        ttk.Label(self.stress, text="Instantaneous asset price shocks", font=("Segoe UI", 11, "bold")).pack(anchor="w")
        ttk.Label(self.stress, text="Example: −30 means price drops 30% now.\nThese shocks do not change optimizer forecasts.",
                  wraplength=290, foreground="#62788d").pack(anchor="w", pady=6)
        grid = ttk.Frame(self.stress); grid.pack(fill="x")
        for i, ticker in enumerate(core.ASSETS):
            ttk.Label(grid, text=ticker, width=10).grid(row=i, column=0, sticky="w", pady=3)
            var = tk.StringVar(value="-30"); self.shock_vars[ticker] = var
            ttk.Entry(grid, textvariable=var, width=10).grid(row=i, column=1, sticky="w")
            ttk.Label(grid, text="%").grid(row=i, column=2, padx=4)
        ttk.Separator(self.stress).pack(fill="x", pady=12)
        self.custom_enabled = tk.BooleanVar(value=False)
        ttk.Checkbutton(self.stress, text="Include custom portfolio", variable=self.custom_enabled).pack(anchor="w")
        ttk.Label(self.stress, text="Weights in %, must sum to 100. No normalization or hidden caps.",
                  wraplength=285, foreground="#62788d").pack(anchor="w", pady=5)
        for ticker in core.ASSETS:
            row = ttk.Frame(self.stress); row.pack(fill="x", pady=2)
            ttk.Label(row, text=ticker, width=10).pack(side="left")
            self.custom_vars[ticker] = tk.StringVar(value="10")
            ttk.Entry(row, textvariable=self.custom_vars[ticker], width=10).pack(side="left")

    def set_settings(self, settings):
        d = asdict(settings)
        for key, _, _, scale, _ in FIELDS:
            self.vars[key].set("" if d[key] is None else f"{d[key] * scale:g}")
        self.model.set(d["model"]); self.risk.set(d["risk"]); self.months.set(str(d["months"]))
        self.frequency.set(d["frequency"])
        for i, ticker in enumerate(core.ASSETS):
            self.shock_vars[ticker].set(f"{d['shocks'][i]*100:g}")
            self.custom_vars[ticker].set(f"{(d['custom_weights'][i] if d['custom_weights'] else .1)*100:g}")
        self.custom_enabled.set(d["custom_weights"] is not None)

    def reset(self):
        self.set_settings(Settings())
        self.status.set("Inputs reset. Click Apply to calculate. Baseline remains pinned until you replace it.")

    def read_settings(self):
        values = {}
        for key, _, _, scale, _ in FIELDS:
            text = self.vars[key].get().strip().replace(",", ".")
            if not text and key not in ("smb", "hml", "asset_cap", "stock_cap"):
                raise ValueError(f"{key} is required")
            values[key] = None if not text else float(text) / scale
        values.update(model=self.model.get(), risk=self.risk.get(), months=int(self.months.get()), frequency=self.frequency.get())
        values["shocks"] = [float(v.get().replace(",", "."))/100 for v in self.shock_vars.values()]
        values["custom_weights"] = ([float(v.get().replace(",", "."))/100 for v in self.custom_vars.values()]
                                    if self.custom_enabled.get() else None)
        s = Settings(**values); s.validate(); return s

    def preset(self, name):
        presets = {
            "base": {"vol_mult": "1", "corr_stress": "0", "shrink": "0", "return_shift": "0", "inflation": "2.5", "erp": "4.5"},
            "recession": {"vol_mult": "1.5", "corr_stress": "50", "shrink": "0", "return_shift": "-2", "inflation": "2.5", "erp": "3"},
            "inflation": {"vol_mult": "1.25", "corr_stress": "25", "shrink": "0", "return_shift": "-1", "inflation": "5", "erp": "4.5"},
        }
        for key, val in presets[name].items(): self.vars[key].set(val)
        shocks = [-30]*10 if name != "inflation" else [-30, -30, -20, -15, -15, 10, -20, -30, -25, -18]
        for ticker, value in zip(core.ASSETS, shocks): self.shock_vars[ticker].set(str(value))
        self.status.set(f"Preset '{name}' filled. RF, A, caps, model and costs unchanged. Click Apply.")

    def recalculate(self):
        if self.future and not self.future.done(): return
        try: settings = self.read_settings()
        except Exception as exc: messagebox.showerror("Check inputs", str(exc)); return
        self.status.set("Calculating on saved data… Inputs can be edited; charts retain the last completed calculation.")
        self.progress.start(12)
        self.future = self.executor.submit(calculate, settings, self.baseline)
        self.root.after(100, self.poll)

    def poll(self):
        if self.closed: return
        if not self.future.done(): self.root.after(100, self.poll); return
        self.progress.stop()
        try:
            result = self.future.result()
        except Exception as exc:
            self.status.set("Calculation failed; prior results remain visible.")
            messagebox.showerror("Cannot calculate", str(exc)); return
        self.accept(result)

    def accept(self, result):
        old = {name: var.get() for name, var in self.checks.items()}
        self.result = result
        for child in self.check_frame.winfo_children(): child.destroy()
        self.checks = {}
        s = result["settings"]
        preset = {"Sample GMV", "Sample Max Sharpe", f"Sample Max Utility A={s.a:g}",
                  "100% USMV", "100% VTI"}
        for name in result["candidates"]:
            prior = name
            if "Max Utility A=" in name:
                prior = next((n for n in old if n.startswith(name.split(" A=")[0])), name)
            var = tk.BooleanVar(value=old.get(prior, name in preset))
            self.checks[name] = var
            pid, _ = identity(result, name)
            text = f"{pid}  {name}" + ("  [cap breach]" if not result["metrics"][name]["optional_limits_feasible"] else "")
            ttk.Checkbutton(self.check_frame, text=text, variable=var, command=self.schedule_draw).pack(anchor="w")
        nominal_goal = s.real_goal * (1+s.inflation)**8
        need = (max(nominal_goal-core.SURPLUS_COUPONS_USD, 0)/core.SURPLUS_USD)**(1/8)-1
        self.cards.set(f"SURPLUS  ${core.SURPLUS_USD/1e6:.3f}m     |     REAL GOAL  ${s.real_goal/1e6:g}m     |     REQUIRED CAGR  {need:.2%}\n"
                       f"{s.months} training months  •  36 evaluation months  •  {len(result['candidates'])} candidates  •  "
                       f"Baseline {'pinned' if self.baseline else 'not pinned'}")
        self.status.set("Ready. Input edits take effect only after Apply. Hover a frontier point for exact figures.")
        self.draw()

    def selected(self): return [name for name, var in self.checks.items() if var.get()]

    def select_all(self, value):
        for var in self.checks.values(): var.set(value)
        self.schedule_draw()

    def select_core(self):
        if not self.result: return
        a = self.result["settings"].a
        selected = {"Sample GMV", "Sample Max Sharpe", f"Sample Max Utility A={a:g}", "100% USMV", "100% VTI"}
        for name, var in self.checks.items(): var.set(name in selected)
        self.schedule_draw()

    def schedule_draw(self):
        if self.redraw_job: self.root.after_cancel(self.redraw_job)
        self.redraw_job = self.root.after(130, self.draw)

    def draw(self):
        self.redraw_job = None
        if self.result is None: return
        view = self.view.get()
        if view in VIEWS:
            self.table_frame.pack_forget(); self.graph_frame.pack(fill="both", expand=True)
            self.points = draw_figure(self.figure, view, self.result, self.selected(), self.details.get())
            self.canvas.draw_idle()
        else:
            self.graph_frame.pack_forget(); self.table_frame.pack(fill="both", expand=True)
            self.populate_table(view)

    def populate_table(self, view):
        names = self.selected()
        if view == "Baseline comparison":
            frame = baseline_comparison(self.result, names)
            if frame.empty: frame = pd.DataFrame({"Instructions": ["Pin a baseline, edit assumptions, then Apply."]})
        else:
            rows = []
            for name in names:
                m = self.result["metrics"][name]
                rows.append({"ID": identity(self.result, name)[0], "Portfolio": name,
                    "E[R] %": m["expected_return"]*100, "Vol %": m["annual_volatility"]*100,
                    "Variance": m["annual_variance"], "Sharpe": m["forecast_sharpe"], "U %": m["utility_at_A"]*100,
                    "2023-25 CAGR %": m["evaluation_CAGR_2023_25"]*100,
                    "2023-25 DD %": m["evaluation_max_drawdown"]*100,
                    "2030 rough real $m": m["projected_2030_real_USD_rough"]/1e6,
                    "Caps OK": m["optional_limits_feasible"],
                    **{f"{t} %": w*100 for t, w in zip(core.ASSETS, self.result["candidates"][name])}})
            frame = pd.DataFrame(rows)
        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(frame.columns)
        for c in frame:
            self.table.heading(c, text=c)
            self.table.column(c, width=230 if c in ("Portfolio", "portfolio", "Instructions") else 150, stretch=False)
        for i, row in frame.iterrows():
            self.table.insert("", "end", values=[f"{v:.5g}" if isinstance(v, float) else v for v in row], tags=("even" if i%2 == 0 else "odd",))
        self.table.tag_configure("even", background="#f0f5f9")
        self.table.tag_configure("odd", background="white")

    def hover(self, event):
        if self.view.get() != "Risk / return" or not event.inaxes or not self.points: return
        distances = [np.linalg.norm(event.inaxes.transData.transform((x,y))-np.array([event.x,event.y]))
                     for x,y,n in self.points]
        i = int(np.argmin(distances))
        if distances[i] < 18:
            x,y,n = self.points[i]; m = self.result["metrics"][n]
            self.status.set(f"{n}  |  σ {x:.3%}  E[R] {y:.3%}  Variance {m['annual_variance']:.6f}  "
                            f"Sharpe {m['forecast_sharpe']:.3f}  U {m['utility_at_A']:.3%}")

    def pin(self):
        if self.result is None: return
        if self.future and not self.future.done():
            messagebox.showinfo("Calculation in progress", "Wait for the current result before pinning it."); return
        # Store only immutable calculation data, avoiding chains of prior results.
        self.baseline = {k: self.result[k] for k in ("settings", "mu", "cov", "candidates")}
        self.result["baseline"] = self.baseline
        self.cards.set(self.cards.get().replace("Baseline not pinned", "Baseline pinned"))
        self.status.set("Current calculated assumptions and weights pinned. Change inputs and Apply to compare.")
        self.draw()

    def load(self):
        path = filedialog.askopenfilename(title="Load scenario", filetypes=[("JSON", "*.json")])
        if not path: return
        try:
            payload = json.loads(__import__("pathlib").Path(path).read_text(encoding="utf-8"))
            settings = Settings(**payload["settings"]); settings.validate()
            self.set_settings(settings)
            # Do not silently mix a loaded scenario with another run's baseline.
            self.baseline = None
            self.status.set("Loaded scenario inputs. Previous baseline cleared. Click Apply; then pin if needed.")
        except Exception as exc: messagebox.showerror("Cannot load", str(exc))

    def export(self):
        if self.result is None or not self.selected():
            messagebox.showinfo("Choose portfolios", "Calculate, then tick at least one portfolio."); return
        path = filedialog.askdirectory(title="Choose parent folder for a new scenario export", initialdir=core.DEFAULT_OUTPUT)
        if not path: return
        from pathlib import Path
        from matplotlib.figure import Figure
        folder = Path(path) / datetime.now().strftime("kappa_lab_%Y%m%d_%H%M%S_%f")
        export_bundle(self.result, self.selected(), folder)
        for view in VIEWS:
            fig = Figure(figsize=(14, 10), dpi=100)
            draw_figure(fig, view, self.result, self.selected(), self.details.get())
            filename = view.lower().replace(" / ", "_").replace(" ", "_")
            fig.savefig(folder / f"{filename}.png", dpi=180)
            fig.savefig(folder / f"{filename}.svg")
        self.status.set(f"Exported 8 charts (PNG/SVG), checked metrics, full sensitivity grid and settings: {folder}")
        messagebox.showinfo("Export complete", f"Only checked portfolios included.\nSensitivity map/grid always contains all 30 parameter combinations.\n\n{folder}")

    def close(self):
        self.closed = True
        self.executor.shutdown(wait=False, cancel_futures=True)
        self.root.destroy()
