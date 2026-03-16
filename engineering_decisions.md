1️⃣ How the License System Was Designed

The license enforcement mechanism was implemented as an offline validation system that controls the maximum number of users allowed to register in OpenWebUI.

The system uses a local configuration file called:

license.json


During the user registration process, the system performs the following steps:

Load the license configuration.

Count the number of registered users in the database.

Compare the count with the max_users limit.

If the limit is reached, the system blocks further registrations and returns an error message.

This validation is integrated directly into the signup endpoint, ensuring that every user creation request passes through the license check.

2️⃣ Why This Approach Was Chosen

This approach was selected because it satisfies the assignment requirements:

Works offline (no internet or license server required)

Simple and reliable

Integrates naturally into the application workflow

Placing the license validation inside the user creation flow ensures that the limit is enforced consistently regardless of how the registration request is made (UI or API).

This approach also minimizes performance overhead since the validation only runs during signup.

3️⃣ How Bypass Attempts Were Mitigated

Several measures were taken to reduce the likelihood of bypassing the license mechanism:

License Signature

The license file contains a signature field that verifies its authenticity.
The system validates this signature before accepting the license configuration.

Server-Side Validation

The license check is implemented on the backend, not only in the UI.
This prevents bypassing the restriction through API calls or modified frontend code.

Integrated Validation Layer

The validation is embedded directly into the user registration logic, making it difficult to disable without modifying core system functionality.

File Validation

The application checks whether the license file exists and whether it has valid content before allowing user creation.

4️⃣ Integration with OpenWebUI

The license system was integrated into the OpenWebUI backend inside the authentication and user management module.

Specifically:

The validation is executed during the signup process.

The system queries the database to count existing users.

The license validator is called before creating a new user record.

This ensures that all user creation attempts are subject to license enforcement.

The integration follows the existing architecture of OpenWebUI and avoids modifying unrelated components.

5️⃣ Design Patterns and Engineering Principles

The implementation follows several software engineering practices:

Separation of Concerns

The license validation logic is implemented in a separate module, keeping it independent from the main authentication logic.


Single Responsibility Principle (SRP)

The license module is responsible only for:

reading the license

validating it

enforcing limits

Configuration-Based Design

License limits are defined in a configuration file rather than hardcoded values.
This makes the system easier to modify without changing source code.

Defensive Programming

The system validates:

license file existence

file format

license values

before enforcing restrictions.

6️⃣ Limitations and Assumptions

This implementation assumes that:

administrators do not manually manipulate the database

the license file is stored securely on the host system

Future improvements could include:

stronger cryptographic license validation

hardware-bound licensing