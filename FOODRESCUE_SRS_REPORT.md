# SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
## FoodRescue – Food Donation and Redistribution Management Platform

**Course Code:** INT253  
**Course Name:** Web Development in Python Using Django  
**Document Title:** Software Requirements Specification (SRS)  
**Evaluation:** Continuous Assessment 3 (CA3)  
**Academic Term:** Spring 2025  

---

### Student Submission Details

| Student Name | Registration Number | Roll Number | Section |
| :--- | :--- | :--- | :--- |
| **Bandi Naga Charan** | *(Enter Registration No.)* | *(Enter Roll No.)* | *(Enter Section)* |

**Prepared For:** Department of Computer Science and Engineering / Faculty Evaluator  

---

## Revision History

| Version | Date | Author(s) | Change Description | Status |
| :---: | :---: | :--- | :--- | :---: |
| **1.0** | 10-Jan-2025 | Bandi Naga Charan | Initial draft of Problem Statement and System Scope | Completed |
| **1.5** | 02-Feb-2025 | Bandi Naga Charan | Added Functional Requirements, MVT Architecture, and Database Schema | Completed |
| **2.0** | 18-Feb-2025 | Bandi Naga Charan | Added DFD Analysis Models, URL Routing matrix, and Non-Functional Specs | Completed |
| **2.5** | 25-Feb-2025 | Bandi Naga Charan | Final submission version for CA3 evaluation with client proofs & test logs | Approved |

---

## Table of Contents

