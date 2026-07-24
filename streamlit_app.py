import streamlit as st
import tempfile
import os

from src.discovery import DocumentDiscovery
from src.detector import PIIDetector
from src.generation import PIIGenerator
from src.mapping_store import MappingStore
from src.rewrite import DocumentRewriter


st.set_page_config(
    page_title="PII Redaction",
    page_icon="🔒",
    layout="centered"
)

st.title("🔒 PII Document Redaction")
st.write("Upload a DOCX file to anonymize sensitive information.")

uploaded_file = st.file_uploader(
    "Choose a DOCX file",
    type=["docx"]
)

if uploaded_file is not None:

    if st.button("Anonymize Document"):

        with st.spinner("Processing document..."):

            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp:

                temp.write(uploaded_file.read())
                input_path = temp.name

            # Load document
            discovery = DocumentDiscovery(input_path)
            discovery.load_document()

            # Extract text
            document_text = discovery.extract_text()

            # Detect entities
            detector = PIIDetector()
            entities = detector.detect_entities(document_text)

            # Generate mapping
            generator = PIIGenerator()
            mapping = MappingStore()

            for entity in entities:

                original = entity["text"]

                if not mapping.exists(original):
                    fake = generator.generate(entity)
                    mapping.add(original, fake)

            # Rewrite document
            rewriter = DocumentRewriter(discovery.document)
            rewriter.rewrite(mapping.get_mapping())

            # Save output
            output_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".docx"
            ).name

            rewriter.save(output_path)

        st.success("Document anonymized successfully!")

        with open(output_path, "rb") as file:

            st.download_button(
                label="⬇ Download Anonymized Document",
                data=file,
                file_name="anonymized.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        st.info(f"Total Entities Detected: {len(entities)}")