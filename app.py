import os
import dash
from dash import dcc, html, Input, Output, State, callback
import plotly.graph_objects as go
import numpy as np

app = dash.Dash(__name__)

MATERIALS = {
    "Steel": 210,
    "Aluminum": 69,
    "Titanium": 114,
    "Copper": 117,
}

# ── Reusable styles ──

COLOR_PRIMARY = "#4f46e5"
COLOR_PRIMARY_HOVER = "#4338ca"
COLOR_BG = "#f0f2f5"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#1e293b"
COLOR_LABEL = "#475569"
COLOR_SECTION = "#6366f1"
COLOR_BORDER = "#e2e8f0"
COLOR_ACCENT_GREEN = "#10b981"
COLOR_ACCENT_BLUE = "#3b82f6"
COLOR_ACCENT_AMBER = "#f59e0b"
COLOR_ACCENT_RED = "#ef4444"

STYLE_INPUT = {
    "width": "100%",
    "padding": "10px 12px",
    "border": f"1.5px solid {COLOR_BORDER}",
    "borderRadius": "8px",
    "fontSize": "14px",
    "color": COLOR_TEXT,
    "backgroundColor": "#f8fafc",
    "outline": "none",
    "boxSizing": "border-box",
}

STYLE_LABEL = {
    "fontSize": "13px",
    "fontWeight": "600",
    "color": COLOR_LABEL,
    "marginBottom": "4px",
    "display": "block",
}

STYLE_SECTION_TITLE = {
    "fontSize": "14px",
    "fontWeight": "700",
    "color": COLOR_SECTION,
    "textTransform": "uppercase",
    "letterSpacing": "0.05em",
    "marginBottom": "12px",
    "marginTop": "0",
    "paddingBottom": "8px",
    "borderBottom": f"2px solid {COLOR_BORDER}",
}

STYLE_CARD = {
    "backgroundColor": COLOR_CARD,
    "borderRadius": "16px",
    "padding": "24px",
    "boxShadow": "0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04)",
    "border": f"1px solid {COLOR_BORDER}",
}


def make_field(label_text, input_component):
    return html.Div(
        style={"marginBottom": "14px"},
        children=[
            html.Label(label_text, style=STYLE_LABEL),
            input_component,
        ],
    )


