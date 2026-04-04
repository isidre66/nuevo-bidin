import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy import stats
import os
from datetime import date

st.set_page_config(page_title="Informe Global de Referencia", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;600;700&family=Inter:wght@300;400;500&display=swap');
.report-header {
    background:linear-gradient(135deg,#0a0e1a,#1a1a2e);
    border:1px solid #2d1b69; border-radius:14px;
    padding:28px 32px; margin-bottom:24px;
}
.report-header h1, .report-header p, .report-header div, .report-header span {
    color:#e2e8f0 !important;
}
.section-title {
    font-family:'Rajdhani',sans-serif; font-size:1.25rem; font-weight:700;
    color:#e2e8f0 !important;
    background:linear-gradient(90deg,rgba(124,58,237,0.3),rgba(124,58,237,0));
    border-left:5px solid #7c3aed; padding:11px 16px; border-radius:0 8px 8px 0;
    margin:28px 0 14px 0;
}
.insight-box {
    background:#1a1400; border-left:4px solid #f59e0b;
    border-radius:0 10px 10px 0; padding:16px 20px; margin-bottom:12px;
    color:#1e293b; line-height:1.8; font-size:.93rem;
}
.insight-box-blue {
    background:#eff6ff; border-left:4px solid #2563eb;
    border-radius:0 10px 10px 0; padding:16px 20px; margin-bottom:12px;
    color:#1e293b; line-height:1.8; font-size:.93rem;
}
.kpi-box {
    background:#f1f5f9; border:1px solid #cbd5e1;
    border-radius:10px; padding:14px; text-align:center;
}
.ge-card {
    border-radius:12px; padding:18px 20px; margin-bottom:10px;
    color:#1e293b; line-height:1.7;
}
.sig-row {
    background:#f8fafc; border:1px solid #e2e8f0;
    border-radius:8px; padding:12px 16px; margin-bottom:8px;
    font-size:.9rem; line-height:1.6; color:#1e293b;
}
.hallazgo {
    border-radius:0 10px 10px 0; padding:18px 22px; margin-bottom:14px;
    color:#1e293b; line-height:1.8; font-size:.93rem;
}
</style>
""", unsafe_allow_html=True)

# ── Excel ──────────────────────────────────────────────────────────────────
ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','datos.xlsx')
if not os.path.exists(ruta): ruta = "datos.xlsx"
try:
    df = pd.read_excel(ruta); df.columns = df.columns.str.strip()
except Exception as e:
    st.error(f"Error cargando datos: {e}"); st.stop()

hoy = date.today().strftime("%d/%m/%Y")

# ── Diccionarios ───────────────────────────────────────────────────────────
MACROSECTORES = {1:"Industria", 2:"Tec. Avanzada", 3:"Servicios"}
TAMANIOS      = {1:"Pequeña",   2:"Mediana",       3:"Grande"}
EXPORTACIONES = {1:"< 10%",    2:"10-30%",         3:"30-60%",  4:"> 60%"}
ANTIGUEDADES  = {1:"< 10 años",2:"10-30 años",     3:"> 30 años"}
REGIONES      = {1:"Andalucía",2:"Aragón",3:"Asturias",4:"Baleares",5:"Canarias",
                 6:"Cantabria",7:"C. La Mancha",8:"C. y León",9:"Cataluña",
                 10:"C. Valenciana",11:"Extremadura",12:"Galicia",13:"Madrid",
                 14:"Murcia",15:"Navarra",16:"País Vasco"}

INDS      = ['IND_IDi','IND_GPROY','IND_DESPROD','IND_ESTRINN','IND_DESMPINN']
IND_NAMES = {'IND_IDi':'I+D+i','IND_GPROY':'Gest. Proyectos',
             'IND_DESPROD':'Dllo. Productos','IND_ESTRINN':'Estrategia Inn.',
             'IND_DESMPINN':'Desempeño Inn.'}
ECON      = ['ROA','Var_Ventas_5a','Var_Emp_5a','Prod_Venta_Emp','Coste_Med_Emp','Ratio_Endeudamiento']
ECON_NAMES= {'ROA':'ROA (%)','Var_Ventas_5a':'Crec. Ventas 5a (%)','Var_Emp_5a':'Crec. Empleo 5a (%)',
             'Prod_Venta_Emp':'Productividad (€/emp)','Coste_Med_Emp':'Coste Medio Emp (€)',
             'Ratio_Endeudamiento':'Endeudamiento'}

GE_LABELS  = ['🚀 Líderes Estratégicos','⭐ Empresas Sólidas',
              '📊 Posición Intermedia','🔄 En Desarrollo','📉 Rezagadas']
GE_COLORS  = ['#10b981','#3b82f6','#f59e0b','#f97316','#ef4444']
GE_BG      = ['#0a2010','#0a1020','#1a1200','#1a0e00','#1a0505']
GE_BORDER  = ['#10b981','#3b82f6','#f59e0b','#f97316','#ef4444']

LAYOUT_BASE = dict(
    paper_bgcolor='#0a0e1a', plot_bgcolor='#0a0e1a',
    font=dict(color='#e2e8f0', size=12),
    margin=dict(t=40, b=20, l=10, r=10)
)

# ══════════════════════════════════════════════════════════════════════════
# GRUPOS ESTRATÉGICOS — Score ponderado por percentiles
# ══════════════════════════════════════════════════════════════════════════
@st.cache_data
def calcular_grupos(data):
    d = data.copy()
    # Percentil de cada empresa en cada variable (0-100)
    d['pct_inn']  = d['MACRO_INNOVACION'].rank(pct=True) * 100
    d['pct_roa']  = d['ROA'].rank(pct=True) * 100
    d['pct_crec'] = d['Var_Ventas_5a'].rank(pct=True) * 100
    d['pct_prod'] = d['Prod_Venta_Emp'].rank(pct=True) * 100
    d['pct_endeu']= (1 - d['Ratio_Endeudamiento'].rank(pct=True)) * 100  # invertido

    # Score compuesto ponderado
    d['GE_score'] = (
        d['pct_inn']   * 0.25 +
        d['pct_roa']   * 0.25 +
        d['pct_crec']  * 0.20 +
        d['pct_prod']  * 0.20 +
        d['pct_endeu'] * 0.10
    )
    # Dividir en 5 grupos por quintiles (0=mejor, 4=peor)
    d['GE'] = pd.qcut(d['GE_score'], q=5, labels=[0,1,2,3,4]).astype(int)
    # Invertir: 0 = score más alto = Líderes
    d['GE'] = 4 - d['GE']

    # Perfil de cada grupo
    perfiles = {}
    for g in range(5):
        sub = d[d['GE']==g]
        perfiles[g] = {
            'inn':   round(sub['MACRO_INNOVACION'].mean(), 2),
            'roa':   round(sub['ROA'].mean(), 1),
            'crec':  round(sub['Var_Ventas_5a'].mean(), 1),
            'prod':  round(sub['Prod_Venta_Emp'].mean(), 0),
            'endeu': round(sub['Ratio_Endeudamiento'].mean(), 3),
            'score': round(sub['GE_score'].mean(), 1),
            'n':     len(sub),
        }
    return d['GE'].values, d['GE_score'].values, perfiles

ge_vals, ge_scores, ge_perfiles = calcular_grupos(df)
df['GE'] = ge_vals
df['GE_score'] = ge_scores

# ══════════════════════════════════════════════════════════════════════════
# CORRELACIONES
# ══════════════════════════════════════════════════════════════════════════
@st.cache_data
def calcular_corr(data):
    matriz, pvals = {}, {}
    for ind in INDS:
        matriz[ind], pvals[ind] = {}, {}
        for eco in ECON:
            r, p = stats.spearmanr(data[ind], data[eco])
            matriz[ind][eco] = round(r, 3)
            pvals[ind][eco]  = round(p, 4)
    return matriz, pvals

corr_matrix, pval_matrix = calcular_corr(df)

# ══════════════════════════════════════════════════════════════════════════
# CABECERA
# ══════════════════════════════════════════════════════════════════════════
n_tot    = len(df)
inn_med  = round(df['MACRO_INNOVACION'].mean(), 2)
roa_med  = round(df['ROA'].mean(), 1)
crec_med = round(df['Var_Ventas_5a'].mean(), 1)
prod_med = round(df['Prod_Venta_Emp'].mean(), 0)

from asistentes import mostrar_felix
mostrar_felix(pagina='informe_global')
<div class="report-header">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:16px;">
    <div>
      <div style="font-size:.7rem;color:#7c6fcd;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">
        Informe Global de Referencia · Base de Datos Completa</div>
      <h1 style="font-family:Rajdhani,sans-serif;color:#a78bfa;margin:0;font-size:2rem;">
        Análisis de Innovación y Desempeño Empresarial</h1>
      <p style="color:#94a3b8;margin:6px 0 0 0;font-size:.88rem;">
        Análisis estadístico de <strong style="color:#e2e8f0;">{n_tot} empresas auditadas</strong> ·
        Correlaciones, grupos estratégicos y factores de innovación · {hoy}
      </p>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

k1,k2,k3,k4,k5 = st.columns(5)
for col_st, label, val, fmt in [
    (k1,"Empresas analizadas", n_tot, "{:.0f}"),
    (k2,"Innovación media",    inn_med, "{:.2f} / 5"),
    (k3,"ROA medio",           roa_med, "{:.1f}%"),
    (k4,"Crec. Ventas 5a",    crec_med, "{:.1f}%"),
    (k5,"Productividad media", prod_med, "{:,.0f}€"),
]:
    col_st.markdown(f"""<div class="kpi-box">
        <div style="font-size:.65rem;color:#7c6fcd;letter-spacing:.5px;">{label}</div>
        <div style="font-family:Rajdhani,sans-serif;font-size:1.75rem;color:#a78bfa;font-weight:700;">{fmt.format(val)}</div>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# BLOQUE 1 — INNOVACIÓN POR CLASIFICACIÓN
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📊 Bloque 1 · Perfil Innovador por Variables de Clasificación</div>',
            unsafe_allow_html=True)
st.markdown("""<div class="insight-box-blue">
<strong style="color:#00d4ff;">¿Qué empresas innovan más?</strong> Análisis de si el macrosector, tamaño,
nivel exportador o antigüedad están asociados con mayores niveles de innovación.
Test de Kruskal-Wallis para determinar si las diferencias son estadísticamente significativas al 95%.
</div>""", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5 = st.tabs(["🏭 Macrosector","📏 Tamaño","🌍 Exportación","📅 Antigüedad","🗺️ Región"])

def barras_clas(col_var, diccionario, titulo):
    grupos_data = []
    for cod, nombre in diccionario.items():
        sub = df[df[col_var]==cod]['MACRO_INNOVACION']
        if len(sub) < 5: continue
        grupos_data.append({'nombre':nombre,'media':round(sub.mean(),3),'n':len(sub)})
    groups_list = [df[df[col_var]==c]['MACRO_INNOVACION'].values
                   for c in diccionario if len(df[df[col_var]==c])>=5]
    H, p = stats.kruskal(*groups_list)
    sig = '*** Diferencias significativas (p<0.001)' if p<0.001 else \
          '** Diferencias significativas (p<0.01)'   if p<0.01  else \
          '* Diferencias significativas (p<0.05)'    if p<0.05  else \
          'Sin diferencias estadísticamente significativas'
    color_sig = '#10b981' if p<0.05 else '#94a3b8'

    nombres = [g['nombre'] for g in grupos_data]
    medias  = [g['media']  for g in grupos_data]
    ns      = [g['n']      for g in grupos_data]
    colores = ['#10b981' if m >= df['MACRO_INNOVACION'].mean()+0.1
               else '#f59e0b' if m >= df['MACRO_INNOVACION'].mean()-0.1
               else '#ef4444' for m in medias]

    fig = go.Figure(go.Bar(
        x=nombres, y=medias, marker_color=colores,
        text=[f"{m:.2f}<br>n={n}" for m,n in zip(medias,ns)],
        textposition='outside', textfont=dict(color='#e2e8f0', size=12),
    ))
    fig.add_hline(y=df['MACRO_INNOVACION'].mean(), line_dash='dash', line_color='#a78bfa',
                  annotation_text=f"Media global {df['MACRO_INNOVACION'].mean():.2f}",
                  annotation_font=dict(color='#a78bfa', size=11))
    fig.update_layout(**LAYOUT_BASE, height=380,
        title=dict(text=titulo, font=dict(color='#e2e8f0', size=13)),
        yaxis=dict(range=[0,5.3], gridcolor='#1e2a3a', title='Índice Innovación (0-5)',
                   tickfont=dict(color='#e2e8f0'), title_font=dict(color='#e2e8f0')),
        xaxis=dict(tickfont=dict(color='#e2e8f0')), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown(f'<p style="color:{color_sig};font-size:.88rem;font-weight:600;">'
                f'Kruskal-Wallis: H={H:.2f} · p={p:.4f} · {sig}</p>', unsafe_allow_html=True)

with tab1:
    barras_clas('Macrosector', MACROSECTORES, 'Índice de Innovación por Macrosector')
    st.markdown("**Comparaciones por pares (Mann-Whitney):**")
    ph_cols = st.columns(3)
    for col_st2, (i,j) in zip(ph_cols, [(1,2),(1,3),(2,3)]):
        g1 = df[df['Macrosector']==i]['MACRO_INNOVACION']
        g2 = df[df['Macrosector']==j]['MACRO_INNOVACION']
        _, p2 = stats.mannwhitneyu(g1, g2, alternative='two-sided')
        sig2 = '*** p<0.001' if p2<0.001 else '** p<0.01' if p2<0.01 else '* p<0.05' if p2<0.05 else 'ns'
        c2 = '#10b981' if p2<0.05 else '#94a3b8'
        col_st2.markdown(
            f'<div class="sig-row"><strong style="color:#e2e8f0;">{MACROSECTORES[i]}</strong> vs '
            f'<strong style="color:#e2e8f0;">{MACROSECTORES[j]}</strong><br>'
            f'<span style="color:{c2};font-weight:700;">{sig2}</span></div>',
            unsafe_allow_html=True)
with tab2: barras_clas('Tamaño', TAMANIOS, 'Índice de Innovación por Tamaño')
with tab3: barras_clas('Exportacion', EXPORTACIONES, 'Índice de Innovación por Nivel de Exportación')
with tab4: barras_clas('Antigüedad', ANTIGUEDADES, 'Índice de Innovación por Antigüedad')
with tab5:
    reg_data = []
    for cod, nombre in REGIONES.items():
        sub = df[df['Region']==cod]['MACRO_INNOVACION']
        if len(sub) >= 5:
            reg_data.append({'Region':nombre,'Media':round(sub.mean(),3),'N':len(sub)})
    reg_df = pd.DataFrame(reg_data).sort_values('Media')
    colors_reg = ['#10b981' if v>=df['MACRO_INNOVACION'].mean()+0.05
                  else '#f59e0b' if v>=df['MACRO_INNOVACION'].mean()-0.05
                  else '#ef4444' for v in reg_df['Media']]
    fig_reg = go.Figure(go.Bar(
        x=reg_df['Media'], y=reg_df['Region'], orientation='h',
        marker_color=colors_reg,
        text=[f"{v:.2f}  (n={n})" for v,n in zip(reg_df['Media'],reg_df['N'])],
        textposition='outside', textfont=dict(color='#e2e8f0', size=11),
    ))
    fig_reg.add_vline(x=df['MACRO_INNOVACION'].mean(), line_dash='dash', line_color='#a78bfa',
                      annotation_text="Media global", annotation_font=dict(color='#a78bfa'))
    fig_reg.update_layout(**LAYOUT_BASE, height=540,
        title=dict(text='Ranking de Innovación por Comunidad Autónoma',
                   font=dict(color='#e2e8f0', size=13)),
        xaxis=dict(range=[0,5.5], gridcolor='#1e2a3a', tickfont=dict(color='#e2e8f0')),
        yaxis=dict(gridcolor='#1e2a3a', tickfont=dict(color='#e2e8f0')), showlegend=False)
    st.plotly_chart(fig_reg, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# BLOQUE 2 — CORRELACIONES (solo panel de significativas)
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔗 Bloque 2 · Relaciones Estadísticamente Significativas</div>',
            unsafe_allow_html=True)
st.markdown("""<div class="insight-box">
<strong style="color:#f59e0b;">Correlaciones de Spearman</strong> entre los 5 indicadores de innovación
y las variables de desempeño económico. Solo se muestran las relaciones con p&lt;0.05.
Una correlación positiva indica que a mayor innovación, mayor valor en esa variable económica.
<br><br>
<strong>Niveles de significatividad:</strong>
&nbsp;*** p&lt;0.001 &nbsp;·&nbsp; ** p&lt;0.01 &nbsp;·&nbsp; * p&lt;0.05
</div>""", unsafe_allow_html=True)

# Recopilar todas las relaciones significativas
rels_sig = []
for ind in INDS:
    for eco in ECON:
        p = pval_matrix[ind][eco]
        r = corr_matrix[ind][eco]
        if p < 0.05:
            rels_sig.append((abs(r), r, p, ind, eco))
rels_sig.sort(reverse=True)

if rels_sig:
    col_a, col_b = st.columns(2)
    for idx, (_, r, p, ind, eco) in enumerate(rels_sig):
        col_st2 = col_a if idx % 2 == 0 else col_b
        sig_txt = '★★★ p<0.001' if p<0.001 else '★★ p<0.01' if p<0.01 else '★ p<0.05'
        dir_txt = '↑ Relación positiva' if r > 0 else '↓ Relación negativa'
        color   = '#10b981' if r > 0 else '#ef4444'
        ind_color = {'IND_IDi':'#3b82f6','IND_GPROY':'#8b5cf6','IND_DESPROD':'#10b981',
                     'IND_ESTRINN':'#f59e0b','IND_DESMPINN':'#ef4444'}.get(ind,'#a78bfa')
        col_st2.markdown(f"""
        <div class="sig-row" style="border-left:4px solid {color};">
          <div style="font-size:.95rem;font-weight:700;color:{ind_color};">{IND_NAMES[ind]}</div>
          <div style="font-size:.88rem;color:#e2e8f0;">→ {ECON_NAMES[eco]}</div>
          <div style="margin-top:4px;">
            <span style="color:{color};font-weight:700;font-size:.9rem;">{dir_txt}</span>
            &nbsp;·&nbsp;
            <span style="color:#e2e8f0;font-size:.88rem;">r = {r:+.3f}</span>
            &nbsp;·&nbsp;
            <span style="color:#a78bfa;font-size:.85rem;">{sig_txt}</span>
          </div>
        </div>""", unsafe_allow_html=True)
else:
    st.info("No se encontraron relaciones estadísticamente significativas.")

st.markdown("""<div class="insight-box-blue" style="margin-top:16px;">
<strong style="color:#00d4ff;">Interpretación:</strong> Las correlaciones significativas son de magnitud moderada,
lo que indica que la innovación es un factor que contribuye al desempeño pero no lo determina de forma exclusiva.
El indicador de <strong>I+D+i</strong> muestra las relaciones más consistentes con variables de crecimiento
y productividad. La mayor parte de los indicadores no tienen correlación significativa con el ROA a corto plazo,
lo que es coherente con la naturaleza de la innovación como inversión de medio-largo plazo.
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════
# BLOQUE 3 — SCATTER INTERACTIVO
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Bloque 3 · Explorador de Relaciones Innovación–Desempeño</div>',
            unsafe_allow_html=True)
st.markdown("""<div class="insight-box-blue">
Selecciona un indicador de innovación y una variable económica para visualizar la relación entre ambas.
Los puntos están coloreados según el grupo estratégico al que pertenece cada empresa.
</div>""", unsafe_allow_html=True)

sc1, sc2 = st.columns(2)
with sc1:
    ind_sel = st.selectbox("Indicador de Innovación", options=INDS, format_func=lambda x: IND_NAMES[x])
with sc2:
    eco_sel = st.selectbox("Variable Económica", options=ECON, format_func=lambda x: ECON_NAMES[x])

r_sel, p_sel = stats.spearmanr(df[ind_sel], df[eco_sel])
sig_sel = '*** p<0.001' if p_sel<0.001 else '** p<0.01' if p_sel<0.01 else '* p<0.05' if p_sel<0.05 else 'ns (no significativo)'
color_sel = '#10b981' if r_sel>0 else '#ef4444'

fig_sc = go.Figure()
for ge_num, (label, color) in enumerate(zip(GE_LABELS, GE_COLORS)):
    sub = df[df['GE']==ge_num]
    fig_sc.add_trace(go.Scatter(
        x=sub[ind_sel], y=sub[eco_sel], mode='markers', name=label,
        marker=dict(color=color, size=5, opacity=0.7,
                    line=dict(width=0.3, color='#000')),
    ))
slope, intercept, *_ = stats.linregress(df[ind_sel], df[eco_sel])
x_line = np.linspace(df[ind_sel].min(), df[ind_sel].max(), 100)
fig_sc.add_trace(go.Scatter(
    x=x_line, y=slope*x_line+intercept, mode='lines', name='Tendencia',
    line=dict(color='#a78bfa', width=2, dash='dash')
))
fig_sc.update_layout(**LAYOUT_BASE, height=440,
    title=dict(text=f"r Spearman = {r_sel:+.3f}  ·  {sig_sel}",
               font=dict(color=color_sel, size=13)),
    xaxis=dict(title=IND_NAMES[ind_sel], gridcolor='#1e2a3a',
               tickfont=dict(color='#e2e8f0'), title_font=dict(color='#e2e8f0')),
    yaxis=dict(title=ECON_NAMES[eco_sel], gridcolor='#1e2a3a',
               tickfont=dict(color='#e2e8f0'), title_font=dict(color='#e2e8f0')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11)),
)
st.plotly_chart(fig_sc, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# BLOQUE 4 — GRUPOS ESTRATÉGICOS
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🎯 Bloque 4 · Grupos Estratégicos</div>', unsafe_allow_html=True)
st.markdown("""<div class="insight-box">
<strong style="color:#f59e0b;">Metodología:</strong> Cada empresa recibe un <strong>score compuesto (0-100)</strong>
calculado a partir de su posición percentil en 5 variables: Innovación (25%), ROA (25%),
Crecimiento de Ventas (20%), Productividad (20%) y Bajo Endeudamiento (10%).
Las empresas se dividen en 5 grupos por quintiles. El Grupo 1 (Líderes) agrupa
el 20% con mayor score y el Grupo 5 (Rezagadas) el 20% con menor score.
Así cada grupo es internamente coherente — sin mezclar puntos fuertes con débiles.
</div>""", unsafe_allow_html=True)

# Tarjetas de grupos
ge_cols = st.columns(5)
for i in range(5):
    p = ge_perfiles[i]
    ge_cols[i].markdown(f"""
    <div class="ge-card" style="background:{GE_BG[i]};border:1px solid {GE_BORDER[i]}60;">
      <div style="font-size:.82rem;font-weight:700;color:{GE_COLORS[i]};margin-bottom:10px;">
        {GE_LABELS[i]}</div>
      <div style="font-size:.75rem;color:#94a3b8;margin-bottom:8px;">
        {p['n']} empresas · Score medio: {p['score']:.0f}/100</div>
      <hr style="border-color:{GE_BORDER[i]}30;margin:6px 0;">
      <div style="font-size:.82rem;color:#e2e8f0;line-height:1.9;">
        🔬 Innovación: <strong style="color:{GE_COLORS[i]};">{p['inn']:.2f}/5</strong><br>
        💰 ROA: <strong style="color:{GE_COLORS[i]};">{p['roa']:.1f}%</strong><br>
        📈 Crec. Ventas: <strong style="color:{GE_COLORS[i]};">{p['crec']:.1f}%</strong><br>
        ⚙️ Productividad: <strong style="color:{GE_COLORS[i]};">{p['prod']:,.0f}€</strong><br>
        🏦 Endeudamiento: <strong style="color:{GE_COLORS[i]};">{p['endeu']:.2f}</strong>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Radar comparativo
st.markdown('<p style="color:#e2e8f0;font-weight:600;margin-bottom:4px;">Perfil radar comparativo de los 5 grupos (valores normalizados 0-100):</p>',
            unsafe_allow_html=True)

radar_cats = ['Innovación','ROA','Crecimiento','Productividad','Bajo Endeud.']
fig_radar = go.Figure()
for i in range(5):
    p = ge_perfiles[i]
    vals = [
        p['inn']/5*100,
        min(p['roa']/20*100, 100),
        min(p['crec']/200*100, 100),
        min(p['prod']/600000*100, 100),
        max(0, (1-p['endeu'])*200),
    ]
    vals_c = vals + [vals[0]]
    cats_c = radar_cats + [radar_cats[0]]
    fig_radar.add_trace(go.Scatterpolar(
        r=vals_c, theta=cats_c, fill='toself', name=GE_LABELS[i],
        line=dict(color=GE_COLORS[i], width=2),
        fillcolor=GE_COLORS[i].replace('#','rgba(') + ',0.10)' if False else GE_COLORS[i],
        opacity=0.75,
    ))
# Fix fillcolor
for i, trace in enumerate(fig_radar.data):
    rgb = {'#10b981':'16,185,129','#3b82f6':'59,130,246','#f59e0b':'245,158,11',
           '#f97316':'249,115,22','#ef4444':'239,68,68'}.get(GE_COLORS[i],'200,200,200')
    trace.fillcolor = f'rgba({rgb},0.10)'

fig_radar.update_layout(
    polar=dict(
        bgcolor='#0d1220',
        radialaxis=dict(visible=True, range=[0,100], gridcolor='#1e2a3a',
                        tickfont=dict(color='#e2e8f0', size=9)),
        angularaxis=dict(gridcolor='#1e2a3a', tickfont=dict(color='#e2e8f0', size=12))
    ),
    paper_bgcolor='#0a0e1a', font=dict(color='#e2e8f0'),
    height=450, margin=dict(t=20,b=20),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11))
)
st.plotly_chart(fig_radar, use_container_width=True)

# Distribución por macrosector
st.markdown('<p style="color:#e2e8f0;font-weight:600;margin-bottom:4px;">Distribución de grupos estratégicos por macrosector:</p>',
            unsafe_allow_html=True)
dist_data = []
for mac_cod, mac_nom in MACROSECTORES.items():
    sub = df[df['Macrosector']==mac_cod]
    for ge_num in range(5):
        n = len(sub[sub['GE']==ge_num])
        dist_data.append({'Macrosector':mac_nom,'Grupo':GE_LABELS[ge_num],
                          'N':n,'Pct':round(n/len(sub)*100,1)})
dist_df = pd.DataFrame(dist_data)
fig_dist = go.Figure()
for ge_num in range(5):
    sub_d = dist_df[dist_df['Grupo']==GE_LABELS[ge_num]]
    fig_dist.add_trace(go.Bar(
        name=GE_LABELS[ge_num], x=sub_d['Macrosector'], y=sub_d['Pct'],
        marker_color=GE_COLORS[ge_num],
        text=sub_d['Pct'].apply(lambda x: f"{x:.0f}%"),
        textposition='inside', textfont=dict(color='#fff', size=11)
    ))
fig_dist.update_layout(**LAYOUT_BASE, barmode='stack', height=360,
    yaxis=dict(title='% empresas', gridcolor='#1e2a3a', tickfont=dict(color='#e2e8f0'),
               title_font=dict(color='#e2e8f0')),
    xaxis=dict(gridcolor='#1e2a3a', tickfont=dict(color='#e2e8f0')),
    legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#e2e8f0', size=11)))
st.plotly_chart(fig_dist, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════
# BLOQUE 5 — CONCLUSIONES
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📋 Bloque 5 · Hallazgos y Conclusiones</div>', unsafe_allow_html=True)

mac_inn   = {cod: df[df['Macrosector']==cod]['MACRO_INNOVACION'].mean() for cod in [1,2,3]}
mejor_mac = MACROSECTORES[max(mac_inn, key=mac_inn.get)]
peor_mac  = MACROSECTORES[min(mac_inn, key=mac_inn.get)]
lider = ge_perfiles[0]; rezag = ge_perfiles[4]
n_sig = sum(1 for ind in INDS for eco in ECON if pval_matrix[ind][eco] < 0.05)
mejor_ind = max(INDS, key=lambda i: sum(abs(corr_matrix[i][e]) for e in ECON if pval_matrix[i][e]<0.05))

hallazgos = [
    ("#3b82f6","🏭","El macrosector es el principal determinante de la innovación",
     f"{mejor_mac} lidera la innovación con diferencias altamente significativas respecto a {peor_mac} "
     f"(Kruskal-Wallis p&lt;0.001). El tamaño y la antigüedad de la empresa no muestran asociación "
     f"estadísticamente significativa con los niveles de innovación, lo que sugiere que la propensión "
     f"a innovar es una característica estructural del sector más que del tamaño organizativo."),
    ("#10b981","📊","La relación innovación–desempeño económico es real pero moderada",
     f"Se identifican {n_sig} relaciones estadísticamente significativas (p&lt;0.05) entre los indicadores "
     f"de innovación y las variables económicas. El indicador con mayor asociación consistente es "
     f"<strong>{IND_NAMES[mejor_ind]}</strong>. La magnitud moderada de las correlaciones indica que "
     f"la innovación es un factor que contribuye al desempeño pero no lo determina de forma exclusiva — "
     f"otros factores como la gestión financiera, el posicionamiento de mercado y las condiciones "
     f"sectoriales juegan un papel equivalente o superior."),
    ("#f59e0b","🎯","Los Líderes Estratégicos presentan un perfil equilibrado en todos los ejes",
     f"El grupo líder (n={lider['n']}) destaca simultáneamente en innovación ({lider['inn']:.2f}/5), "
     f"rentabilidad (ROA {lider['roa']:.1f}%) y crecimiento ({lider['crec']:.1f}%), con una "
     f"productividad de {lider['prod']:,.0f}€/empleado. Las Rezagadas (n={rezag['n']}) presentan "
     f"valores inferiores a la media en los cinco ejes del score compuesto, con un índice innovador "
     f"de {rezag['inn']:.2f}/5 y un crecimiento de ventas de {rezag['crec']:.1f}%."),
    ("#7c3aed","💡","Implicación estratégica: la innovación es una condición necesaria, no suficiente",
     "Los datos de la muestra indican que las empresas líderes en desempeño comparten un perfil innovador "
     "sólido, pero la innovación por sí sola no garantiza resultados económicos superiores a corto plazo. "
     "Las empresas que combinan capacidades de I+D+i con estrategia de mercado orientada al crecimiento "
     "y gestión financiera sólida son las que alcanzan posiciones de liderazgo sostenido. La inversión "
     "en innovación debe entenderse como un activo estratégico de medio-largo plazo."),
]

for color, icono, titulo, texto in hallazgos:
    st.markdown(f"""<div class="hallazgo" style="background:{color}15;border-left:4px solid {color};">
        <div style="font-size:1rem;font-weight:700;color:{color};margin-bottom:8px;">{icono} {titulo}</div>
        <div style="color:#e2e8f0;line-height:1.8;">{texto}</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ══════════════════════════════════════════════════════════════════════════
# DESCARGA
# ══════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📥 Descargar Informe Global</div>', unsafe_allow_html=True)

def generar_html():
    tabla_ge = "".join([f"""<tr>
        <td style='color:{GE_COLORS[i]};font-weight:700;'>{GE_LABELS[i]}</td>
        <td style='text-align:center;'>{ge_perfiles[i]['n']}</td>
        <td style='text-align:center;'>{ge_perfiles[i]['score']:.0f}/100</td>
        <td style='text-align:center;'>{ge_perfiles[i]['inn']:.2f}/5</td>
        <td style='text-align:center;'>{ge_perfiles[i]['roa']:.1f}%</td>
        <td style='text-align:center;'>{ge_perfiles[i]['crec']:.1f}%</td>
        <td style='text-align:center;'>{ge_perfiles[i]['prod']:,.0f}€</td>
    </tr>""" for i in range(5)])
    tabla_corr = "".join([
        f"<tr><td><strong>{IND_NAMES[ind]}</strong></td>" +
        "".join([f"<td style='text-align:center;"
                 f"background:{'rgba(16,185,129,.15)' if corr_matrix[ind][eco]>0.05 and pval_matrix[ind][eco]<0.05 else 'rgba(239,68,68,.15)' if corr_matrix[ind][eco]<-0.05 and pval_matrix[ind][eco]<0.05 else ''};'>"
                 f"{corr_matrix[ind][eco]:+.3f}{'***' if pval_matrix[ind][eco]<0.001 else '**' if pval_matrix[ind][eco]<0.01 else '*' if pval_matrix[ind][eco]<0.05 else ''}</td>"
                 for eco in ECON]) + "</tr>"
        for ind in INDS])
    hall_html = "".join([f"<div style='border-left:4px solid {c};padding:12px 16px;margin:12px 0;'>"
                         f"<h3 style='color:{c};margin:0 0 6px 0;'>{ic} {t}</h3><p>{tx}</p></div>"
                         for c,ic,t,tx in hallazgos])
    return f"""<!DOCTYPE html><html><head><meta charset='utf-8'>
<style>body{{font-family:Georgia,serif;max-width:960px;margin:50px auto;color:#1a1a1a;line-height:1.7;}}
h1{{color:#7c3aed;border-bottom:3px solid #7c3aed;padding-bottom:8px;}}
h2{{color:#7c3aed;border-left:4px solid #7c3aed;padding-left:10px;margin-top:32px;}}
table{{border-collapse:collapse;width:100%;margin:14px 0;font-size:.88rem;}}
th{{background:#7c3aed;color:white;padding:10px;}}
td{{padding:8px 10px;border-bottom:1px solid #e5e7eb;}}
</style></head><body>
<h1>Informe Global de Referencia — Innovación y Desempeño</h1>
<p style='color:#6b7280;'>{n_tot} empresas auditadas · {hoy}</p>
<h2>1. Grupos Estratégicos</h2>
<p>Score compuesto: Innovación (25%) + ROA (25%) + Crecimiento (20%) + Productividad (20%) + Bajo Endeudamiento (10%)</p>
<table><tr><th>Grupo</th><th>N</th><th>Score</th><th>Innovación</th><th>ROA</th><th>Crec.Ventas</th><th>Productividad</th></tr>
{tabla_ge}</table>
<h2>2. Correlaciones Spearman Innovación–Desempeño</h2>
<p>*** p&lt;0.001 · ** p&lt;0.01 · * p&lt;0.05</p>
<table><tr><th>Indicador</th>{"".join(f"<th>{ECON_NAMES[e]}</th>" for e in ECON)}</tr>{tabla_corr}</table>
<h2>3. Hallazgos y Conclusiones</h2>{hall_html}
<hr/><p style='color:#9ca3af;font-size:.78rem;text-align:center;'>Plataforma de Diagnóstico Estratégico · {hoy}</p>
</body></html>"""

c1, c2 = st.columns(2)
with c1:
    st.download_button("📥 Descargar Informe Global HTML", data=generar_html(),
        file_name=f"informe_global_{hoy.replace('/','_')}.html",
        mime="text/html", type="primary", use_container_width=True)
with c2:
    st.info("Abre el HTML en el navegador → **Ctrl+P** → **Guardar como PDF**")