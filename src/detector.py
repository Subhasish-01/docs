import re
import spacy


class PIIDetector:
    """
    Detect PII using spaCy + Regex.
    """

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

        # Only keep useful entity types
        self.allowed_labels = {
            "PERSON",
            "ORG",
            "GPE",
            "LOC",
            "FAC"
        }

    def detect_entities(self, text):

        entities = []

        # -----------------------------
        # spaCy Detection
        # -----------------------------
        doc = self.nlp(text)

        for ent in doc.ents:

            if ent.label_ not in self.allowed_labels:
                continue

            entities.append({
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            })

        # -----------------------------
        # Regex Detection
        # -----------------------------
        regex_patterns = {

            "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

            "PHONE": r"\b(?:\+91[- ]?)?[6-9]\d{9}\b",

            "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]{1}\b",

            "AADHAAR": r"\b\d{4}\s\d{4}\s\d{4}\b",

            "PASSPORT": r"\b[A-Z][0-9]{7}\b",

            "IFSC": r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
        }

        for label, pattern in regex_patterns.items():

            for match in re.finditer(pattern, text):

                entities.append({
                    "text": match.group(),
                    "label": label,
                    "start": match.start(),
                    "end": match.end()
                })

        # Remove duplicates
        unique = {}

        for entity in entities:

            key = (
                entity["text"],
                entity["label"],
                entity["start"],
                entity["end"]
            )

            unique[key] = entity

        return list(unique.values())

    def print_entities(self, entities):

        print("\nDetected Entities")
        print("-" * 60)

        if not entities:
            print("No entities detected.")
            return

        for i, entity in enumerate(entities, start=1):

            print(f"{i}.")
            print(f"Text  : {entity['text']}")
            print(f"Label : {entity['label']}")
            print(f"Start : {entity['start']}")
            print(f"End   : {entity['end']}")
            print("-" * 60)