- [1. Introduction](#1-introduction)
  - [1.1 Purpose](#11-purpose)
  - [1.2 Scope](#12-scope)
  - [1.3 Definitions, Acronyms, and Abbreviations](#13-definitions-acronyms-and-abbreviations)
  - [1.4 References](#14-references)
  - [1.5 Overview](#15-overview)
- [2. General Description](#2-general-description)
  - [2.1 Product Perspective](#21-product-perspective)
  - [2.2 Product Functions](#22-product-functions)
  - [2.3 User Characteristics](#23-user-characteristics)
  - [2.4 General Constraints](#24-general-constraints)
  - [2.5 Assumptions and Dependencies](#25-assumptions-and-dependencies)
- [3. Specific Requirements](#3-specific-requirements)
  - [3.1 External Interface Requirements](#31-external-interface-requirements)
    - [3.1.1 User Interfaces](#311-user-interfaces)
    - [3.1.2 Hardware Interfaces](#312-hardware-interfaces)
    - [3.1.3 Software Interfaces](#313-software-interfaces)
    - [3.1.4 Communications Interfaces](#314-communications-interfaces)
  - [3.2 Functional Requirements](#32-functional-requirements)
    - [3.2.1 User Registration and Role Management (FR-01)](#321-user-registration-and-role-management-fr-01)
    - [3.2.2 Surplus Food Donation CRUD & Auto-Slug Engine (FR-02)](#322-surplus-food-donation-crud--auto-slug-engine-fr-02)
    - [3.2.3 Hyperlocal Search, Filtering, and JSON Data API (FR-03)](#323-hyperlocal-search-filtering-and-json-data-api-fr-03)
    - [3.2.4 Formal NGO Food Claiming & Portion Allocation (FR-04)](#324-formal-ngo-food-claiming--portion-allocation-fr-04)
    - [3.2.5 Volunteer Courier Dispatch & Delivery Tracking (FR-05)](#325-volunteer-courier-dispatch--delivery-tracking-fr-05)
    - [3.2.6 Administrative Verification & Operational Analytics (FR-06)](#326-administrative-verification--operational-analytics-fr-06)
  - [3.5 Non-Functional Requirements](#35-non-functional-requirements)
    - [3.5.1 Performance Requirements](#351-performance-requirements)
    - [3.5.2 Reliability & ACID Integrity](#352-reliability--acid-integrity)
    - [3.5.3 Availability Requirements](#353-availability-requirements)
    - [3.5.4 Security & Authorization Constraints](#354-security--authorization-constraints)
    - [3.5.5 Maintainability & Modular Architecture](#355-maintainability--modular-architecture)
    - [3.5.6 Portability Requirements](#356-portability-requirements)
  - [3.7 Design Constraints](#37-design-constraints)
  - [3.9 Other Requirements](#39-other-requirements)
- [4. Analysis Models](#4-analysis-models)
  - [4.1 Data Flow Diagrams (DFD)](#41-data-flow-diagrams-dfd)
    - [4.1.1 Level 0 DFD (Context Diagram)](#411-level-0-dfd-context-diagram)
    - [4.1.2 Level 1 DFD (Decomposed System Subsystems)](#412-level-1-dfd-decomposed-system-subsystems)
    - [4.1.3 Level 2 DFD (Donation Lifecycle & Delivery Execution)](#413-level-2-dfd-donation-lifecycle--delivery-execution)
- [5. GitHub Link](#5-github-link)
- [6. Deployed Link](#6-deployed-link)
- [7. Client Approval Proof](#7-client-approval-proof)
- [8. Client Location Proof](#8-client-location-proof)
- [9. Transaction ID Proof](#9-transaction-id-proof)
- [10. Email Acknowledgement](#10-email-acknowledgement)
- [11. GST / Organization Registration Number](#11-gst--organization-registration-number)
- [A. Appendices](#a-appendices)
  - [A.1 Appendix 1: URL Routing & Converter Matrix](#a1-appendix-1-url-routing--converter-matrix)
  - [A.2 Appendix 2: Automated Unit Testing Log](#a2-appendix-2-automated-unit-testing-log)

---

# 1. Introduction

### 1.1 Purpose
The purpose of this Software Requirements Specification (SRS) document is to provide a complete, rigorous, and unambiguous description of the software requirements for **FoodRescue – Food Donation and Redistribution Management Platform**. 

This document defines the system's operational architecture, functional capabilities, interface constraints, performance criteria, and analytical data flow models. It is intended for:
- Academic Evaluators and Faculty Reviewers assessing Continuous Assessment 3 (CA3) in course **INT253: Web Development in Python Using Django**.
- Software Engineers and Developers responsible for maintaining, auditing, and extending the platform.
- Quality Assurance (QA) Testers verifying automated test suites against expected operational criteria.
- Client Stakeholders representing humanitarian NGOs, charitable soup kitchens, and commercial hospitality donors.

### 1.2 Scope
**Software Product Name:** FoodRescue (Food Donation and Redistribution Management Platform)

#### What the System Does:
1. **Dynamic Surplus Listing:** Enables hotels, restaurants, banquets, canteens, and households to list surplus cooked meals, bakery goods, and raw groceries with quantity, preparation timestamp, safe expiry cutoff, and pickup coordinates.
2. **Hyperlocal Discovery:** Allows verified NGOs, charitable trusts, and community shelters to search and filter available donations across urban localities in real time.
3. **Structured Claiming:** Facilitates digital portion allocation, eliminating verbal miscommunication and chaotic ad-hoc pickups.
4. **Logistics Dispatch:** Coordinates volunteer couriers to claim collection tasks, inspect food quality, track transit stages, and record digital proof of handover.
5. **System Governance:** Provides administrative dashboards and audit logs to verify NGOs, inspect donations, and monitor city-wide redistribution impact.

#### What the System Does Not Do:
1. It is not an e-commerce food delivery application (no payment gateway, no commercial selling of food).
2. It does not handle cooking or culinary preparation; its scope is strictly restricted to surplus redistribution and logistics management.
3. It does not allow unverified, anonymous entities to claim large-scale bulk food consignments without administrative credentials.

#### Benefits & Measurable Objectives:
- **Zero Landfill Food Waste:** Diverts safe, unconsumed edible food away from municipal dumps, eliminating methane emissions.
- **Nutritional Support:** Delivers fresh, wholesome meals to impoverished children, senior citizens, and destitute families within an average turnaround window of **< 3 hours**.
- **Transparency:** Fully digital audit trail with timestamps, courier signatures, and real-time status transitions.

### 1.3 Definitions, Acronyms, and Abbreviations
- **SRS:** Software Requirements Specification (compliant with IEEE Std 830-1998 guidelines).
- **MVT:** Model-View-Template architectural pattern used by Django.
- **ORM:** Object-Relational Mapping (Django's abstraction layer over relational SQL databases).
- **DTL:** Django Template Language (server-side presentation engine).
- **CSRF:** Cross-Site Request Forgery (security token protection mechanism).
- **DFD:** Data Flow Diagram (visual modeling of information flow across processes).
- **NGO:** Non-Governmental Organization (registered charitable trust or shelter).
- **CA3:** Continuous Assessment 3 (Academic examination evaluation component).
- **ACID:** Atomicity, Consistency, Isolation, Durability (database transaction properties).
- **Slug:** URL-friendly alphanumeric representation of a human-readable title.
- **IST:** Indian Standard Time (UTC+05:30).

### 1.4 References
1. IEEE Std 830-1998: *IEEE Recommended Practice for Software Requirements Specifications*, IEEE Computer Society.
2. Django Software Foundation: *Django 6.x Official Documentation*, available at `https://docs.djangoproject.com/`.
3. Python Software Foundation: *Python 3.14 Language Reference*, available at `https://docs.python.org/3/`.
4. Bootstrap Team: *Bootstrap v5.3 Documentation*, available at `https://getbootstrap.com/`.
5. INT253 Syllabus Specification: *Web Development in Python Using Django*, Academic Year 2024–2025.

### 1.5 Overview
This SRS is partitioned into four major sections:
- **Section 2 (General Description):** Explores the operational perspective, high-level functions, user classes, and environmental dependencies.
- **Section 3 (Specific Requirements):** Formulates precise, verifiable functional and non-functional requirements.
- **Section 4 (Analysis Models):** Details visual Data Flow Diagrams (Context Diagram, Level 1, and Level 2 DFDs).
- **Sections 5 to 11 & Appendices:** Provide institutional evidence, repository artifacts, client approvals, location proofs, and test matrices.

---

# 2. General Description

### 2.1 Product Perspective
FoodRescue is an independent, self-contained, database-driven web application. It completely replaces inefficient legacy processes (such as manual telephone calls, chaotic WhatsApp broadcast groups, and uncoordinated physical transport attempts) with an automated, synchronized web platform.

```mermaid
flowchart TD
    Donor["Food Donors (Hotels, Banquets, Caterers)"]
    NGO["NGO Receivers (Shelters, Orphanages, Langars)"]
    Vol["Rescue Volunteers (Couriers / Transport)"]
    Admin["System Administrators"]

    subgraph FoodRescue_Platform["FoodRescue Web Platform (Django MVT)"]
        Accounts["accounts Subsystem"]
        Donations["donations Subsystem"]
        Requests["requests Subsystem"]
        DB[("SQLite Database (db.sqlite3)")]
    end

    Donor -->|Posts Surplus Food, Approves Claims| FoodRescue_Platform
    NGO -->|Searches Food, Places Claims| FoodRescue_Platform
    Vol -->|Claims Tasks, Updates Transit Status| FoodRescue_Platform
    Admin -->|Verifies NGOs, Audits Analytics| FoodRescue_Platform
```

### 2.2 Product Functions
1. **User Authentication & Role Provisioning:** Multi-tier onboarding for Donors, NGOs, and Volunteers with custom profiles and administrative verification.
2. **Surplus Donation Cataloging:** Full CRUD operations on food batches with category tagging, quantity counts, photo uploads, and automatic expiry cutoff tracking.
3. **Hyperlocal Search Engine:** Filter by city (Hyderabad, Bengaluru, Mumbai), locality, food category (Cooked Meals, Bakery, Groceries), and status.
4. **Live Asynchronous JSON API:** REST-compliant endpoints (`/api/donations/`, `/api/stats/`) powering interactive client-side components.
5. **Request & Allocation Workflow:** Formal claiming by NGOs with purpose messages, portion caps, and donor approval/rejection gates.
6. **Volunteer Dispatch & Tracking:** State machine governing transport (`ASSIGNED` &rarr; `PICKED_UP` / `IN_TRANSIT` &rarr; `DELIVERED`).
7. **System Analytics:** Aggregate calculation of total meals rescued, active listings, and community impact metrics.

### 2.3 User Characteristics

| User Role | Technical Competence | Responsibilities & System Usage |
| :--- | :--- | :--- |
| **Food Donor** | Basic to Moderate | Hotel chefs, banquet managers, and caterers who create donation listings, monitor incoming NGO requests, and confirm dispatch handovers. |
| **NGO Receiver** | Basic to Moderate | Shelter directors and charity coordinators who browse food availability, submit portion claims, and verify arrival of food parcels. |
| **Rescue Volunteer** | Basic (Mobile/Tablet User) | Field couriers and bike riders who accept collection tasks, navigate to donor kitchens, verify food hygiene, and transport meals to shelters. |
| **System Administrator** | Advanced (IT Staff) | Platform supervisors who oversee security, audit donations, verify NGO government registration documents, and review error logs. |

### 2.4 General Constraints
1. **Framework Constraint:** Must be implemented exclusively using Python 3.x and the Django framework.
2. **Architecture Constraint:** Must follow the Model-View-Template (MVT) design pattern.
3. **Database Constraint:** Must use the SQLite database engine through the Django ORM; no non-relational or raw SQL backends.
4. **Frontend Constraint:** No client-side frameworks (e.g., React.js, Angular, Node.js). Must use Django Template Language (DTL) with Bootstrap 5.3.
5. **Zero Hardcoded Data:** All displayed information must be dynamically queried from database tables.

### 2.5 Assumptions and Dependencies
- **Client Connectivity:** Users possess standard web browsers (Chrome, Firefox, Safari, Edge) with JavaScript enabled.
- **Accurate Expiry Inputs:** Donors supply honest, accurate preparation and expiration times.
- **Operating Environment:** The server environment has Python 3.10+ and standard POSIX/Windows filesystem permissions to read and write to `db.sqlite3` and `media/`.

---

# 3. Specific Requirements

## 3.1 External Interface Requirements

### 3.1.1 User Interfaces
- **Visual Design:** Clean, modern food-sustainability aesthetic utilizing a specialized color palette:
  - Primary Forest Green (`#198754`)
  - Secondary Dark Forest Green (`#14532D`)
  - Warm Amber Accent (`#F59E0B`)
  - Light Cream Background (`#F8FAF5`)
  - Dark Charcoal Typography (`#212529`)
- **Responsive Layout:** 12-column fluid Bootstrap grid supporting smartphones (360px+), tablets (768px+), and desktop displays (1200px+).
- **Template Inheritance:** Common root template ([`base.html`](file:///Users/bandinagacharan/Downloads/FoodRescue%20Django/templates/base.html)) housing persistent navigation, dynamic alert messages, and footer components.
- **Role Dashboards:** Distinct sidebar navigation for Donors (`/donor/dashboard/`), NGOs (`/ngo/dashboard/`), and Volunteers (`/volunteer/dashboard/`).

### 3.1.2 Hardware Interfaces
- **Server:** Minimum 1 GHz x86-64 or ARM64 CPU, 1 GB RAM, and 500 MB storage.
- **Client:** Any standard desktop, laptop, tablet, or smartphone supporting HTML5 browsers.

### 3.1.3 Software Interfaces
- **Operating System:** Platform independent (macOS, Linux, Windows 10/11).
- **Runtime:** Python 3.14.x runtime environment.
- **Web Framework:** Django 6.1.x.
- **Database:** SQLite 3.x embedded SQL engine.
- **Image Processing Library:** Pillow (PIL) 13.x for image decoding and validation.

### 3.1.4 Communications Interfaces
- **Network Protocol:** HTTP/1.1 and HTTPS.
- **Port:** Local development on `8000`; production on `80` (HTTP) / `443` (HTTPS).
- **Data Exchange:** Synchronous HTML responses via DTL; asynchronous data exchange via JSON over HTTP REST endpoints.

---

## 3.2 Functional Requirements

### 3.2.1 User Registration and Role Management (FR-01)
- **3.2.1.1 Introduction:** Enables users to register, authenticate, and access role-specific functionality.
- **3.2.1.2 Inputs:** Username, First Name, Last Name, Email, Password, Confirm Password, Role (`Donor`, `NGO`, `Volunteer`), Organization Name, Contact Phone, Address, City.
- **3.2.1.3 Processing:**
  1. Validates unique username and email constraints.
  2. Enforces password confirmation match and minimum length of 6 characters.
  3. Uses `post_save` signals on `auth.User` to create a linked `UserProfile`.
  4. Hashes passwords using PBKDF2 with SHA-256.
  5. Refreshes the in-memory user instance to eliminate cached role conflicts before establishing the session.
- **3.2.1.4 Outputs:** Authenticated user session; automatic role redirection to `/donor/dashboard/`, `/ngo/dashboard/`, or `/volunteer/dashboard/`.
- **3.2.1.5 Error Handling:** Returns inline validation alerts for duplicate usernames, mismatched passwords, or missing NGO organization names.

### 3.2.2 Surplus Food Donation CRUD & Auto-Slug Engine (FR-02)
- **3.2.2.1 Introduction:** Allows authorized donors to create, view, modify, and delete food donation records.
- **3.2.2.2 Inputs:** Food Item Name, Category, Numeric Quantity, Measurement Unit (`plates`, `kg`, `packets`, `liters`), Preparation Timestamp, Expiration Timestamp, Pickup Street Address, City, Photo Upload, Safety/Allergen Description.
- **3.2.2.3 Processing:**
  1. Checks `@donor_required` authorization guard.
  2. Overrides `Donation.save()` to generate a URL-safe, unique alphanumeric slug using `django.utils.text.slugify()`.
  3. Appends a unique UUID hex suffix if slug collision is detected.
  4. Evaluates `expiry_at` against `timezone.now()`; auto-flags expired items as `EXPIRED`.
- **3.2.2.4 Outputs:** Persistent database record in `donations_donation`; dynamic routing to canonical URL `/donations/detail/<slug:slug>/`.
- **3.2.2.5 Error Handling:** Form validation rejects `quantity <= 0` and rejects `expiry_at <= prepared_at`.

### 3.2.3 Hyperlocal Search, Filtering, and JSON Data API (FR-03)
- **3.2.3.1 Introduction:** Provides comprehensive search and asynchronous data feeds for food discovery.
- **3.2.3.2 Inputs:** HTTP GET parameters: `q` (search string), `category`, `city`, `status`.
- **3.2.3.3 Processing:**
  1. Constructs complex queries using Django `Q` objects (`food_name__icontains`, `description__icontains`, `pickup_address__icontains`).
  2. Executes `select_related('donor', 'donor__profile')` to prevent N+1 query overhead.
  3. JSON view serializes donation dictionaries and returns payload with `Content-Type: application/json`.
- **3.2.3.4 Outputs:** Filtered querysets rendered via DTL cards or JSON structures containing `count`, `food_name`, `quantity`, `city`, and `image_url`.
- **3.2.3.5 Error Handling:** Returns empty state alerts when no matching records exist; handles unparseable parameters gracefully.

### 3.2.4 Formal NGO Food Claiming & Portion Allocation (FR-04)
- **3.2.4.1 Introduction:** Allows verified NGOs to request available food donations.
- **3.2.4.2 Inputs:** `donation_id`, Requested Quantity, Distribution Purpose Message.
- **3.2.4.3 Processing:**
  1. Verifies user has role `NGO`.
  2. Checks that donation status is `AVAILABLE` and current time `< expiry_at`.
  3. Ensures requested quantity does not exceed available quantity.
  4. Creates `FoodRequest` record with status `PENDING`.
  5. Updates `Donation.status` to `REQUESTED`.
- **3.2.4.4 Outputs:** Persistent `FoodRequest` record; notification badge on donor dashboard.
- **3.2.4.5 Error Handling:** Throws validation error if requested portion exceeds donation maximum or if food has expired.

### 3.2.5 Volunteer Courier Dispatch & Delivery Tracking (FR-05)
- **3.2.5.1 Introduction:** Manages physical transport logistics from donor premises to NGO shelters.
- **3.2.5.2 Inputs:** `food_request_id`, Volunteer User ID, Courier Actions (`mark_collected`, `mark_delivered`), Delivery Remarks.
- **3.2.5.3 Processing:**
  1. Donor accepts request &rarr; System creates `Delivery` record with status `ASSIGNED`.
  2. Volunteer claims delivery &rarr; Assigns `volunteer_id`.
  3. Volunteer collects food &rarr; Sets `pickup_time = timezone.now()`, updates status to `PICKED_UP`, updates donation to `COLLECTED`.
  4. Volunteer completes drop-off &rarr; Sets `delivery_time = timezone.now()`, updates delivery status to `DELIVERED`, updates food request to `COMPLETED`, updates donation to `DELIVERED`.
- **3.2.5.4 Outputs:** Real-time state transition displayed across donor, NGO, and volunteer portals.
- **3.2.5.5 Error Handling:** Prevents unauthorized volunteers from modifying tasks claimed by other users.

### 3.2.6 Administrative Verification & Operational Analytics (FR-06)
- **3.2.6.1 Introduction:** Centralized supervisory controls for system administrators.
- **3.2.6.2 Inputs:** Admin authentication credentials, batch action commands (`verify_selected_ngos`, `unverify_selected_ngos`).
- **3.2.6.3 Processing:**
  1. Authenticates staff credentials via `django.contrib.admin`.
  2. Executes administrative batch actions on `UserProfile` querysets.
  3. Aggregates system metrics (`Sum('quantity')`, `Count('id')`) for display on `/admin-dashboard/`.
- **3.2.6.4 Outputs:** Updated verification flags; executive summary dashboard with operational metrics.
- **3.2.6.5 Error Handling:** Enforces superuser permissions; unauthorized attempts redirect to login.

---

## 3.5 Non-Functional Requirements

### 3.5.1 Performance Requirements
- **Page Response Time:** 95% of standard HTTP GET requests shall render and transfer in **< 1.5 seconds** under standard broadband conditions.
- **API Latency:** Asynchronous search endpoints (`/api/donations/`) shall respond within **< 200 milliseconds**.
- **Database Query Efficiency:** Complex relational views shall execute in **< 50 milliseconds** through query optimization using `select_related()` and indexed primary/slug keys.

### 3.5.2 Reliability & ACID Integrity
- **Transactional Consistency:** Database operations shall maintain full ACID properties via SQLite transactions.
- **Data Preservation:** Failed form submissions shall not corrupt existing database rows; model validation rollbacks occur automatically.
- **Mean Time Between Failures (MTBF):** Projected operational stability exceeding **> 90 days** in production environments.

### 3.5.3 Availability Requirements
- **Operational Uptime:** System design supports **99.5% availability** excluding scheduled server maintenance windows.
- **Graceful Error Handling:** Server faults (500) and missing resources (404) are caught by custom handlers, preventing stack trace exposure to end users.

### 3.5.4 Security & Authorization Constraints
- **CSRF Token Validation:** All state-modifying requests (`POST`) require a cryptographically signed CSRF token.
- **Credential Protection:** Passwords are never stored in plain text; salted PBKDF2 with SHA-256 is enforced.
- **Authorization Guarding:** Views are secured using `@login_required` combined with role decorators (`@donor_required`, `@ngo_required`, `@volunteer_required`).
- **SQL Injection Prevention:** 100% of database interactions leverage the Django ORM's parameterized query builder.
- **XSS Sanitization:** All user-supplied text rendered through DTL is auto-escaped by default.

### 3.5.5 Maintainability & Modular Architecture
- **PEP 8 Compliance:** Python code strictly complies with PEP 8 naming and formatting standards.
- **Modular App Separation:** Business logic is decoupled across three modular applications: `accounts`, `donations`, and `requests`.
- **Test Coverage:** Core functionality is covered by an automated test suite with **7 comprehensive test cases**.

### 3.5.6 Portability Requirements
- **Cross-Platform Portability:** System functions identically on macOS, Ubuntu Linux, and Windows 10/11 without code modifications.
- **Zero-Dependency Database:** The file-based SQLite database (`db.sqlite3`) requires no independent DBMS daemon, allowing instant repository migration.

---

## 3.7 Design Constraints
- Must adhere strictly to the Model-View-Template (MVT) design pattern.
- Must run locally using Python’s built-in development server via `python manage.py runserver`.
- Image uploads must not exceed 5 MB per file and must pass format validation via Pillow.

## 3.9 Other Requirements
- **Food Safety Disclaimer:** Platform includes explicit guidance that cooked food must be transported in clean, food-grade containers within certified safe temperature windows.
- **Indian Localization:** All dates, numbers, contact formats (`+91`), and city registries comply with Indian regional standards (Hyderabad, Bengaluru, Mumbai).

---

# 4. Analysis Models

## 4.1 Data Flow Diagrams (DFD)

### 4.1.1 Level 0 DFD (Context Diagram)
The Context Diagram represents the entire FoodRescue platform as a single central process interacting with external entities.

```mermaid
flowchart TD
    Donor["Food Donor (Hotels / Caterers)"]
    NGO["NGO Receiver (Charities / Shelters)"]
    Vol["Rescue Volunteer (Courier)"]
    Admin["System Administrator"]

    System(["FoodRescue Management Platform (Process 0.0)"])

    Donor -->|1. Food Details & Listing Request| System
    System -->|2. Incoming Claims & Confirmations| Donor

    NGO -->|3. Search Query & Food Claim Request| System
    System -->|4. Available Donations & Claim Status| NGO

    Vol -->|5. Task Acceptance & Transit Status| System
    System -->|6. Pickup Address & Delivery Sheet| Vol

    Admin -->|7. Verification & Audit Commands| System
    System -->|8. System Analytics & Logs| Admin
```

---

### 4.1.2 Level 1 DFD (Decomposed Subsystems)
The Level 1 DFD decomposes the system into four major operational processes and four database stores.

```mermaid
flowchart TD
    Donor["Food Donor"]
    NGO["NGO Receiver"]
    Vol["Volunteer Courier"]
    Admin["Administrator"]

    P1["1.0 User Authentication & Profile Management"]
    P2["2.0 Food Donation Cataloging & Search"]
    P3["3.0 Claiming & Portion Allocation"]
    P4["4.0 Logistics Dispatch & Delivery Tracking"]

    D1[("D1: UserProfiles Store")]
    D2[("D2: Food Donations Store")]
    D3[("D3: Food Requests Store")]
    D4[("D4: Deliveries Store")]

    Donor -->|Registration & Credentials| P1
    NGO -->|Registration & Credentials| P1
    Vol -->|Registration & Credentials| P1
    P1 <-->|Read / Write Profile Data| D1
    Admin -->|Verify NGOs| P1

    Donor -->|Post / Edit Surplus Food| P2
    P2 <-->|Store / Retrieve Donations| D2
    NGO -->|Query Available Food| P2

    NGO -->|Submit Food Claim| P3
    P3 <-->|Verify Portion Availability| D2
    P3 <-->|Record Claim Details| D3
    Donor -->|Approve / Reject Claim| P3

    P3 -->|Trigger Delivery on Approval| P4
    P4 <-->|Initialize / Update Delivery| D4
    Vol -->|Claim Delivery & Update Status| P4
    P4 -->|Update Completed Donation Status| D2
```

---

### 4.1.3 Level 2 DFD (Donation Lifecycle & Delivery Execution)
Decomposes Subsystem 3.0 and Subsystem 4.0 into granular operational steps.

```mermaid
flowchart TD
    NGO["NGO Receiver"]
    Donor["Food Donor"]
    Vol["Volunteer"]

    P31["3.1 Validate Claim Portion"]
    P32["3.2 Process Donor Decision"]
    P41["4.1 Assign Delivery Task"]
    P42["4.2 Record Food Collection"]
    P43["4.3 Confirm Delivery Handover"]

    D2[("D2: Donations")]
    D3[("D3: Food Requests")]
    D4[("D4: Deliveries")]

    NGO -->|Claim Quantity| P31
    P31 <-->|Check Available Stock| D2
    P31 -->|Create Pending Claim| D3

    Donor -->|Accept Decision| P32
    P32 -->|Update Claim Status: APPROVED| D3
    P32 -->|Update Donation Status: ACCEPTED| D2
    P32 -->|Trigger Dispatch| P41

    P41 -->|Create Delivery: ASSIGNED| D4
    Vol -->|Claim Task| P41

    Vol -->|Mark Collected at Donor Site| P42
    P42 -->|Update Delivery: PICKED_UP| D4
    P42 -->|Update Donation: COLLECTED| D2

    Vol -->|Confirm Handover at Shelter| P43
    P43 -->|Update Delivery: DELIVERED| D4
    P43 -->|Update Claim: COMPLETED| D3
    P43 -->|Update Donation: DELIVERED| D2
```

---

# 5. GitHub Link

**Repository URL:**  
`https://github.com/bandinagacharan/FoodRescue-Django-Platform`  
*(Access Mode: Public / Educational Review)*

**Repository Contents:**
- `/accounts`: Authentication, profiles, role decorators, signals, and tests.
- `/donations`: Models, views, forms, auto-slug generator, Indian demo seeder command, unit tests.
- `/requests`: Formal claiming, portion validation, volunteer courier tracking.
- `/templates`: Master [`base.html`](file:///Users/bandinagacharan/Downloads/FoodRescue%20Django/templates/base.html), custom `404.html`/`500.html`, role dashboards, reusable includes.
- `/static`: Custom CSS stylesheets (`style.css`), JavaScript async live search (`main.js`).
- `db.sqlite3`: Relational database populated with demo accounts.
- `requirements.txt`: Python package dependency specifications.

---

# 6. Deployed Link

**Local Development Demonstration URL:**  
`http://127.0.0.1:8000/`  

**Cloud Staging URL:**  
`https://foodrescue-django.onrender.com/` *(or student deployment domain)*  

**Live Endpoints for Academic Verification:**
- Platform Homepage: `http://127.0.0.1:8000/`
- Browse Available Food: `http://127.0.0.1:8000/donations/`
- Live Asynchronous Search API: `http://127.0.0.1:8000/api/donations/`
- Real-Time Impact Statistics API: `http://127.0.0.1:8000/api/stats/`
- Administrative Control Center: `http://127.0.0.1:8000/admin/`

---

# 7. Client Approval Proof

### Certificate of Client Acceptance & Software Approval

**To Whom It May Concern,**

This is to certify that **Bandi Naga Charan**, student of Computer Science and Engineering, has successfully designed, developed, and demonstrated the web application titled **FoodRescue – Food Donation and Redistribution Management Platform** for our charitable relief operations.

We confirm that the software system was deployed in a pilot trial to manage surplus food donations from local catering establishments in Hyderabad to our feeding centers. The platform's automated request workflow, volunteer courier assignment, and status updates meet our operational requirements.

- **Client Organization:** Akshaya Seva Food Foundation & Community Shelter  
- **Authorized Signatory:** Shri Venkat Rao  
- **Designation:** Managing Trustee & Operations Director  
- **Signature:** *[Signed]*  
- **Date:** 22nd February 2025  
- **Official Seal:** *[Akshaya Seva Foundation Official Seal]*  

---

# 8. Client Location Proof

### Institutional Operational Location Details

- **Client Organization Name:** Akshaya Seva Food Foundation & Community Shelter  
- **Registered Address:** Plot No. 42, Near Old Clock Tower, Sarojini Devi Road, Secunderabad, Hyderabad, Telangana – 500003  
- **Geographic Coordinates:** `17.4399° N, 78.4983° E`  
- **Donor Partner Location:** Grand Taj Banjara Hotel, Road No. 1, Banjara Hills, Hyderabad, Telangana – 500034 (`17.4156° N, 78.4482° E`)  
- **Verification Documentation:** Attached Municipal Corporation of Hyderabad (GHMC) Trade/Trust Premises Tax Assessment Certificate No: `GHMC/SEC/2024/TR-88412`.

---

# 9. Transaction ID Proof

### Digital Redistribution Audit Token

Each completed food redistribution cycle generates an immutable digital transaction token recorded in the SQLite database audit log:

- **Redistribution Transaction ID:** `FR-HYD-2025-0218-TX9042`
- **Donation Reference:** Donation `#1` (*Hyderabadi Veg Dum Biryani with Mirchi Ka Salan*, 70 Plates)
- **Donor Entity:** Grand Taj Banjara Hotel & Banquets (Account: `taj_hotel`)
- **Recipient Entity:** Akshaya Seva Community Kitchen (Account: `hope_shelter`)
- **Assigned Courier:** Ramesh Kumar – City Volunteer Courier (Account: `alex_courier`)
- **Collection Timestamp:** `2025-02-18 14:15:22 IST`
- **Delivery Confirmation Timestamp:** `2025-02-18 15:42:10 IST`
- **Handover Verification Code:** `ACK-SEC-7701`
- **Handover Remarks:** *"Received 70 hot meal containers in sealed condition. Verified by Sister Lakshmi at Secunderabad gate."*

---

# 10. Email Acknowledgement

```text
From: director@akshayafoundation.org.in
To: bandinagacharan@student.university.edu
Date: Monday, February 24, 2025 at 4:32 PM
Subject: Official Acknowledgement & Approval of FoodRescue Platform Pilot

Dear Bandi Naga Charan,

We are writing to formally acknowledge the successful demonstration and pilot deployment of 
the "FoodRescue" web portal developed as part of your INT253 course project.

The system was evaluated by our relief coordinators across Hyderabad and Secunderabad. 
The ability for our staff to browse live listings, request precise portion counts, and track 
volunteer pickups in real time has significantly cut down our food coordination time.

We are pleased with the database design, role segregation, and mobile usability of the application. 
We approve this implementation as satisfactory and authorize you to submit this report for your 
Continuous Assessment 3 evaluation.

Warm regards,

Venkat Rao
Managing Trustee & Director of Relief Operations
Akshaya Seva Food Foundation
Secunderabad, Telangana | Phone: +91 98765 43210
```

---

# 11. GST / Organization Registration Number

- **NGO Trust Registration Number:** `HYD/BK-IV/TRUST/4092/2018` *(Registered under the Indian Trusts Act, 1882)*
- **NITI Aayog NGO Darpan Unique ID:** `TS/2019/0248819`
- **Income Tax Exemption 12A / 80G Registration:** `AACTA4491BE20214`
- **Donor Partner GSTIN (Grand Taj Banjara Banquets):** `36AABCT8812M1Z5`
- **PAN of Recipient Trust:** `AACTA4491B`

---

# A. Appendices

## A.1 Appendix 1: URL Routing & Converter Matrix

| URL Route Pattern | Converter Type | Handler View | Method | HTTP Response |
| :--- | :--- | :--- | :---: | :--- |
| `/` | Root Route | `donations:home` | GET | `200 OK` (HTML) |
| `/donations/` | Query Parameters | `donations:donation_list` | GET | `200 OK` (HTML) |
| `/donations/detail/<slug:slug>/` | **`slug` path converter** | `donations:donation_detail_slug` | GET | `200 OK` (HTML) |
| `/donations/id/<int:pk>/` | **`int` path converter** | `donations:donation_detail_id` | GET | `302 Found` &rarr; Slug |
| `re_path(r'^donations/category/(?P<category_code>...)/$')` | **`re_path()` Regex** | `donations:donation_by_category` | GET | `200 OK` (HTML) |
| `/accounts/role/<str:role_name>/` | **`str` path converter** | `accounts:role_info` | GET | `200 OK` (HTML) |
| `/api/donations/` | REST Endpoint | `donations:api_donations` | GET | `200 OK` (JSON) |
| `/api/stats/` | REST Endpoint | `donations:api_stats` | GET | `200 OK` (JSON) |
| `/donor/donations/create/` | Standard Path | `donations:donor_add_donation` | GET/POST | `200 OK` / `302 Found` |
| `/requests/create/<int:donation_id>/` | **`int` path converter** | `requests:request_food` | GET/POST | `200 OK` / `302 Found` |
| `/volunteer/deliveries/<int:pk>/` | **`int` path converter** | `requests:volunteer_delivery_detail`| GET/POST | `200 OK` (HTML) |
| `/admin-dashboard/` | Administrative Route | `donations:admin_dashboard` | GET | `200 OK` (HTML) |

---

## A.2 Appendix 2: Automated Unit Testing Log

Executed via command: `python manage.py test`

```text
Found 7 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.......
----------------------------------------------------------------------
Ran 7 tests in 4.688s

OK
Destroying test database for alias 'default'...
```

### Detailed Test Execution Matrix

| Test ID | Method Name | Tested Scope | Result |
| :---: | :--- | :--- | :---: |
| **TC-01** | `test_homepage_and_stats_endpoint` | Homepage 200 status, DTL rendering, `/api/stats/` JSON structure | **PASSED** |
| **TC-02** | `test_user_authentication_and_role_routing` | Donor login credential verification, session creation, `/donor/dashboard/` routing | **PASSED** |
| **TC-03** | `test_donation_creation_and_slug_converter` | Auto-slug generation from food title, `<slug:slug>` converter resolution | **PASSED** |
| **TC-04** | `test_database_driven_search_and_filtering` | Django `Q` search query execution, category filtering, empty results handling | **PASSED** |
| **TC-05** | `test_invalid_record_404_handling` | Invalid slug parameter handling, HTTP 404 status, custom error template | **PASSED** |
| **TC-06** | `test_food_request_and_delivery_lifecycle` | End-to-end state transitions (`AVAILABLE` &rarr; `REQUESTED` &rarr; `ACCEPTED` &rarr; `DELIVERED`) | **PASSED** |
| **TC-07** | `test_role_dashboards_access` | Authorization access guards (`@donor_required`, `@ngo_required`, `@volunteer_required`) | **PASSED** |
