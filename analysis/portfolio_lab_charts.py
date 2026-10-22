"""Readable standalone figures shared by the desktop interface and exports."""
import textwrap
import numpy as np
from matplotlib.ticker import PercentFormatter
from matplotlib import colormaps
import interactive_surplus_portfolio_lab as core
from portfolio_lab_scenarios import risk_contributions, radar_scores, baseline_comparison

VIEWS = ["Risk / return", "Radar profile", "Allocation weights", "Risk contributions",
         "Shock losses", "Sensitivity map", "2023-25 wealth", "2023-25 drawdown"]
# Modern vibrant, high-contrast palette tailored for financial visualizations
PALETTE = ["#008080", "#2563eb", "#d97706", "#db2777", "#059669",
           "#7c3aed", "#dc2626", "#0891b2", "#ea580c", "#4f46e5",
           "#0d9488", "#c026d3", "#65a30d", "#e11d48", "#0284c7"]


def separate_labels(fig, annotations):
    """Fast, smooth text-box overlap resolution without heavy full-figure re-rendering."""
    if len(annotations) <= 1 or len(annotations) > 16:
        return
    try:
        renderer = fig._get_renderer() if hasattr(fig, "_get_renderer") else None
        if renderer is None and hasattr(fig.canvas, "get_renderer"):
            renderer = fig.canvas.get_renderer()
    except Exception:
        renderer = None

    if renderer is not None:
        try:
            boxes = [ann.get_window_extent(renderer) for ann in annotations]
            for step in range(12):
                moved = False
                for i in range(len(annotations)):
                    for j in range(i):
                        if boxes[i].overlaps(boxes[j].expanded(1.08, 1.15)):
                            pos = annotations[i].get_position()
                            annotations[i].set_position((pos[0], pos[1] + 16))
                            boxes[i] = annotations[i].get_window_extent(renderer)
                            moved = True
                if not moved:
                    break
        except Exception:
            pass


def identity(result, name):
    i = list(result["candidates"]).index(name)
    return f"P{i + 1:02d}", PALETTE[i % len(PALETTE)]


