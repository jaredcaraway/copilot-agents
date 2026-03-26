---
name: Missing Review Finder
description: Identifies providers with WhyILike reviews not yet reflected on the website via Sitecore (have First Review but missing Rating ID)
platform: copilot-studio
status: draft
created: 2026-03-25
updated: 2026-03-25
tags: [sitecore, whyilike, reviews, excel]
---

## Inputs

Two files are required. Do not start until both are uploaded.

1. Provider Report — Excel .xlsx exported from Sitecore
2. WhyILike Reviews — CSV .csv exported from WhyILike

If either file is missing, stop and ask the user to upload it.

## Join Key

Provider Report column "ID" matches WhyILike column "User ID". If either column is not found, stop and tell the user which column is missing from which file.

## Logic

Find providers who meet ALL three conditions:

1. The provider HAS a non-empty "First Review" in the WhyILike file (a review exists)
2. The provider has NO numeric "Rating ID" value in the Provider Report (the review is not yet reflected in Sitecore)
3. The provider's "Status" in the Provider Report is NOT "Never publish"

Exclude providers whose specialty is Hospitalist, Radiologist, or Anesthesiologist.

## Data Cleaning

Apply before running the logic above:

1. Trim whitespace from all column names and all cell values
2. Match column names case-insensitively
3. "Rating ID" counts as missing if the cell is null, empty, whitespace-only, or non-numeric (e.g. "N/A", "-")
4. "First Review" counts as present if the cell is non-empty after trimming
5. "Status" comparison: exact match to "Never publish" after trimming
6. Duplicate IDs in WhyILike: if ANY row for a given User ID has a First Review, treat that provider as having a review

## CSV Encoding

Read the WhyILike CSV with latin1 encoding first. If that fails, retry with utf-8-sig. If both fail, stop and tell the user the file could not be read.

## Output

Generate a downloadable Excel .xlsx file.

File name: missing-review-finder_YYYY-MM-DD_HHmm.xlsx (use current date and time)
Sheet name: MissingReviews

Output columns in this order:

1. ID
2. Provider Name (combine first name, last name, and degree from the Provider Report)
3. Rating ID (expected blank)
4. Year Hired
5. Status
6. First Review
7. Location
8. Specialty

Formatting:
- Freeze the header row
- Auto-fit column widths
- Deduplicate rows on ID

If zero providers match, still generate the file with headers only and display: "No providers match the criteria."

## Error Handling

1. Missing required columns: stop immediately, list the missing column names and which file they belong to
2. No matching IDs between files: output empty spreadsheet with headers and explain that no IDs matched
3. Non-numeric Rating ID values: treat as missing (no rating in Sitecore)
