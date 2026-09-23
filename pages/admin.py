import streamlit as st
from supabase import create_client
import re
import time

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="Movie Admin",
    page_icon="🔐",
    layout="wide"
)

# =====================================================
# SUPABASE - ADMIN KEY
# =====================================================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_ADMIN_KEY"]
)

# =====================================================
# LOGIN
# =====================================================
st.title("🔐 Movie Admin Panel")

password = st.text_input(
    "Admin Password",
    type="password"
)

if not password:
    st.info("Enter your admin password to continue.")
    st.stop()

if password != st.secrets["ADMIN_PASSWORD"]:
    st.error("Incorrect password.")
    st.stop()

st.success("✅ Admin access granted")


# =====================================================
# HELPERS
# =====================================================
def create_slug(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")


def upload_poster(file, slug):

    if file is None:
        return None

    extension = file.name.rsplit(".", 1)[-1].lower()

    filename = (
        f"{slug}-{int(time.time())}.{extension}"
    )

    supabase.storage.from_("movie-posters").upload(
        filename,
        file.getvalue(),
        {
            "content-type": file.type,
            "upsert": "false"
        }
    )

    return (
        supabase.storage
        .from_("movie-posters")
        .get_public_url(filename)
    )


# =====================================================
# ADMIN TABS
# =====================================================
tab_add, tab_manage = st.tabs(
    [
        "➕ Add Movie",
        "✏️ Edit / Delete Movie"
    ]
)


# =====================================================
# ADD MOVIE
# =====================================================
with tab_add:

    st.header("🎬 Add New Movie")

    title = st.text_input(
        "Movie Title",
        key="add_title"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        year = st.number_input(
            "Year",
            min_value=1900,
            max_value=2100,
            value=2026,
            step=1,
            key="add_year"
        )

    with col2:

        category = st.selectbox(
            "Category",
            [
                "Bollywood",
                "Hollywood",
                "South Indian",
                "Web Series",
                "TV Show",
                "Animation",
                "Other"
            ],
            key="add_category"
        )

    with col3:

        language = st.text_input(
            "Language",
            placeholder="Hindi / English / Tamil",
            key="add_language"
        )

    description = st.text_area(
        "Description",
        height=150,
        key="add_description"
    )

    imdb_rating = st.text_input(
        "IMDb Rating",
        placeholder="Example: 7.8",
        key="add_rating"
    )

    st.subheader("🖼️ Movie Poster")

    poster = st.file_uploader(
        "Upload Poster",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ],
        key="add_poster"
    )

    st.subheader("⬇️ Download Options")

    st.markdown("#### 480p")

    url_480 = st.text_input(
        "480p Download URL",
        key="add_url480"
    )

    size_480 = st.text_input(
        "480p File Size",
        placeholder="Example: 450 MB",
        key="add_size480"
    )

    st.markdown("#### 720p")

    url_720 = st.text_input(
        "720p Download URL",
        key="add_url720"
    )

    size_720 = st.text_input(
        "720p File Size",
        placeholder="Example: 1.2 GB",
        key="add_size720"
    )

    st.markdown("#### 1080p")

    url_1080 = st.text_input(
        "1080p Download URL",
        key="add_url1080"
    )

    size_1080 = st.text_input(
        "1080p File Size",
        placeholder="Example: 2.4 GB",
        key="add_size1080"
    )

    featured = st.checkbox(
        "⭐ Featured Movie",
        key="add_featured"
    )

    if st.button(
        "🚀 Publish Movie",
        type="primary",
        width="stretch"
    ):

        if not title.strip():

            st.error(
                "Please enter the movie title."
            )

        else:

            try:

                # Unique slug
                base_slug = create_slug(title)

                slug = (
                    f"{base_slug}-"
                    f"{int(time.time())}"
                )

                # Upload poster
                poster_url = upload_poster(
                    poster,
                    slug
                )

                movie_data = {

                    "title":
                        title.strip(),

                    "slug":
                        slug,

                    "year":
                        int(year),

                    "category":
                        category,

                    "language":
                        language.strip(),

                    "description":
                        description.strip(),

                    "imdb_rating":
                        imdb_rating.strip() or None,

                    "poster_url":
                        poster_url,

                    "quality_480p":
                        url_480.strip() or None,

                    "file_size_480p":
                        size_480.strip() or None,

                    "quality_720p":
                        url_720.strip() or None,

                    "file_size_720p":
                        size_720.strip() or None,

                    "quality_1080p":
                        url_1080.strip() or None,

                    "file_size_1080p":
                        size_1080.strip() or None,

                    "featured":
                        featured
                }

                supabase.table(
                    "movies"
                ).insert(
                    movie_data
                ).execute()

                st.success(
                    f"✅ '{title}' published successfully!"
                )

                st.balloons()

            except Exception as e:

                st.error(
                    "Movie could not be published."
                )

                st.code(str(e))


# =====================================================
# EDIT / DELETE MOVIE
# =====================================================
with tab_manage:

    st.header("✏️ Manage Movies")

    try:

        response = (
            supabase
            .table("movies")
            .select("*")
            .order(
                "created_at",
                desc=True
            )
            .execute()
        )

        movies = response.data or []

    except Exception as e:

        st.error(
            "Could not load movies."
        )

        st.code(str(e))

        movies = []


    if not movies:

        st.info(
            "No movies have been added yet."
        )

    else:

        movie_options = {
            f"{movie['title']} — ID {movie['id']}":
                movie
            for movie in movies
        }

        selected_label = st.selectbox(
            "Select Movie",
            list(movie_options.keys())
        )

        movie = movie_options[
            selected_label
        ]

        st.markdown("---")

        # =================================================
        # EDIT DETAILS
        # =================================================

        edit_title = st.text_input(
            "Movie Title",
            value=movie.get("title") or "",
            key=f"title_{movie['id']}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            edit_year = st.number_input(
                "Year",
                min_value=1900,
                max_value=2100,
                value=int(
                    movie.get("year") or 2026
                ),
                step=1,
                key=f"year_{movie['id']}"
            )

        categories = [
            "Bollywood",
            "Hollywood",
            "South Indian",
            "Web Series",
            "TV Show",
            "Animation",
            "Other"
        ]

        existing_category = (
            movie.get("category")
            or "Other"
        )

        if (
            existing_category
            not in categories
        ):
            categories.append(
                existing_category
            )

        with col2:

            edit_category = st.selectbox(
                "Category",
                categories,
                index=categories.index(
                    existing_category
                ),
                key=f"category_{movie['id']}"
            )

        with col3:

            edit_language = st.text_input(
                "Language",
                value=(
                    movie.get("language")
                    or ""
                ),
                key=f"language_{movie['id']}"
            )

        edit_description = st.text_area(
            "Description",
            value=(
                movie.get("description")
                or ""
            ),
            height=150,
            key=f"description_{movie['id']}"
        )

        edit_rating = st.text_input(
            "IMDb Rating",
            value=str(
                movie.get("imdb_rating")
                or ""
            ),
            key=f"rating_{movie['id']}"
        )

        # =================================================
        # POSTER
        # =================================================

        st.subheader("🖼️ Movie Poster")

        current_poster = movie.get(
            "poster_url"
        )

        if current_poster:

            st.image(
                current_poster,
                width=250
            )

            st.caption(
                "Upload another poster only if you want to replace this one."
            )

        else:

            st.warning(
                "⚠️ This movie currently has no poster."
            )

        replacement_poster = (
            st.file_uploader(
                "Upload / Replace Poster",
                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp"
                ],
                key=f"poster_{movie['id']}"
            )
        )

        # =================================================
        # DOWNLOAD OPTIONS
        # =================================================

        st.subheader(
            "⬇️ Download Options"
        )

        edit_url480 = st.text_input(
            "480p Download URL",
            value=(
                movie.get("quality_480p")
                or ""
            ),
            key=f"url480_{movie['id']}"
        )

        edit_size480 = st.text_input(
            "480p File Size",
            value=(
                movie.get("file_size_480p")
                or ""
            ),
            key=f"size480_{movie['id']}"
        )

        edit_url720 = st.text_input(
            "720p Download URL",
            value=(
                movie.get("quality_720p")
                or ""
            ),
            key=f"url720_{movie['id']}"
        )

        edit_size720 = st.text_input(
            "720p File Size",
            value=(
                movie.get("file_size_720p")
                or ""
            ),
            key=f"size720_{movie['id']}"
        )

        edit_url1080 = st.text_input(
            "1080p Download URL",
            value=(
                movie.get("quality_1080p")
                or ""
            ),
            key=f"url1080_{movie['id']}"
        )

        edit_size1080 = st.text_input(
            "1080p File Size",
            value=(
                movie.get("file_size_1080p")
                or ""
            ),
            key=f"size1080_{movie['id']}"
        )

        edit_featured = st.checkbox(
            "⭐ Featured Movie",
            value=bool(
                movie.get("featured")
            ),
            key=f"featured_{movie['id']}"
        )

        st.markdown("---")

        update_col, delete_col = (
            st.columns(2)
        )

        # =================================================
        # UPDATE
        # =================================================

        with update_col:

            if st.button(
                "💾 Update Movie",
                type="primary",
                width="stretch",
                key=f"update_{movie['id']}"
            ):

                if not edit_title.strip():

                    st.error(
                        "Movie title cannot be empty."
                    )

                else:

                    try:

                        poster_url = (
                            current_poster
                        )

                        if replacement_poster:

                            poster_url = (
                                upload_poster(
                                    replacement_poster,
                                    movie["slug"]
                                )
                            )

                        update_data = {

                            "title":
                                edit_title.strip(),

                            "year":
                                int(edit_year),

                            "category":
                                edit_category,

                            "language":
                                edit_language.strip(),

                            "description":
                                edit_description.strip(),

                            "imdb_rating":
                                edit_rating.strip()
                                or None,

                            "poster_url":
                                poster_url,

                            "quality_480p":
                                edit_url480.strip()
                                or None,

                            "file_size_480p":
                                edit_size480.strip()
                                or None,

                            "quality_720p":
                                edit_url720.strip()
                                or None,

                            "file_size_720p":
                                edit_size720.strip()
                                or None,

                            "quality_1080p":
                                edit_url1080.strip()
                                or None,

                            "file_size_1080p":
                                edit_size1080.strip()
                                or None,

                            "featured":
                                edit_featured
                        }

                        supabase.table(
                            "movies"
                        ).update(
                            update_data
                        ).eq(
                            "id",
                            movie["id"]
                        ).execute()

                        st.success(
                            "✅ Movie updated successfully!"
                        )

                    except Exception as e:

                        st.error(
                            "Movie could not be updated."
                        )

                        st.code(str(e))


        # =================================================
        # DELETE
        # =================================================

        with delete_col:

            confirm_delete = (
                st.checkbox(
                    "I confirm that I want to delete this movie",
                    key=f"confirm_{movie['id']}"
                )
            )

            if st.button(
                "🗑️ Delete Movie",
                width="stretch",
                disabled=not confirm_delete,
                key=f"delete_{movie['id']}"
            ):

                try:

                    supabase.table(
                        "movies"
                    ).delete().eq(
                        "id",
                        movie["id"]
                    ).execute()

                    st.success(
                        "🗑️ Movie deleted successfully."
                    )

                    time.sleep(1)

                    st.rerun()

                except Exception as e:

                    st.error(
                        "Movie could not be deleted."
                    )

                    st.code(str(e))
