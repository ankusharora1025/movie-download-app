import streamlit as st
from supabase import create_client

st.set_page_config(
    page_title="CinemaHub",
    page_icon="🎬",
    layout="wide"
)

# -------------------------
# SUPABASE
# -------------------------
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# -------------------------
# STYLE
# -------------------------
st.markdown("""
<style>

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}

.movie-card {
    padding: 8px;
    margin-bottom: 25px;
}

.movie-title {
    font-size: 20px;
    font-weight: 700;
    margin-top: 8px;
}

.movie-info {
    color: #999;
    font-size: 14px;
}

div.stButton > button {
    width: 100%;
}

</style>
""", unsafe_allow_html=True)

# -------------------------
# DATABASE
# -------------------------
try:
    response = (
        supabase.table("movies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    movies = response.data or []

except Exception as e:
    st.error("Could not load movies.")
    st.code(str(e))
    st.stop()


# -------------------------
# MOVIE DETAIL PAGE
# -------------------------
selected_slug = st.query_params.get("movie")

if selected_slug:

    movie = next(
        (m for m in movies if m["slug"] == selected_slug),
        None
    )

    if not movie:
        st.error("Movie not found.")
        st.stop()

    if st.button("← Back to Movies"):
        st.query_params.clear()
        st.rerun()

    st.markdown("---")

    poster_col, info_col = st.columns([1, 2])

    with poster_col:

        if movie.get("poster_url"):
            st.image(
                movie["poster_url"],
                use_container_width=True
            )
        else:
            st.info("No poster available")

    with info_col:

        st.title(movie["title"])

        details = []

        if movie.get("year"):
            details.append(str(movie["year"]))

        if movie.get("language"):
            details.append(movie["language"])

        if movie.get("category"):
            details.append(movie["category"])

        if details:
            st.write(" • ".join(details))

        if movie.get("imdb_rating"):
            st.markdown(
                f"⭐ **IMDb Rating:** {movie['imdb_rating']}/10"
            )

        st.markdown("### About")

        if movie.get("description"):
            st.write(movie["description"])
        else:
            st.write("No description available.")

        st.markdown("---")

        st.subheader("⬇️ Download Options")

        download_found = False

        if movie.get("quality_480p"):

            label = "⬇️ Download 480p"

            if movie.get("file_size_480p"):
                label += f" — {movie['file_size_480p']}"

            st.link_button(
                label,
                movie["quality_480p"],
                use_container_width=True
            )

            download_found = True

        if movie.get("quality_720p"):

            label = "⬇️ Download 720p"

            if movie.get("file_size_720p"):
                label += f" — {movie['file_size_720p']}"

            st.link_button(
                label,
                movie["quality_720p"],
                use_container_width=True
            )

            download_found = True

        if movie.get("quality_1080p"):

            label = "⬇️ Download 1080p"

            if movie.get("file_size_1080p"):
                label += f" — {movie['file_size_1080p']}"

            st.link_button(
                label,
                movie["quality_1080p"],
                use_container_width=True
            )

            download_found = True

        if not download_found:
            st.info("No download links available.")

    st.stop()


# -------------------------
# HOMEPAGE
# -------------------------
st.title("🎬 CinemaHub")

st.caption(
    "Movies • Series • Entertainment"
)

# Search
search = st.text_input(
    "🔎 Search Movies",
    placeholder="Search by movie name..."
)

# Categories
categories = sorted(
    list(
        set(
            m["category"]
            for m in movies
            if m.get("category")
        )
    )
)

category_options = ["All"] + categories

selected_category = st.selectbox(
    "🎞️ Category",
    category_options
)

# -------------------------
# FILTER
# -------------------------
filtered_movies = movies

if search:

    filtered_movies = [
        m for m in filtered_movies
        if search.lower() in m["title"].lower()
    ]

if selected_category != "All":

    filtered_movies = [
        m for m in filtered_movies
        if m.get("category") == selected_category
    ]


# -------------------------
# FEATURED
# -------------------------
featured_movies = [
    m for m in filtered_movies
    if m.get("featured")
]

if featured_movies:

    st.markdown("---")
    st.subheader("⭐ Featured")

    featured_cols = st.columns(
        min(4, len(featured_movies))
    )

    for i, movie in enumerate(featured_movies[:4]):

        with featured_cols[i]:

            if movie.get("poster_url"):
                st.image(
                    movie["poster_url"],
                    use_container_width=True
                )

            st.markdown(
                f"### {movie['title']}"
            )

            if st.button(
                "View Movie",
                key=f"featured_{movie['id']}",
                use_container_width=True
            ):
                st.query_params["movie"] = movie["slug"]
                st.rerun()


# -------------------------
# LATEST MOVIES
# -------------------------
st.markdown("---")
st.subheader("🔥 Latest Movies")

if not filtered_movies:

    st.info("No movies found.")

else:

    for start in range(
        0,
        len(filtered_movies),
        4
    ):

        cols = st.columns(3)

        row = filtered_movies[start:start + 3]

        for index, movie in enumerate(row):

            with cols[index]:

               if movie.get("poster_url"):

    st.markdown(
        f"""
        <div style="
            width:100%;
            height:420px;
            overflow:hidden;
            border-radius:12px;
            background:#171a21;
        ">
            <img
                src="{movie['poster_url']}"
                style="
                    width:100%;
                    height:100%;
                    object-fit:cover;
                    object-position:center top;
                "
            >
        </div>
        """,
        unsafe_allow_html=True
    )

                else:

                    st.info("🎬 No Poster")

                st.markdown(
                    f"""
                    <div class="movie-title">
                        {movie['title']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                movie_details = []

                if movie.get("year"):
                    movie_details.append(
                        str(movie["year"])
                    )

                if movie.get("language"):
                    movie_details.append(
                        movie["language"]
                    )

                if movie_details:

                    st.caption(
                        " • ".join(movie_details)
                    )

                if st.button(
                    "🎬 View Movie",
                    key=f"movie_{movie['id']}",
                    use_container_width=True
                ):

                    st.query_params["movie"] = movie["slug"]

                    st.rerun()
