import streamlit as st
from supabase import create_client

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="CinemaHub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)
st.success("TEST: CINEMAHUB NEW APP.PY IS RUNNING")
# =====================================================
# SUPABASE
# =====================================================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# =====================================================
# CUSTOM CSS
# =====================================================
st.markdown("""
<style>

/* Main container */
.block-container {
    max-width: 1450px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Hide Streamlit default header */
header[data-testid="stHeader"] {
    background: transparent;
}

/* CinemaHub Header */
.cinema-header {
    background: linear-gradient(135deg, #111111, #252525);
    padding: 22px 30px;
    border-radius: 15px;
    margin-bottom: 20px;
}

.cinema-logo {
    font-size: 38px;
    font-weight: 900;
    letter-spacing: 1px;
}

.cinema-tagline {
    color: #aaaaaa;
    font-size: 14px;
    margin-top: 3px;
}

/* Movie title */
.movie-title {
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
    margin-bottom: 2px;
}

/* Movie metadata */
.movie-meta {
    color: #999999;
    font-size: 13px;
    margin-bottom: 5px;
}

/* Rating */
.rating {
    font-size: 13px;
    font-weight: 600;
}

/* Buttons */
div.stButton > button {
    width: 100%;
    border-radius: 8px;
}

div.stLinkButton > a {
    width: 100%;
    border-radius: 8px;
}

/* Section titles */
.section-title {
    font-size: 25px;
    font-weight: 800;
    margin-top: 15px;
    margin-bottom: 15px;
}

/* Detail information */
.movie-description {
    font-size: 16px;
    line-height: 1.7;
}

/* Mobile */
@media (max-width: 768px) {

    .cinema-logo {
        font-size: 29px;
    }

    .cinema-header {
        padding: 18px;
    }

    .movie-title {
        font-size: 16px;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD MOVIES
# =====================================================
try:

    response = (
        supabase
        .table("movies")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    movies = response.data or []

except Exception as e:

    st.error("Unable to load the movie library.")
    st.code(str(e))
    st.stop()


# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="cinema-header">

    <div class="cinema-logo">
        🎬 CinemaHub
    </div>

    <div class="cinema-tagline">
        Movies • Series • Entertainment
    </div>

</div>
""", unsafe_allow_html=True)


# =====================================================
# MOVIE DETAILS PAGE
# =====================================================
selected_slug = st.query_params.get("movie")

