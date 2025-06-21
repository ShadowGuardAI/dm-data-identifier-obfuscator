import argparse
import logging
import random
import re
import sys
from faker import Faker

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DataIdentifierObfuscator:
    """
    Replaces sensitive data identifiers with randomly generated, valid-looking ones.
    """

    def __init__(self):
        """
        Initializes the DataIdentifierObfuscator with Faker for data generation.
        """
        self.fake = Faker()

    def generate_fake_ssn(self):
        """
        Generates a fake Social Security Number (SSN).  Basic format check only.
        """
        return self.fake.ssn()
    
    def obfuscate_ssn(self, text):
        """
        Finds and obfuscates SSNs within the given text.
        Args:
            text (str): The input text to process.
        Returns:
            str: The text with SSNs replaced.
        """
        ssn_pattern = r"\b\d{3}-\d{2}-\d{4}\b"  # Basic SSN regex
        return re.sub(ssn_pattern, self.generate_fake_ssn(), text)
    
    def obfuscate_text(self, text, identifier_type="ssn"):
        """
        Obfuscates specified identifiers in the given text.
        Args:
            text (str): The input text to process.
            identifier_type (str): The type of identifier to obfuscate (default: "ssn").
        Returns:
            str: The text with identifiers replaced.
        Raises:
            ValueError: If an unsupported identifier_type is provided.
        """
        try:
            if identifier_type == "ssn":
                return self.obfuscate_ssn(text)
            else:
                raise ValueError(f"Unsupported identifier type: {identifier_type}")
        except Exception as e:
            logging.error(f"Error during obfuscation: {e}")
            raise

def setup_argparse():
    """
    Sets up the command line argument parser.
    Returns:
        argparse.ArgumentParser: The configured argument parser.
    """
    parser = argparse.ArgumentParser(
        description="Replaces sensitive data identifiers with randomly generated values."
    )
    parser.add_argument(
        "input_file",
        help="The input file to process."
    )
    parser.add_argument(
        "output_file",
        help="The output file to write to."
    )
    parser.add_argument(
        "--identifier_type",
        default="ssn",
        choices=["ssn"],
        help="The type of identifier to obfuscate (default: ssn)."
    )

    return parser

def main():
    """
    Main function to execute the data obfuscation process.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        # Input validation: Check if input file exists
        try:
            with open(args.input_file, 'r') as f:
                input_data = f.read()
        except FileNotFoundError:
            logging.error(f"Input file not found: {args.input_file}")
            sys.exit(1)
        except Exception as e:
            logging.error(f"Error reading input file: {e}")
            sys.exit(1)

        obfuscator = DataIdentifierObfuscator()
        obfuscated_data = obfuscator.obfuscate_text(input_data, args.identifier_type)

        # Output handling: Write obfuscated data to the output file
        try:
            with open(args.output_file, 'w') as f:
                f.write(obfuscated_data)
            logging.info(f"Data obfuscated and written to: {args.output_file}")
        except Exception as e:
            logging.error(f"Error writing to output file: {e}")
            sys.exit(1)

    except ValueError as e:
        logging.error(e)
        sys.exit(1)
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Example Usage:
    # Create a dummy input.txt file:
    #   "My SSN is 123-45-6789 and another one is 987-65-4321."
    # Run:
    #   python main.py input.txt output.txt --identifier_type ssn
    # output.txt will contain:
    #   "My SSN is xxx-xx-xxxx and another one is xxx-xx-xxxx." (with different random SSNs)
    main()