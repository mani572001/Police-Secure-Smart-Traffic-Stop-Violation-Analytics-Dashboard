🚔 Police-Secure-Smart-Traffic-Stop-Violation-Analytics-Dashboard
📘 Overview

Police-Secure-Smart-Traffic-Stop-Violation-Analytics-Dashboard is a Streamlit-based web application designed to visualize, analyze, and predict insights from police traffic stop data. It integrates with a MySQL database to fetch real-time data and provides an interactive user interface for exploration, analysis, and prediction.

⚙️ Technologies Used

Python

Streamlit – Web application framework

MySQL (pymysql) – Database connection and querying

Pandas – Data manipulation and analysis

Plotly Express – Interactive data visualization

🧩 Key Functional Components
1. Database Connection

Uses pymysql to establish a connection with a MySQL database named Digital_Ledger_db.

Data is fetched from the table Digital_Ledger_data.

Implements caching with @st.cache_resource and @st.cache_data for optimized performance.

2. Dashboard Tab (🏠)

Displays key traffic statistics:

Total Stops

Total Arrests

Drug-Related Stops

Unique Vehicles

Visualizes violation frequency using an interactive bar chart.

Lists top 10 vehicle numbers involved in drug-related stops.

3. Traffic Analysis Tab (📊)

Allows filtering data by country.

Shows filtered metrics such as:

Filtered Stops

Filtered Arrests

Drug-Related Stops

Unique Vehicles

Displays violation distribution using a pie chart.

4. Data Explorer / Advanced Insights Tab (💻)

Provides an interactive SQL Query Explorer with multiple predefined analytical queries, including:

Top vehicles in drug-related stops

Arrest rate by driver age group

Gender and race distributions

Violations linked to searches and arrests

Yearly and country-level breakdowns

Displays query results in tables with optional bar charts for numeric data.

5. New Log & Prediction Tab (🚔)

Enables users to view the complete dataset within the app.

Provides a form to add or predict a new police stop log.

Automatically matches entered vehicle numbers with existing records.

Displays a prediction summary describing the stop outcome in natural language, including:

Violation

Search status

Stop duration

Arrest and drug-related status

6. Creator Info Tab (👨‍💻)

Displays developer information including name, course, and batch details.

🎨 UI & Styling

Custom CSS integrated directly into Streamlit for:

Gradient background

Styled cards and metrics

Rounded and shadowed buttons

Consistent and responsive design optimized for dashboard presentation.

📊 Features Summary
Feature	Description
Database Integration	Real-time MySQL connection using pymysql
Interactive Dashboard	Metrics, bar, and pie charts for quick insights
Query Execution	Predefined analytical SQL queries
Search & Prediction	Vehicle-based log lookup and text summary
Caching	Streamlit cache for faster query response
Responsive Design	Clean UI with custom CSS styling
