# Provider Biography Document Processing Instructions

## Objective
Process Word documents containing new provider information and extract data into a structured spreadsheet format for easy copy/paste into Sitecore CMS.

## Input Document Structure
Word documents follow a consistent field-label format with the provider information following each label.

## Output Spreadsheet Structure

### Column Headers (in order):
1. Page Title
2. Meta Description
3. Name
4. Gender
5. Specialty
6. Chief
7. Location(s)
8. Language(s)
9. KSC Start Month and Year
10. Biography Section (formatted HTML) containing copy for bio section as well as philosophy of care.
11. Hobbies and Interests
12. Awards and Publications
13. Medical School
14. Residency/Fellowship (combined)
15. Board Certification(s)
16. Professional Associations
17. Hospital Affiliation
18. ANOW


## Processing Rules by Field

### Simple Copy Fields (Extract as-is)
These fields can be copied directly from the document to the spreadsheet:
- **Page Title**
- **Meta Description**
- **Name**
- **Gender**
- **Specialty**
- **Chief**
- **Location(s)**
- **Language(s)**
- **KSC Start Month and Year**
- **Board Certification(s)**
- **Professional Associations**
- **Hospital Affiliation**
- **ANOW**

### Biography Section (Requires HTML Formatting)

**Extract from:** Everything below the "Biography Section" heading up to (but not including) "Awards & Publications"

**Formatting requirements:**
1. Start extraction immediately after "Biography Section" heading (do not include the heading itself)
2. Identify subsection headings:
   - "Philosophy of Care"
3. Mark all subsection headings as `<h3>Heading Text</h3>`
4. Wrap each paragraph in `<p>` tags
5. Maintain paragraph breaks between sections
6. Then do the same separate for Hobbies & Interests and Awards & Publications (see special instructions below for this section)

