****Police-Secure-Smart-Traffic-Stop-Violation-Analytics-Dashboard**

**Overview**
Police-Secure-Smart-Traffic-Stop-Violation-Analytics-Dashboard is a Streamlit-based analytical web application for visualizing and predicting insights from police traffic stop data. It connects to a MySQL database and provides an interactive user interface for data exploration, analysis, and summary generation.

**Technologies Used (In VS code)**
- Python
- Streamlit
- MySQL (via pymysql)
- Pandas
- Plotly Express

**Functional Components**

**1. Database Connection**
- Establishes a connection to the MySQL database 'Digital_Ledger_db' using pymysql.
- Retrieves data from the table 'Digital_Ledger_data'.
- Utilizes Streamlit caching (@st.cache_resource and @st.cache_data) for efficient data retrieval.

**2. Dashboard Tab**
- Displays overall statistics:
  - Total Stops
  - Total Arrests
  - Drug-Related Stops
  - Unique Vehicles
- Visualizes violations using a bar chart.
- Lists the top 10 vehicle numbers involved in drug-related stops.

**3. Traffic Analysis Tab**
- Allows data filtering by country.
- Displays filtered metrics:
  - Filtered Stops
  - Filtered Arrests
  - Filtered Drug-Related Stops
  - Unique Vehicles
- Provides a pie chart visualization of violation distribution.

**4. Data Explorer / Advanced Insights Tab**
- Contains a predefined list of analytical SQL queries such as:
  - Top vehicles involved in drug-related stops
  - Arrest rate by driver age group
  - Gender and race distribution by country
  - Violations most associated with searches and arrests
  - Yearly and country-level breakdowns
- Displays query results in tabular format.
- Generates bar charts for queries with numeric results.

**5. New Log and Prediction Tab**
- Displays the full cleaned dataset.
- Provides a data entry form for adding or predicting new police stop logs.
- Searches for existing vehicle records in the dataset.
- Generates a summary text based on either dataset match or user input:
  - Violation type
  - Search conducted or not
  - Stop duration
  - Arrest and drug-related information

**6. Creator Information Tab**
- Displays developer details such as:
  - Name
  - Course
  - Batch
**User Interface and Styling**
- Custom CSS applied for:
  - Gradient background
  - Styled cards and buttons
  - Rounded edges and shadow effects
- Responsive layout with consistent visual hierarchy.

**Features Summary**
- Real-time database connectivity using pymysql.
- Interactive metrics and visualizations.
- Predefined analytical SQL queries.
- Vehicle-based search and prediction.
- Streamlit caching for improved performance.
- Clean and responsive design using custom CSS.
**