app.layout = html.Div(
    style={
        "fontFamily": "'Segoe UI', 'Inter', -apple-system, sans-serif",
        "backgroundColor": COLOR_BG,
        "minHeight": "100vh",
    },
    children=[
        # ── Header bar ──
        html.Div(
            style={
                "background": f"linear-gradient(135deg, {COLOR_PRIMARY} 0%, #7c3aed 100%)",
                "padding": "28px 40px",
                "color": "white",
            },
            children=[
                html.H1(
                    "Cantilever Beam Calculator",
                    style={"margin": "0", "fontSize": "28px", "fontWeight": "700", "letterSpacing": "-0.02em"},
                ),
                html.P(
                    "Calculate and visualize deflection of rectangular cantilever beams under point loads",
                    style={"margin": "6px 0 0 0", "fontSize": "15px", "opacity": "0.85"},
                ),
            ],
        ),

        # ── Main content area ──
        html.Div(
            style={"display": "flex", "padding": "30px 40px", "gap": "30px", "maxWidth": "1400px", "margin": "0 auto",
                   "flexWrap": "wrap"},
            children=[
                # ── Left panel: Inputs ──
                html.Div(
                    style={"flex": "1", "minWidth": "320px", "maxWidth": "400px"},
                    children=[
                        # Cross-section card
                        html.Div(
                            style={**STYLE_CARD, "marginBottom": "20px"},
                            children=[
                                html.H4("Cross-Section", style=STYLE_SECTION_TITLE),
                                make_field("Height — h (mm)", dcc.Input(id="height", type="number", value=100, min=0.1, style=STYLE_INPUT)),
                                make_field("Width — w (mm)", dcc.Input(id="width", type="number", value=50, min=0.1, style=STYLE_INPUT)),
                                html.Div(
                                    style={"marginBottom": "14px"},
                                    children=[
                                        dcc.Checklist(
                                            id="solid-check",
                                            options=[{"label": "  Solid beam (no hollow core)", "value": "solid"}],
                                            value=[],
                                            style={"fontSize": "14px", "color": COLOR_TEXT, "accentColor": COLOR_PRIMARY},
                                            inputStyle={"marginRight": "6px", "transform": "scale(1.15)", "cursor": "pointer"},
                                            labelStyle={"cursor": "pointer", "fontWeight": "500"},
                                        ),
                                    ],
                                ),
                                make_field("Wall Thickness — t (mm)", dcc.Input(id="thickness", type="number", value=5, min=0.1, style=STYLE_INPUT)),
                            ],
                        ),

                        # Material card
                        html.Div(
                            style={**STYLE_CARD, "marginBottom": "20px"},
                            children=[
                                html.H4("Material", style=STYLE_SECTION_TITLE),
                                make_field(
                                    "Select material",
                                    dcc.Dropdown(
                                        id="material-dropdown",
                                        options=[{"label": m, "value": e} for m, e in MATERIALS.items()],
                                        value=210,
                                        clearable=False,
                                        style={"fontSize": "14px"},
                                    ),
                                ),
                                make_field("Modulus of Elasticity — E (GPa)", dcc.Input(id="modulus", type="number", value=210, min=0.1, style=STYLE_INPUT)),
                            ],
                        ),

                        # Beam geometry & loading card
                        html.Div(
                            style={**STYLE_CARD, "marginBottom": "20px"},
                            children=[
                                html.H4("Beam Geometry & Loading", style=STYLE_SECTION_TITLE),
                                make_field("Length — L (m)", dcc.Input(id="length", type="number", value=1, min=0.001, style=STYLE_INPUT)),
                                make_field("Force — F (N)", dcc.Input(id="force", type="number", value=1000, min=0, style=STYLE_INPUT)),
                            ],
                        ),

                        # Calculate button
                        html.Button(
                            "Calculate",
                            id="calc-btn",
                            n_clicks=0,
                            style={
                                "width": "100%",
                                "padding": "14px",
                                "fontSize": "16px",
                                "fontWeight": "700",
                                "backgroundColor": COLOR_PRIMARY,
                                "color": "white",
                                "border": "none",
                                "borderRadius": "12px",
                                "cursor": "pointer",
                                "letterSpacing": "0.02em",
                                "boxShadow": f"0 4px 14px rgba(79, 70, 229, 0.35)",
                                "transition": "all 0.2s ease",
                            },
                        ),
                    ],
                ),

                # ── Right panel: Results & Plot ──
                html.Div(
                    style={"flex": "2", "minWidth": "500px"},
                    children=[
                        # Results cards row
                        html.Div(
                            id="results",
                            style={"marginBottom": "24px"},
                            children=[
                                html.Div(
                                    style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "16px"},
                                    children=[
                                        _result_card("Reaction Force", "R_A", "—", COLOR_ACCENT_BLUE),
                                        _result_card("Max Moment", "M_max", "—", COLOR_ACCENT_AMBER),
                                        _result_card("Moment of Inertia", "I", "—", COLOR_ACCENT_GREEN),
                                        _result_card("Max Deflection", "delta_B", "—", COLOR_ACCENT_RED),
                                    ],
                                )
                            ] if False else [
                                html.Div(
                                    style={
                                        **STYLE_CARD,
                                        "textAlign": "center",
                                        "padding": "40px 24px",
                                        "color": COLOR_LABEL,
                                    },
                                    children=[
                                        html.P("Enter beam parameters and click Calculate to see results.",
                                               style={"margin": "0", "fontSize": "15px"}),
                                    ],
                                )
                            ],
                        ),

                        # Plot card
                        html.Div(
                            style=STYLE_CARD,
                            children=[dcc.Graph(id="deflection-plot", config={"displayModeBar": True, "displaylogo": False})],
                        ),
                    ],
                ),
            ],
        ),
    ],
)


def _result_card(title, symbol, value, accent_color):
    return html.Div(
        style={
            **STYLE_CARD,
            "borderLeft": f"4px solid {accent_color}",
            "padding": "18px 20px",
        },
        children=[
            html.P(title, style={"margin": "0 0 4px 0", "fontSize": "12px", "fontWeight": "600",
                                  "color": COLOR_LABEL, "textTransform": "uppercase", "letterSpacing": "0.04em"}),
            html.P(value, style={"margin": "0", "fontSize": "22px", "fontWeight": "700", "color": COLOR_TEXT}),
        ],
    )