**Example output:**
```html
<p>Raymond Nieto, MD, is a graduate of Baylor College of Medicine...</p>

<p>Dr. Nieto was inspired to pursue his passion...</p>

<h3>Philosophy of Care</h3>
<p>Dr. Nieto listens carefully and explains...</p>



### Awards & Publications Section (Special Handling)

**Location:** Within Biography Section, may or may not exist

**Scenarios:**
1. **Both Awards and Publications present**
2. **Only Awards present**
3. **Only Publications present**
4. **Neither present** (omit section entirely)

**Processing rules:**

1. **If Awards exist:**
   - Add heading: `<h3>Awards</h3>`
   - Convert each award to an unordered list item
   - Even single awards should be in `<ul>` tags
   
   Example:
   ```html
   <h3>Awards</h3>
   <ul>
   <li>IES Hospital Medicine Physician of the Year, 2023</li>
   </ul>
   ```

2. **If Publications exist:**
   - Add heading: `<h3>Publications</h3>`
   - Convert each publication to an unordered list item
   - **IMPORTANT:** Look for bold text indicating author names
   - Preserve bold formatting using `<b>` tags around author names
   - Each publication is typically on its own line in the source
   
   Example:
   ```html
   <h3>Publications</h3>
   <ul>
   <li>Mery, C.M., & <b>Nieto, R.M.</b>, & DeLeon, L.E., et al. The Role of Echocardiography and Intracardiac Exploration in the Evaluation of Candidacy for Biventricular Repair in Patients With Borderline Left Heart Structures. The Annals of Thoracic Surgery. 2016 Oct.</li>
   <li><b>Nieto, R.M.</b>, & DeLeon, L.E., & Krauklis, K., & Fraser Jr., C.D. Routine Preoperative Laboratory Testing in Elective Pediatric Cardiothoracic Surgery is Largely Unnecessary. The Journal of Thoracic and Cardiovascular Surgery. 2016 Nov.</li>
   </ul>
   ```

3. **Order matters:** Awards should appear before Publications if both exist

### Residency/Fellowship (Combined Field)

**Source fields:**
- "Residency (School/Program and year)"
- "Fellowship (Program and year)"

**Combination rules:**
1. If **both** Residency and Fellowship exist: Combine with semicolon separator
   - Format: `[Residency]; [Fellowship]`
   - Example: `Latrobe Family Medicine Residency – Latrobe, PA, 2020; Internal Medicine Fellowship - Scranton, PA, 2021`

2. If **only** Residency exists: Use residency value only with no semicolon or additional values.

**Output column name:** "Residency/Fellowship"

### Medical School

**Source field:** "Medical School (School and year)"
**Extract:** The complete value as-is
**Example:** `Baylor College of Medicine – Houston, TX, 2013`

### Professional Associations
Wrap this text in <p> tags and convert it to a complete, grammatically correct sentence if it's only a list of associations.

## Quality Checks

Before finalizing each row, verify:

1. ✅ All simple fields are populated (check for empty cells)
2. ✅ Biography Section, Awards & Publications, and Hobbies & Interests contains properly formatted HTML with opening/closing tags
3. ✅ All paragraph tags are closed: `<p>...</p>`
4. ✅ All heading tags are closed: `<h3>...</h3>`
5. ✅ Awards/Publications lists are properly formatted with `<ul>` and `<li>` tags
6. ✅ Bold tags in publications are properly closed: `<b>...</b>`
7. ✅ Residency/Fellowship are combined with semicolon if both exist
8. ✅ No source document headings (like "Biography Section", "Education & Board Certifications") appear in output except for "Philosophy of Care"
9. Professional Associations is wrapped in <p> tags.

## Common Errors to Avoid

❌ Including section headings like "Biography Section" in the Biography field
❌ Missing `<p>` tags around paragraphs
❌ Not converting Awards/Publications to unordered lists
❌ Losing bold formatting on author names in publications
❌ Forgetting to combine Residency and Fellowship fields
❌ Including "Awards & Publications" as heading when neither awards nor publications exist

## Processing Workflow

1. Open Word document
2. Create new row in spreadsheet
3. Extract simple fields first (columns 1-9, 13-17)
4. Process Biography Section with HTML formatting (column 10)
5. Combine Residency/Fellowship (column 12)
6. Extract Medical School (column 11)
7. Run quality checks
8. Move to next provider document

## Example Complete Row

| Page Title | Meta Description | Name | Gender | Specialty | Chief | Location(s) | Language(s) | KSC Start Month and Year | Biography Section | Hobbies & Interests | Awards & Publications | Medical School | Residency/Fellowship | Board Certification(s) | Professional Associations | Hospital Affiliation | ANOW | 
|------------|------------------|------|--------|-----------|-------|-------------|-------------|--------------------------|-------------------|----------------|---------------------|------------------------|--------------------------|---------------------|------|---------------|
| Raymond Nieto, MD \| Family Medicine \| Kelsey-Seybold | Raymond Nieto, MD, is a Family Medicine physician at Kelsey-Seybold Clinic... | Raymond Nieto, MD | Male | Family Medicine, Primary Care | No | Lake Jackson Clinic | English | December 2025 | `<p>Raymond Nieto, MD, is a graduate...</p><p>Dr. Nieto was inspired...</p><h3>Philosophy of Care</h3><p>Dr. Nieto listens carefully...</p>...` | `<p>In his free time Dr. Nieto...` | `<p>Dr. Nieto's awards...` | Baylor College of Medicine – Houston, TX, 2013 | Latrobe Family Medicine Residency – Latrobe, PA, 2020; N/A | American Board of Family Medicine - Family Medicine | Dr. Nieto is a member of the American Academy of Family Physicians... | St. Luke's Health - Brazosport Hospital | Y | Raymond Nieto, MD, is a graduate of Baylor College of Medicine... |

## Notes
- Some fields may be empty in source documents - leave corresponding spreadsheet cells empty
- Maintain consistent spacing and formatting for easier Sitecore import
- Biography Section HTML should be production-ready (no additional formatting needed in Sitecore)
