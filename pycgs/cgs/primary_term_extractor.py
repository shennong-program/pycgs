import marisa_trie


class PrimaryTermExtractor:
    """
    A class used to extract primary terms from texts using an exact match from a dictionary of terms.

    Attributes:
        primary_term_dict (dict): A dictionary mapping terms to their primary terms.
        trie (marisa_trie.Trie): A trie structure to efficiently match terms from the primary_term_dict.
        ignore_case (bool): Flag to indicate if the matching should be case-insensitive.

    Methods:
        extract_primary_terms(text): Extracts primary terms from the input text using the trie.
    """

    def __init__(self, primary_term_dict: dict[str, str], ignore_case: bool = False):
        """
        Initializes the PrimaryTermExtractor with a primary term dictionary and builds a trie for efficient matching.

        Args:
            primary_term_dict (dict): A dictionary where keys are terms and values are their corresponding primary terms.
            ignore_case (bool): Whether to enable case-insensitive matching. Default is False.
        """
        self.ignore_case = ignore_case

        # If ignore_case is True, convert both keys and values of the dictionary to lowercase
        if self.ignore_case:
            self.primary_term_dict = {
                k.lower(): v for k, v in primary_term_dict.items()
            }
            self.trie = marisa_trie.Trie(k.lower() for k in primary_term_dict.keys())
        else:
            self.primary_term_dict = primary_term_dict
            self.trie = marisa_trie.Trie(primary_term_dict.keys())

    def extract_primary_terms(self, text: str) -> dict[str, str]:
        """
        Extracts primary terms from the given text by matching terms from the primary_term_dict.

        This method searches for terms in the input text by looking for the longest prefix matches
        from the trie built from the primary_term_dict. When a match is found, it maps the term to
        its corresponding primary term.

        Args:
            text (str): The input text from which to extract primary terms.

        Returns:
            dict[str, str]: A dictionary where the keys are the matched terms found in the text and
            the values are their corresponding primary terms.
        """
        primary_term_map = {}

        # If ignore_case is enabled, convert the text to lowercase
        if self.ignore_case:
            text = text.lower()

        n = len(text)
        i = 0

        while i < n:
            # Search for the longest prefix match starting from the current position
            candidates = self.trie.prefixes(text[i:])
            if candidates:
                # Select the longest match from the candidates
                longest_match = max(candidates, key=len)
                primary_term_map[longest_match] = self.primary_term_dict[longest_match]
                # Move the index forward by the length of the longest match
                i += len(longest_match)
            else:
                # If no match is found, move to the next character
                i += 1

        return primary_term_map
