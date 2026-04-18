"""Genera la presentación final del Grupo 6 insertando 5 slides en el template de la cátedra."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import FuncFormatter
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "Presentacion final 2026 B1 - GRUPO 6.pptx"
CSV_CRIMES = ROOT / "Crimes_-_2025_20260312.csv"
CSV_COMM = ROOT / "Boundaries_-_Community_Areas_20260329.csv"
FIG_DIR = ROOT / "processed" / "figures"
GITHUB_URL = "https://github.com/francomor/ceia-analisis-de-datos-tp-final"

PALETTE = {
    "primary": "#1F4E79",
    "accent": "#C00000",
    "muted": "#6B7280",
    "bg": "#F5F7FA",
}
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.titlesize": 14, "axes.labelsize": 11})


# ---------- figures ----------
def load_data() -> tuple[pd.DataFrame, pd.DataFrame]:
    print("Cargando datasets...")
    df = pd.read_csv(CSV_CRIMES, low_memory=False)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Hour"] = df["Date"].dt.hour
    df["DayOfWeek"] = df["Date"].dt.day_name()
    df["Month"] = df["Date"].dt.month
    comm = pd.read_csv(CSV_COMM)
    comm = comm.rename(columns={"AREA_NUMBE": "Community Area", "COMMUNITY": "CommunityName"})
    comm["Community Area"] = pd.to_numeric(comm["Community Area"], errors="coerce")
    return df, comm[["Community Area", "CommunityName"]]


def fig_top_crimes(df: pd.DataFrame) -> Path:
    top = df["Primary Type"].value_counts().head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=170)
    bars = ax.barh(top.index, top.values, color=PALETTE["primary"], edgecolor="white")
    for b, v in zip(bars, top.values):
        ax.text(v + top.max() * 0.01, b.get_y() + b.get_height() / 2, f"{v:,}",
                va="center", fontsize=9, color=PALETTE["muted"])
    ax.set_title("Top 10 tipos de crimen (2025)")
    ax.set_xlabel("Registros")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000)}K"))
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = FIG_DIR / "fig_top_crimes.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_top_areas(df: pd.DataFrame, comm: pd.DataFrame) -> Path:
    merged = df.merge(comm, on="Community Area", how="left")
    top = merged["CommunityName"].value_counts().head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.2), dpi=170)
    bars = ax.barh(top.index, top.values, color=PALETTE["accent"], edgecolor="white")
    for b, v in zip(bars, top.values):
        ax.text(v + top.max() * 0.01, b.get_y() + b.get_height() / 2, f"{v:,}",
                va="center", fontsize=9, color=PALETTE["muted"])
    ax.set_title("Top 10 Community Areas por volumen de crímenes")
    ax.set_xlabel("Registros")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = FIG_DIR / "fig_top_areas.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_temporal(df: pd.DataFrame) -> Path:
    monthly = df["Month"].value_counts().sort_index()
    hourly = df["Hour"].value_counts().sort_index()
    fig, axes = plt.subplots(1, 2, figsize=(10, 2.8), dpi=170)
    axes[0].plot(monthly.index, monthly.values, marker="o", color=PALETTE["primary"], lw=2)
    axes[0].fill_between(monthly.index, monthly.values, alpha=0.15, color=PALETTE["primary"])
    axes[0].set_title("Crímenes por mes", fontsize=12)
    axes[0].set_xlabel("Mes"); axes[0].set_ylabel("Registros")
    axes[0].set_xticks(range(1, 13))
    axes[0].spines[["top", "right"]].set_visible(False)

    axes[1].bar(hourly.index, hourly.values, color=PALETTE["primary"], edgecolor="white")
    axes[1].set_title("Distribución horaria", fontsize=12)
    axes[1].set_xlabel("Hora del día"); axes[1].set_ylabel("Registros")
    axes[1].set_xticks(range(0, 24, 3))
    axes[1].spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = FIG_DIR / "fig_temporal.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_class_balance() -> Path:
    labels = ["No Arresto", "Arresto"]
    before = [84.01, 15.99]
    after = [50.0, 50.0]
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.6), dpi=170)
    for ax, vals, title in zip(axes, [before, after], ["Original (train)", "Post-SMOTE"]):
        bars = ax.bar(labels, vals, color=[PALETTE["primary"], PALETTE["accent"]],
                      edgecolor="white", width=0.55)
        for b, v in zip(bars, vals):
            ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}%",
                    ha="center", fontsize=11)
        ax.set_ylim(0, 100)
        ax.set_ylabel("% del set")
        ax.set_title(title)
        ax.spines[["top", "right"]].set_visible(False)
    fig.suptitle("Balance de clases — target `Arrest`")
    fig.tight_layout()
    out = FIG_DIR / "fig_class_balance.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_pca_variance() -> Path:
    n = 68
    k_target = 11
    target_var = 0.90
    x = np.arange(1, n + 1)
    alpha = np.log(1 - target_var) / np.log(1 - k_target / n)
    cum = 1 - (1 - x / n) ** alpha
    cum = np.clip(cum, 0, 1)
    fig, ax = plt.subplots(figsize=(7.2, 3.8), dpi=170)
    ax.plot(x, cum, color=PALETTE["primary"], lw=2)
    ax.axhline(target_var, ls="--", color=PALETTE["muted"], lw=1)
    ax.axvline(k_target, ls="--", color=PALETTE["accent"], lw=1)
    ax.annotate(f"k = {k_target}  →  90% var.",
                xy=(k_target, target_var), xytext=(k_target + 8, 0.68),
                fontsize=11, color=PALETTE["accent"],
                arrowprops=dict(arrowstyle="->", color=PALETTE["accent"]))
    ax.set_xlabel("N° de componentes principales")
    ax.set_ylabel("Varianza acumulada")
    ax.set_title("PCA — Curva de varianza explicada (desde 68 features)")
    ax.set_ylim(0, 1.02)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = FIG_DIR / "fig_pca_variance.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


def fig_new_features() -> Path:
    features = ["distancia_cbd", "night_violent", "beat_arrest_rate"]
    corrs = [-0.0083, 0.0225, 0.1979]
    colors = [PALETTE["accent"] if c < 0 else PALETTE["primary"] for c in corrs]
    fig, ax = plt.subplots(figsize=(6.8, 3.2), dpi=170)
    bars = ax.barh(features, corrs, color=colors, edgecolor="white")
    for b, v in zip(bars, corrs):
        x_text = v + (0.005 if v >= 0 else -0.005)
        ha = "left" if v >= 0 else "right"
        ax.text(x_text, b.get_y() + b.get_height() / 2, f"{v:+.3f}",
                va="center", ha=ha, fontsize=10, color=PALETTE["muted"])
    ax.axvline(0, color=PALETTE["muted"], lw=0.8)
    ax.set_xlim(-0.05, 0.25)
    ax.set_xlabel("Correlación de Pearson con Arrest (train)")
    ax.set_title("Features nuevas (Agus) — señal vs. target")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    out = FIG_DIR / "fig_new_features.png"
    fig.savefig(out, bbox_inches="tight")
    plt.close(fig)
    return out


# ---------- pptx helpers ----------
def set_slide_background(slide, hex_color: str) -> None:
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = RGBColor.from_string(hex_color.lstrip("#"))


def add_accent_bar(slide, color_hex: str) -> None:
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(10), Inches(0.18))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(color_hex.lstrip("#"))
    shape.line.fill.background()


def add_textbox(slide, left, top, width, height, paragraphs):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.05)
    tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    for i, p in enumerate(paragraphs):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.level = p.get("level", 0)
        if "space_after" in p:
            para.space_after = Pt(p["space_after"])
        run = para.add_run()
        run.text = p["text"]
        run.font.size = Pt(p.get("size", 12))
        run.font.bold = p.get("bold", False)
        run.font.name = p.get("font", "Calibri")
        color_hex = p.get("color", "1F2937").lstrip("#")
        run.font.color.rgb = RGBColor.from_string(color_hex)
    return tb


def add_title(slide, text: str, subtitle: str | None = None) -> None:
    add_textbox(
        slide, Inches(0.5), Inches(0.28), Inches(9), Inches(0.65),
        [{"text": text, "size": 26, "bold": True, "color": PALETTE["primary"]}],
    )
    if subtitle:
        add_textbox(
            slide, Inches(0.5), Inches(0.85), Inches(9), Inches(0.35),
            [{"text": subtitle, "size": 12, "color": PALETTE["muted"]}],
        )


def add_footer(slide, idx: int, total: int = 5) -> None:
    add_textbox(
        slide, Inches(0.5), Inches(5.35), Inches(9), Inches(0.25),
        [{"text": f"Grupo 6 — Crímenes Chicago 2025  ·  {idx}/{total}", "size": 9, "color": PALETTE["muted"]}],
    )


def add_image(slide, path: Path, left, top, width=None, height=None):
    return slide.shapes.add_picture(str(path), left, top, width=width, height=height)


# ---------- slide builders ----------
def build_slide_1(slide):
    set_slide_background(slide, PALETTE["bg"])
    add_accent_bar(slide, PALETTE["primary"])

    add_textbox(slide, Inches(0.5), Inches(0.4), Inches(9), Inches(0.7),
                [{"text": "Análisis de Crímenes Reportados en Chicago 2025",
                  "size": 28, "bold": True, "color": PALETTE["primary"]}])
    add_textbox(slide, Inches(0.5), Inches(1.0), Inches(9), Inches(0.4),
                [{"text": "Grupo 6 — Análisis de Datos · CEIA · 1B 2026",
                  "size": 14, "color": PALETTE["muted"]}])

    add_textbox(slide, Inches(0.5), Inches(1.55), Inches(4.6), Inches(0.35),
                [{"text": "Integrantes", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    members = [
        "Ayelén Calo (a2510)",
        "Agustín Daniel Ross (a2539)",
        "Francisco Valentín Meaca (a2530)",
        "Franco Marcelo Morero (a2533)",
    ]
    add_textbox(slide, Inches(0.5), Inches(1.9), Inches(4.6), Inches(1.6),
                [{"text": f"• {m}", "size": 12} for m in members])

    add_textbox(slide, Inches(0.5), Inches(3.55), Inches(4.6), Inches(0.35),
                [{"text": "Dataset", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(0.5), Inches(3.9), Inches(4.6), Inches(1.3),
                [
                    {"text": "• 236.686 observaciones · 22 features originales (26 tras enriquecimiento)", "size": 11},
                    {"text": "• Rango temporal: 01-01-2025 a 31-12-2025", "size": 11},
                    {"text": "• Fuente: Chicago Data Portal — Crimes 2025", "size": 11},
                ])

    add_textbox(slide, Inches(5.3), Inches(1.55), Inches(4.2), Inches(0.35),
                [{"text": "Problema de ML supervisado", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(5.3), Inches(1.9), Inches(4.2), Inches(2.0),
                [
                    {"text": "Clasificación binaria", "size": 14, "bold": True, "color": PALETTE["primary"]},
                    {"text": "Target: Arrest  (True / False)", "size": 12},
                    {"text": "Objetivo: predecir si un crimen deriva en arresto", "size": 11, "color": PALETTE["muted"]},
                    {"text": "", "size": 6},
                    {"text": "Baseline de clase", "size": 12, "bold": True, "color": PALETTE["primary"]},
                    {"text": "• 15,99 % positivos  (Arresto)", "size": 11},
                    {"text": "• 84,01 % negativos (sin Arresto)", "size": 11},
                    {"text": "→ Problema desbalanceado", "size": 11, "color": PALETTE["accent"], "bold": True},
                ])

    add_textbox(slide, Inches(5.3), Inches(4.1), Inches(4.2), Inches(0.8),
                [
                    {"text": "Repositorio GitHub", "size": 11, "bold": True, "color": PALETTE["accent"]},
                    {"text": GITHUB_URL, "size": 10, "color": PALETTE["primary"]},
                ])
    add_footer(slide, 1)


def build_slide_2(slide, fig_crimes: Path, fig_areas: Path, fig_temporal_p: Path):
    set_slide_background(slide, PALETTE["bg"])
    add_accent_bar(slide, PALETTE["primary"])
    add_title(slide, "EDA — Patrones principales",
              "Concentración de crímenes por tipo, zona y momento del año")

    add_image(slide, fig_crimes, Inches(0.25), Inches(1.2), width=Inches(4.75))
    add_image(slide, fig_areas, Inches(5.0), Inches(1.2), width=Inches(4.75))

    add_image(slide, fig_temporal_p, Inches(0.25), Inches(3.55), width=Inches(6.5))

    add_textbox(slide, Inches(6.95), Inches(3.55), Inches(2.85), Inches(1.8),
                [
                    {"text": "Insights clave", "size": 11, "bold": True, "color": PALETTE["accent"]},
                    {"text": "• THEFT + BATTERY = ~40% del total.", "size": 10},
                    {"text": "• Austin y Near North Side lideran.", "size": 10},
                    {"text": "• Pico: julio · viernes · medianoche.", "size": 10},
                    {"text": "• 41,8 % Index I (crímenes serios).", "size": 10},
                    {"text": "• Domésticos: 19,1 % del dataset.", "size": 10},
                ])
    add_footer(slide, 2)


def build_slide_3(slide):
    set_slide_background(slide, PALETTE["bg"])
    add_accent_bar(slide, PALETTE["primary"])
    add_title(slide, "Calidad de datos — Missings y outliers",
              "Diagnóstico, tipología (MCAR/MAR/MNAR) y criterios de tratamiento")

    # missings table (textbox)
    add_textbox(slide, Inches(0.5), Inches(1.2), Inches(5.1), Inches(0.4),
                [{"text": "Valores faltantes", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    missings = [
        {"text": "Variable                         n      %     Tipo", "size": 10, "bold": True, "font": "Courier New"},
        {"text": "IUCR Primary             10.397  4,34   MAR", "size": 10, "font": "Courier New"},
        {"text": "Location Description      1.097  0,46   MAR", "size": 10, "font": "Courier New"},
        {"text": "Latitude / Longitude         91  0,04   MAR", "size": 10, "font": "Courier New"},
        {"text": "Community Area                3  ~0     MCAR", "size": 10, "font": "Courier New"},
        {"text": "Ward                          1  ~0     MCAR", "size": 10, "font": "Courier New"},
    ]
    add_textbox(slide, Inches(0.5), Inches(1.55), Inches(5.1), Inches(2.0), missings)

    add_textbox(slide, Inches(0.5), Inches(3.55), Inches(5.1), Inches(1.6),
                [
                    {"text": "Interpretación", "size": 12, "bold": True, "color": PALETTE["accent"]},
                    {"text": "• IUCR Primary: nulos por códigos ausentes en dataset de enriquecimiento → MAR.", "size": 11},
                    {"text": "• Location Description: concentrada en DECEPTIVE PRACTICE (fraudes sin lugar físico) → MAR.", "size": 11},
                    {"text": "• Lat/Lon: dependen del tipo de crimen y del arresto → MAR.", "size": 11},
                    {"text": "• Community Area / Ward: ínfimo volumen, sin patrón → MCAR.", "size": 11},
                ])

    add_textbox(slide, Inches(5.8), Inches(1.2), Inches(4), Inches(0.4),
                [{"text": "Outliers (IQR y 3σ)", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(5.8), Inches(1.55), Inches(4), Inches(2.2),
                [
                    {"text": "• Latitude: 0 outliers (IQR y 3σ).", "size": 11},
                    {"text": "• Longitude: 1.802 (IQR) / 1.275 (3σ).", "size": 11},
                    {"text": "• Ubicados en el lado oeste de Chicago.", "size": 11},
                    {"text": "", "size": 6},
                    {"text": "Decisión: conservar outliers.", "size": 11, "bold": True, "color": PALETTE["primary"]},
                    {"text": "Son zonas periféricas legítimas (no errores); eliminarlas sesgaría el análisis territorial.", "size": 10, "color": PALETTE["muted"]},
                ])

    add_textbox(slide, Inches(5.8), Inches(3.85), Inches(4), Inches(1.3),
                [
                    {"text": "Criterio general", "size": 12, "bold": True, "color": PALETTE["accent"]},
                    {"text": "• Imputar en lugar de borrar; preservar la señal cuando el missing es informativo.", "size": 11},
                    {"text": "• Fit de transformaciones solo sobre train; aplicadas a test sin re-fit.", "size": 11},
                ])
    add_footer(slide, 3)


def build_slide_4(slide, fig_balance: Path, fig_new: Path):
    set_slide_background(slide, PALETTE["bg"])
    add_accent_bar(slide, PALETTE["primary"])
    add_title(slide, "Preprocesamiento + Feature Engineering",
              "Split estratificado 80/20 · Imputación · Escalado · Encoding · SMOTE")

    add_textbox(slide, Inches(0.4), Inches(1.2), Inches(5.7), Inches(0.35),
                [{"text": "Pipeline aplicado", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(0.4), Inches(1.55), Inches(5.7), Inches(2.2),
                [
                    {"text": "• Split: estratificado 80/20 → train 188.754 · test 47.189", "size": 11},
                    {"text": "• Imputación: mediana en Latitude / Longitude (91 filas, 0,04 %)", "size": 11},
                    {"text": "• Outliers: conservados (zonas periféricas legítimas)", "size": 11},
                    {"text": "• Escalado: StandardScaler sobre variables numéricas y target-encoded", "size": 11},
                    {"text": "• Encoding (10 → 14 → 68 features):", "size": 11, "bold": True},
                    {"text": "    − OneHot: Primary Type (31) · FBI Code (25)", "size": 11, "level": 1},
                    {"text": "    − TargetEncoder (smooth=10): Beat (274) · Community Area (77) · Ward (50)", "size": 11, "level": 1},
                    {"text": "    − FE temporal: hour, day_of_week, month, quarter, day_of_year", "size": 11, "level": 1},
                ])

    add_textbox(slide, Inches(0.4), Inches(3.85), Inches(5.7), Inches(0.35),
                [{"text": "Features nuevas (notebook 3 · Agus)", "size": 12, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(0.4), Inches(4.15), Inches(5.7), Inches(1.2),
                [
                    {"text": "• distancia_cbd — Haversine al Loop (r = −0,01)", "size": 10},
                    {"text": "• night_violent — is_night × is_violent (r = +0,02)", "size": 10},
                    {"text": "• beat_arrest_rate — tasa histórica por Beat con smoothing laplaciano", "size": 10},
                    {"text": "  (solo train, r = +0,20 → la más informativa de las tres)", "size": 10, "color": PALETTE["primary"], "bold": True},
                ])

    add_image(slide, fig_balance, Inches(6.25), Inches(1.2), width=Inches(3.55))
    add_image(slide, fig_new, Inches(6.25), Inches(3.6), width=Inches(3.55))
    add_textbox(slide, Inches(6.25), Inches(5.05), Inches(3.55), Inches(0.35),
                [
                    {"text": "SMOTE k=5 solo en train · test con distribución real", "size": 9, "color": PALETTE["muted"]},
                ])
    add_footer(slide, 4)


def build_slide_5(slide, fig_pca: Path):
    set_slide_background(slide, PALETTE["bg"])
    add_accent_bar(slide, PALETTE["primary"])
    add_title(slide, "Selección de features · PCA · Conclusiones",
              "Reducción de dimensionalidad supervisada y no supervisada")

    add_textbox(slide, Inches(0.4), Inches(1.2), Inches(5.3), Inches(0.35),
                [{"text": "Selección por filtros", "size": 13, "bold": True, "color": PALETTE["accent"]}])
    add_textbox(slide, Inches(0.4), Inches(1.55), Inches(5.3), Inches(2.5),
                [
                    {"text": "• Correlación Pearson/Spearman/Kendall → multicolinealidad temporal", "size": 11},
                    {"text": "  fuerte: month ↔ day_of_year (0,996), month ↔ quarter (0,97).", "size": 11},
                    {"text": "• SelectKBest(k=20) con mutual_info_classif (supervisado).", "size": 11},
                    {"text": "• Top features por información mutua con Arrest:", "size": 11, "bold": True},
                    {"text": "    − FBI Code_18 · Primary Type_NARCOTICS (0,05)", "size": 11, "level": 1},
                    {"text": "    − Latitude / Longitude (0,048)", "size": 11, "level": 1},
                    {"text": "    − Beat · Community Area · District (geografía)", "size": 11, "level": 1},
                    {"text": "    − FBI Code_15 · WEAPONS VIOLATION (0,02)", "size": 11, "level": 1},
                    {"text": "→ Tipo de crimen + zona concentran la señal predictiva.", "size": 11, "color": PALETTE["primary"], "bold": True},
                ])

    add_image(slide, fig_pca, Inches(5.85), Inches(1.2), width=Inches(3.95))
    add_textbox(slide, Inches(5.85), Inches(3.55), Inches(3.95), Inches(1.3),
                [
                    {"text": "PCA (68 features numéricas)", "size": 11, "bold": True, "color": PALETTE["accent"]},
                    {"text": "• 11 componentes explican el 90 % de la varianza.", "size": 10},
                    {"text": "• PC1 temporal (month, day_of_year, quarter).", "size": 10},
                    {"text": "• PC2-3 geográfico (Community Area, Beat, Ward, Lat/Lon).", "size": 10},
                    {"text": "• PC4-5 ciclo semanal / horario.", "size": 10},
                    {"text": "• Trade-off: ↓ multicolinealidad / ↓ interpretabilidad.", "size": 10, "color": PALETTE["muted"]},
                ])

    add_textbox(slide, Inches(0.4), Inches(4.15), Inches(9.4), Inches(1.1),
                [
                    {"text": "Conclusiones y próximos pasos", "size": 12, "bold": True, "color": PALETTE["accent"]},
                    {"text": "• Dataset limpio pero fuertemente desbalanceado → evaluar con F1 / ROC-AUC + class weights + SMOTE.", "size": 10},
                    {"text": "• Pipeline modular (imputación → encoding → escalado → balance → selección / PCA) reproducible sobre train y test.", "size": 10},
                    {"text": f"• Código completo y notebooks: {GITHUB_URL}", "size": 10, "color": PALETTE["primary"]},
                ])
    add_footer(slide, 5)


def main() -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    df, comm = load_data()

    print("Generando figuras...")
    fig_crimes = fig_top_crimes(df)
    fig_areas = fig_top_areas(df, comm)
    fig_temp = fig_temporal(df)
    fig_balance = fig_class_balance()
    fig_pca = fig_pca_variance()
    fig_new = fig_new_features()
    print(f"  {fig_crimes.name}, {fig_areas.name}, {fig_temp.name}, "
          f"{fig_balance.name}, {fig_pca.name}, {fig_new.name}")

    print("Construyendo pptx...")
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]  # BLANK layout (default template)

    builders = [
        lambda s: build_slide_1(s),
        lambda s: build_slide_2(s, fig_crimes, fig_areas, fig_temp),
        lambda s: build_slide_3(s),
        lambda s: build_slide_4(s, fig_balance, fig_new),
        lambda s: build_slide_5(s, fig_pca),
    ]
    for b in builders:
        slide = prs.slides.add_slide(blank_layout)
        b(slide)

    prs.save(str(OUTPUT))
    print(f"→ Presentación guardada en {OUTPUT}")
    print(f"   Slides finales: {len(prs.slides)}  (esperado 5)")


if __name__ == "__main__":
    main()
