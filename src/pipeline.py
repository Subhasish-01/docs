from discovery import DocumentDiscovery
from detector import PIIDetector
from generation import PIIGenerator
from mapping_store import MappingStore
from rewrite import DocumentRewriter


def anonymize_document(input_path, output_path):

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

    # Save document
    rewriter.save(output_path)

    return {
        "entities": len(entities),
        "mapping": mapping.get_mapping()
    }