def draw_figure(fig, view, result, names, detailed=True):
    fig.clear()
    fig.set_facecolor("#ffffff")
    is_polar = (view == "Radar profile")
    ax = fig.add_subplot(111, polar=is_polar)
    fig.subplots_adjust(left=.11, right=.96, top=.87, bottom=.22)
    s = result["settings"]
    subtitle = (f"{s.model} · {s.risk} risk · {s.months} months to Dec 2022 · "
                f"A={s.a:g} · equity sleeve only")
    fig.text(.06, .965, view, fontsize=17, fontweight="bold", color="#0f172a")
    fig.text(.06, .925, subtitle, fontsize=9, color="#64748b")
    if not names and view != "Sensitivity map":
        ax.text(.5, .5, "Select portfolios in the Portfolios panel", transform=ax.transAxes,
                ha="center", fontsize=13, color="#64748b", fontweight="bold")
        ax.set_axis_off()
        return []
    metrics = result["metrics"]
    candidates = result["candidates"]
    points = []; annotations = []
    note = ""

    if view == "Risk / return":
        frontier = result["frontier"]
        if len(frontier):
            order = np.argsort(frontier[:, 0])
            fv = frontier[order, 0]
            fr = frontier[order, 1]
            ax.plot(fv, fr, color="#008080", lw=2.4, zorder=2, label=f"{s.risk} frontier")
            # Subtle shaded region under efficient frontier for aesthetic depth
            ax.fill_between(fv, fr, min(s.rf, float(fr.min())), color="#008080", alpha=0.06, zorder=1)

        ret, vol, _ = result["tangent"]
        if ret > s.rf and vol > 1e-9:
            ax.plot([0, vol], [s.rf, ret], ls=(0, (4, 3)), color="#64748b", lw=1.6,
                    label="Illustrative CAL", zorder=2)
        ax.scatter([0], [s.rf], marker="D", color="#0f172a", s=45, edgecolors="#ffffff",
                   linewidths=1.5, label=f"Forecast RF {s.rf:.1%}", zorder=4)

        # Identify highest Sharpe among plotted feasible portfolios to highlight
        feasible_names = [n for n in names if metrics[n]["optional_limits_feasible"]]
        best_sharpe_name = max(feasible_names, key=lambda n: metrics[n]["forecast_sharpe"]) if feasible_names else None

        for i, name in enumerate(names):
            m = metrics[name]; pid, color = identity(result, name)
            x, y = m["annual_volatility"], m["expected_return"]
            is_feasible = m["optional_limits_feasible"]
            marker = "o" if is_feasible else "X"
            size = 90 if is_feasible else 100
            ax.scatter(x, y, s=size, color=color, edgecolors="#ffffff", linewidths=1.8,
                       marker=marker, zorder=4)

            # Highlight ring for highest Sharpe portfolio
            if name == best_sharpe_name:
                ax.scatter(x, y, s=220, facecolors="none", edgecolors="#d97706",
                           linewidths=2.0, ls="--", zorder=3)

            label = f"{pid}\n({x:.2%}; {y:.2%})" if detailed and len(names) <= 8 else pid
            if detailed or len(names) <= 8:
                offset_patterns = [(14, 16), (18, -30), (-64, 28), (-72, -22),
                                   (22, 38), (-74, 8), (14, -50), (-70, 48)]
                offset = offset_patterns[i % len(offset_patterns)]
                annotations.append(ax.annotate(
                    label, (x, y), xytext=offset, textcoords="offset points", fontsize=8,
                    bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.25", fc="#ffffff",
                              ec=color, lw=1.2, alpha=0.95),
                    arrowprops=dict(arrowstyle="->", color=color, lw=0.9, shrinkA=3, shrinkB=4)
                ))
            points.append((x, y, name, pid, color))

        ax.xaxis.set_major_formatter(PercentFormatter(1))
        ax.yaxis.set_major_formatter(PercentFormatter(1))
        ax.set_xlabel("Annual volatility σ", fontsize=10, color="#1e293b", labelpad=6)
        ax.set_ylabel("Expected annual arithmetic return", fontsize=10, color="#1e293b", labelpad=6)
        ax.margins(x=.18, y=.20)
        ax.set_xlim(left=-.012)
        ax.legend(loc="upper left", fontsize=8.5, frameon=True, facecolor="#ffffff",
                  edgecolor="#e2e8f0", framealpha=0.92)
        note = "CAL is illustrative: the optimizer allocates 100% to equities; it does not choose a cash weight. Dashed amber ring highlights highest Sharpe portfolio."

    elif view == "Radar profile":
        scores = radar_scores(metrics)
        labels = ["Return ↑", "Utility ↑", "Sharpe ↑", "Low volatility ↑", "Shallow training DD ↑"]
        angles = np.linspace(0, 2*np.pi, 5, endpoint=False)
        angles_loop = np.r_[angles, angles[0]]

        for name in names:
            pid, color = identity(result, name)
            vals = scores.loc[name].to_numpy()
            vals_loop = np.r_[vals, vals[0]]
            suffix = " (cap breach)" if not metrics[name]["optional_limits_feasible"] else ""
            # Semi-transparent filled polygon for vivid, intuitive profile visualization
            ax.fill(angles_loop, vals_loop, color=color, alpha=0.18)
            ax.plot(angles_loop, vals_loop, label=pid + suffix, color=color,
                    marker="o", markersize=4.5, markeredgecolor="#ffffff", markeredgewidth=1.2,
                    lw=1.8, ls="--" if suffix else "-")

        ax.set_xticks(angles, labels, fontsize=9.5, fontweight="bold", color="#1e293b")
        y_min = min(0, float(scores.loc[names].min().min())) if names else 0
        y_max = max(100, float(scores.loc[names].max().max())) if names else 100
        ax.set_ylim(y_min, y_max)
        ax.set_yticks([25, 50, 75, 100])
        ax.tick_params(axis="y", labelsize=8, colors="#64748b")
        ax.grid(color="#cbd5e1", linestyle="--", linewidth=0.7, alpha=0.8)
        fig.subplots_adjust(right=.85)
        handles, labels_ids = ax.get_legend_handles_labels()
        ax.legend(handles[:12], labels_ids[:12], loc="upper left", bbox_to_anchor=(1.02, 1.0),
                  fontsize=8.5, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0", title="Portfolios")
        note = "Relative to all feasible candidates in THIS scenario. Higher is better; never sum axes or polygon area."

    elif view in ("Allocation weights", "Risk contributions"):
        matrix = np.array([candidates[n] if view == "Allocation weights"
                           else risk_contributions(candidates[n], result["cov"]) for n in names])
        ids = [identity(result, n)[0] for n in names]
        limit = max(abs(matrix.min()), abs(matrix.max()), .01)
        cmap = "YlGnBu" if matrix.min() >= 0 else "RdBu_r"
        im = ax.imshow(matrix, aspect="auto", cmap=cmap,
                       vmin=0 if matrix.min() >= 0 else -limit, vmax=limit)
        cbar = fig.colorbar(im, ax=ax, fraction=.025, pad=.02, format=PercentFormatter(1))
        cbar.ax.tick_params(labelsize=8)
        ax.set_xticks(range(len(core.ASSETS)), core.ASSETS, fontsize=9.5, fontweight="bold", color="#1e293b")
        ax.set_yticks(range(len(names)), ids, fontsize=9.5, fontweight="bold", color="#1e293b")

        # Tile cell dividers for a clean, modern card look
        ax.set_xticks(np.arange(-0.5, len(core.ASSETS), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(names), 1), minor=True)
        ax.grid(which="minor", color="#ffffff", linestyle="-", linewidth=2.0)
        ax.tick_params(which="minor", bottom=False, left=False)

        if len(names) <= 16:
            for i in range(len(names)):
                for j in range(len(core.ASSETS)):
                    val = matrix[i, j]
                    is_dark = (abs(val) > .55 * limit)
                    text_color = "#ffffff" if is_dark else "#0f172a"
                    ax.text(j, i, f"{val:.1%}", ha="center", va="center", fontsize=8.5,
                            fontweight="bold" if abs(val) >= 0.1 else "normal",
                            color=text_color)
        note = ("Rows sum to 100%. Optional-limit breaches stay visible as comparison candidates."
                if view == "Allocation weights" else
                "Variance share = wi (Σw)i / (w'Σw). Shares sum to 100%; a hedge can have a negative share.")

    elif view == "Shock losses":
        ids = [identity(result, n)[0] for n in names]
        current = [float(candidates[n] @ s.shocks) for n in names]
        comparison = baseline_comparison(result, names)
        base_map = comparison.set_index("portfolio").fixed_weight_shock.to_dict() if not comparison.empty else {}
        yy = np.arange(len(names))

        # Dynamic bar colors: crimson for losses, emerald for cushions
        current_colors = ["#ef4444" if v < 0 else "#10b981" for v in current]
        ax.barh(yy + .17, current, height=.32, color=current_colors, edgecolor="#ffffff",
                lw=1, label="Current candidate weights")
        if base_map:
            ax.barh(yy - .17, [base_map.get(n, np.nan) for n in names], height=.32,
                    color="#f59e0b", edgecolor="#ffffff", lw=1, label="Pinned baseline weights")

        for i, value in enumerate(current):
            dollar_m = value * core.SURPLUS_USD / 1e6
            ax.annotate(f"{value:+.1%} (${dollar_m:+.2f}m)",
                        (value, i + .17), xytext=(6 if value >= 0 else -6, 0),
                        textcoords="offset points", ha="left" if value >= 0 else "right", va="center",
                        fontsize=8.5, color="#0f172a")

        ax.set_yticks(yy, ids, fontsize=9.5, fontweight="bold")
        ax.invert_yaxis()
        ax.margins(x=.35)
        ax.xaxis.set_major_formatter(PercentFormatter(1))
        ax.axvline(0, lw=1.2, color="#64748b", ls="-")
        ax.set_xlabel("Instantaneous equity-sleeve return", fontsize=10, color="#1e293b", labelpad=6)
        ax.legend(fontsize=8.5, frameon=True, facecolor="#ffffff", edgecolor="#e2e8f0")
        note = "User-defined shocks, not historical data or probabilities. Bonds and their price changes are excluded."

    elif view == "Sensitivity map":
        grid = result["sensitivity"].pivot(index="A", columns="ERP", values="volatility")
        im = ax.imshow(grid.to_numpy(), cmap="YlGnBu", aspect="auto")
        cbar = fig.colorbar(im, ax=ax, format=PercentFormatter(1), fraction=.025, pad=.02)
        cbar.ax.tick_params(labelsize=8)
        ax.set_xticks(range(len(grid.columns)), [f"{x:.1%}" for x in grid.columns], fontsize=9.5)
        ax.set_yticks(range(len(grid.index)), [f"{x:g}" for x in grid.index], fontsize=9.5)

        # Tile divider borders
        ax.set_xticks(np.arange(-0.5, len(grid.columns), 1), minor=True)
        ax.set_yticks(np.arange(-0.5, len(grid.index), 1), minor=True)
        ax.grid(which="minor", color="#ffffff", linestyle="-", linewidth=2.0)
        ax.tick_params(which="minor", bottom=False, left=False)

        for i in range(len(grid.index)):
            for j in range(len(grid.columns)):
                val = grid.iloc[i, j]
                is_dark = val > (grid.max().max() + grid.min().min()) / 2
                ax.text(j, i, f"{val:.1%}", ha="center", va="center", fontsize=10.5,
                        fontweight="bold", color="#ffffff" if is_dark else "#0f172a")
        ax.set_xlabel("Annual market risk premium", fontsize=10, color="#1e293b", labelpad=6)
        ax.set_ylabel("Risk aversion A", fontsize=10, color="#1e293b", labelpad=6)
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
            is_vti = (name == "100% VTI")
            line_color = "#0f172a" if is_vti else color
            line_lw = 2.4 if is_vti else 1.8
            line_ls = "--" if is_vti else "-"
            label_text = f"{pid} VTI benchmark" if is_vti else pid
            ax.plot(dates, series, color=line_color, lw=line_lw, ls=line_ls, label=label_text)
            if view.endswith("drawdown"):
                # Vivid underwater shaded fill
                ax.fill_between(dates, series, 0, color=color, alpha=0.12)

        ax.legend(fontsize=8.5, ncol=min(len(to_plot), 4), frameon=True,
                  facecolor="#ffffff", edgecolor="#e2e8f0")
        if view.endswith("drawdown"):
            ax.yaxis.set_major_formatter(PercentFormatter(1))
            ax.set_ylabel("Drawdown from running peak", fontsize=10, color="#1e293b", labelpad=6)
        else:
            ax.set_ylabel("Growth of $1 at start of evaluation", fontsize=10, color="#1e293b", labelpad=6)
        note = f"Retrospective check · {s.frequency} rebalance · {s.cost * 10000:g} bps per dollar traded. No entry/exit fee. Tick VTI to show the benchmark."

    if view not in ("Allocation weights", "Risk contributions", "Sensitivity map"):
        ax.grid(color="#e2e8f0", linestyle="--", linewidth=0.7, alpha=0.8)
        if view != "Radar profile":
            ax.spines[["top", "right"]].set_visible(False)
            ax.spines[["left", "bottom"]].set_color("#94a3b8")

    # Compact identity key separate from metrics: never a clipped one-line spreadsheet.
    if view != "Sensitivity map":
        labels = [f"{identity(result, n)[0]}  {n}" for n in names]
        lines = ["   |   ".join(labels[i:i+2]) for i in range(0, len(labels), 2)]
        if len(lines) > 5:
            lines = lines[:4] + [f"+ {len(names)-8} more; see exported scorecard for complete IDs and metrics."]
        fig.text(.07, .145, "\n".join(lines), fontsize=8, va="top", color="#334155")
    fig.text(.07, .025, "\n".join(textwrap.wrap(note, 130)), fontsize=8, color="#64748b", va="bottom")
    if annotations:
        separate_labels(fig, annotations)
    return points
