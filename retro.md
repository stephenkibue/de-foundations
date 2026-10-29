# Daily Retrospective

## Day 2
1. Warm-up score & biggest surprise
my warm up score is 77 and what tripped me up today is how easy it is to prompt the user for an input

2. Most frequent error today:
Forgetting to save the file before running it

3. What // and % do 
* // means: division giving only the full answer whthout remainder
* % means: give only the remainder of a division.

4. One question I still have:
how do we resolve wrong onput errors.

## Day 3
**1. Warm-up score & biggest surprise:**
My biggest surprise was during the warm-up: I realized that if a list is empty or the `if` condition is never met, the loop just silently skips the math and returns 0. 

**2. Most frequent error today:**
The `ZeroDivisionError`. I had to think carefully about how to use guard clauses (`if birds <= 0:` and `if days == 0:`) to stop the math from running and crashing the program if there was missing data.

**3. What I learned about loops and accumulators:**
I learned how to keep a running total, count up specific categories, and use the "King of the Hill" pattern to constantly update the highest and lowest numbers. I also learned how to switch from a `for` loop to a `while True` loop so the user can type data until they say "done".

**4. One question I still have:**
Now that my `while` loop lets a user type in all this data, how do I actually save it permanently so it isn't erased the moment the program finishes running?
## Day 4
**1. Warm-up score & biggest surprise:**
My biggest surprise was seeing how easy it is to pull the last item in a list using index `[-1]`, and learning that `in` on a list of dictionaries looks for an exact dictionary match, not a value inside them.

**2. Most frequent error today:**
String quote collisions (`SyntaxError` from mixing double quotes inside an f-string) and missing dictionary keys (`KeyError` when looking for "eggs" due to a typo).

**3. What I learned about dictionaries and Group-By:**
I learned how to group data dynamically by using an empty dictionary, checking if a key (like a flock name) exists, and either creating a new bucket or adding to an existing one. I also learned how to use `lambda` to sort a list of dictionaries by a specific key.

**4. One question I still have:**
How do we get this kind of data out of an actual file or database instead of hard-coding a massive list of dictionaries at the top of the script?

## Day 5
**1. Warm-up score & biggest surprise:**
My biggest surprise was seeing how much cleaner the code becomes when you move the math out of the main script and into small, reusable functions. List and dictionary comprehensions are also surprisingly powerful for doing complex filtering in just one line of code.

**2. Most frequent error today:**
`AssertionError`. I learned that the `assert` tests are strictly case-sensitive (e.g., expecting exactly "no data" and failing if there is a typo or capital letter).

