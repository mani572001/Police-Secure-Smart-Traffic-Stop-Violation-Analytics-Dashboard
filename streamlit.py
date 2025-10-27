## %%writefile app.py
import streamlit as st
import pymysql
import pandas as pd
import plotly.express as px

# ====================== STYLING ======================
st.set_page_config(page_title="SecureCheck Dashboard", layout="wide")
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #e0f7fa, #b2ebf2);
    color: #1b1b2f;
}
h1, h2, h3, h4 {
    color: #1b1b2f;
}
.card {
    background: #ffffff;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 3px 3px 10px rgba(0,0,0,0.1);
}
.stButton>button {
    background-color: #00bcd4;
    color: white;
    border-radius: 10px;
    height: 3em;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ====================== DATABASE CONNECTION ======================
@st.cache_resource
def get_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="572001",
        database="Digital_Ledger_db"
    )

conn = get_connection()

# ====================== HELPER FUNCTION ======================
@st.cache_data
def fetch_data(query):
    df = pd.read_sql(query, conn)
    return df

# ====================== TOP NAVIGATION ======================
tabs = [
    "🏠 Dashboard",
    "📊 Traffic Analysis",
    "💻 Data Explorer",
    "🚔 New Log & Prediction",
    "👨‍💻 Creator Info"
]
selected_tab = st.tabs(tabs)
dashboard_tab, traffic_tab, sql_tab, newlog_tab, creator_tab = selected_tab

# ====================== DASHBOARD TAB ======================
with dashboard_tab:
    st.title("🚓 SecureCheck Dashboard")
    st.markdown("Real-time insights into traffic stops and violations")

    df = fetch_data("SELECT * FROM Digital_Ledger_data")

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Stops", len(df))
    col2.metric("Total Arrests", df['is_arrested'].sum())
    col3.metric("Drug-Related Stops", df['drugs_related_stop'].sum())
    col4.metric("Unique Vehicles", df['vehicle_number'].nunique())

    # Chart
    st.subheader("🚨 Stops by Violation")
    violation_count = df['violation'].value_counts().reset_index()
    violation_count.columns = ['Violation', 'Count']
    fig1 = px.bar(violation_count, x='Violation', y='Count', text='Count', color='Count', color_continuous_scale='Teal')
    st.plotly_chart(fig1, use_container_width=True)

    # Table
    st.subheader("🚗 Top Vehicle Numbers (Drug-Related)")
    top_vehicle = df[df['drugs_related_stop']==1]['vehicle_number'].value_counts().head(10)
    st.table(top_vehicle.reset_index().rename(columns={'index':'Vehicle Number', 'vehicle_number':'Count'}))

# ====================== TRAFFIC ANALYSIS TAB ======================
with traffic_tab:
    st.title("📊 Traffic Violation Visualization")

    countries = ["All"] + df['country_name'].dropna().unique().tolist()
    country = st.selectbox("Filter by Country", countries, key="country_filter")
    
    df_filtered = df.copy()
    if country != "All":
        df_filtered = df_filtered[df_filtered['country_name'] == country]

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Filtered Stops", len(df_filtered))
    col2.metric("Filtered Arrests", df_filtered['is_arrested'].sum())
    col3.metric("Filtered Drug-Related", df_filtered['drugs_related_stop'].sum())
    col4.metric("Unique Vehicles", df_filtered['vehicle_number'].nunique())

    # Visualization
    st.subheader("Stops by Violation")
    violation_count = df_filtered['violation'].value_counts().reset_index()
    violation_count.columns = ['Violation', 'Count']
    fig3 = px.pie(violation_count, names='Violation', values='Count', title="Violation Distribution")
    st.plotly_chart(fig3, use_container_width=True)

