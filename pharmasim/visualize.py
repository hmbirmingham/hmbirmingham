"""
Visualization module for PharmaSimPlots concentration-time curves with clinical markers.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from pk_model import (
    concentration_single_dose,
    concentration_iv_bolus,
    multi_dose_superposition,
    half_life,
    time_to_peak,
    cmax_single,
    auc_inf,
    clearance,
)


def plot_single_dose(D=500, F=0.9, Vd=30, ka=1.2, ke=0.15,
                     t_end=48, route="oral", show_markers=True):
    """
    Plot a single-dose concentration-time curve with key PK metrics annotated.

    Default values approximate a typical oral antibiotic (e.g., amoxicillin-like).
    """
    t = np.linspace(0, t_end, 500)

    if route == "oral":
        C = concentration_single_dose(t, D, F, Vd, ka, ke)
        title = f"Single Oral Dose — {D} mg"
    else:
        C = concentration_iv_bolus(t, D, Vd, ke)
        F = 1.0  # IV is 100% bioavailable
        title = f"Single IV Bolus — {D} mg"

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, C, color="#2563eb", linewidth=2.5, label="Plasma concentration")

    if show_markers and route == "oral":
        tmax = time_to_peak(ka, ke)
        cmax = cmax_single(D, F, Vd, ka, ke)
        t12 = half_life(ke)
        auc = auc_inf(D, F, Vd, ke)
        cl = clearance(Vd, ke)

        # Cmax / Tmax marker
        ax.axvline(tmax, color="orange", linestyle="--", alpha=0.7)
        ax.axhline(cmax, color="orange", linestyle="--", alpha=0.7)
        ax.plot(tmax, cmax, "o", color="orange", markersize=10, zorder=5)
        ax.annotate(
            f"  Cmax = {cmax:.2f} mg/L\n  Tmax = {tmax:.2f} hr",
            xy=(tmax, cmax), fontsize=9, color="darkorange",
            va="bottom"
        )

        # Half-life annotation
        # Find C at t½ after Tmax
        t_half_point = tmax + t12
        C_half = concentration_single_dose(np.array([t_half_point]), D, F, Vd, ka, ke)[0]
        ax.annotate(
            f"t½ = {t12:.2f} hr\n(ke = {ke} /hr)",
            xy=(t_half_point, C_half),
            xytext=(t_half_point + 3, C_half + 0.5),
            arrowprops=dict(arrowstyle="->", color="gray"),
            fontsize=9, color="gray"
        )

        # AUC shading
        ax.fill_between(t, C, alpha=0.12, color="#2563eb", label=f"AUC∞ = {auc:.1f} mg·hr/L")

        info = (
            f"D={D} mg | F={F} | Vd={Vd} L\n"
            f"ka={ka} /hr | ke={ke} /hr\n"
            f"CL={cl:.2f} L/hr | AUC={auc:.1f} mg·hr/L"
        )
        ax.text(0.98, 0.95, info, transform=ax.transAxes,
                fontsize=8, va="top", ha="right",
                bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))

    ax.set_xlabel("Time (hr)", fontsize=12)
    ax.set_ylabel("Plasma Concentration (mg/L)", fontsize=12)
    ax.set_title(title, fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("single_dose.png", dpi=150)
    plt.show()
    print(f"\n[Saved] single_dose.png")


def plot_multi_dose(D=500, F=0.9, Vd=30, ka=1.2, ke=0.15,
                    interval=8, n_doses=6):
    """
    Plot multiple-dose regimen showing accumulation toward steady state.

    Steady state is reached after ~4-5 half-lives.
    """
    t12 = half_life(ke)
    t_end = dose_times = [i * interval for i in range(n_doses)]
    t_end = n_doses * interval + 24
    t = np.linspace(0, t_end, 2000)
    dose_times = [i * interval for i in range(n_doses)]

    C = multi_dose_superposition(t, D, F, Vd, ka, ke, dose_times)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(t, C, color="#16a34a", linewidth=2, label="Plasma concentration")

    # Mark each dose
    for i, td in enumerate(dose_times):
        ax.axvline(td, color="gray", linestyle=":", alpha=0.5,
                   label="Dose" if i == 0 else "")

    ax.set_xlabel("Time (hr)", fontsize=12)
    ax.set_ylabel("Plasma Concentration (mg/L)", fontsize=12)
    ax.set_title(
        f"Multiple Dose — {D} mg q{interval}h × {n_doses} doses\n"
        f"(t½ = {t12:.1f} hr, steady state ≈ {4*t12:.0f}–{5*t12:.0f} hr)",
        fontsize=13, fontweight="bold"
    )
    ax.legend(fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("multi_dose.png", dpi=150)
    plt.show()
    print(f"\n[Saved] multi_dose.png")


def plot_oral_vs_iv(D=500, F=0.85, Vd=30, ka=1.2, ke=0.15, t_end=48):
    """
    Overlay oral and IV curves — visualizes the first-pass effect and Tmax delay.
    """
    t = np.linspace(0, t_end, 500)
    C_oral = concentration_single_dose(t, D, F, Vd, ka, ke)
    C_iv = concentration_iv_bolus(t, D, Vd, ke)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(t, C_iv, color="#dc2626", linewidth=2.5, label=f"IV bolus (F=1.0, instant Cmax)")
    ax.plot(t, C_oral, color="#2563eb", linewidth=2.5,
            label=f"Oral (F={F}, delayed Cmax due to absorption)")

    ax.set_xlabel("Time (hr)", fontsize=12)
    ax.set_ylabel("Plasma Concentration (mg/L)", fontsize=12)
    ax.set_title(f"Oral vs IV Bolus — {D} mg", fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.3)

    auc_oral = auc_inf(D, F, Vd, ke)
    auc_iv = auc_inf(D, 1.0, Vd, ke)
    ax.text(0.98, 0.95,
            f"Oral AUC = {auc_oral:.1f}  |  IV AUC = {auc_iv:.1f}\nF = AUC_oral/AUC_iv = {F:.2f}",
            transform=ax.transAxes, fontsize=9, va="top", ha="right",
            bbox=dict(boxstyle="round", facecolor="lightyellow", alpha=0.8))

    plt.tight_layout()
    plt.savefig("oral_vs_iv.png", dpi=150)
    plt.show()
    print(f"\n[Saved] oral_vs_iv.png")


if __name__ == "__main__":
    print("=== PharmaSimVisualization Demo ===\n")
    print("Plot 1: Single oral dose")
    plot_single_dose()
    print("\nPlot 2: Multiple dose accumulation")
    plot_multi_dose()
    print("\nPlot 3: Oral vs IV comparison")
    plot_oral_vs_iv()
