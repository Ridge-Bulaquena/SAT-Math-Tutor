import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def calculate_performance_metrics(history):
    """Calculate student performance metrics"""
    df = pd.DataFrame(history)

    metrics = {
        "total_questions": len(df),
        "correct_answers": len(df[df["correct"] == True]),
        "accuracy": round(len(df[df["correct"] == True]) / len(df) * 100 if len(df) > 0 else 0, 2),
        "by_topic": df.groupby("topic")["correct"].mean().to_dict(),
        "by_difficulty": df.groupby("difficulty")["correct"].mean().to_dict()
    }

    return metrics

def create_progress_chart(history):
    """Create an animated progress chart using plotly"""
    df = pd.DataFrame(history)
    df["cumulative_accuracy"] = df["correct"].expanding().mean() * 100

    fig = go.Figure()

    # Add animated line trace
    fig.add_trace(
        go.Scatter(
            x=list(range(len(df))),
            y=df["cumulative_accuracy"],
            mode="lines+markers",
            name="Accuracy",
            line=dict(width=3, color="#1f77b4"),
            marker=dict(size=8, symbol="circle")
        )
    )

    # Add animation configuration
    fig.update_layout(
        title="Progress Over Time",
        xaxis_title="Questions Attempted",
        yaxis_title="Accuracy (%)",
        showlegend=False,
        hovermode="x unified",
        # Add animation settings
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [{
                "label": "Play Progress",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True,
                    "transition": {"duration": 300, "easing": "quadratic-in-out"}
                }]
            }]
        }]
    )

    return fig

def create_topic_performance_chart(history):
    """Create an animated topic-wise performance chart"""
    df = pd.DataFrame(history)
    topic_performance = df.groupby("topic")["correct"].agg(["count", "mean"]).reset_index()
    topic_performance["accuracy"] = topic_performance["mean"] * 100

    fig = go.Figure()

    # Add animated bar trace
    fig.add_trace(
        go.Bar(
            x=topic_performance["topic"],
            y=topic_performance["accuracy"],
            marker_color="#1f77b4",
            marker_line_color="#1f77b4",
            marker_line_width=1.5,
            opacity=0.8
        )
    )

    # Add animation configuration
    fig.update_layout(
        title="Performance by Topic",
        xaxis_title="Topic",
        yaxis_title="Accuracy (%)",
        showlegend=False,
        # Add animation settings
        updatemenus=[{
            "type": "buttons",
            "showactive": False,
            "buttons": [{
                "label": "Update Chart",
                "method": "animate",
                "args": [None, {
                    "frame": {"duration": 500, "redraw": True},
                    "fromcurrent": True,
                    "transition": {"duration": 300, "easing": "quadratic-in-out"}
                }]
            }]
        }]
    )

    return fig