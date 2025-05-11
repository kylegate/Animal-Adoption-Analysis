### EXAMPLE ***

'''


*** Goals:
Columns:
DOB
Time in Shelter
Breed
Coloring
Sex
Animal Type
Intake & Outcome Age
Intake & Outcome Type
Intake & Outcome Date
Location

Intake Condition ?


'''

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd

# Data Preprocessing
df = pd.read_csv('Student_performance_data _.csv')

df['Tutoring'] = df['Tutoring'].map({0: "No Tutor", 1: "Has Tutor"})

df['Extracurricular'] = df['Extracurricular'].map(
    {0: "Participation in Extracurricular", 1: "No Participation in Extracurricular"}
)

df['ParentalSupport'] = df['ParentalSupport'].map({0: 'None', 1: 'Low', 2: 'Moderate', 3: 'High', 4: 'Very High'})
df['ParentalSupport'] = df['ParentalSupport'].astype('category')

bins = [0, 5, 10, 15, 20, 25, 30]
labels = ["0-5 Days", "5-10 Days", "10-15 Days", "15-20 Days", "20-25 Days", "25-30 Days"]
df["Absent_Range"] = pd.cut(df["Absences"], bins=bins, labels=labels, right=False)

bins = [0, 2.0, 2.5, 3.0, 3.5, 4.0]
labels = ['F', 'D', 'C', 'B', 'A']
df['GPA_Category'] = pd.cut(df['GPA'], bins=bins, labels=labels, right=False)

app = Dash(__name__)
app.title = "Dashboard"

# Specific Dataframe creation
extra_involve_df = df[['Age','Extracurricular']]
gpa_parental_df = df[['ParentalSupport','GPA']]
studyTime_gradeRank_df = df[["StudyTimeWeekly","GPA_Category"]]
gpa_tutor_df = df[['GPA','Tutoring']]

# Dash Creation
app.layout = html.Div([
    html.Div([
        html.H2("Students with Extracurricular Involvement"),
        dcc.Graph(
            figure=px.histogram(
                extra_involve_df,
                x="Age",
                title="Age Groups by Extracurricular Involvement",
                color="Extracurricular",
            )
            .update_layout(
                title_font_size=24,
                plot_bgcolor="LightGoldenRodYellow",
                bargap = 0.1,
                bargroupgap = 0.05,
                yaxis=dict(
                    title="Count",
                    tickfont=dict(size=16),
                ),
                xaxis=dict(
                    title="Age Group",
                    tickfont=dict(size=16),

                )
            ))
    ]),

    html.Div([
        html.H2("Boxplot of GPA By Parental Support"),
        dcc.Graph(figure=px.box(
            gpa_parental_df,
            x="ParentalSupport",
            y="GPA",
            title="GPA By Parental Support",
            color='ParentalSupport',
            category_orders={"ParentalSupport": ["None", "Low", "Moderate", "High", "Very High"]}
        )
              .update_layout(
                title_font_size=24,
                autosize=True,
                yaxis = dict(
                    title="GPA",
                    tickfont=dict(size=20),
                ),
                xaxis = dict(
                    title="Parental Support",
                    tickfont=dict(size=20),
                )
        ))
    ]),


    html.Div([
        html.H2("Study Time Weekly by Grade Ranking"),
        dcc.Graph(
            figure=px.violin(
                studyTime_gradeRank_df,
                y="StudyTimeWeekly",
                x="GPA_Category",
                box=True,
                title="Study Time of Grade Distribution",
                category_orders={"GPA_Category": ['A', 'B', 'C', 'D', 'F']}
            )
            .update_layout(
                title_font_size=24,
                plot_bgcolor="Pink",
                autosize=True,
            )
        )
    ]),

    html.Div([
        html.H2("GPA Distribution by Tutor Status"),
        dcc.Graph(
            figure=px.box(
                gpa_tutor_df,
                y="GPA",
                title="GPA vs Tutor Status",
                color="Tutoring",
                labels={"Tutoring": "Tutor Status", "GPA": "GPA"}
            )
            .update_layout(
                title_font_size=24,
                plot_bgcolor="MistyRose",
                autosize=True,
            )
        ),
    ]),

    html.Div([
        html.H2("GPA by Parental Support"),
        dcc.Checklist(
            id="ParentalSupport-checklist",
            options=[
                {"label": str(parent_sup), "value": str(parent_sup)} for parent_sup in df["ParentalSupport"].cat.categories
            ],
            value=df["ParentalSupport"].cat.categories,
            inline=True,
        ),
        dcc.Graph(id="ParentalSupport-histogram")
    ]),


    html.Div([
        html.H2("GPA by Absence Range"),
        dcc.Dropdown(
            id="Absent-GPA-dropdown",
            options=[{"label": str(absent), "value": str(absent)} for absent in df["Absent_Range"].cat.categories],
            value=str(df["Absent_Range"].cat.categories[0]),
        ),
        dcc.Graph(id="Absent-GPA-histogram")
    ]),

    html.Div([
        html.H2("GPA by Study Time (Weekly)"),
        dcc.RangeSlider(
            id="study-time-slider",
            min=df["GPA"].min(),
            max=df["GPA"].max(),
            step=0.1,
            marks={i: str(i) for i in range(int(df["GPA"].min()), int(df["GPA"].max()) + 1)},
            value=[df["GPA"].min(), df["GPA"].max()]
        ),
        dcc.Graph(id="study-time-chart")
    ]),

    html.Div([
        html.H2("Study Time (Weekly) by GPA minimum"),
        dcc.Input(
            id="GPA-text-input",
            type="number",
            placeholder="Enter a minimum GPA"
        ),
        dcc.Graph(id="GPA-scatter")
    ])

])

