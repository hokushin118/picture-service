# Picture microservice

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9](https://img.shields.io/badge/Python-3.9-green.svg)](https://shields.io/)

This repository provides the implementation for the `picture-service`, a
cloud-native microservice built to **scale horizontally and handle high volumes
of requests efficiently.**

## Microservice Purpose: Picture Management

The `picture-service` is a cloud-native microservice designed to provide robust
and scalable image management capabilities. Its primary function is to handle *
*CRUD (Create, Read, Update, Delete)** operations for application images.

**Design Principles:**

* **Scalability:** Designed to handle a large volume of picture-related
  requests.
* **Reliability:** Implemented with error handling and robust data validation.
* **Maintainability:** Follows clean code principles and adheres to best
  practices.
* **Cloud-Native:** Built to leverage cloud infrastructure and
  containerization.

## Key Components and Libraries

This microservice is built using the following core technologies:

* **[Python 3.9](https://www.python.org/downloads/release/python-390/):**
    * The primary programming language used for development.
    * Chosen for its readability, extensive libraries, and strong community
      support.
* **[FastAPI](https://fastapi.tiangolo.com):**
    * A lightweight and flexible web framework for Python.
    * Used to create the RESTful API endpoints and handle HTTP requests.
    * Allows for rapid development and easy prototyping.

**Additional Libraries and Tools:**

* **(Add other relevant libraries and tools here, e.g.,):**
    * **Pydantic:** For data validation.
    * **Gunicorn:** For WSGI HTTP server.
    * **pytest:** For unit testing.
    * **pylint:** For linting.

**Rationale:**

* [Python 3.9](https://www.python.org/downloads/release/python-390/)
  provides a stable and modern environment for development.
* [FastAPI](https://fastapi.tiangolo.com)'s simplicity and extensibility
  make it an ideal choice for building microservices.
* The additional libraries are selected based on their functionality and
  suitability for the project's requirements.

## Prerequisites

To develop and run this project, you'll need the following tools and software
installed:

**Required:**

* **Python 3.9:**
    * Download and install Python 3.9 from the official
      website: [Python 3.9 Downloads](https://www.python.org/downloads/release/python-390/)
    * Ensure
      that [Python 3.9 Downloads](https://www.python.org/downloads/release/python-390/)
      is added to your system's PATH environment variable.
* **Docker Desktop:**
    * Install Docker Desktop for your operating
      system: [Docker Desktop Downloads](https://www.docker.com/products/docker-desktop)
    * Docker is essential for running infrastructure services and
      containerizing the application.

**Optional (Recommended for Development):**

* **Integrated Development Environment (IDE):**
    * Choose an IDE for efficient development:
        * [PyCharm](https://www.jetbrains.com/pycharm) (Recommended for Python
          development)
        * [Visual Studio Code](https://code.visualstudio.com) (Highly versatile
          and extensible)

**Operating System Compatibility:**

* While development has been primarily conducted
  on [Red Hat Enterprise Linux for Workstations](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux/workstations),
  this project is designed to be cross-platform compatible.
* **Gunicorn and Windows:**
    * This project uses Gunicorn as the WSGI HTTP server for local development.
    * Gunicorn is designed for Unix-like operating systems (Linux, macOS).
    * To run the application locally on Windows, it is highly recommended to
      use Docker.
    * Follow the instructions for installing docker on windows found
      here: [Docker for Windows Installation](https://docs.docker.com/desktop/setup/install/windows-install/).

**Important Notes:**

* Ensure that all required software is installed and configured correctly
  before proceeding with development.
* Using a virtual environment for Python development is strongly recommended to
  isolate project dependencies.
* If you are having issues with gunicorn on windows, use docker.

## Project Versioning

This project adheres to [Semantic Versioning 2.0.0](https://semver.org) for
managing releases.

**Version File:**

* The current project version is defined in the `VERSION` file, located in the
  root directory of the repository.
* This file contains a single line representing the version number.

**Versioning Scheme:**

* The version number follows the format `X.Y.Z`, where:
    * `X` (Major Version): Incremented when incompatible API changes are made.
    * `Y` (Minor Version): Incremented when new functionality is added in a
      backward-compatible manner.
    * `Z` (Patch Version): Incremented when backward-compatible bug fixes are
      made.

**Example:**

* `1.2.3` indicates major version 1, minor version 2, and patch version 3.

**Benefits of Semantic Versioning:**

* **Clarity:** Provides a clear indication of the type of changes included in
  each release.
* **Compatibility:** Helps users understand the potential impact of upgrading
  to a new version.
* **Automation:** Enables automated dependency management and release
  processes.

**Updating the Version:**

* When making changes to the project, update the `VERSION` file accordingly.
* Follow the [Semantic Versioning 2.0.0](https://semver.org) rules to determine
  which part of the version number to increment.

**Release Notes:**

* Each release should be accompanied by detailed release notes that describe
  the changes made.

## Environment Profiles

This microservice utilizes distinct environment profiles to manage
infrastructure and application configurations for different stages of
development and deployment.

**Available Profiles:**

* **development (default):**
    * Used for local development and testing.
    * Provides a development-friendly configuration.
* **docker:**
    * Used for running microservices within Docker containers.
    * Configures the application for a containerized environment.
* **production:**
    * Used for deploying microservices in a production environment.
    * Optimized for performance and security.

**Profile-Specific Environment Variables:**

Environment variables specific to each profile are defined in `.env.<profile>`
files located in the microservice's root directory.

* `.env`: Default environment variables (development profile).
* `.env.docker`: Environment variables for the Docker profile.
* `.env.production`: Environment variables for the production profile.

**Important Security Note (Production):**

* The `.env.production` file may contain sensitive information (e.g., database
  credentials, API keys). **Never commit this file to a version control
  repository.** Use secure methods for deploying production secrets, such as
  environment variables managed by your deployment platform or dedicated secret
  management tools.

**Setting the Active Profile:**

The active profile is determined by the `APP_SETTINGS` environment variable.

* Example (setting the Docker profile):
    ```bash
    export APP_SETTINGS=docker
    ```

## Local Development Setup

This section outlines the steps to set up and run the microservice in a local
development environment.

**1. Start Infrastructure Services:**

* Ensure that the necessary infrastructure services (e.g., databases, message
  queues) are running.
* Refer to
  the [Local Development](https://github.com/hokushin118/cba-devops/blob/main/README.md#local-development)
  section of the `cba-devops` repository's README for detailed instructions on
  setting up these services.

**2. Clone the Repository:**

* Clone the `picture-service` repository to your local machine:

    ```bash
    git clone [https://github.com/hokushin118/picture-service.git](https://github.com/hokushin118/picture-service.git)
    ```

**3. Navigate to the Project Directory:**

* Change your current directory to the cloned repository:

    ```bash
    cd picture-service
    ```

**4. Create and Activate a Virtual Environment:**

* Create a virtual environment to isolate project dependencies:

    ```bash
    python3.9 -m venv .venv
    ```

    * Note: Ensure you have Python 3.9 installed. Adjust the version if needed.

* Activate the virtual environment:

    ```bash
    source .venv/bin/activate  # On macOS/Linux
    .venv\Scripts\activate     # On Windows
    ```

**5. Install Dependencies:**

* Install the required Python packages using `pip`:

    ```bash
    python3.9 -m pip install --upgrade pip
    python3.9 -m pip install -r requirements.txt
    ```

**6. Install or upgrade the cba-core-lib shared library from test.pypi.org:**

* To install or upgrade the library from the test PyPI repository, use the
  following command:

    ```bash
    pip install --index-url https://test.pypi.org/simple/ --upgrade cba-core-lib
    ```

* To verify the installation and check the library's details, use the following
  command:

    ```bash
    pip show cba-core-lib
    ```

This command will display information about the installed `cba-core-lib`
library, including its version, location, and dependencies. It helps confirm
that the package was installed correctly.

**7. Run the Microservice:**

* Start the microservice using the `wsgi.py` file. This is for development
  purposes only.

    ```bash
    python3.9 asgi.py
    ```

* The microservice will be accessible at `http://127.0.0.1:8000` (or the port
  specified in your application's configuration).

**Important Notes:**

* Verify that your application's configuration is correctly set up for the
  local development environment.
* If you encounter any dependency issues, ensure that your virtual environment
  is activated and that you have the correct Python version.
* When you are finished, deactivate the virtual environment:

    ```bash
    deactivate
    ```

## Running the Microservice with Docker

This section describes how to build and run the microservice using Docker.

**1. Build the Docker Image:**

* Navigate to the directory containing microservice `Dockerfile` (root
  directory of microservice).
* Use the following command to build the Docker image:

    ```bash
    docker build -t picture-service .
    ```

    * `docker build`: Builds a Docker image.
    * `-t picture-service`: Tags the image with the name `picture-service`.
    * `.`: Specifies the build context (current directory).

**2. Run the Docker Container:**

* Use the following command to run the Docker container:

    ```bash
    docker run -p 5000:5000 picture-service
    ```

    * `docker run`: Runs a Docker container.
    * `-p 5000:5000`: Maps port 5000 on the host to port 5000 in the container.
    * `picture-service`: Specifies the image to run.

**Important Notes:**

* Ensure that Docker is installed and running on your system.
* Verify that your `Dockerfile` is correctly configured.
* The `-p 5000:5000` option maps the container's port to the host. If your
  application uses a different port, adjust the mapping accordingly.
* If you are running a database or other dependencies, you will need to run
  them as separate containers or use Docker Compose.
* To run the container in detached mode (background), add the `-d` flag:

    ```bash
    docker run -d -p 5000:5000 picture-service
    ```
* To remove the container after stopping it, add the `--rm` flag:

    ```bash
    docker run --rm -p 5000:5000 picture-service
    ```

* To run a specific version of the image, use the tag. For example:

    ```bash
    docker run -p 5000:5000 picture-service:v1
    ```

## Running the Microservice with Docker Compose

This section outlines how to run the microservice using Docker Compose,
including infrastructure setup, and service access.

**1. Start Infrastructure Services:**

* Before running the microservice, ensure that the necessary infrastructure
  services (e.g., databases, message queues) are running.
* Refer to
  the [Local Development](https://github.com/hokushin118/cba-devops/blob/main/README.md#local-development)
  section of the README for detailed instructions.

**2. Build and Run the Microservice:**

* Before executing any Docker Compose commands, ensure you are in the root
  directory of the microservice repository.
* Use the following command to navigate to the root directory, if needed:

    ```bash
    cd /path/to/picture-service
    ```

* Use Docker Compose to build and run the microservice, along with any
  profile-specific configurations.
* Replace `<profile>` with the desired profile (e.g., `dev`, `test`, `prod`).

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.<profile>.yml up --build
    ```

* Example (dev profile):

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build
    ```

* To run the services in detached mode (background), add the `-d` flag:

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d
    ```

**3. Access the Microservice:**

* Once the microservice is running, you can access it
  at `http://127.0.0.1:5000`.
* Replace `5000` with the port defined in your `docker-compose.<profile>.yml`
  file if necessary.

**5. Stop the Services:**

* To stop the services, press **Ctrl+C** in the terminal where they are
  running (if not detached), or use the following command:

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.<profile>.yml down
    ```

* Example (dev profile):

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.dev.yml down
    ```

* To remove volumes as well, add the `-v` flag:

    ```bash
    docker compose -f docker-compose.yml -f docker-compose.dev.yml down -v
    ```

**6. Extending Docker Compose Configuration:**

* For more details on extending Docker Compose configurations,
  see: [Extend your Compose files](https://docs.docker.com/compose/how-tos/multiple-compose-files/extends)

## Running Tests

### Introduction

The microservice utilizes unit tests to verify individual components and
integration tests to ensure system-wide functionality.

**1. Unit Tests: Verifying Individual Components**

* **Focus on Isolation:**
    * Unit tests are designed to isolate and examine the smallest testable
      parts of the microservice, typically individual functions, methods, or
      classes.
    * This isolation is achieved through techniques like mocking and stubbing,
      which replace external dependencies with controlled simulations.
* **Granular Validation:**
    * The primary goal is to ensure that each component behaves as expected in
      isolation. This allows to pinpoint bugs at the most granular level,
      making debugging significantly easier.
* **Speed and Efficiency:**
    * Unit tests are generally fast to execute, enabling rapid feedback during
      development. This promotes a test-driven development (TDD) approach,
      where tests are written before the actual code.
* **Benefits:**
    * Improved code quality and maintainability.
    * Early detection of bugs.
    * Facilitates refactoring by providing confidence in the code's behavior.
    * Enhanced code documentation through executable examples.

**2. Integration Tests: Ensuring System-Wide Functionality**

* **Focus on Interactions:**
    * Integration tests go beyond individual components and examine how
      different parts of the microservice interact with each other.
    * This includes testing the communication between modules, services,
      databases, and external APIs.
* **Benefits:**
    * Detection of integration issues that are not apparent in unit tests.
    * Validation of system-level functionality and performance.
    * Increased confidence in the microservice's overall stability.
    * Verifying that all parts of the system work together.

### Execution

To execute the microservice's tests, follow these steps:

1. **Start Infrastructure Services:**
    * Ensure that the necessary infrastructure services (e.g., databases,
      message queues) are running using Docker Compose. For more information,
      see
      the [Start Infrastructure Services](https://github.com/hokushin118/cba-devops?tab=readme-ov-file#local-development)
      section of the README.

2. **Run Unit Tests:**
    * Execute the microservice's unit tests using `pytest`. You can run a basic
      test execution or include coverage reporting.
    * **Basic Test Execution:**
      ```bash
      pytest -v tests/unit
      ```
        * `pytest`: Executes the pytest test runner.
        * `-v`: Enables verbose output.
        * `tests/unit`: Specifies the directory where pytest should discover
          and execute unit tests.
    * **Test Execution with Coverage Reporting:**
      ```bash
      pytest -v --cov=service --cov-report=term-missing --cov-branch tests/unit
      ```
        * `pytest`: Executes the pytest test runner.
        * `-v`: Enables verbose output.
        * `--cov=service`: Enables test coverage measurement for the `service`
          module.
        * `--cov-report=term-missing`: Enables detailed terminal output,
          showing lines not covered by tests.
        * `--cov-branch`: Enables branch coverage measurement in addition to
          line coverage.
        * `tests/unit`: Specifies the directory where pytest should discover
          and execute unit tests.

    * **Test Execution with Coverage Reporting and Minimum Threshold:**
      ```bash
      pytest -v --cov=service --cov-report=term-missing --cov-branch --cov-fail-under=80 tests/unit
      ```
        * `pytest`: Executes the pytest test runner.
        * `-v`: Enables verbose output.
        * `--cov=service`: Enables test coverage measurement for the `service`
          module.
        * `--cov-report=term-missing`: Enables detailed terminal output,
          showing lines not covered by tests.
        * `--cov-branch`: Enables branch coverage measurement in addition to
          line coverage.
        * `--cov-fail-under=80`: Fails the test run if overall coverage is
          below 80%.
        * `tests/unit`: Specifies the directory where pytest should discover
          and execute unit tests.

    * **Explanation of Coverage Options:**

        * `--cov=service`: Specifies the module to measure coverage for.
        * `--cov-report=term-missing`: Displays missing lines in the terminal
          report.
        * `--cov-branch`: Enables branch coverage measurement.
        * `--cov-fail-under=80`: Enforces a minimum coverage threshold of 80%.
        * `--cov-report=html`: Generates an HTML coverage report.
        * `--cov-report=xml`: Generates an XML coverage report.

3. **Run Integration Tests:**
    * Execute the microservice's integration tests using `pytest`.
   ```bash
   pytest -v --with-integration tests/integration
   ```
   or in debug mode:
   ```bash
   pytest -v --with-integration --log-cli-level=DEBUG tests/integration
    ```
    * `pytest`: Executes the pytest test runner.
    * `-v`: Enables verbose output.
    * `--with-integration`: Enables the execution of integration tests.
    * `-log-cli-level=DEBUG`: Sets the logging level to DEBUG, providing more
      detailed log output.
    * `tests/integration`: Specifies the directory where pytest should
      discover and execute integration tests.

**Important Notes:**

* Verify that your application's configuration is set up correctly for the
  testing environment.
* Review the test output for any failures or errors.
* If you are using a different testing framework than pytest, update the
  testing command accordingly.

## Lint

This project uses `pylint` to enforce code quality and style standards. To lint
the code, use the following command:

```bash
pylint service/
```

## Environment Variables

Environment variables for each profile are configured in the `.env` files.

## Endpoints

This section describes the available API endpoints.

**General Endpoints:**

* `/` (GET):
    * Renders an HTML welcome page (index.html) containing links to the
      OpenAPI (Swagger) and ReDoc API documentation.
* `/api` (GET):
    * Returns a welcome message indicating the API is running.
    * Example Response: `{"message": "Welcome to the API!"}`
* `/api/health` (GET):
    * Provides the health status of the service.
    * Response: `{"status": "UP"}` (Note: Currently always "UP").
* `/api/info` (GET):
    * Returns service information, including name, version, and uptime.
    * Example
      Response: `{"name": "Account Service", "version": "1.0.0", "uptime": "1d 2h 3m"}`

**Picture Management (v1):**

**Notes:**

* `{picture_id}` refers to a version
  4 [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier) (
  Universally Unique Identifier).
* Request and response formats are in JSON.
* Error handling and response codes are omitted for brevity. Refer to the API
  documentation ([Swagger](https://swagger.io)) for detailed error information.

## API Versioning

This API employs path-based versioning to manage changes and ensure backward
compatibility.

**Current Version:**

* The current API version is **v1**.
* All API endpoints are prefixed with `/api/v1/`.
* Example: `/api/v1/pictures`

**Future Versions:**

* When significant changes are introduced to the API, a new version will be
  released (e.g., **v2**).
* New versions will be accessible through their respective path prefixes (
  e.g., `/api/v2/`).
* Previous versions will be deprecated, and a migration period will be provided
  before they are removed.

**Deprecation Policy:**

* A clear deprecation notice will be provided when a new API version is
  released.
* The deprecation period will allow developers sufficient time to migrate to
  the latest version.
* The exact deprecation period will be announced in the release notes and
  documentation.

**Benefits of Versioning:**

* **Backward Compatibility:** Allows existing applications to continue
  functioning without immediate changes.
* **Controlled Updates:** Provides a structured way to introduce breaking
  changes.
* **Improved Communication:** Clearly indicates which version is being used.

## API Documentation

This API utilizes [Swagger](https://swagger.io)
and [ReDoc](https://github.com/Redocly/redoc) for interactive
documentation.

**Accessing OpenAPI (Swagger):**

* You can access the [Swagger](https://swagger.io) UI
  at [http://127.0.0.1:5000/docs](http://127.0.0.1:5000/docs).
* This interface allows you to explore the available API endpoints, understand
  their parameters, and even make test requests directly from your browser.

**Accessing ReDoc:**

* You can access the [ReDoc](https://github.com/Redocly/redoc) UI
  at [http://127.0.0.1:5000/redoc](http://127.0.0.1:5000/redoc).
* This interface allows you to explore the available API endpoints, understand
  their parameters, and make test requests directly from your browser.

**Enabling/Disabling OpenAPI (Swagger) / ReDoc:**

* [Swagger](https://swagger.io) can be conditionally enabled or disabled using
  the `SWAGGER_ENABLED` environment variable.
* To enable Swagger, set `SWAGGER_ENABLED` to `true` (or any value that your
  application interprets as true).
* To disable Swagger, set `SWAGGER_ENABLED` to `false` (or omit the variable
  entirely).
* Example (using bash):
    ```bash
    export SWAGGER_ENABLED=true
    ```

**Important Notes:**

* Ensure that your application is running on port 5000 (or the port specified
  in your application's configuration) for the [Swagger](https://swagger.io) UI
  to be accessible.
* In production environments, it's generally recommended to disable Swagger for
  security reasons, unless access is carefully controlled.
