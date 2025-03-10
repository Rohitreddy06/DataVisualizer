import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# --- USER AUTHENTICATION SETUP ---
USER_CREDENTIALS = {"admin": "password123", "user": "pass456"}  # Define valid usernames & passwords

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Login function
def login():
    st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='icon.png')

    st.title("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.success("Login successful!")
            st.experimental_rerun()  # Reload the page after login
        else:
            st.error("Invalid username or password.")

# Logout function
def logout():
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.experimental_rerun()

# --- LOGIN PAGE ---
if not st.session_state["authenticated"]:
    login()
    st.stop()  # Stop the app from proceeding unless logged in

# --- MAIN APP AFTER LOGIN ---
st.set_page_config(page_title='Data Visualizer', layout='centered', page_icon='icon.png')

st.sidebar.title(f"👤 Welcome, {st.session_state['user']}!")
if st.sidebar.button("Logout"):
    logout()

# --- DATA VISUALIZATION SECTION ---
st.title('Demographic Statistics Visualizer')

working_dir = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(working_dir, "data")

if not os.path.exists(folder_path):
    os.makedirs(folder_path)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully!")
else:
    if not files:
        st.warning("No CSV files found in the data folder. Please upload a file.")
        st.stop()
    selected_file = st.selectbox('Select a file', files, index=None)
    if selected_file:
        file_path = os.path.join(folder_path, selected_file)
        df = pd.read_csv(file_path)

st.write("### Preview of Data")
st.write(df.head())

columns = df.columns.tolist()
x_axis = st.selectbox('Select the X-axis', options=["None"] + columns)
y_axis = st.selectbox('Select the Y-axis', options=["None"] + columns)

plot_list = ['Line Plot', 'Bar Chart', 'Scatter Plot', 'Distribution Plot', 'Count Plot']
plot_type = st.selectbox('Select the type of plot', options=plot_list)

if st.button('Generate Plot'):
    if x_axis == "None":
        st.error("Please select a valid X-axis variable.")
    elif plot_type in ["Line Plot", "Bar Chart", "Scatter Plot"] and y_axis == "None":
        st.error("Please select a valid Y-axis variable for this plot.")
    else:
        fig, ax = plt.subplots(figsize=(6, 4))

        if plot_type == 'Line Plot':
            sns.lineplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Bar Chart':
            sns.barplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Scatter Plot':
            sns.scatterplot(x=df[x_axis], y=df[y_axis], ax=ax)
        elif plot_type == 'Distribution Plot':
            sns.histplot(df[x_axis], kde=True, ax=ax)
            ax.set_ylabel("Density")
        elif plot_type == 'Count Plot':
            sns.countplot(x=df[x_axis], ax=ax)
            ax.set_ylabel("Count")

        ax.tick_params(axis='x', labelsize=10)
        ax.tick_params(axis='y', labelsize=10)
        ax.set_title(f'{plot_type} of {y_axis} vs {x_axis}', fontsize=12)
        ax.set_xlabel(x_axis, fontsize=10)

        st.pyplot(fig)