if selected_slug:

    movie = next(
        (
            movie
            for movie in movies
            if movie.get("slug") == selected_slug
        ),
        None
    )

    if not movie:

        st.error("Movie not found.")

        if st.button("← Back to CinemaHub"):
            st.query_params.clear()
            st.rerun()

        st.stop()

    if st.button("← Back to CinemaHub"):

        st.query_params.clear()
        st.rerun()

    st.markdown("---")

    poster_column, information_column = st.columns(
        [1, 2],
        gap="large"
    )

    # POSTER
    with poster_column:

        if movie.get("poster_url"):

            st.image(
                movie["poster_url"],
                use_container_width=True
            )

        else:

            st.info("🎬 Poster unavailable")

    # INFORMATION
    with information_column:

        st.title(movie["title"])

        metadata = []

        if movie.get("year"):
            metadata.append(str(movie["year"]))

        if movie.get("language"):
            metadata.append(movie["language"])

        if movie.get("category"):
            metadata.append(movie["category"])

        if metadata:

            st.caption(
                " • ".join(metadata)
            )

        if movie.get("imdb_rating"):

            st.markdown(
                f"⭐ **IMDb:** {movie['imdb_rating']}/10"
            )

        st.markdown("### About")

        if movie.get("description"):

            st.markdown(
                f"""
                <div class="movie-description">
                    {movie["description"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.write(
                "No description available."
            )

        st.markdown("---")

        # =============================================
        # DOWNLOAD OPTIONS
        # =============================================

        st.subheader("⬇️ Download Options")

        download_available = False

        # 480P
        if movie.get("quality_480p"):

            label = "⬇️ Download 480p"

            if movie.get("file_size_480p"):

                label += (
                    f" • {movie['file_size_480p']}"
                )

            st.link_button(
                label,
                movie["quality_480p"],
                use_container_width=True
            )

            download_available = True

        # 720P
        if movie.get("quality_720p"):

            label = "⬇️ Download 720p"

            if movie.get("file_size_720p"):

                label += (
                    f" • {movie['file_size_720p']}"
                )

            st.link_button(
                label,
                movie["quality_720p"],
                use_container_width=True
            )

            download_available = True

        # 1080P
        if movie.get("quality_1080p"):

            label = "⬇️ Download 1080p"

            if movie.get("file_size_1080p"):

                label += (
                    f" • {movie['file_size_1080p']}"
                )

            st.link_button(
                label,
                movie["quality_1080p"],
                use_container_width=True
            )

            download_available = True

        if not download_available:

            st.info(
                "Download links are not available yet."
            )

    st.stop()


# =====================================================
# SEARCH
# =====================================================
search = st.text_input(
    "🔎 Search",
    placeholder="Search movies and series...",
    label_visibility="collapsed"
)


# =====================================================
# CATEGORY FILTER
# =====================================================
available_categories = sorted(
    {
        movie["category"]
        for movie in movies
        if movie.get("category")
    }
)

category_options = [
    "All"
] + available_categories

selected_category = st.radio(
    "Browse",
    category_options,
    horizontal=True,
    label_visibility="collapsed"
)


# =====================================================
# FILTER MOVIES
# =====================================================
filtered_movies = movies.copy()

if search:

    filtered_movies = [
        movie
        for movie in filtered_movies
        if search.lower()
        in movie.get("title", "").lower()
    ]

if selected_category != "All":

    filtered_movies = [
        movie
        for movie in filtered_movies
        if movie.get("category")
        == selected_category
    ]


# =====================================================
# FEATURED MOVIES
# =====================================================
featured_movies = [
    movie
    for movie in filtered_movies
    if movie.get("featured")
]

if featured_movies:

    st.markdown(
        '<div class="section-title">'
        '⭐ Featured Movies'
        '</div>',
        unsafe_allow_html=True
    )

    featured_columns = st.columns(
        min(4, len(featured_movies))
    )

    for index, movie in enumerate(
        featured_movies[:4]
    ):

        with featured_columns[index]:

            if movie.get("poster_url"):

                st.image(
                    movie["poster_url"],
                    use_container_width=True
                )

            else:

                st.info("🎬 No Poster")

            st.markdown(
                f"""
                <div class="movie-title">
                    {movie["title"]}
                </div>
                """,
                unsafe_allow_html=True
            )

            meta = []

            if movie.get("year"):
                meta.append(str(movie["year"]))

            if movie.get("language"):
                meta.append(movie["language"])

            if meta:

                st.caption(
                    " • ".join(meta)
                )

            if movie.get("imdb_rating"):

                st.caption(
                    f"⭐ {movie['imdb_rating']}/10"
                )

            if st.button(
                "View Details",
                key=f"featured_{movie['id']}",
                use_container_width=True
            ):

                st.query_params["movie"] = (
                    movie["slug"]
                )

                st.rerun()

    st.markdown("---")


# =====================================================
# LATEST MOVIES
# =====================================================
st.markdown(
    '<div class="section-title">'
    '🔥 Latest Movies'
    '</div>',
    unsafe_allow_html=True
)

if not filtered_movies:

    st.info(
        "No movies found."
    )

else:

    # 5 movies per row
    movies_per_row = 5

    for start in range(
        0,
        len(filtered_movies),
        movies_per_row
    ):

        columns = st.columns(
            movies_per_row
        )

        row_movies = filtered_movies[
            start:start + movies_per_row
        ]

        for index, movie in enumerate(
            row_movies
        ):

            with columns[index]:

                # POSTER
                if movie.get("poster_url"):

                    st.image(
                        movie["poster_url"],
                        use_container_width=True
                    )

                else:

                    st.info(
                        "🎬 No Poster"
                    )

                # TITLE
                st.markdown(
                    f"""
                    <div class="movie-title">
                        {movie["title"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # DETAILS
                metadata = []

                if movie.get("year"):

                    metadata.append(
                        str(movie["year"])
                    )

                if movie.get("language"):

                    metadata.append(
                        movie["language"]
                    )

                if metadata:

                    st.markdown(
                        f"""
                        <div class="movie-meta">
                            {" • ".join(metadata)}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # RATING
                if movie.get("imdb_rating"):

                    st.markdown(
                        f"""
                        <div class="rating">
                            ⭐ {movie["imdb_rating"]}/10
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # VIEW
                if st.button(
                    "🎬 View Details",
                    key=f"movie_{movie['id']}",
                    use_container_width=True
                ):

                    st.query_params["movie"] = (
                        movie["slug"]
                    )

                    st.rerun()


# =====================================================
# FOOTER
# =====================================================
st.markdown("---")

st.caption(
    "© 2026 CinemaHub • Movies • Series • Entertainment"
)

# CinemaHub deployment refresh

# CinemaHub v2