**3. What I learned about functional programming:**
I learned the DRY principle (Don't Repeat Yourself) by passing a `field` variable into my group-by function so it can sum up *any* column. I also learned how to use a guard clause (`if rate is None:`) to prevent errors from crashing the program, and how `main()` acts as a conductor to just run the final report.

**4. One question I still have:**
Now that we have clean functions and a solid `main()` report, how do we handle real-world messy data formats like actual calendar dates instead of just treating them as strings?
## Day 6 (Week 2, Day 1)
**1. Warm-up score:**
70

**2. Hardest problem to spot by eye:**
The invisible spaces, like the flock listed as "B " instead of "B", or the eggs recorded as " 405 ". You would never catch those just scrolling through a spreadsheet visually.

**3. Cleaning rules:**
1. Duplicates: Check the row tuple against a seen set; drop exact duplicates.
2. Date: Check for slashes (/). If found, split and rearrange DD/MM/YYYY into YYYY-MM-DD.
3. Flock: Trim spaces and make uppercase. If the result is not exactly 'A', 'B', or 'C', reject the row.
4. Eggs: Trim spaces. If blank, negative, or not a perfect digit string, reject the row.
5. Birds: Trim spaces. If blank, negative, or not a perfect digit string, reject the row.

**4. One question I still have:**
When we "reject" a row on Wednesday, do we just delete it entirely, or do we save the bad rows into a separate error file so people like Otieno can fix their mistakes?

## Day 7 (Week 2, Day 2 - Mashujaa Day)
**1. Warm-up score:**
68

**2. Shape of farm.json:**
- farm (dict)
  - name
  - county
  - exported_at
  - active
- flocks (list)
  - flock (dict)
    - id
    - breed
    - house
    - placed_on
    - vaccinations (list of dicts)
      - vaccine
      - date
    - records (list of dicts)
      - date
      - eggs
      - birds
      - feed_kg
      - notes

**3. Questions for the farm:**
- Flock C (Oct 17): "There is no record for Flock C on October 17. Was the data simply not recorded, or did something happen that prevented data collection?"
- Flock B (Oct 15): "I noticed a dip in production on Oct 15 and a note about a blocked water line. Was the blockage resolved quickly, and should we expect any lingering effects on the flock's performance?"

**4. One question I still have:**
When flattening nested JSON, how do we handle extremely deep nesting (like 5 or 6 levels down) without writing massive, confusing loops?
## Day 8 (Week 2, Day 3 - Validation Pipeline)
**1. Warm-up score:**
78

**2. Why reject number-words like "twelve hundred"?**
Writing code to parse every possible word variation is complex and error-prone. Rejecting it with a clear reason forces the data entry source to fix their behavior. Guessing risks corrupting downstream totals if the guess is wrong.

**3. Why check duplicates by (flock, date) and not the whole row?**
A flock can only have one true record per day. If a duplicate row has a different egg count, checking the whole row would treat it as a unique valid entry, doubling that day's production in our totals.

**4. Why keep raw values in the reject file?**
The person correcting the data needs to see exactly what they typed to understand the error. If we partially clean it before writing to the reject file, the original context of the typo is destroyed.

**5. One question I still have:**
 how to handle massive files that don't fit in memory
 ## Retro: Kuku Package Refactoring & Pipeline Expansion

1. **Warm-up score:** 10/10 — Successfully transitioned a single-script proof-of-concept into a modular, production-grade Python package.
2. **Package layout (from memory):**
   - `src/kuku/__init__.py` — Initializes the package namespace and module structure.
   - `src/kuku/reader.py` — Handles robust CSV file input and output with logging.
   - `src/kuku/validate.py` — Cleans and validates row schemas, rules, counts, and calendar dates.
   - `src/kuku/transform.py` — Runs chronological gap detection and calculates aggregate flock totals using collections.
   - `src/kuku/main.py` — Orchestrates the full pipeline workflow, CLI argument parsing (`--debug`), and final summary reporting.
3. **Missing days priority:** I would ask the farm about the **Sunday** gaps first. Since multiple missing records cluster on Sundays, it strongly suggests a regular staffing or operational shift change rather than random data entry errors.
4. **Remaining question:** How should the pipeline handle retroactive corrections if farm workers submit late data for previously flagged missing days?

## Week 2: Working with real files

The `kuku` package automates the ingestion, validation, and transformation of raw poultry farm production data into clean, analysis-ready records. The pipeline processes production records, successfully outputting 42 clean records and rejecting 8 with detailed diagnostic reasons.

### How to Run
```powershell
python -m src.kuku.main

---

### 2. Create or Update `retro.md`
Populate your `retro.md` file with your weekly review:

```markdown
# Week 2 Retrospective

### 1. Which day was hardest, and why?
Refactoring the core data structures from raw dictionaries to the strongly-typed `ProductionRecord` dataclass was the most challenging part. It caused ripples across validation, transformation, and testing modules, requiring careful alignment of attribute access and test mocks.

### 2. Which idea could you now teach someone else?
I feel confident teaching how to write parameterized unit tests with `pytest` and how to use isolation strategies (testing small mock datasets instead of raw production files) to make tests lightning-fast and deterministic.

### 3. Which idea is still shaky?
Advanced package installation states and path configurations (`pip install -e .` combined with structured namespace layouts) still require deliberate focus to ensure absolute import clarity.

### 4. Hours actually worked against the 12 to 15 planned?
Worked approximately 14 hours, aligning closely with the 12-to-15-hour planned target.
3. Tidy the Repository Structure

## Day 11 (Week 3) - EDA with Pandas

1. **Warm-Up Score & Q9 Explanation:** 
   -  7 / 10.
   - **Q9 Explanation:** When parsing date strings during file ingestion using `parse_dates=["date"]`, Pandas converts text strings into structured `datetime64` objects. This allows direct date filtering and comparison (e.g., `>= "2026-10-10"`) without worrying about raw string formatting inconsistencies like `10/10/2026`.

2. **Week 2 Loop to Replace with Pandas:** 
   - Replaced manual dictionary grouping loops for counts with a single clean Pandas line: `df["flock"].value_counts()`.

3. **Difference Between `loc` and `iloc`:** 
   - `loc` selects data using explicit row/column labels, while `iloc` selects data using integer index positions.
## Day 12 (Week 3) - Data Cleaning with Pandas

1. **Warm-Up Score & Surprises (#2 and #7):**
   - 6 / 10.
   - **Surprise #2:** How easily standard defaults silently swallow literal text like `"n/a"` by converting it straight into `NaN`.
   - **Surprise #7:** How efficiently vectorised boolean masking in Pandas handles complex multi-condition validation checks without writing explicit Python `for` loops.

2. **The Two Silent Changes Pandas Made:**
   - **Automatic NaT/NaN conversion:** Default CSV loading interprets ambiguous strings (like `"n/a"`, `""`, spaces) as missing values (`NaN`).
   - **Type inference:** Pandas automatically guesses data types (e.g., treating columns with mixed text/numbers as `object` rather than integers) during default imports.

3. **Lines of Code (Day 8 vs. Today):**
   - Pandas made the cleaning logic much more concise and declarative compared to Day 8's manual Python iteration approach. Vectorized operations and `.apply()`/`loc` rules were much cleaner to maintain.

## Day 13 (Week 3) - Analysis with Pandas

1. **Warm-Up Score & Method Selection:**
   - 9 / 10. Method 3 (total eggs ÷ total bird-days) is the correct approach because it correctly accounts for differing population sizes across groups and days.

2. **The "Never Average a Rate" Rule:**
   - Averaging percentages or rates directly gives equal weight to groups of vastly different sizes (treating a tiny sample with the exact same weight as a massive flock), which severely distorts the true aggregate picture. Always sum the numerators and denominators separately before computing the ratio.

3. **Message to the Owner About Flocks B and C:**
   - "Flock B saw a slight dip in week 42 but remains healthy, whereas Flock C continues to underperform consistently at 71.1% and requires immediate investigation into feed quality and management."

4. **Remaining Question:**
   - How can we best automate this analysis pipeline to handle daily CSV drops and flag anomalies automatically as soon as new data lands?