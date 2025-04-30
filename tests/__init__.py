"""
Package: tests
Package for the application tests.
"""
import pathlib

from service.schemas import UploadResponseDTO

# Find the project root directory (where Dockerfile is located)
PROJECT_ROOT = pathlib.Path(__file__).parent.parent
# Image name to build
TEST_IMAGE_NAME = 'fastapi-picture-service-test:latest'
# Internal port the service listens on inside the container
SERVICE_PORT = 5000

TEST_BUCKET_NAME = 'test-bucket'
TEST_FILE_NAME = 'test-object.txt'
TEST_OBJECT_NAME = 'test-object.txt'
TEST_CONTENT = b"test content"
TEST_CONTENT_TYPE = 'text/plain'
TEST_FILE_SIZE = len(TEST_CONTENT)
TEST_ETAG = 'test-etag'
TEST_URL = 'http://example.com/test-object.txt'


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


def create_upload_response_dto() -> UploadResponseDTO:
    """Creates an UploadResponseDTO with predefined test values.

    This function constructs an UploadResponseDTO object populated with
    constants defined for testing purposes.  It's intended to provide a
    consistent, valid DTO for use in test cases.

    Returns:
        UploadResponseDTO: An instance of UploadResponseDTO with test data.
    """
    return UploadResponseDTO(
        original_filename=TEST_FILE_NAME,
        object_name=TEST_OBJECT_NAME,
        file_url=TEST_URL,
        size=TEST_FILE_SIZE,
        etag=TEST_ETAG
    )
