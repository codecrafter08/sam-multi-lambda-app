# SamMultiLambdaApp

SamMultiLambdaApp is a CRM web application tailored for the home improvement industry similar to Lead perfection with extended features.

It includes the below features;
*   **Lead Management & Automation**: Centralizes all leads, automates their distribution to call centers according to the different sources and subsources as well as different markets.
*   **Appointment Scheduling**: Schedule Appointments for different Sales Person and Sales Manager for smooth processing of installation requests from the leads.
*   **Manage Calls and Callbacks**: Manage Calls and Callbacks according to the Lead Response.
*   **Production Management**: After the appointment process completes, generates Jobs by using the documents uploaded by the Sales Manager and Sales Pro.
*   **Installation Management**: Capability of adding and modifying the payments, permits, materials for installation and documents.
*   **Notifications**: Seamless integration of Email and Notification service to keep the employees as well as the leads on track.
*   **Job Scheduling**: Manage Scheduling of Jobs or unresolved tickets according to the production events.
*   **Access Control**: Offers granular access controls, including user-specific permissions, time-based access restrictions, and detailed activity logs.
*   **Reporting**: Provides customizable reports and dashboards to monitor sales performance and call center performance.
*   **Employee Management**: Manage Employees according to the employee type and the market they belongs to.
*   **AI Integration**: A key differentiator is the "Ask SamMultiLambdaApp" feature, which integrates a large language model (LLM) to support text-to-SQL queries, allowing users to retrieve database insights through natural language input.
*   **AI Insights**: It provides an AI Insights which gives the detailed insights of Call Center and Sales Performance as well as the Employees.

## Project Structure

- `entity_service/`: Contains Lambda functions for entity-related operations.
- `root_service/`: Root handler and data cleanup utilities.
- `db_helper/`: Database models (SQLAlchemy) and migration scripts (Alembic).
- `common_db_layer/`: Shared database layer dependencies.
- `template.yaml`: AWS SAM template defining the application resources.

## Prerequisites

- AWS CLI
- AWS SAM CLI
- Python 3.9+
- Docker (for local testing)

## Setup

1.  **Install Dependencies**:
    Ensure you have the required Python packages installed. You can install them using pip:
    ```bash
    pip install -r common_db_layer/requirements.txt
    ```

2.  **Database Migrations**:
    This project uses Alembic for database migrations. To run migrations:
    ```bash
    cd db_helper
    alembic upgrade head
    ```

3.  **Build and Deploy**:
    Use the Makefile commands to build and deploy the application.
    ```bash
    make build
    make deploy
    ```
    (Note: Ensure your AWS credentials are configured correctly.)

## Configuration

- **Environment Variables**: Check `template.yaml` and `samconfig.toml` for configuration settings.
- **Secrets**: Sensitive information should be managed via AWS Secrets Manager or environment variables. Do not commit secrets to the repository.
- **Local Config**: The `samconfig.toml` file is ignored by git to prevent accidental commit of secrets. Use `samconfig.toml.example` as a template to create your local `samconfig.toml`.

## Author

**codecrafet08**

## License

[License Information]
