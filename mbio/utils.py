"""Utility functionality."""
import unicodedata

def nfdk_normalize_ignore_case(string):
    return unicodedata.normalize("NFKD", string.casefold())

def is_str_equal_ignore_case(str1, str2):
    """
    Compares if strings are equal ignoring letter case.

    This function uses the NFKD unicode normalization.
    """
    return nfdk_normalize_ignore_case(str1) == nfdk_normalize_ignore_case(str2)