# ====================== SQL QUERIES TAB ======================
with sql_tab:
    st.title("💻 ADVANCED INSIGHTS")
    queries_list = [
        "Top 10 vehicle_Number involved in drug-related stops",
        "Vehicles most frequently searched",
        "Driver age group with highest arrest rate",
        "Gender distribution by country",
        "Race & gender with highest search rate",
        "Average stop duration by violation",
        "Stops during night vs arrests",
        "Violations most associated with searches/arrests",
        "Violations common among younger drivers (<25)",
        "Rare violations with few searches/arrests",
        "Top highest countries (drug-related stops)",
        "Arrest rate by country & violation",
        "Country with most searches",
        "Yearly breakdown of stops & arrests",
        "Driver violation trends by age & race",
        "Stop pattern by year, month, hour",
        "Top 10 violations by arrest rate",
        "Driver demographics by country"
    ]

    query_map = {
        "Top 10 vehicle_Number involved in drug-related stops": """
            SELECT vehicle_number 
            FROM Digital_Ledger_data 
            WHERE drugs_related_stop = TRUE 
            LIMIT 10;
        """,
        "Vehicles most frequently searched": """
            SELECT vehicle_number, COUNT(*) AS search_count 
            FROM digital_ledger_data 
            GROUP BY vehicle_number 
            ORDER BY search_count DESC 
            LIMIT 10;
        """,
        "Driver age group with highest arrest rate": """
            SELECT age_group, COUNT(*) AS total_stops, SUM(is_arrested) AS total_arrests,
                   ROUND(SUM(is_arrested)/COUNT(*)*100,2) AS arrest_rate_percent
            FROM (
                SELECT *,
                    CASE 
                        WHEN driver_age < 25 THEN 'Under 25'
                        WHEN driver_age BETWEEN 25 AND 40 THEN '25-40'
                        WHEN driver_age BETWEEN 41 AND 60 THEN '41-60'
                        ELSE '60+' 
                    END AS age_group
                FROM Digital_Ledger_data
            ) AS age_groups
            GROUP BY age_group
            ORDER BY arrest_rate_percent DESC
            LIMIT 1;
        """,
        "Gender distribution by country": """
            SELECT country_name, driver_gender, COUNT(*) AS total_stops 
            FROM digital_ledger_data 
            GROUP BY country_name, driver_gender 
            ORDER BY country_name, total_stops DESC;
        """,
        "Race & gender with highest search rate": """
            SELECT driver_race, driver_gender, COUNT(*) AS Count1 
            FROM digital_ledger_data 
            WHERE search_conducted=TRUE 
            GROUP BY driver_race, driver_gender 
            ORDER BY Count1 DESC 
            LIMIT 1;
        """,
        "Average stop duration by violation": """
            SELECT violation, AVG(CAST(stop_duration AS SIGNED)) AS avg_stop_duration, COUNT(*) AS total_stops 
            FROM digital_ledger_data 
            GROUP BY violation 
            ORDER BY avg_stop_duration DESC;
        """,
        "Stops during night vs arrests": """
            SELECT CASE 
                    WHEN HOUR(stop_time) BETWEEN 20 AND 23 THEN 'Night'
                    WHEN HOUR(stop_time) BETWEEN 0 AND 4 THEN 'Late Night'
                    ELSE 'Daytime'
                END AS time_period,
                COUNT(*) AS total_stops,
                SUM(CASE WHEN is_arrested=TRUE THEN 1 ELSE 0 END) AS arrests,
                ROUND(SUM(CASE WHEN is_arrested=TRUE THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate_percent
            FROM digital_ledger_data
            GROUP BY time_period
            ORDER BY arrest_rate_percent DESC;
        """,
        "Violations most associated with searches/arrests": """
            SELECT violation, COUNT(*) AS hg 
            FROM digital_ledger_data 
            WHERE search_conducted=TRUE OR is_arrested=TRUE 
            GROUP BY violation 
            ORDER BY hg DESC 
            LIMIT 3;
        """,
        "Violations common among younger drivers (<25)": """
            SELECT violation, COUNT(*) AS aba 
            FROM digital_ledger_data 
            WHERE driver_age<25 
            GROUP BY violation 
            ORDER BY aba DESC 
            LIMIT 1;
        """,
        "Rare violations with few searches/arrests": """
            SELECT violation, COUNT(*) AS aba 
            FROM digital_ledger_data 
            WHERE search_conducted=TRUE OR is_arrested=TRUE 
            GROUP BY violation 
            HAVING aba<10 
            ORDER BY aba 
            LIMIT 1;
        """,
        "Top highest countries (drug-related stops)": """
            SELECT country_name, COUNT(*) AS ds 
            FROM digital_ledger_data 
            WHERE drugs_related_stop=TRUE 
            GROUP BY country_name 
            ORDER BY ds DESC 
            LIMIT 5;
        """,
        "Arrest rate by country & violation": """
            SELECT country_name, violation,
                   SUM(CASE WHEN is_arrested=TRUE THEN 1 ELSE 0 END) AS arrest_count,
                   COUNT(*) AS total_count,
                   ROUND(SUM(CASE WHEN is_arrested=TRUE THEN 1 ELSE 0 END)/COUNT(*)*100,2) AS arrest_rate_percent
            FROM digital_ledger_data
            GROUP BY country_name, violation
            ORDER BY arrest_rate_percent DESC
            LIMIT 5;
        """,
        "Country with most searches": """
            SELECT country_name, COUNT(*) AS df 
            FROM digital_ledger_data 
            WHERE search_conducted=TRUE 
            GROUP BY country_name 
            ORDER BY df DESC 
            LIMIT 1;
        """,
        "Yearly breakdown of stops & arrests": """
            SELECT country_name, YEAR(stop_time) AS year, COUNT(*) AS total_stops, SUM(is_arrested) AS total_arrests 
            FROM digital_ledger_data 
            GROUP BY country_name, year 
            ORDER BY country_name, year;
        """,
        "Driver violation trends by age & race": """
            SELECT CASE 
                        WHEN driver_age<25 THEN 'Under 25' 
                        WHEN driver_age BETWEEN 25 AND 40 THEN '25-40' 
                        WHEN driver_age BETWEEN 41 AND 60 THEN '41-60' 
                        ELSE '60+' 
                   END AS age_group,
                   driver_race, violation, COUNT(*) AS total 
            FROM digital_ledger_data 
            GROUP BY age_group, driver_race, violation 
            ORDER BY age_group, driver_race, total DESC;
        """,
        "Stop pattern by year, month, hour": """
            SELECT YEAR(stop_time) AS year, MONTH(stop_time) AS month, HOUR(stop_time) AS hour, COUNT(*) AS total_stops 
            FROM digital_ledger_data 
            GROUP BY year, month, hour 
            ORDER BY year, month, hour;
        """,
        "Top 10 violations by arrest rate": """
            SELECT violation, COUNT(*) AS total_stops, SUM(is_arrested) AS total_arrests, 
                   ROUND(100*SUM(is_arrested)/COUNT(*),2) AS arrest_rate 
            FROM digital_ledger_data 
            GROUP BY violation 
            ORDER BY arrest_rate DESC 
            LIMIT 10;
        """,
        "Driver demographics by country": """
            SELECT country_name, ROUND(AVG(driver_age),1) AS avg_age, 
                   COUNT(DISTINCT driver_gender) AS gender_diversity, 
                   COUNT(DISTINCT driver_race) AS race_diversity, 
                   COUNT(*) AS total_drivers 
            FROM digital_ledger_data 
            GROUP BY country_name 
            ORDER BY total_drivers DESC;
        """
    }

    selected_query = st.selectbox("Select a Query", queries_list)

    if st.button("Run Query"):
        df_result = fetch_data(query_map[selected_query])
        if not df_result.empty:
            st.write(df_result)
            numeric_cols = df_result.select_dtypes(include='number').columns
            if len(numeric_cols) > 0:
                st.bar_chart(df_result.set_index(df_result.columns[0])[numeric_cols[0]])
            else:
                st.info("No numeric data to plot for this query.")
        else:
            st.warning("No results found for this query.")

