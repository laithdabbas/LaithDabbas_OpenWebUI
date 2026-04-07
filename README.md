# OpenWebUI Engineering Extension

## Overview

This repository contains an extended version of **OpenWebUI v0.6.5** developed as part of the AI Academy Final Assignment.

The goal of this project is to demonstrate software engineering skills by extending an existing system with new features while maintaining good architecture, maintainability, and security considerations.

The implementation focuses on an **offline license enforcement mechanism** and additional system improvements integrated directly into the OpenWebUI codebase.

---

# Implemented Features

## 1. Offline License Enforcement System (Required Feature)

A licensing mechanism was implemented to control the **maximum number of users allowed to register** in the system.

### Key Characteristics

* Works in a **fully offline environment**
* Does **not depend on external license servers**
* Prevents user registrations when the license limit is reached
* Integrated directly into the **signup flow**
* Implemented on the **backend side to prevent bypass**

### How It Works

1. The system reads a local configuration file:

```
license.json
```

Example:

```json
{
  "max_users": 5,
  "signature": "encrypted_hash"
}
```

2. When a user attempts to register:

   * The system counts existing users in the database
   * Compares the number with the license limit
   * Blocks the registration if the limit is exceeded

3. If the limit is reached, the API returns:

```
License limit reached
```

---

## 2. Additional Feature



Example:

### Auditable Activity Trail

A structured audit logging system was implemented to track sensitive operations such as:

* user creation
* permission changes
* license-related actions
* configuration updates

The audit records are stored and displayed in a dedicated **Admin Audit Page** within the OpenWebUI interface.

---

# Project Structure

```
OpenWebUI/
│
├── backend/
│
├── services/
│   └── license_service.py
│
├── license.json
│
└── deliverables/
```

---

# Setup Instructions

### Requirements

* Docker
* Docker Compose

### Run the System

Clone the repository:

```
git clone <repository_url>
```

Navigate to the project:

```
cd OpenWebUI
```

Start the application:

```
docker compose up -d
```

Open the UI:

```
http://localhost:3000
```

---

# Testing the License Feature

1. Open the application
2. Create new users
3. Once the number of users reaches the configured limit, new registrations will be blocked.

Example response:

```
License limit reached
```

---

# Deliverables Folder

All materials required for grading are located in:

```
deliverables/
```

This folder includes:

* setup and running instructions
* license configuration example
* rationale / engineering decisions document
* testing instructions

---

# Documentation

Additional documentation is provided in the **deliverables folder**, including:

* Setup Guide
* Rationale and Engineering Decisions
* Feature Testing Instructions

---

# Author

**Laith Dabbas**
Artificial Intelligence & Robotics Student
Al-Balqa Applied University