@app.callback(
    Output("Absent-GPA-histogram", "figure"),
    Input("Absent-GPA-dropdown", "value")
)
def update_Absent_vs_GPA_histogram(filter_category):
    filtered_df = df[df["Absent_Range"] == filter_category]  # filter df based on desired category

    fig = px.histogram(
        filtered_df,
        x="GPA",
        title=f"GPA by Absences {filter_category}"
    )
    fig.update_layout(
        yaxis=dict(title="Count"),
        xaxis=dict(title="GPA", range=[0, 4.0]),
        title_font_size=24,
        plot_bgcolor="lightgray",
    )
    fig.update_traces(
        marker=dict(
            line=dict(color="black", width=2)
        )
    )
    return fig

@app.callback(
    Output("study-time-chart", "figure"),
    Input("study-time-slider", "value")
)
def update_study_time_vs_GPA_heatmap(GPA_Range):
    filtered_df = df[
        (df["GPA"] >= GPA_Range[0]) &
        (df["GPA"] <= GPA_Range[1])
        ]
    fig = px.density_heatmap(
        filtered_df,
        y="StudyTimeWeekly",
        x="GPA",
        title="Study Time Weekly vs GPA"
    )
    fig.update_layout(
        xaxis=dict(
            title="GPA"
        ),
        yaxis=dict(
            title="Study Time (Weekly)"
        ),
        title_font_size=24,
    )
    return fig
    return fig

@app.callback(
    Output("GPA-scatter", "figure"),
    Input("GPA-text-input", "value")
)
def update_GPA_vs_StudyTime_scatter(GPA):
    if GPA is None:
        fig = px.scatter(
            df,
            x="StudyTimeWeekly",
            y="GPA",
            color="GPA_Category",
            title="GPA vs StudyTimeWeekly",
            category_orders = {"GPA_Category": ["A", "B", "C", "D", "F"]}
        )
        fig.update_layout(
            xaxis=dict(
                title="Study Time (Weekly)"
            ),
            yaxis=dict(
                title="GPA"
            ),
            title_font_size=24,
            plot_bgcolor="Gainsboro",
            legend_title="Letter Grade"
        )
        return fig

    GPA = float(GPA)
    filtered_df = df[df["GPA"] >= GPA]
    fig = px.scatter(
        filtered_df,
        x="StudyTimeWeekly",
        y="GPA",
        color="GPA_Category",
        title=f"GPA vs StudyTimeWeekly: {GPA}",
        category_orders = {"GPA_Category": ["A", "B", "C", "D", "F"]}
    )
    fig.update_layout(
        xaxis=dict(
            range=[0, 40],
            title="Study Time (Weekly)"
        ),
        yaxis=dict(
            range=[0, 4.0],
            title="GPA"
        ),
        title_font_size=24,
        plot_bgcolor="Gainsboro",
        legend_title="Letter Grade"
    )
    return fig

@app.callback(
    Output("ParentalSupport-histogram", "figure"),
    Input("ParentalSupport-checklist", "value")
)
def update_parental_support_histogram(support_levels):
    filtered_df = df[df["ParentalSupport"].isin(support_levels)]
    fig = px.histogram(
        filtered_df,
        x="GPA",
        title="GPA Distribution by Parental Support",
        color="ParentalSupport",
        category_orders={"ParentalSupport": ["None", "Low", "Moderate", "High", "Very High"]}
    )
    fig.update_layout(
        xaxis=dict(range=[0, 4.0], title='GPA'),
        yaxis=dict(range=[0, 40], title='Study Time (Weekly)'),
        title_font_size=24,
        plot_bgcolor="LemonChiffon"
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
