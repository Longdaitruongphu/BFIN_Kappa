"""Readable standalone figures shared by the desktop interface and exports."""
import textwrap
import numpy as np
from matplotlib.ticker import PercentFormatter
from matplotlib import colormaps
import interactive_surplus_portfolio_lab as core
from portfolio_lab_scenarios import risk_contributions, radar_scores, baseline_comparison

VIEWS = ["Risk / return", "Radar profile", "Allocation weights", "Risk contributions",
         "Shock losses", "Sensitivity map", "2023-25 wealth", "2023-25 drawdown"]
PALETTE = ["#007f86", "#5168df", "#d98724", "#a85394", "#469954", "#d05b5b",
           "#59788b", "#8160ba", "#a67c49", "#28a7b6"]


def separate_labels(fig, annotations):
    """Resolve text-box overlap in display coordinates, preserving point leader lines."""
    if len(annotations) > 12: return
    from matplotlib.backends.backend_agg import RendererAgg
    renderer = RendererAgg(int(fig.bbox.width), int(fig.bbox.height), fig.dpi)
    fig.draw(renderer)
    for _ in range(30):
        changed = False
        for i, label in enumerate(annotations):
            label.update_positions(renderer); label.update_bbox_position_size(renderer)
            box = label.get_bbox_patch().get_window_extent(renderer).expanded(1.07, 1.12)
            for other in annotations[:i]:
                other.update_positions(renderer); other.update_bbox_position_size(renderer)
                box2 = other.get_bbox_patch().get_window_extent(renderer).expanded(1.07, 1.12)
                if box.overlaps(box2):
                    x, y = label.get_position()
                    label.set_position((x, y + (box2.y1-box.y0+5)*72/fig.dpi))
                    changed = True
                    break
        if not changed: break


def identity(result, name):
    i = list(result["candidates"]).index(name)
    return f"P{i + 1:02d}", PALETTE[i % len(PALETTE)]


