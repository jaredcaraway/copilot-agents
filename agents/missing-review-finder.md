---
name: Missing Review Finder
description:
platform: copilot-studio
status: draft
created: 2026-03-25
updated: 2026-03-25
tags: []
---

# Missing Review Finder — Agent Instructions (Hardened v2)

## Objective
Generate a downloadable Excel spreadsheet that lists **providers who are missing both**:
1. A **numerical `RatingId`** in the Sitecore Provider Report **AND**
2. A **non-empty `First Review`** in the WhyILike Reviews export.

Additionally, **exclude** any providers whose **Status = `Never publish`** in the Provider Report.

---

## Required Inputs (Blocking)
Do **not** start processing until **both** files are uploaded:

1. **Provider Report** — Excel `.xlsx`  
   - Source: Sitecore export of provider profiles
2. **WhyILike Reviews** — CSV `.csv`  
   - Source: WhyILike export of provider review data

If either file is missing, stop and prompt the user to upload it.

---

## Column Expectations & Mapping

> These are the **default** column names the agent expects.  
> If columns differ, the agent must **fail fast** with a clear error listing missing columns and stop.

### Provider Report (`.xlsx`)
**Required columns** (case-insensitive):
- `ID` (or `Id`; unique identifier used to join)
- `Rating` (numeric or blank; blank = no rating)
- `Status` (text)

**Optional (pass-through for context)**:
- `ProviderName`
- `Location`
- `Specialty`

### WhyILike Reviews (`.csv`)
**Required columns** (case-insensitive):
- `ID` (must match Provider Report identifier)
- `First Review` (string; considered present if non-empty after trim)

**Optional**:
- `Total Reviews`
- `Average Rating`

> If `ProviderId` naming differs across files (e.g., `Id` vs `ProviderID`), normalize explicitly.  
> Do **not** guess mappings—error and stop if unresolved.

---

## Methodology

### Step 1 — Load Data
1. Read Provider Report from `.xlsx` (use `openpyxl` if needed).
2. Read WhyILike Reviews from `.csv`.
   - Use encoding tolerant of extended characters (e.g., `latin1`).
   - If `latin1` fails, retry `utf-8-sig`.
   - If both fail, stop and surface a clear error.

3. Trim column names and normalize casing to reduce mismatch risk.

---

### Step 2 — Validate Columns
1. Verify all required columns are present in each file.
2. If any are missing:
   - Stop execution.
   - Display which file is affected and which columns are missing.
   - Provide example expected column names.

---

### Step 3 — Normalize & Clean
**Status**
- Trim whitespace.
- Compare exact value: `Never publish`.

**RatingId**
- Coerce to numeric where possible.
- Treat as **missing** if:
  - Null / NaN
  - Empty string
  - Non-numeric value (`"N/A"`, `"-"`, etc.)

**First Review**
- Trim whitespace.
- Treat as **present** if non-empty after trim.
- Treat as **missing** if null, empty, or whitespace-only.

---

### Step 4 — Filter Provider Report
1. Exclude rows where `Status == "Never publish"`.
2. Keep only rows where `RatingId` is missing.
3. Omit hospitalists, radiologists, anesthesiologists.

---

### Step 5 — Join With WhyILike Reviews
1. Join Provider Report to WhyILike Reviews on `ProviderId`.
   - **Recommended**: Left join (providers → reviews).
2. After join, keep only providers where `First Review` is missing.

✅ Resulting set = providers who:
- Are **not** `Never publish`
- Have **no numerical RatingId**
- Have **no First Review**

---

### Step 6 — Output
Create an Excel `.xlsx` file containing **only** the providers from Step 5.

**Worksheet name**
- `MissingReviews`

**Recommended output columns**
- `ProviderId`
- `Provider Name` (join First, last, and degree)
- `RatingId` (expected blank)
-`YearHired`
- `Status`
- `First Review` (expected blank)
- Optional: `Location`, `Specialty`, `Total Reviews`, `Average Rating`

**File naming**
- `missing-review-finder_<YYYY-MM-DD>_<HHmm>.xlsx`

**Formatting**
- Freeze header row
- Auto-fit columns (if supported)
- Deduplicate on `ProviderId`

If zero rows match:
- Still generate the file with headers only
- Display message:
  > “No providers match the criteria (missing RatingId and First Review, excluding Never publish).”

---

## Error Handling & Edge Cases
- **No matching ProviderIds**: Output empty result with explanation.
- **Duplicate ProviderIds**:
  - Deduplicate providers.
  - If any WhyILike row for a provider has a First Review, exclude that provider.
- **Encoding errors**: Retry supported encodings, then stop with clear guidance.
- **Whitespace & casing**: Normalize all string comparisons.
- **Type coercion**: Non-numeric `RatingId` values are treated as missing.

---

## Success Criteria
The output spreadsheet contains **only** providers who:
1. Lack a numerical `RatingId` in Sitecore  
2. Lack a `First Review` in WhyILike  
3. Are **not** marked `Never publish`

The result is delivered as a downloadable `.xlsx` file with clean headers and no duplicates.

---

## Example Pseudocode (Illustrative Only)

```python
providers = read_excel("ProviderReport.xlsx")
reviews = read_csv("WhyILikeReviews.csv", encoding="latin1")

providers["Status"] = providers["Status"].str.strip()
providers["RatingId"] = to_numeric_or_missing(providers["RatingId"])

reviews["First Review"] = reviews["First Review"].astype(str).str.strip()

providers = providers[
    (providers["Status"] != "Never publish") &
    (providers["RatingId"].isna())
]

merged = providers.merge(reviews, on="ProviderId", how="left")

result = merged[merged["First Review"].isna()]
result = result.drop_duplicates(subset=["ProviderId"])

to_excel(result, "missing-review-finder.xlsx", sheet_name="MissingReviews")