# ====================== NEW LOG & PREDICTION TAB ======================
with newlog_tab:
    st.markdown("""
    <div class="card">
        <h2 style='text-align:center;'>🚔 Add New Police Log & Predict Outcome and Violation</h2>
    </div>
    """, unsafe_allow_html=True)

    # --- Show full cleaned dataset with scroll ---
    st.markdown("### 📋 View Full Cleaned Dataset")
    st.dataframe(df, use_container_width=True, height=400)

    st.markdown("---")
    st.markdown("<div class='card'><h4>🔎 Search & Predict</h4></div>", unsafe_allow_html=True)

    # --- User input form (manual typing for all fields) ---
    with st.form("new_log_form"):
        col1, col2 = st.columns(2)

        with col1:
            stop_date = st.text_input("📅 Stop Date (e.g., 2025-10-27)")
            stop_time = st.text_input("⏰ Stop Time (e.g., 2:30 PM)")
            country_name = st.text_input("🌍 Country Name (optional)")
            driver_gender = st.text_input("🚻 Driver Gender (Male/Female/Other)")
            driver_age = st.number_input("🎯 Driver Age", min_value=16, max_value=100,)
            driver_race = st.text_input("🏁 Driver Race")
            is_arrested = st.text_input("🚨 Was the Driver Arrested? (Yes/No)")

        with col2:
            search_conducted = st.text_input("🔍 Was a Search Conducted? (Yes/No)")
            search_type = st.text_input("🔎 Search Type (if any)")
            stop_duration = st.text_input("⏱ Stop Duration (e.g., 6-15 min)")
            drugs_related_stop = st.text_input("💊 Was it Drug Related? (Yes/No)")
            violation = st.text_input("⚠️ Violation (e.g., Speeding)")
            stop_outcome = st.text_input("📄 Stop Outcome (e.g., Citation, Warning)")
            vehicle_number = st.text_input("🚗 Vehicle Number")

        submitted = st.form_submit_button("🚨 Predict Stop Outcome & Violation")

    # --- When user submits ---
    if submitted:
        try:
            # Search for vehicle number in dataset
            match = df[df['vehicle_number'].astype(str).str.contains(vehicle_number, case=False, na=False)]

            if not match.empty:
                # Use the first match
                record = match.iloc[0]

                driver_gender_val = record.get('driver_gender', 'Unknown')
                driver_age_val = record.get('driver_age', 'Unknown')
                violation_val = record.get('violation', 'Unknown')
                stop_time_val = record.get('stop_time', 'Unknown')
                search_conducted_val = record.get('search_conducted', False)
                stop_outcome_val = record.get('stop_outcome', 'Unknown')
                stop_duration_val = record.get('stop_duration', 'Unknown')
                drugs_related_val = record.get('drugs_related_stop', False)

                # Text conversion
                search_text = "A search was conducted" if search_conducted_val in [True, "True", "Yes", "yes"] else "No search was conducted"
                drug_text = "was drug-related" if drugs_related_val in [True, "True", "Yes", "yes"] else "was not drug-related"
                pronoun = "he" if str(driver_gender_val).lower() == "male" else "she"

                # --- Prediction Summary ---
                st.markdown(f"""
                    <div class='card' style='background:#e0f7fa;padding:15px;border-radius:10px;'>
                        <h3 style='text-align:center;'>🧠 Prediction Summary</h3>
                        <p style='font-size:16px;'>
                            🚗 A {driver_age_val}-year-old {driver_gender_val} driver was stopped for <b>{violation_val}</b> at <b>{stop_time_val}</b>.<br>
                            {search_text}, and {pronoun} received a <b>{stop_outcome_val}</b>.<br>
                            The stop lasted <b>{stop_duration_val}</b> and {drug_text}.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

                st.success(f"✅ Record found for vehicle number: {vehicle_number}")
                st.dataframe(match)

            else:
                # No match found → use manual inputs for prediction
                search_text = "A search was conducted" if search_conducted.lower() == "yes" else "No search was conducted"
                drug_text = "was drug-related" if drugs_related_stop.lower() == "yes" else "was not drug-related"
                pronoun = "he" if driver_gender.lower() == "male" else "she"

                st.warning("⚠️ No matching records found in dataset. Showing based on your inputs.")

                st.markdown(f"""
                    <div class='card' style='background:#fff3cd;padding:15px;border-radius:10px;'>
                        <h3 style='text-align:center;'>🧠 Predicted Summary</h3>
                        <p style='font-size:16px;'>
                            🚗 A {driver_age}-year-old {driver_gender} driver was stopped for <b>{violation}</b> at <b>{stop_time}</b>.<br>
                            {search_text}, and {pronoun} received a <b>{stop_outcome}</b>.<br>
                            The stop lasted <b>{stop_duration}</b> and {drug_text}.
                        </p>
                    </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error in prediction: {e}")
            st.info("Please check your dataset columns and formats.")

# ====================== CREATOR INFO TAB ======================
with creator_tab:
    st.title("👨‍💻 Creator Info")
    st.write("**Name:** Manikandan")
    st.write("**Course:** Data Science - GUVI")
    st.write("**Batch:** DS-S-WD-T-B91")