def draw_figure(fig, view, result, names, detailed=True):
    fig.clear()
    fig.set_facecolor("#ffffff")
    ax = fig.add_subplot(111, polar=view == "Radar profile")
    fig.subplots_adjust(left=.11, right=.96, top=.87, bottom=.22)
    s = result["settings"]
    subtitle = (f"{s.model} · {s.risk} risk · {s.months} months to Dec 2022 · "
                f"A={s.a:g} · equity sleeve only")
    fig.text(.06, .965, view, fontsize=17, fontweight="bold", color="#162f47")
    fig.text(.06, .925, subtitle, fontsize=9, color="#5b6c7d")
    if not names and view != "Sensitivity map":
        ax.text(.5, .5, "Select portfolios in the Portfolios panel", transform=ax.transAxes,
                ha="center", fontsize=13, color="#62788d")
        ax.set_axis_off()
        return []
    metrics = result["metrics"]
    candidates = result["candidates"]
    points = []; annotations = []
    note = ""
    if view == "Risk / return":
        frontier = result["frontier"]
        if len(frontier):
            ax.plot(frontier[:, 0], frontier[:, 1], color="#007f86", lw=2, label=f"{s.risk} frontier")
        ret, vol, _ = result["tangent"]
        if ret > s.rf and vol > 1e-9:
            ax.plot([0, vol], [s.rf, ret], ls="--", color="#9ca9b5", lw=1.5, label="Illustrative CAL")
        ax.scatter([0], [s.rf], marker="D", color="#25374a", s=35, label=f"Forecast RF {s.rf:.1%}")
        for i, name in enumerate(names):
            m = metrics[name]; pid, color = identity(result, name)
            x, y = m["annual_volatility"], m["expected_return"]
            ax.scatter(x, y, s=80, color=color, edgecolors="white", linewidths=1,
                       marker="o" if m["optional_limits_feasible"] else "X", zorder=4)
            label = f"{pid}\n({x:.2%}; {y:.2%})" if detailed and len(names) <= 8 else pid
            if detailed or len(names) <= 8:
                # Stagger labels; exact values remain in the scorecard and hover readout.
                offset = [(12, 16), (18, -32), (-62, 32), (-76, -24), (22, 42), (-78, 6), (14, -55), (-75, 54)][i % 8]
                annotations.append(ax.annotate(label, (x, y), xytext=offset, textcoords="offset points", fontsize=8,
                    bbox=dict(boxstyle="round,pad=.35", fc="white", ec=color, alpha=.92),
                    arrowprops=dict(arrowstyle="-", color=color, lw=.8)))
            points.append((x, y, name))
        ax.xaxis.set_major_formatter(PercentFormatter(1))
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_xlabel("Annual volatility σ"); ax.set_ylabel("Expected annual arithmetic return")
        ax.margins(x=.2, y=.22)
        ax.set_xlim(left=-.012)
        ax.legend(loc="upper left", fontsize=8, frameon=False)
        note = "CAL is illustrative: the optimizer allocates 100% to equities; it does not choose a cash weight."
    elif view == "Radar profile":
        scores = radar_scores(metrics)
        labels = ["Return ↑", "Utility ↑", "Sharpe ↑", "Low volatility ↑", "Shallow training DD ↑"]
        angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
        for name in names:
            pid, color = identity(result, name)
            vals = scores.loc[name].to_numpy()
            ax.plot(np.r_[angles, angles[0]], np.r_[vals, vals[0]], label=pid, color=color,
                    marker="o", markersize=3, lw=1.6)
        ax.set_xticks(angles, labels, fontsize=9)
        ax.set_ylim(min(0, float(scores.loc[names].min().min())), max(100, float(scores.loc[names].max().max())))
        ax.set_yticks([25, 50, 75, 100]); ax.tick_params(axis="y", labelsize=8)
        fig.subplots_adjust(right=.85)
        handles, labels_ids = ax.get_legend_handles_labels()
        ax.legend(handles[:10], labels_ids[:10], loc="upper left", bbox_to_anchor=(1.02, 1.0),
                  fontsize=9, frameon=False, title="Portfolio ID")
        note = "Relative to all feasible candidates in THIS scenario. Higher is better; never sum axes or polygon area."
    elif view in ("Allocation weights", "Risk contributions"):
        matrix = np.array([candidates[n] if view == "Allocation weights"
                           else risk_contributions(candidates[n], result["cov"]) for n in names])
        ids = [identity(result, n)[0] for n in names]
        limit = max(abs(matrix.min()), abs(matrix.max()), .01)
        im = ax.imshow(matrix, aspect="auto", cmap="Blues" if matrix.min() >= 0 else "RdBu",
                       vmin=0 if matrix.min() >= 0 else -limit, vmax=limit)
        fig.colorbar(im, ax=ax, fraction=.025, pad=.02, format=PercentFormatter(1))
        ax.set_xticks(range(len(core.ASSETS)), core.ASSETS, fontsize=9)
        ax.set_yticks(range(len(names)), ids, fontsize=9)
        if len(names) <= 16:
            for i in range(len(names)):
                for j in range(len(core.ASSETS)):
                    ax.text(j, i, f"{matrix[i,j]:.1%}", ha="center", va="center", fontsize=8,
                            color="white" if abs(matrix[i,j]) > .6 * limit else "#20354c")
        note = ("Rows sum to 100%. Optional-limit breaches stay visible as comparison candidates."
                if view == "Allocation weights" else
                "Variance share = wi (Σw)i / (w'Σw). Shares sum to 100%; a hedge can have a negative share.")
    elif view == "Shock losses":
        ids = [identity(result, n)[0] for n in names]
        current = [float(candidates[n] @ s.shocks) for n in names]
        comparison = baseline_comparison(result, names)
        base_map = comparison.set_index("portfolio").fixed_weight_shock.to_dict() if not comparison.empty else {}
        yy = np.arange(len(names))
        ax.barh(yy + .17, current, height=.32, color="#007f86", label="Current candidate weights")
        if base_map:
            ax.barh(yy - .17, [base_map.get(n, np.nan) for n in names], height=.32,
                    color="#c69a52", label="Pinned baseline weights")
        for i, value in enumerate(current):
            ax.annotate(f"{value:.1%} · ${value * core.SURPLUS_USD / 1e6:+.2f}m",
                        (value, i + .17), xytext=(5 if value >= 0 else -5, 0),
                        textcoords="offset points", ha="left" if value >= 0 else "right", va="center", fontsize=8)
        ax.set_yticks(yy, ids); ax.invert_yaxis(); ax.margins(x=.4)
        ax.xaxis.set_major_formatter(PercentFormatter(1)); ax.axvline(0, lw=.8, color="#9ca9b5")
        ax.set_xlabel("Instantaneous equity-sleeve return"); ax.legend(fontsize=8, frameon=False)
        note = "User-defined shocks, not historical data or probabilities. Bonds and their price changes are excluded."
    elif view == "Sensitivity map":
        grid = result["sensitivity"].pivot(index="A", columns="ERP", values="volatility")
        im = ax.imshow(grid.to_numpy(), cmap="YlGnBu", aspect="auto")
        fig.colorbar(im, ax=ax, format=PercentFormatter(1), fraction=.025, pad=.02)
        ax.set_xticks(range(len(grid.columns)), [f"{x:.1%}" for x in grid.columns])
        ax.set_yticks(range(len(grid.index)), [f"{x:g}" for x in grid.index])
        for i in range(len(grid.index)):
            for j in range(len(grid.columns)):
                val = grid.iloc[i, j]
                ax.text(j, i, f"{val:.1%}", ha="center", va="center", fontsize=11,
                        color="white" if val > (grid.max().max()+grid.min().min())/2 else "#20354c")
        ax.set_xlabel("Annual market risk premium"); ax.set_ylabel("Risk aversion A")
        note = "Each cell REOPTIMIZES maximum utility. Color = volatility, not a score. Export includes every cell's weights."
    elif view in ("2023-25 wealth", "2023-25 drawdown"):
        ev = result["data"]["eval"]
        month_ends = ev.index.to_period("M").to_timestamp("M")
        dates = month_ends.insert(0, month_ends[0] - __import__("pandas").offsets.MonthEnd(1))
        to_plot = list(names)
        for name in to_plot:
            pid, color = identity(result, name)
            r = core.rebalanced_monthly_returns(ev, candidates[name], s.cost, s.frequency)
            wealth = np.r_[1., np.cumprod(1+r)]
            series = wealth if view.endswith("wealth") else wealth / np.maximum.accumulate(wealth) - 1
            ax.plot(dates, series, color="#1c3043" if name == "100% VTI" else color,
                    lw=2.3 if name == "100% VTI" else 1.5, ls="--" if name == "100% VTI" else "-",
                    label=f"{pid} VTI benchmark" if name == "100% VTI" else pid)
        ax.legend(fontsize=8, ncol=3, frameon=False)
        if view.endswith("drawdown"):
            ax.yaxis.set_major_formatter(PercentFormatter(1)); ax.set_ylabel("Drawdown from running peak")
        else:
            ax.set_ylabel("Growth of $1 at start of evaluation")
        note = f"Retrospective check · {s.frequency} rebalance · {s.cost * 10000:g} bps per dollar traded. No entry/exit fee. Tick VTI to show the benchmark."
    if view not in ("Allocation weights", "Risk contributions", "Sensitivity map"):
        ax.grid(alpha=.17)
        if view != "Radar profile":
            ax.spines[["top", "right"]].set_visible(False)
    # Compact identity key separate from metrics: never a clipped one-line spreadsheet.
    if view != "Sensitivity map":
        labels = [f"{identity(result, n)[0]}  {n}" for n in names]
        lines = ["   |   ".join(labels[i:i+2]) for i in range(0, len(labels), 2)]
        if len(lines) > 5:
            lines = lines[:4] + [f"+ {len(names)-8} more; see exported scorecard for complete IDs and metrics."]
        fig.text(.07, .145, "\n".join(lines), fontsize=8, va="top", color="#42576c")
    fig.text(.07, .025, "\n".join(textwrap.wrap(note, 130)), fontsize=8, color="#68798b", va="bottom")
    if annotations: separate_labels(fig, annotations)
    return points
