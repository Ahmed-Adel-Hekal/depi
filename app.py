import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load available group CSV files from the current directory
group_files = [f for f in os.listdir() if f.endswith('.csv')]
group_names = [os.path.splitext(f)[0] for f in group_files]

# Sidebar for group selection with improved design
st.sidebar.title("🚀 Welcome to the Student Leaderboard!")
selected_group = st.sidebar.selectbox("📋 Choose Your Group", group_names)

# Function to calculate total points with error handling
def calculate_points(row):
    try:
        return row["Interaction"] * 1 + row["Quiz"] * 2 + row["Assignment"] * 3
    except KeyError as e:
        st.error(f"Column missing in the data: {e}")
        return 0

# Load the selected group's data from the CSV file
df = pd.read_csv(f"{selected_group}.csv")

# Ensure the correct columns are in the data
if all(col in df.columns for col in ["Interaction", "Quiz", "Assignment", "Student", "Gender"]):
    # Calculate total points for each student
    df["Total Points"] = df.apply(calculate_points, axis=1)
    df = df.sort_values(by="Total Points", ascending=False)

    # Display header with dynamic greeting
    st.markdown(f"<h1 style='text-align: center; color: #302883;'>🌟 Leaderboard for {selected_group} 🌟</h1>", unsafe_allow_html=True)

    # Top performer summary with background and text styling
    top_student = df.iloc[0]
    avg_score = df["Total Points"].mean()
    st.markdown(f"<div style='background-color: #e0c2d7; padding: 15px; border-radius: 10px; text-align: center; color: #2e205d;'>"
                f"<h2>🏆 Top Performer: {top_student['Student']} with {top_student['Total Points']} points!</h2>"
                f"<h3>📈 Average Group Score: {avg_score:.2f}</h3>"
                f"</div>", unsafe_allow_html=True)
    
    # Student progress section with redesigned color scheme
    st.subheader("🎯 Individual Progress")
    for index, row in df.iterrows():
        with st.container():
            cols = st.columns([3, 1])
            with cols[0]:
                # Custom style for top student
                if row['Student'] == top_student['Student']:
                    st.markdown(f"<h3 style='color: #ba547e;'>{row['Student']} ({row['Gender']}) - {row['Total Points']} points 🥇</h3>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<h3 style='color: #595f9f;'>{row['Student']} ({row['Gender']}) - {row['Total Points']} points</h3>", unsafe_allow_html=True)
                
                # Progress bar for visualizing points
                st.progress(row['Total Points'] / df["Total Points"].max())
                if row['Total Points'] > avg_score:
                    st.markdown("🥇 <span style='color: #7c9de7;'>Top Scorer</span>", unsafe_allow_html=True)
            
            # Collapsible points breakdown
            with cols[1], st.expander(f"🔍 Points Breakdown for {row['Student']}", expanded=False):
                st.write(f"**Interaction**: {row['Interaction']} points 💬")
                st.write(f"**Quiz**: {row['Quiz'] * 2} points 📝")
                st.write(f"**Assignment**: {row['Assignment'] * 3} points 📄")
                st.write("Keep up the great work! 💪🚀")

        # Divider for clarity between students
        st.markdown("---")

    # Gender Analysis - using the new color palette for the pie chart
    gender_analysis = df.groupby('Gender')['Total Points'].sum().reset_index()
    st.subheader("📊 Gender Points Analysis")
    fig, ax = plt.subplots()
    colors = ['#799cca', '#ba547e']  # Custom colors for the pie chart
    ax.pie(gender_analysis['Total Points'], labels=gender_analysis['Gender'], autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')
    st.pyplot(fig)

    # Final encouragement section with GIF
    st.markdown("### Keep pushing towards your goals! 🌈 Every point counts toward victory! 🚀")
    st.image("q.webp", caption="Great things take time, never give up!", use_column_width=True)

    # Custom background and text colors in the app using color palette
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(120deg, #e0c2d7, #302883);
            color: #2e205d;
        }
        h1, h2, h3 {
            font-family: 'Arial', sans-serif;
            color: #302883;
        }
        .css-1aumxhk, .css-18ni7ap {
            color: #2e205d;
        }
        .stButton>button {
            background-color: #76cced;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

else:
    st.error("CSV file is missing required columns. Please ensure it has 'Interaction', 'Quiz', 'Assignment', 'Student', and 'Gender'.")
