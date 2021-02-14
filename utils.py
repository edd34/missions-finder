def is_subseq(v2, v1):
    """Check whether v2 is a subsequence of v1."""
    for elem2 in v2:
        for elem1 in v1:
            if elem2.lower() not in elem1.lower():
                return False
    return True