# Disable wall thickness when solid is checked
@callback(Output("thickness", "disabled"), Input("solid-check", "value"))
def toggle_thickness(solid):
    return "solid" in solid


# Sync material dropdown -> modulus field
@callback(Output("modulus", "value"), Input("material-dropdown", "value"))
def sync_modulus(e_val):
    return e_val


# Main calculation
@callback(
    Output("results", "children"),
    Output("deflection-plot", "figure"),
    Input("calc-btn", "n_clicks"),
    State("height", "value"),
    State("width", "value"),
    State("solid-check", "value"),
    State("thickness", "value"),
    State("modulus", "value"),
    State("length", "value"),
    State("force", "value"),
)
def calculate(n_clicks, h_mm, w_mm, solid, t_mm, E_gpa, L, F):
    if n_clicks == 0:
        empty_fig = go.Figure()
        empty_fig.update_layout(
            template="plotly_white",
            height=460,
            margin=dict(t=40, b=40, l=60, r=30),
            xaxis_title="Position along beam x (m)",
            yaxis_title="Deflection (mm)",
            title="Beam Deflection Along Length",
            font=dict(family="Segoe UI, Inter, sans-serif"),
        )
        placeholder = html.Div(
            style={
                **STYLE_CARD,
                "textAlign": "center",
                "padding": "40px 24px",
                "color": COLOR_LABEL,
            },
            children=[
                html.P("Enter beam parameters and click Calculate to see results.",
                       style={"margin": "0", "fontSize": "15px"}),
            ],
        )
        return placeholder, empty_fig

    # Convert mm -> m
    h = h_mm / 1000
    w = w_mm / 1000
    t = t_mm / 1000 if t_mm else 0

    # Modulus: GPa -> Pa
    E = E_gpa * 1e9

    # Moment of inertia
    if "solid" in solid:
        I = (w * h**3) / 12
    else:
        I = (w * h**3 - (w - 2 * t) * (h - 2 * t) ** 3) / 12

    # Reaction force
    R_A = F

    # Maximum moment
    M_max = -F * L

    # Maximum deflection
    delta_B = (F * L**3) / (3 * E * I)

    # Deflection curve
    x = np.linspace(0, L, 500)
    delta_x = F * x**2 * (3 * L - x) / (6 * E * I)

    # Build result cards
    results = html.Div(
        style={"display": "grid", "gridTemplateColumns": "repeat(auto-fit, minmax(200px, 1fr))", "gap": "16px"},
        children=[
            _result_card("Reaction Force", "R_A", f"{R_A:,.2f} N", COLOR_ACCENT_BLUE),
            _result_card("Max Moment", "M_max", f"{M_max:,.2f} N\u00b7m", COLOR_ACCENT_AMBER),
            _result_card("Moment of Inertia", "I", f"{I:.4e} m\u2074", COLOR_ACCENT_GREEN),
            _result_card("Max Deflection", "\u03b4_B", f"{delta_B * 1000:.4f} mm", COLOR_ACCENT_RED),
        ],
    )

    # Build plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=delta_x * 1000, mode="lines", name="Deflection",
        line=dict(color=COLOR_PRIMARY, width=3),
        fill="tozeroy",
        fillcolor="rgba(79, 70, 229, 0.08)",
        hovertemplate="x = %{x:.3f} m<br>\u03b4 = %{y:.4f} mm<extra></extra>",
    ))
    fig.update_layout(
        title="Beam Deflection Along Length",
        xaxis_title="Position along beam x (m)",
        yaxis_title="Deflection \u03b4 (mm)",
        template="plotly_white",
        height=460,
        margin=dict(t=40, b=40, l=60, r=30),
        font=dict(family="Segoe UI, Inter, sans-serif", color=COLOR_TEXT),
        plot_bgcolor="white",
        hoverlabel=dict(bgcolor="white", font_size=13, bordercolor=COLOR_PRIMARY),
    )

    return results, fig


server = app.server

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run(host="0.0.0.0", port=port, debug=False)
