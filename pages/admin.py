import streamlit as st
from supabase import create_client
import re
import time

st.set_page_config(
    page_title="Movie Admin",
    page_icon="🔐",
    layout="wide"
)

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

st.title("🔐 Movie Admin Panel")

# -------------------------
# LOGIN
# -------------------------
password = st.text_input("Admin Password", type="password")

if not password:
    st.info("Enter your admin password.")
    st.stop()

if password != st.secrets["ADMIN_PASSWORD"]:
    st.error("Incorrect password.")
    st.stop()

st.success("Admin access granted")

st.markdown("---")

# -------------------------
# ADD MOVIE
# -------------------------
st.header("🎬 Add New Movie")

title = st.text_input("Movie Title")

col1, col2, col3 = st.columns(3)

with col1:
    year = st.number_input(
        "Year",
        min_value=1900,
        max_value=2100,
        value=2026
    )

with col2:
    category = st.selectbox(
        "Category",
        [
            "Bollywood",
            "Hollywood",
            "South Indian",
            "Web Series",
            "Animation",
            "Other"
        ]
    )

with col3:
    language = st.text_input(
        "Language",
        placeholder="Hindi / English / Tamil"
    )

description = st.text_area("Description")

imdb_rating = st.text_input(
    "IMDb Rating",
    placeholder="Example: 7.8"
)

st.subheader("🖼️ Movie Poster")

poster = st.file_uploader(
    "Upload Poster",
    type=["jpg", "jpeg", "png", "webp"]
)

st.subheader("⬇️ Download Links")

url_480 = st.text_input("480p Download URL")
size_480 = st.text_input("480p File Size", placeholder="Example: 450 MB")

url_720 = st.text_input("720p Download URL")
size_720 = st.text_input("720p File Size", placeholder="Example: 1.2 GB")

url_1080 = st.text_input("1080p Download URL")
size_1080 = st.text_input("1080p File Size", placeholder="Example: 2.4 GB")

featured = st.checkbox("Featured Movie")

# -------------------------
# CREATE SLUG
# -------------------------
def create_slug(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    return text.strip("-")

# -------------------------
# PUBLISH
# -------------------------
if st.button(
    "🚀 Publish Movie",
    type="primary",
    use_container_width=True
):

    if not title:
        st.error("Movie title is required.")
        st.stop()

    slug = create_slug(title)

    poster_url = None

    try:

        # Upload poster
        if poster:

            extension = poster.name.split(".")[-1].lower()

            filename = (
                f"{slug}-{int(time.time())}.{extension}"
            )

            supabase.storage.from_("movie-posters").upload(
                filename,
                poster.getvalue(),
                {
                    "content-type": poster.type
                }
            )

            poster_url = (
                supabase.storage
                .from_("movie-posters")
                .get_public_url(filename)
            )

        # Add movie to database
        movie_data = {
            "title": title,
            "slug": slug,
            "year": int(year),
            "category": category,
            "language": language,
            "description": description,
            "poster_url": poster_url,
            "quality_480p": url_480 or None,
            "quality_720p": url_720 or None,
            "quality_1080p": url_1080 or None,
            "file_size_480p": size_480 or None,
            "file_size_720p": size_720 or None,
            "file_size_1080p": size_1080 or None,
            "imdb_rating": imdb_rating or None,
            "featured": featured
        }

        supabase.table("movies").insert(
            movie_data
        ).execute()

        st.success(
            f"✅ {title} published successfully!"
        )

        st.balloons()

    except Exception as e:
        st.error("Movie could not be published.")
        st.code(str(e))
