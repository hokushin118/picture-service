"""
Package: integration
Package for the integration tests.
"""


############################################################
# TEST HELPER FUNCTIONS
############################################################
def ensure_url(
        url: str
) -> str:
    """Ensure the URL has the proper protocol.

    This function checks if the given URL starts with either
    'http://' or 'https://'. If it does not, it prepends 'http://'
    to the URL. This is a utility function to help ensure that URLs are
    properly formatted before being used, for example, in making requests.

    Args:
        url (str): The URL string to check.

    Returns:
        str: The URL string, guaranteed to start with 'http://' or 'https://'.
             If the original URL already had a protocol, it is returned
             unchanged.
    """
    if not url.startswith(('http://', 'https://')):
        return f"http://{url}"
    return url


def join_urls(
        base: str,
        path: str
) -> str:
    """Join URLs while preserving the protocol and handling slashes.

    This function joins a base URL and a path, ensuring that the resulting
    URL is correctly formatted.  It handles cases where the base URL might
    have a trailing slash or the path might have a leading slash, preventing
    duplicate slashes in the final URL.  It also uses ensure_url to guarantee
    the base URL has a protocol.

    Args:
        base (str): The base URL string.
        path (str): The path to append to the base URL.

    Returns:
        str: The joined URL string.  The returned URL will have the protocol
             of the base URL, and will not have duplicate slashes.
    """
    base = ensure_url(base)
    base = base.rstrip('/')
    path = path.lstrip('/')
    return f"{base}/{path}"
