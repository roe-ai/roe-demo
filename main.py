import streamlit as st
import fitz
import json

def display_pdf_image(file_path, page_number):
    document = fitz.open(file_path)
    page = document.load_page(page_number)
    pix = page.get_pixmap()
    img = pix.tobytes("ppm")
    st.image(img, caption=f"Page {page_number} of {num_pages}", use_column_width=True)
    return img

def display_markdown(data, page_number):
    st.info("Markdown below")
    for page in data:
        if page["page_number"] == page_number:
            st.markdown(page["markdown"])

def display_tables(data, page_number):
    optional = st.empty()
    has_data = False
    optional.success("Tables or charts data below")

    with st.spinner("Loading tables"):
        for page in data:
            if page["page_number"] == page_number:
                if len(page["charts"]) > 0:
                    for chart in page["charts"]:
                        has_data = True
                        st.markdown(f"chart name: {chart["name"]}")
                        st.markdown(f"chart description: {chart["description"]}")
                        st.table(chart["data"])
                if len(page["tables"]) > 0:
                    for chart in page["tables"]:
                        has_data = True
                        st.markdown(f"table name: {chart["name"]}")
                        st.markdown(f"table description: {chart["description"]}")
                        st.table(chart["data"])
    if not has_data:
        optional.empty()
with st.sidebar:
    st.header("Roe AI PDF Parser Visualizer",
    )
    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

    json_input = st.text_area("Paste JSON content here")
    json_data = None
    try:
        json_data = json.loads(json_input)
    except json.JSONDecodeError:
        if json_input:
            st.error("Invalid JSON. Please check the format of your input.")


if uploaded_pdf is not None and json_data is not None:
    with st.sidebar:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_pdf.getvalue())

        doc = fitz.open("temp.pdf")
        num_pages = doc.page_count
        page_number = st.session_state.get("page_number", 1) 
        
        col1, col2 = st.columns([1,1])
        with col1:
            if st.button("Previous Page"):
                if page_number > 1:
                    page_number -= 1
                    st.session_state["page_number"] = page_number
        with col2:
            if st.button("Next Page"):
                if page_number < num_pages:
                    page_number += 1
                    st.session_state["page_number"] = page_number
        display_pdf_image("temp.pdf", page_number - 1)

    display_markdown(json_data, page_number)
    display_tables(json_data, page_number)