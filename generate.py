import random
from faker import Faker

fake = Faker()


def generate_contract():
    parties = f"This agreement is made between {fake.company()} (hereinafter referred to as 'Party A') and {fake.company()} (hereinafter referred to as 'Party B')."
    agreement_terms = f"The agreement will commence on {fake.date_this_year()} and will continue until {fake.date_this_year()}."
    confidentiality_clause = "Both parties agree to keep confidential any proprietary information disclosed."
    termination_conditions = f"This agreement may be terminated by either party upon {random.randint(30, 90)} days' written notice."
    liability_statement = "Neither party shall be liable for any indirect, incidental, or consequential damages."
    intellectual_property = "Any intellectual property developed during the term of this agreement shall remain the sole property of the originating party, unless otherwise agreed in writing."
    dispute_resolution = "Any disputes arising out of or in connection with this agreement shall be resolved through good faith negotiations. If unresolved, disputes shall be submitted to binding arbitration in accordance with the rules of the American Arbitration Association."
    governing_law = f"This agreement shall be governed by and construed in accordance with the laws of {fake.state()} without regard to its conflict of laws principles."
    force_majeure = "Neither party shall be held responsible for any failure or delay in performance due to circumstances beyond their control, including but not limited to acts of God, war, terrorism, or government regulations."
    payment_terms = f"Party B agrees to pay Party A a total of ${random.randint(10000, 100000)} for services rendered, with payment due within {random.randint(15, 45)} days of receipt of invoice."
    amendments = "Any amendments or modifications to this agreement must be in writing and signed by both parties."

    # Compiling the full contract text
    contract = f"{parties}\n\n{agreement_terms}\n\n{confidentiality_clause}\n\n{termination_conditions}\n\n{liability_statement}\n\n{intellectual_property}\n\n{dispute_resolution}\n\n{governing_law}\n\n{force_majeure}\n\n{payment_terms}\n\n{amendments}"

    return contract



def generate_contracts(num_contracts):
    contracts = []
    for _ in range(num_contracts):
        contracts.append(generate_contract())
    return contracts


if __name__ == "__main__":
    contracts = generate_contracts(5)
    for i, contract in enumerate(contracts):
        with open(f"contract_{i + 1}.txt", "w") as file:
            file.write(contract)
