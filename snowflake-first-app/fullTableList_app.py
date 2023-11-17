import streamlit as st
from snowflake.snowpark import Session

# Set the page layout to wide
st.set_page_config(layout="wide")

st.title('❄️ Quick Access to Tables in Snowflake Warehouses')

# Establish Snowflake session
@st.cache_resource
def create_session():
    return Session.builder.configs(st.secrets.snowflake).create()

# Function to fetch schema names
@st.cache_data
def get_schema_names(database_name):
    query = f"SELECT SCHEMA_NAME FROM {database_name}.INFORMATION_SCHEMA.SCHEMATA"
    result = session.sql(query).collect()
    return [row[0] for row in result]

# Function to fetch table names
@st.cache_data
def get_table_names(database_name, schema_name):
    query = f"SELECT TABLE_NAME FROM {database_name}.INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '{schema_name}'"
    result = session.sql(query).collect()
    return [f"{database_name}.{schema_name}.{row[0]}" for row in result]

# Load data table
@st.cache_data
def load_data(full_table_name):
    st.write(f"Displaying data from `{full_table_name}`:")
    table = session.table(full_table_name)
    table = table.limit(100)  # Limiting to 100 rows
    table = table.collect()
    return table

# Create Snowflake session
session = create_session()
st.success("Connected to Snowflake!")

# Input field for database name
user_database_name = st.text_input("Enter the database name", "")

if user_database_name:
    # Fetch and display available schemas
    available_schemas = get_schema_names(user_database_name)
    selected_schema = st.selectbox("Select a schema", available_schemas)

    if selected_schema:
        # Fetch and display available tables based on selected schema
        available_tables = get_table_names(user_database_name, selected_schema)
        selected_table = st.selectbox("Select a table to display", available_tables)

        # Display data table
        with st.expander("See Table"):
            df = load_data(selected_table)
            st.dataframe(df)

            # # Optional: Writing out data
            # for row in df:
            #     st.write(f"{row[0]} has a :{row[1]}:")

else:
    st.warning("Please enter a database name to proceed.")
