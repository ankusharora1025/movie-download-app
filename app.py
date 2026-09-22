import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="Movie Download",
    page_icon="🎬",
    layout="wide"
)

# -------------------------
# SUPABASE CONNECTION
# -------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# -------------------------
# HEADER
# -------------------------
st.title("🎬 Movie Download")
st.write("Download and watch movies from our collection.")

# Search
search = st.text_input(
    "🔎 Search Movies",
    placeholder="Search by movie name..."
)

st.markdown("---")

# -------------------------
# GET MOVIES FROM DATABASE
# -------------------------
try:
    response = (
        supabase.table("movies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    movies = response.data

except Exception as e:
    st.error("Could not connect to movie database.")
    st.code(str(e))
    movies = []

# -------------------------
# SEARCH
# -------------------------
if search:
    movies = [
        movie for movie in movies
        if search.lower() in movie["title"].lower()
    ]

# -------------------------
# DISPLAY MOVIES
# -------------------------
st.subheader("🔥 Latest Movies")

if not movies:

    st.info("No movies have been added yet.")

else:

    for i in range(0, len(movies), 4):

        cols = st.columns(4)

        for j, movie in enumerate(movies[i:i+4]):

            with cols[j]:

                if movie.get("poster_url"):
                    st.image(
                        movie["poster_url"],
                        use_container_width=True
                    )

                st.markdown(
                    f"### {movie['title']}"
                )

                details = []

                if movie.get("year"):
                    details.append(str(movie["year"]))

                if movie.get("language"):
                    details.append(movie["language"])

                if movie.get("category"):
                    details.append(movie["category"])

                if details:
                    st.caption(" • ".join(details))

                if movie.get("description"):
                    st.write(movie["description"])

                if movie.get("quality_480p"):
                    st.link_button(
                        "⬇️ 480p",
                        movie["quality_480p"],
                        use_container_width=True
                    )

                if movie.get("quality_720p"):
                    st.link_button(
                        "⬇️ 720p",
                        movie["quality_720p"],
                        use_container_width=True
                    )

                if movie.get("quality_1080p"):
                    st.link_button(
                        "⬇️ 1080p",
                        movie["quality_1080p"],
                        use_container_width=True
                    )
