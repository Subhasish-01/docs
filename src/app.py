from pipeline import anonymize_document


def main():

    input_path = "input/Red Herring Prospectus.docx"
    output_path = "output/anonymized.docx"

    result = anonymize_document(input_path, output_path)

    print(f"\nTotal Entities : {result['entities']}")


if __name__ == "__main__":
    main()