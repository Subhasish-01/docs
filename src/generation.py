import random
import string
from faker import Faker


class PIIGenerator:
    """
    Generate realistic fake values for detected PII.
    """

    def __init__(self):
        self.fake = Faker("en_IN")

    def generate(self, entity):

        label = entity["label"]

        if label == "PERSON":
            return self.fake.name()

        elif label == "ORG":
            return self.fake.company()

        elif label == "GPE":
            return self.fake.city()

        elif label == "LOC":
            return self.fake.city()

        elif label == "FAC":
            return self.fake.street_name()

        elif label == "EMAIL":
            return self.fake.email()

        elif label == "PHONE":
            return self.fake.phone_number()

        elif label == "PAN":
            return self.generate_pan()

        elif label == "AADHAAR":
            return self.generate_aadhaar()

        elif label == "PASSPORT":
            return self.generate_passport()

        elif label == "IFSC":
            return self.generate_ifsc()

        else:
            return entity["text"]

    def generate_pan(self):
        letters = ''.join(random.choices(string.ascii_uppercase, k=5))
        digits = ''.join(random.choices(string.digits, k=4))
        last = random.choice(string.ascii_uppercase)

        return letters + digits + last

    def generate_aadhaar(self):
        return (
            f"{random.randint(1000,9999)} "
            f"{random.randint(1000,9999)} "
            f"{random.randint(1000,9999)}"
        )

    def generate_passport(self):
        letter = random.choice(string.ascii_uppercase)
        digits = ''.join(random.choices(string.digits, k=7))

        return letter + digits

    def generate_ifsc(self):
        bank = ''.join(random.choices(string.ascii_uppercase, k=4))
        branch = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )

        return bank + "0" + branch