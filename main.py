import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="CSV Visualizer", layout="wide")
st.title("🚀 CSV Visualizer")

# DEMO DATAFRAME (fake sample data)
demo_df = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=10, freq="D"),
    "Sales": [150, 200, 250, 180, 220, 270, 300, 320, 310, 400],
    "Profit": [50, 70, 90, 60, 80, 100, 120, 130, 125, 150],
    "Category": ["Food", "Tech", "Food", "Tech", "Clothing", "Clothing", "Food", "Tech", "Clothing", "Food"],
    "Country": ["USA", "USA", "UK", "Germany", "Germany", "UK", "USA", "Germany", "UK", "USA"]
})

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

# Initialize session state
if "show_demo" not in st.session_state:
    st.session_state.show_demo = False

# Demo button as toggle
if st.button("Show Demo Example"):
    st.session_state.show_demo = True

# LOAD DATA
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ File successfully loaded.")
    st.session_state.show_demo = False  # Reset demo mode if real file uploaded
elif st.session_state.show_demo:
    df = demo_df.copy()
    st.info("ℹ️ Showing demo example data.")
else:
    df = None

# == MAIN LOGIC ==
if df is not None:
    # Filters
    if "Category" in df.columns:
        selected_category = st.selectbox("Filter by Category:", ["All"] + df["Category"].unique().tolist())
        if selected_category != "All":
            df = df[df["Category"] == selected_category]

    if "Country" in df.columns:
        selected_country = st.selectbox("Filter by Country:", ["All"] + df["Country"].unique().tolist())
        if selected_country != "All":
            df = df[df["Country"] == selected_country]

    # Show dataframe
    st.write("### DataFrame preview")
    st.write(df)

    # Data summary
    st.subheader("Dataset Information")
    st.write(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    st.write("Missing values per column:")
    st.write(df.isnull().sum())
    st.write("Data types:")
    st.write(df.dtypes)

    # Sorting
    sort_column = st.selectbox("Select column to sort by:", df.columns)
    df_sorted = df.sort_values(by=sort_column, ascending=False)
    st.write("### Sorted DataFrame")
    st.write(df_sorted)

    # Chart selector
    chart_type = st.selectbox(
        "Choose a chart type",
        ["-- Choose a chart --", "Bar chart", "Line chart", "Scatter plot", "Histogram", "Heatmap"]
    )

    if chart_type != "-- Choose a chart --":
        st.write(f"### {chart_type}")

        if chart_type in ["Bar chart", "Line chart", "Scatter plot"]:
            col_x = st.selectbox("Select X column:", df.columns)
            col_y = st.selectbox("Select Y column:", df.select_dtypes(include=["number"]).columns)

            if chart_type == "Bar chart":
                fig = px.bar(df, x=col_x, y=col_y)
            elif chart_type == "Line chart":
                fig = px.line(df, x=col_x, y=col_y)
            elif chart_type == "Scatter plot":
                fig = px.scatter(df, x=col_x, y=col_y)

            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Histogram":
            col = st.selectbox("Select column for histogram:", df.select_dtypes(include=["number"]).columns)
            fig = px.histogram(df, x=col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Heatmap":
            numeric_cols = df.select_dtypes(include=["number"])
            fig = px.imshow(numeric_cols.corr(), text_auto=True)
            st.plotly_chart(fig, use_container_width=True)

    # Download button
    st.download_button(
        label="Download filtered dataset as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="filtered_dataset.csv",
        mime="text/csv"
    )
