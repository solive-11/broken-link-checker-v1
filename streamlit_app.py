import streamlit as st
from link_checker_advanced import get_internal_links, check_link_status

st.set_page_config(page_title="Broken Link Checker", layout="wide")

st.title("Broken Link Checker")
st.write("Enter a website URL to analyze internal links.")

url = st.text_input("Enter URL")

if st.button("Check Links"):
    if url:
        with st.spinner("Scanning website..."):
            links = get_internal_links(url)

            st.write(f"Total internal links found: {len(links)}")

            healthy, redirect, broken = check_link_status(links)

        st.subheader("Summary")
        col1, col2, col3 = st.columns(3)

        col1.metric("Healthy", len(healthy))
        col2.metric("Redirecting", len(redirect))
        col3.metric("Broken", len(broken))

        st.subheader("✅ Healthy Links")
        st.write(healthy)

        st.subheader("🔁 Redirecting Links")
        st.write(redirect)

        st.subheader("❌ Broken Links")
        st.write(broken)

    else:
        st.warning("Please enter a URL")