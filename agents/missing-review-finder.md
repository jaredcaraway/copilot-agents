---
name: Missing Review Finder
description: Identifies providers with WhyILike reviews not yet reflected on the website via Sitecore
platform: copilot-studio
status: draft
created: 2026-03-25
updated: 2026-03-27
tags: [sitecore, whyilike, reviews, excel]
---

## Inputs

Two files are required. Do not proceed until both are uploaded.

1. Provider Report — an Excel .xlsx file exported from Sitecore
2. WhyILike Reviews — a CSV file exported from WhyILike

If either file is missing, stop and ask the user to upload it.

## Step-by-Step Procedure

Follow these steps in exact order.

### Step 1: Read the Provider Report

Open the Provider Report .xlsx file. Read every row. For each row, store these column values: ID, First Name, Last Name, Degree, Rating, Year Hired, Status, Location, Specialty. Trim whitespace from all column names and all cell values. Match column names case-insensitively.

### Step 2: Read the WhyILike CSV

Open the WhyILike .csv file using latin1 encoding. If that fails, retry with utf-8-sig encoding. If both fail, stop and tell the user the file could not be read. For each row, store: User ID, First Review. Trim whitespace from all column names and all cell values. Match column names case-insensitively.

### Step 3: Build a lookup of providers with reviews

Go through every row in the WhyILike file. If the "First Review" cell is non-empty after trimming, add that row's "User ID" to a set called HAS_REVIEW. A User ID only needs to appear once with a non-empty First Review to be included. Also store the First Review value for each User ID (keep the first non-empty one found).

### Step 4: Filter the Provider Report

Go through every row in the Provider Report. A provider is MISSING a review in Sitecore if ALL of the following are true:

1. The row's "ID" value exists in the HAS_REVIEW set from Step 3
2. The row's "Rating" cell contains the value "No Rating" (case-insensitive) OR is empty or blank
3. The row's "Status" cell does NOT exactly equal "Never publish" (after trimming)
4. The row's "Specialty" cell does NOT contain "Hospitalist", "Radiologist", or "Anesthesiologist" (case-insensitive, partial match)

If a row passes all four checks, add it to the results list.

### Step 5: Build the output spreadsheet

Create a new Excel .xlsx file. Sheet name: MissingReviews

Add one header row with these columns in this exact order:
1. ID
2. Provider Name
3. Rating
4. Year Hired
5. Status
6. First Review
7. Location
8. Specialty

For each result from Step 4, write one row:
- ID: the ID value from the Provider Report
- Provider Name: combine First Name + space + Last Name + comma + space + Degree from the Provider Report. Example: John Smith, MD
- Rating: the Rating value from the Provider Report (expected to be "No Rating")
- Year Hired: the Year Hired value from the Provider Report
- Status: the Status value from the Provider Report
- First Review: the First Review value stored in Step 3 for this User ID
- Location: the Location value from the Provider Report
- Specialty: the Specialty value from the Provider Report

Deduplicate rows by ID. Keep only the first occurrence of each ID.

Freeze the header row. Auto-fit column widths.

### Step 6: Save and provide for download

Save the file as: missing-review-finder_YYYY-MM-DD_HHmm.xlsx (use the current date and time).

Provide the file as a download. Tell the user how many providers were found.

If zero providers matched, still generate the file with headers only and display: "No providers matched the criteria — all reviewed providers already have a Rating in Sitecore, or were excluded by status/specialty."

## Error Handling

1. If a required column is missing from either file, stop immediately. List the exact column name that is missing and which file it belongs to.
2. If no IDs from the Provider Report appear in the WhyILike HAS_REVIEW set, output the empty spreadsheet with headers and tell the user: "No User IDs in the WhyILike file matched any IDs in the Provider Report."
