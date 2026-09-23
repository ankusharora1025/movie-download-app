import streamlit as st
from supabase import create_client
import html

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="CinemaHub",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

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

st.markdown(
    """
    <style>

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    .movie-title {
        font-size: 20px;
        font-weight: 700;
        line-height: 1.3;
        margin-top: 12px;
        margin-bottom: 4px;
        min-height: 52px;
    }

    .movie-meta {
        color: #9da3ae;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .movie-poster {
        width: 100%;
        height: 200px;
        overflow: hidden;
        border-radius: 14px;
        background: #171a21;
    }

    .movie-poster img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center top;
        display: block;
    }

    .no-poster {
        width: 100%;
        height: 200px;
        border-radius: 14px;
        background: #19324a;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #54a6ff;
        font-size: 18px;
        font-weight: 600;
    }

    .rating {
        display: inline-block;
        background: #242832;
        border-radius: 7px;
        padding: 5px 9px;
        margin-top: 4px;
        margin-bottom: 10px;
        font-size: 13px;
    }

    div[data-testid="stButton"] button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True
)

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
    st.error("Could not connect to the movie database.")
    st.code(str(e))
    st.stop()


# =====================================================
# MOVIE DETAILS PAGE
# =====================================================

selected_slug = st.query_params.get("movie")

if selected_slug:

    selected_movie = next(
        (
            movie
            for movie in movies
            if movie.get("slug") == selected_slug
        ),
        None
    )

    if selected_movie is None:

        st.error("Movie not found.")

        if st.button("← Back to CinemaHub"):
            st.query_params.clear()
            st.rerun()

        st.stop()

    if st.button("← Back to CinemaHub"):
        st.query_params.clear()
        st.rerun()

    st.markdown("---")

    left, right = st.columns(
        [1, 2],
        gap="large"
    )

    with left:

        poster_url = selected_movie.get("poster_url")

        if poster_url:

            safe_poster = html.escape(
                str(poster_url),
                quote=True
            )

            st.markdown(
                f"""
                <div class="movie-poster"
                     style="height:560px;">
                    <img src="{safe_poster}">
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="no-poster"
                     style="height:560px;">
                    🎬 No Poster
                </div>
                """,
                unsafe_allow_html=True
            )

    with right:

        title = html.escape(
            str(
                selected_movie.get("title")
                or "Untitled"
            )
        )

        st.title(title)

        details = []

        if selected_movie.get("year"):
            details.append(
                str(selected_movie["year"])
            )

        if selected_movie.get("language"):
            details.append(
                str(selected_movie["language"])
            )

        if selected_movie.get("category"):
            details.append(
                str(selected_movie["category"])
            )

        if details:
            st.caption(
                " • ".join(details)
            )

        rating = selected_movie.get(
            "imdb_rating"
        )

        if rating:
            st.markdown(
                f"⭐ **IMDb {rating} / 10**"
            )

        description = selected_movie.get(
            "description"
        )

        if description:
            st.markdown("### About")
            st.write(description)

        st.markdown("### ⬇️ Download")

        download_available = False

        url_480 = selected_movie.get(
            "quality_480p"
        )

        size_480 = selected_movie.get(
            "file_size_480p"
        )

        if url_480:

            download_available = True

            label = "⬇️ Download 480p"

            if size_480:
                label += f" • {size_480}"

            st.link_button(
                label,
                url_480,
                width="stretch"
            )

        url_720 = selected_movie.get(
            "quality_720p"
        )

        size_720 = selected_movie.get(
            "file_size_720p"
        )

        if url_720:

            download_available = True

            label = "⬇️ Download 720p"

            if size_720:
                label += f" • {size_720}"

            st.link_button(
                label,
                url_720,
                width="stretch"
            )

        url_1080 = selected_movie.get(
            "quality_1080p"
        )

        size_1080 = selected_movie.get(
            "file_size_1080p"
        )

        if url_1080:

            download_available = True

            label = "⬇️ Download 1080p"

            if size_1080:
                label += f" • {size_1080}"

            st.link_button(
                label,
                url_1080,
                width="stretch"
            )

        if not download_available:
            st.info(
                "No download links are available for this movie yet."
            )

    st.stop()


# =====================================================
# HOMEPAGE
# =====================================================

st.title("🎬 CinemaHub")

st.caption(
    "Movies • Series • Entertainment"
)

# =====================================================
# SEARCH
# =====================================================

search = st.text_input(
    "🔎 Search Movies",
    placeholder="Search by movie name..."
)

# =====================================================
# CATEGORY
# =====================================================

categories = sorted(
    {
        movie.get("category")
        for movie in movies
        if movie.get("category")
    }
)

category_options = [
    "All"
] + categories

selected_category = st.selectbox(
    "🎞️ Category",
    category_options
)

# =====================================================
# FILTER MOVIES
# =====================================================

filtered_movies = movies

if search:

    search_text = search.lower().strip()

    filtered_movies = [
        movie
        for movie in filtered_movies
        if search_text
        in str(
            movie.get("title") or ""
        ).lower()
    ]

if selected_category != "All":

    filtered_movies = [
        movie
        for movie in filtered_movies
        if movie.get("category")
        == selected_category
    ]


# =====================================================
# LATEST MOVIES
# =====================================================

st.markdown("---")
st.subheader("🔥 Latest Movies")

if not filtered_movies:

    st.info("No movies found.")

else:

    for start in range(
        0,
        len(filtered_movies),
        3
    ):

        cols = st.columns(
            3,
            gap="medium"
        )

        row = filtered_movies[
            start:start + 3
        ]

        for index, movie in enumerate(row):

            with cols[index]:

                poster_url = movie.get(
                    "poster_url"
                )

                if poster_url:

                    safe_poster = html.escape(
                        str(poster_url),
                        quote=True
                    )

                    st.markdown(
                        f"""
                        <div class="movie-poster">
                            <img src="{safe_poster}">
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.markdown(
                        """
                        <div class="no-poster">
                            🎬 No Poster
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                movie_title = html.escape(
                    str(
                        movie.get("title")
                        or "Untitled"
                    )
                )

                st.markdown(
                    f"""
                    <div class="movie-title">
                        {movie_title}
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
                        str(movie["language"])
                    )

                if movie.get("category"):
                    movie_details.append(
                        str(movie["category"])
                    )

                if movie_details:

                    safe_details = html.escape(
                        " • ".join(
                            movie_details
                        )
                    )

                    st.markdown(
                        f"""
                        <div class="movie-meta">
                            {safe_details}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                rating = movie.get(
                    "imdb_rating"
                )

                if rating:

                    safe_rating = html.escape(
                        str(rating)
                    )

                    st.markdown(
                        f"""
                        <div class="rating">
                            ⭐ IMDb {safe_rating}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                movie_id = movie.get(
                    "id",
                    movie.get("slug")
                )

                if st.button(
                    "🎬 View Movie",
                    key=f"movie_{movie_id}",
                    width="stretch"
                ):

                    st.query_params[
                        "movie"
                    ] = movie["slug"]

                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
