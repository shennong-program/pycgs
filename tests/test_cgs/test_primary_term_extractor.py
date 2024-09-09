from pycgs.cgs.primary_term_extractor import PrimaryTermExtractor


def test_valid_primary_term_dict_initialization():
    """
    Test initializing the PrimaryTermExtractor with a valid primary_term_dict.
    """
    primary_term_dict = {"苹果": "水果", "香蕉": "水果", "汽车": "交通工具"}
    extractor = PrimaryTermExtractor(primary_term_dict)

    assert extractor.primary_term_dict == primary_term_dict


def test_extract_primary_terms_basic():
    """
    Test extracting primary terms from a basic text.
    """
    primary_term_dict = {"苹果": "水果", "香蕉": "水果", "汽车": "交通工具"}
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了苹果和香蕉，还有一辆新汽车。"
    result = extractor.extract_primary_terms(text)

    assert result == {"苹果": "水果", "香蕉": "水果", "汽车": "交通工具"}


def test_extract_primary_terms_with_unmapped_words():
    """
    Test extracting primary terms from a text that contains words not present in the primary_term_dict.
    """
    primary_term_dict = {"苹果": "水果", "香蕉": "水果"}
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了苹果和香蕉，还有一辆新汽车。"
    result = extractor.extract_primary_terms(text)

    # Only "苹果" and "香蕉" should be found and mapped
    assert result == {"苹果": "水果", "香蕉": "水果"}


def test_empty_primary_term_dict():
    """
    Test extracting primary terms when primary_term_dict is empty.
    """
    primary_term_dict = {}
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了苹果和香蕉。"
    result = extractor.extract_primary_terms(text)

    # No terms should be mapped since the primary_term_dict is empty
    assert result == {}


def test_empty_text():
    """
    Test extracting primary terms from an empty string.
    """
    primary_term_dict = {"苹果": "水果", "香蕉": "水果"}
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = ""
    result = extractor.extract_primary_terms(text)

    # An empty input text should result in an empty dictionary
    assert result == {}


def test_extract_primary_terms_chinese_only():
    """
    Test extracting primary terms from a text that contains only Chinese words.
    """
    primary_term_dict = {
        "苹果": "水果",
        "banana": "fruit",
        "car": "vehicle",
        "汽车": "交通工具",
    }
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了苹果和一辆汽车。"
    result = extractor.extract_primary_terms(text)

    # Should find the Chinese terms and map them
    assert result == {"苹果": "水果", "汽车": "交通工具"}


def test_extract_primary_terms_english_only():
    """
    Test extracting primary terms from a text that contains only English words.
    """
    primary_term_dict = {
        "苹果": "水果",
        "banana": "fruit",
        "car": "vehicle",
        "汽车": "交通工具",
    }
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "I bought a banana and a new car today."
    result = extractor.extract_primary_terms(text)

    # Should find the English terms and map them
    assert result == {"banana": "fruit", "car": "vehicle"}


def test_extract_primary_terms_mixed_language():
    """
    Test extracting primary terms from a text that contains both Chinese and English words.
    """
    primary_term_dict = {
        "苹果": "水果",
        "banana": "fruit",
        "car": "vehicle",
        "汽车": "交通工具",
    }
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了一个apple和一辆car。"
    result = extractor.extract_primary_terms(text)

    # Should find the English and Chinese terms and map them
    assert result == {"car": "vehicle"}


def test_extract_primary_terms_full_coverage():
    """
    Test extracting primary terms from a text that contains both Chinese and English words, covering all terms.
    """
    primary_term_dict = {
        "苹果": "水果",
        "banana": "fruit",
        "car": "vehicle",
        "汽车": "交通工具",
    }
    extractor = PrimaryTermExtractor(primary_term_dict)

    text = "我今天买了一个苹果、一个banana和一辆car，还有一辆汽车。"
    result = extractor.extract_primary_terms(text)

    # Should map all English and Chinese terms
    assert result == {
        "苹果": "水果",
        "banana": "fruit",
        "car": "vehicle",
        "汽车": "交通工具",
    }


def test_extract_primary_terms_mixed_nmm():
    """
    Test extracting primary terms from a mixed language text containing Natural Medicinal Materials (NMM).
    """
    primary_term_dict = {
        "Artemisia annua Part-aerial": "nmm-0001",
        "Qing-hao": "nmm-0001",
        "黄花蒿地上部": "nmm-0001",
        "青蒿": "nmm-0001",
        "Ephedra sinica Stem-herbaceous": "nmm-0003",
        "Cao-ma-huang": "nmm-0003",
        "草麻黄草质茎": "nmm-0003",
        "草麻黄": "nmm-0003",
    }

    # Initialize the PrimaryTermExtractor
    extractor = PrimaryTermExtractor(primary_term_dict)

    # Mixed language text containing both English and Chinese terms for Natural Medicinal Materials
    text = (
        "Both Artemisia annua Part-aerial and 草麻黄草质茎 are Natural Medicinal Materials "
        "and are used in traditional Chinese medicine."
    )

    # Extract primary terms
    result = extractor.extract_primary_terms(text)

    # Expected output
    expected_result = {
        "Artemisia annua Part-aerial": "nmm-0001",
        "草麻黄草质茎": "nmm-0003",
    }

    # Check if the result matches the expected output
    assert result == expected_result


