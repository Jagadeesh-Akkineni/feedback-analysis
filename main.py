import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Define updated keywords to search for in bot messages
keywords = [
    "Adhesion", "Bleeding", "Blocking", "Bridging", "Colour Strength", "Colour variation per job",
    "Colour variations across width", "Comet tails", "Density", "Dirty Printing", "Dot gain", 
    "Feathering", "Fill-in of Reverses and Type", "Foaming", "Ghosting", "Halo", "Ink drying too fast",
    "Ink Drying too slowly", "Kick-Out", "Longitudinal stripes", "Misregister", "Missing Print", "Moiré", 
    "Mottling", "Picking", "Pinholes/Fisheyes", "Poor mileage performance", "Pressure - Anilox", 
    "Pressure - Print", "Set-off", "Settling of Ink", "Shade Variation", "Sheet Feeding Problem", 
    "Slur", "Smearing/Tracking", "Streaks", "Striations", "Trapping", "Wash boarding"
]

def extract_keywords(bot_message, keywords):
    """Helper function to extract keywords from a message, case insensitive."""
    found_keywords = [kw for kw in keywords if re.search(rf"\b{re.escape(kw)}\b", bot_message, re.IGNORECASE)]
    return found_keywords[0] if found_keywords else "Other"

# Streamlit UI
st.title("Feedback Data Analysis")
uploaded_file = st.file_uploader("Upload Feedback Data (CSV)", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded data
    data = pd.read_csv(uploaded_file)

    # Check for required columns
    if {'bot_message', 'isuseful', 'created_at', 'created_by'}.issubset(data.columns):
        # Convert 'isuseful' to 1 (True) and 0 (False) if needed
        data['isuseful'] = data['isuseful'].apply(lambda x: 1 if x in [1, True, 'True'] else 0)

        # Extract keywords from bot messages
        data['category'] = data['bot_message'].apply(lambda msg: extract_keywords(str(msg), keywords))

        # Extract date from 'created_at'
        data['created_date'] = pd.to_datetime(data['created_at'], format="%d-%m-%Y %H:%M", dayfirst=True).dt.date

        # Calculate overall feedback usefulness
        total_feedback = len(data)
        useful_feedback_count = data['isuseful'].sum()
        useful_ratio = useful_feedback_count / total_feedback * 100

        st.metric(label="Total Feedback Entries", value=total_feedback)
        st.metric(label="Useful Feedback Ratio", value=f"{useful_ratio:.2f}%")

        # Analyze feedback by category (count, not percentage)
        category_feedback_counts = data.groupby('category')['isuseful'].count()
        fig = px.bar(category_feedback_counts, x=category_feedback_counts.index, y=category_feedback_counts.values, 
                     labels={'y': 'Feedback Count', 'category': 'Category'}, title="Feedback Count by Category")
        st.plotly_chart(fig)

        # Filter negative feedback (isuseful == False) for further analysis
        negative_feedback = data[data['isuseful'] == False]
        st.subheader("Categories with Negative Feedback")
        category_neg_feedback = negative_feedback['category'].value_counts()
        fig = px.pie(category_neg_feedback, values=category_neg_feedback.values, 
                     names=category_neg_feedback.index, title='Negative Feedback Distribution by Category')
        st.plotly_chart(fig)

        # Feedback distribution by day (after negative feedback)
        feedback_by_day = data.groupby('created_date').size()
        fig = px.line(feedback_by_day, x=feedback_by_day.index, y=feedback_by_day.values, 
                      labels={'y': 'Feedback Count', 'created_date': 'Date'}, 
                      title="Feedback Count by Day")
        st.plotly_chart(fig)

        # Pie chart for positive and negative feedback
        feedback_distribution = data['isuseful'].value_counts()
        feedback_labels = {1: 'Positive', 0: 'Negative'}
        fig = px.pie(feedback_distribution, values=feedback_distribution.values, 
                     names=feedback_distribution.index.map(feedback_labels), 
                     title="Positive vs Negative Feedback")
        st.plotly_chart(fig)

        # Insights for 'created_by'
        st.subheader("Feedback Counts by User")
        feedback_by_user = data.groupby('created_by').agg(
            total_feedbacks=('created_by', 'size'),
            positive_feedbacks=('isuseful', 'sum'),
            negative_feedbacks=('isuseful', lambda x: (x == 0).sum())
        ).reset_index()

        st.dataframe(feedback_by_user)

        fig = px.bar(feedback_by_user, x='created_by', y=['positive_feedbacks', 'negative_feedbacks'],
                     title="Feedback Breakdown by User", labels={'value': 'Feedback Count', 'created_by': 'User'},
                     barmode='group')
        st.plotly_chart(fig)

        # Display data table with category breakdown (positive vs negative)
        st.subheader("Category-wise Positive and Negative Feedback Counts")
        category_analysis = data.groupby('category').agg(
            total_count=('category', 'size'),
            positive_count=('isuseful', 'sum'),
            negative_count=('isuseful', lambda x: (x == 0).sum())
        ).reset_index()

        st.dataframe(category_analysis)

        # Display data table with keyword extraction
        st.subheader("Data with Extracted Categories")
        st.dataframe(data[['created_at', 'bot_message', 'category', 'isuseful']])
    else:
        st.error("The uploaded file is missing required columns: 'bot_message', 'isuseful', 'created_at', or 'created_by'.")
