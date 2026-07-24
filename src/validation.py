from docx import Document


class DocumentValidator:

    def __init__(self, document_path):
        self.document = Document(document_path)

    def validate(self, mapping):

        text = "\n".join([p.text for p in self.document.paragraphs])

        missing = []

        for original, fake in mapping.items():

            if original in text:
                missing.append(original)

        if not missing:
            print("\n✓ Validation Successful")
            print("All entities were anonymized.")
        else:
            print("\nEntities still present:")
            for entity in missing:
                print(entity)