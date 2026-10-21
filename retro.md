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