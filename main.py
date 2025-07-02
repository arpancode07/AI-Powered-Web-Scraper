import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parser_module import parse_with_ollama

st.title("🧠 AI Web Scraper & Parser")

url = st.text_input("🔗 Enter Website URL")

# Step 1: Scrape Website
if st.button("🔍 Scrape Website"):
    if url:
        try:
            st.write("⏳ Scraping the website...")
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Save in session state
            st.session_state.dom_content = cleaned_content

            # Preview scraped content
            with st.expander("🧾 View Cleaned DOM Content"):
                st.text_area("Cleaned Content", cleaned_content, height=300)

            st.success("✅ Website scraped and content cleaned.")
        except Exception as e:
            st.error(f"❌ Error while scraping: {e}")

# Step 2: Ask Parsing Questions
if "dom_content" in st.session_state:
    parse_description = st.text_area("📝 Describe what you want to extract")

    if st.button("🚀 Parse Content"):
        if parse_description:
            try:
                st.write("🧠 Parsing with LLM...")

                dom_chunks = split_dom_content(st.session_state.dom_content)
                parsed_result = parse_with_ollama(dom_chunks, parse_description)

                st.subheader("📤 Parsed Output")
                st.write(parsed_result)

                st.download_button(
                    label="📄 Download Result",
                    data=parsed_result,
                    file_name="parsed_result.txt",
                    mime="text/plain",
                )
            except Exception as e:
                st.error(f"❌ Parsing failed: {e}")