def test_extract_primary_terms_case_insensitive():
    """
    Test extracting primary terms with case-insensitive matching.
    """
    primary_term_dict = {
        "Artemisia annua Part-aerial": "nmm-0001",
        "Qing-hao": "nmm-0001",
        "黄花蒿地上部": "nmm-0001",
        "青蒿": "nmm-0001",
        "Ephedra sinica Stem-herbaceous": "nmm-0003",
        "Cao-ma-huang": "nmm-0003",
        "草麻黄草质茎": "nmm-0003",
        "草麻黄": "nmm-0003",
    }

    # Initialize the PrimaryTermExtractor with case-insensitive matching
    extractor = PrimaryTermExtractor(primary_term_dict, ignore_case=True)

    # Mixed language text containing both uppercase and lowercase terms
    text = (
        "Both ARTEMISIA ANNUA Part-aerial and 草麻黄草质茎 are Natural Medicinal Materials "
        "and are used in traditional Chinese medicine."
    )

    # Extract primary terms (case-insensitive)
    result = extractor.extract_primary_terms(text)

    # Expected output
    expected_result = {
        "artemisia annua part-aerial": "nmm-0001",
        "草麻黄草质茎": "nmm-0003",
    }

    # Check if the result matches the expected output
    assert result == expected_result


def test_no_matching_terms():
    """
    Test extracting primary terms when no terms from primary_term_dict are found in the text.
    """
    primary_term_dict = {
        "Artemisia annua Part-aerial": "nmm-0001",
        "Qing-hao": "nmm-0001",
        "黄花蒿地上部": "nmm-0001",
        "青蒿": "nmm-0001",
    }

    # Initialize the PrimaryTermExtractor
    extractor = PrimaryTermExtractor(primary_term_dict)

    # Text that contains no matching terms from the dictionary
    text = "This sentence does not contain any matching terms from the dictionary."

    # Extract primary terms
    result = extractor.extract_primary_terms(text)

    # Should return an empty dictionary since no terms match
    assert result == {}


def test_extract_primary_terms_with_overlapping_matches():
    """
    Test extracting primary terms where there are overlapping terms.
    """
    primary_term_dict = {
        "Artemisia annua": "nmm-0001",
        "Artemisia annua Part-aerial": "nmm-0001",
        "Qing-hao": "nmm-0001",
    }

    # Initialize the PrimaryTermExtractor
    extractor = PrimaryTermExtractor(primary_term_dict)

    # Text containing both "Artemisia annua Part-aerial" and "Artemisia annua"
    text = "The plant Artemisia annua Part-aerial is a Natural Medicinal Material."

    # Extract primary terms
    result = extractor.extract_primary_terms(text)

    # Expected output should match the longest term first
    expected_result = {
        "Artemisia annua Part-aerial": "nmm-0001",
    }

    # Check if the result matches the expected output
    assert result == expected_result


def test_extract_primary_terms_longer_match_exists():
    """
    Test that a longer match is prioritized over a partial match.
    """
    primary_term_dict = {
        "Ephedra sinica": "aaa",
        "Ephedra sinica Stem-herbaceous": "nmm-0003",
    }

    # Initialize the PrimaryTermExtractor
    extractor = PrimaryTermExtractor(primary_term_dict)

    # Text where both a short and a long match exist
    text = (
        "Ephedra sinica Stem-herbaceous is widely used in traditional Chinese medicine."
    )

    # Extract primary terms
    result = extractor.extract_primary_terms(text)

    # Should prioritize the longer match
    expected_result = {
        "Ephedra sinica Stem-herbaceous": "nmm-0003",
    }

    assert result == expected_result


def test_mixed_case_sensitive_and_case_insensitive():
    """
    Test extracting primary terms with mixed case-sensitive and case-insensitive matching.
    """
    primary_term_dict = {
        "Ephedra sinica Stem-herbaceous": "nmm-0003",
        "cao-ma-huang": "nmm-0003",
        "草麻黄草质茎": "nmm-0003",
    }

    # Initialize the PrimaryTermExtractor with case-insensitive matching enabled
    extractor = PrimaryTermExtractor(primary_term_dict, ignore_case=True)

    # Text with mixed case
    text = "Ephedra sinica stem-herbaceous is known as CAO-MA-HUANG or 草麻黄草质茎."

    # Extract primary terms
    result = extractor.extract_primary_terms(text)

    # Expected output should match even with case differences
    expected_result = {
        "ephedra sinica stem-herbaceous": "nmm-0003",
        "cao-ma-huang": "nmm-0003",
        "草麻黄草质茎": "nmm-0003",
    }

    assert result == expected_result
