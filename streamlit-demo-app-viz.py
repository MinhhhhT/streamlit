import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

def sidebar_filters(data):
    st.sidebar.markdown("Select a range on the slider that represents movie scores to view the total number of movies in a genre that fall within that range")
    min_score,max_score = st.sidebar.slider("Choose a value :", min_value=data["score"].min(), max_value=data["score"].max(), value=(3.0,4.0), step=0.1)
    st.sidebar.markdown("Select your preferred genre(s) and year to view the movies released that year and in that genre")
    genre = data['genre'].unique()
    selected_default = list(genre)[:4]
    selected_genre = st.sidebar.multiselect('Select Genre', genre, default=selected_default)
    years = data['year'].unique().astype(str)
    selected_year = st.sidebar.selectbox("Select Year", years)
    return selected_year, selected_genre, min_score, max_score

def main():
    st.set_page_config(layout="wide")
    st.title("Interactive Dashboard")
    st.subheader("Interact with this dashboard using the widgets on the sidebar")
    movies_data = pd.read_csv("https://raw.githubusercontent.com/nv-thang/Data-Visualization-Course/main/movies.csv")
    movies_data.dropna(inplace=True)
    movies_data['score'] = pd.to_numeric(movies_data['score'], errors='coerce')
    movies_data['year'] = movies_data['year'].astype(str)

    row_1, row_2 = st.columns([4, 6])
    with row_1:
        st.subheader("Lists of movies filtered by year and Genre")
        selected_year, selected_genre, min_score, max_score = sidebar_filters(movies_data)
        filtered_data = movies_data[(movies_data['year'] == selected_year) & 
                                    (movies_data['genre'].isin(selected_genre)) & 
                                    (movies_data['score'] >= min_score) & 
                                    (movies_data['score'] <= max_score)]
        df = pd.DataFrame(filtered_data, columns=['name', 'genre', 'year'])
        st.dataframe(df, height=379, width=350)

    with row_2:
        st.subheader("User Score of Movies and Their Genre")
        filtered_data = movies_data[(movies_data['year'] == selected_year) & (movies_data['genre'].isin(selected_genre))]
        avg_user_score = filtered_data.groupby('genre')['score'].mean().round(2)
        st.line_chart(avg_user_score)           
        avg_budget = movies_data.groupby('genre')['budget'].mean().round()
        avg_budget = avg_budget.reset_index()
        genre = avg_budget['genre']
        avg_budget_value = avg_budget['budget']
        
    fig, ax = plt.subplots(figsize=(16, 9))
    st.markdown("Average Movie Budget, Grouped by Genre")
    ax.bar(genre, avg_budget_value, color='maroon')
    ax.set_xlabel("Genre")
    ax.set_ylabel('Budget')
    ax.set_title('Matplotlib Bar Chart Showing The Average Budget of Movies in Each Genre')
    ax.tick_params(axis="x", rotation=0)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
