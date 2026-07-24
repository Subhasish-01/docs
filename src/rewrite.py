from docx import Document

class DocumentRewriter:

    def __init__(self, document):
        self.document = document

    def rewrite(self, mapping):

        for paragraph in self.document.paragraphs:
            self.rewrite_paragraph(paragraph, mapping)

        print("\nDocument rewrite completed.")

    def rewrite_paragraph(self, paragraph, mapping):

        if not paragraph.text.strip():
            return

        original_text = paragraph.text
        new_text = original_text

        # Replace using mapping
        for original, fake in mapping.items():
            new_text = new_text.replace(original, fake)

        # Nothing changed
        if original_text == new_text:
            return

        # No runs? Skip
        if not paragraph.runs:
            return

        # Save formatting of first run
        first_run = paragraph.runs[0]

        bold = first_run.bold
        italic = first_run.italic
        underline = first_run.underline

        if first_run.font.name:
            font_name = first_run.font.name
        else:
            font_name = None

        font_size = first_run.font.size

        # Clear every run
        for run in paragraph.runs:
            run.text = ""

        # Write new text into first run
        paragraph.runs[0].text = new_text

        # Restore formatting
        paragraph.runs[0].bold = bold
        paragraph.runs[0].italic = italic
        paragraph.runs[0].underline = underline

        if font_name:
            paragraph.runs[0].font.name = font_name

        paragraph.runs[0].font.size = font_size

    def save(self, output_path):

        self.document.save(output_path)

        print(f"\nDocument saved to : {output_path}")