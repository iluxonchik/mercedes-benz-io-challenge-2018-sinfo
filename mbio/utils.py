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

def are_list_items_unique(lst):
    num_coords = len(lst)
    for i in range(num_coords):
        for j in range(num_coords):
            if i == j:
                continue
            if lst[i] == lst[j]:
                return False
    return True
