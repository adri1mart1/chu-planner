# CHU planner project

CHU planner is about planning organization. Very recently, I had an opportunity to work on the employees'planning at the hospital, hence, CHU (french version of UHC - University Hospital Center). This work was needed because a vote to update the daily working hours from 7.5h to 12h had been cast. A full working week was before 5 days of 7.5h and now becoming 3 days of 12h. To ease organization, the planning is based on a thread (usually a 10 to 20 weeks threads) which is a logic suite of days indicating if this is a working day or not. This thread is repeated over and over. When you have a team with several people, everyone is having the same thread but they start at different indexes so the team is well balanced (more explaination below).
With some feedback from nurses, logic and a bit of programming, the goal was to find some of the best combinations of work shifts and so, the best thread to match the needs.

Rules are simple:
 - A typical working day is 12 hours, either you work ('J' symbol) or you don't ('o' symbol)
 - The whole planning must be a thread over N weeks, that can be continuously restarted over time.
 - The same thread is shared between people in the same team, starting at different weeks.

Example:

The example thread over 3 weeks is the following:

|    | m | t | w | t | f | s | s |
|----|---|---|---|---|---|---|---|
| week1 | o | o | J | o | o | J | J |
| week2 | o | J | o | o | J | J | J |
| week3 | o | o | J | o | J | o | o |


3 persons are in the same team, sharing the same thread, starting at different starting point in the thread:
- personA following the thread week1, week2, week3
- personB following the thread week2, week3, week1
- personC following the thread week3, week1, week2

|    | m | t | w | t | f | s | s | m | t | w | t | f | s | s | m | t | w | t | f | s | s |
|----|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| person A | o | o | J | o | o | J | J | o | J | o | o | J | J | J | o | o | J | o | J | o | o |
| person B | o | J | o | o | J | J | J | o | o | J | o | J | o | o | o | o | J | o | o | J | J |
| person C | o | o | J | o | J | o | o | o | o | J | o | o | J | J | o | J | o | o | J | J | J |
| working day total | 0 | 1 | 3 | 0 | 3 | 2 | 2 | 0 | 1 | 3 | 0 | 2 | 3 | 3 | 0 | 2 | 2 | 0 | 3 | 3 | 3 |


Ideally, the management wants to have someone working every day to keep a continuous care service so the thread AND the variants of the thread of each person must be well balanced. In this example, the last line shows how many persons are working per day. This is not a really good example as we have multiple days with none of the 3 persons working and some days with everyone working. This manual example is not very interesting to keep then.

The goal of this project is to find good threads and find best combinations of this thread.

# Details of implementation

I choose Python language as it's easy to write and at first, it was not very obvious how to find a good solution for this problem. In addition, when we started to work on this project, we didn't have all rules to follow so, multiple times, we had to add, update or remove some functions to adapt the whole program.

Base hypothesis:
 - Main thread is 12-weeks long
 - Number of employees in the team, 5 persons

The whole algorithm is based on the following phases:
1. Generate all possible 12 weeks threads:
    1.1. generate 1-week all possible variants based on mathematical logic, then filter
    1.2. generate 2-weeks all possible variants based on all 1-week valid results, then filter
    1.3. generate 4-weeks all possible variants based on all 2-weeks valid results, then filter
    1.4. generate 8-weeks all possible variants based on all 4-weeks valid results, then filter
    1.5. generate 12-weeks all possible variants based on all 8-weeks and 4-weeks valid results, then filter
2. For each thread, generate all employees thread combinations and evaluate how well balanced it is

Why the generation of thread is like this ? why not mathematically generate all 12-weeks ?
12 weeks of 7 days each is 84 days.
84 days either worked or not so two possibilities per day. 2^84 ~= 2.10^25 possibilities
Assuming a computer can compute a unique solution in 1ms, we need 2.10^22 seconds, or about 300 trillion years.
This is far more than what a computer can process in a reasonable timeframe so the algorithm must prune some invalid threads as soon as possible.

## Generate all possible threads (or variants)

### STEP 1.1: generate 1-week variants

Starting from nothing, we generate all one-week different threads.
One week is 7 days, each days is either worked or not, so one week is 2^7 = 128 possibilities.
The generation is a per Gray Code (reflected binary)

```
$ cat output/variants_12w/1-week-all-variants.txt
ooooooo
ooooooJ
oooooJo
...
JJJJJJo
JJJJJJJ
```

In this file, we can filter results pruning invalid results. All pruning rules can be seen in the source code, function names are verbose enough to understand what it does.
Some example:

`ooJJJJo` -> Impossible because 4 working days in a row is too many days to work without any break
`oJoooJo` -> Impossible because if a saturday is worked, sunday must be worked too (a weekend is a whole)

Valid results are saved into `output/variants_12w/1-week.txt` file.

### STEP 1.2: generate 2-weeks variants

We retrieve all valid 1-week results and assemble them two by two to generate 2-weeks variants.
1-week variant number is 35 so there are 35² = 1225 2-weeks variant possibilities.
Again, we prune the variants following some rules.

Some new rules used when dealing with 2 weeks-variants:
- It's not possible to work 2 weekends in a row
- You can't work more than 4 days over 7 moving days

### STEP 1.3: generate 4-weeks variants

Same process to generate 4-weeks variants based on 2-weeks valid results, then filter.

### STEP 1.4: generate 8-weeks variants

Same process to generate 8-weeks variants based on 4-weeks valid results, then filter.

### STEP 1.5: generate 12-weeks variants

Same process to generate 12-weeks variants based on 8-weeks and 4-weeks valid results, then filter.

### STEP 2: Generate and evaluate all combinations

At the end of the STEP 1.5, we should have lots of different 12-weeks threads that are valid for a single person. As the same thread is shared between multiple persons in the same team, starting the thread at different starting point, we need to find the best combination matching all of our team working conditions.

These mandatory conditions are:

 - We need 1 or 2 person of the team working every weekend, no more, no less
 - We need 1 person in the team to work each day

Then, we still have multiple choices so to choose the best one, we take the combination that minimize the number of days which only 1 person is working.

Lets take a look at the example we use before:

Say the thread we are using is `ooJooJJoJooJJJooJoJoo` which is represented like this.

|    | m | t | w | t | f | s | s |
|----|---|---|---|---|---|---|---|
| w1 | o | o | J | o | o | J | J |
| w2 | o | J | o | o | J | J | J |
| w3 | o | o | J | o | J | o | o |

We then have the 3 possible ways of following the thread which are `w1-w2-w3` or `w2-w3-w1` or `w3-w1-w2`.
Respecting the initial order of the thread is important but the initial starting point can be any begining of every week.

Say we have a team of 2 persons, these 2 persons can either work:

person_A: `w1-w2-w2` and person_B: `w2-w3-w1`
person_A: `w1-w2-w2` and person_B: `w3-w1-w2`
person_A: `w2-w3-w1` and person_B: `w3-w1-w2`

Note: We do not consider mirror combinations as person_A and person_B are fictive person at that stage. The final attribution of each threads is done manually based on personal preferences and/or calendar predefined constraints.

Considering a real example with 12-weeks threads, 5 persons in a team, there are 792 possible combinations per thread. (See: https://docs.python.org/3/library/itertools.html#itertools.combinations )

## Memory management

On this project, I have used text files with either 'J' or 'o' character to represent data. Depending on which rules are set to prune results, there may be a lot of results, so much that output files was several hundred of megabytes.
To manage this, the `assemble_variants_two_by_two` function computes how much the output file will be. If it is detected to be oversized by a factor N, the function will assemble every N frames two by two.
This is a good way to deal with a lot of data, quite simple, fair and we don't use any random or shuffle native python function which needs to load data into memory before mixing everything.

# How to use

## Generate all week variants

First, generate all week variants based on the differents hypothesis.

```
$ $ ./generate_week_variants.py
generate_all_mathematical_possible_week_variants
filter_all_impossible_week_variants
stats_more_than_3_consecutive_working_days: 20
stats_more_than_4_days_per_week: 13
stats_saturday_nor_sunday: 51
stats_not_enough_days_off_before_or_after_working_days: 7
stats_too_many_single_working_days: 2
reset pruning stats
all valid week variants size:35

assemble_variants_two_by_two
total number of 2-weeks time possibilities before pruning 1224
filter_all_impossible_two_weeks_variants
stats_more_than_3_consecutive_working_days: 78
stats_not_enough_days_off_before_or_after_working_days: 149
stats_too_many_single_working_days: 0
stats_more_than_4_working_days_over_7_moving_days: 35
stats_two_working_week_ends_in_a_row: 66
stats_not_enough_or_too_many_working_days_over_n_weeks: 190
reset pruning stats
all valid 2-weeks variants size: 706

assemble_variants_two_by_two
input_file 1 size 10590 bytes which represents 706 variants
input_file 2 size 10590 bytes which represents 706 variants
We must limit disk usage to 10000000 bytes with frame generation of 29 chars each
total number of possibilities 706 x 706 = 498436
Number of 4-weeks variants to keep to respect disk usage: 344827
total number of 4-weeks time possibilities before pruning 249217
filter_all_impossible_four_weeks_variants
stats_more_than_3_consecutive_working_days: 0
stats_not_enough_days_off_before_or_after_working_days: 5044
stats_too_many_single_working_days: 0
stats_more_than_4_working_days_over_7_moving_days: 1172
stats_two_working_week_ends_in_a_row: 0
stats_not_enough_or_too_many_working_days_over_n_weeks: 37258
stats_not_exactly_1_out_of_3_working_weekend: 49550
stats_more_than_one_3_working_days_in_a_row: 24380
reset pruning stats
all valid 4-weeks variants size after balance pruning: 7204

assemble_variants_two_by_two
input_file 1 size 208916 bytes which represents 7204 variants
input_file 2 size 208916 bytes which represents 7204 variants
We must limit disk usage to 10000000 bytes with frame generation of 57 chars each
total number of possibilities 7204 x 7204 = 51897616
Number of 8-weeks variants to keep to respect disk usage: 175438
total number of 8-weeks time possibilities before pruning 174739
filter_all_impossible_eight_weeks_variants
stats_more_than_3_consecutive_working_days: 0
stats_not_enough_days_off_before_or_after_working_days: 4323
stats_more_than_4_working_days_over_7_moving_days: 1039
stats_two_working_week_ends_in_a_row: 0
stats_not_exactly_1_out_of_3_working_weekend: 122608
stats_more_than_one_3_working_days_in_a_row: 25497
reset pruning stats
all valid 8-weeks variants size: 21272

assemble_variants_two_by_two
input_file 1 size 1212504 bytes which represents 21272 variants
input_file 2 size 208916 bytes which represents 7204 variants
We must limit disk usage to 10000000 bytes with frame generation of 85 chars each
total number of possibilities 21272 x 7204 = 153243488
Number of 12-weeks variants to keep to respect disk usage: 117647
total number of 12-weeks time possibilities before pruning 117518
filter_all_impossible_twelve_weeks_variants
stats_more_than_3_consecutive_working_days: 2325
stats_not_enough_days_off_before_or_after_working_days: 7132
stats_more_than_4_working_days_over_7_moving_days: 1861
stats_two_working_week_ends_in_a_row: 0
stats_not_exactly_1_out_of_3_working_weekend: 81889
stats_more_than_one_3_working_days_in_a_row: 22127
reset pruning stats
all valid 12-weeks variants size: 2184
```

All results are saved under `output/variants_12w` directory.

```
$ ls output/variants_12w/
1-week.txt
1-week.txt-all-variants.txt
2-weeks.txt
2-weeks-all-variants.txt
4-weeks.txt
4-weeks-all-variants.txt
8-weeks.txt
8-weeks-all-variants.txt
12-weeks.txt
12-weeks-all-variants.txt
```

The final file we are interested in is named `12-weeks.txt` and is approximately 2000 lines. So we have 2000 possibles threads that can match all our actual constraints.

## Find best combinations

As we have about 2000 possible threads of 12-weeks, with a team of 5 persons (so about 800 combinations per thread), the script can analyze about 1.6 millions of possibilities for us. It keeps the best result, minimizing the number of day only one person is working.

To starting the script, use:

```
$ ./find_best_combinations.py
Loading wset from output/variants_12w/12-weeks.txt
1/2184 - possible variants: 0/792
2/2184 - possible variants: 60/792
3/2184 - possible variants: 48/792
[..]
find best combination search finished, best result is 6 days with one person working
```

The file `output/combinations/valid-results-12w.txt` stores all valid results.
Each result is a per below:

```
********
shift: JoooJoooJoJJoooJJooJJoooJJooJoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJ
s1: JoooJoooJoJJoooJJooJJoooJJooJoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJ
s2: oJoJJoooJJooJJoooJJooJoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJJoooJoo
s3: oJJooJJoooJJooJoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJJoooJoooJoJJoo
s4: oooJJooJoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJJoooJoooJoJJoooJJooJJ
s5: JoJooooJJoooJJooJoJoooJoJJooJooJoJJooJoJooJJoooooooJooJJJoooJoooJoJJoooJJooJJoooJJoo
1-person working num: 6/84
```

The `shift` line is the thread pattern to follow.
The lines `sN` are each variant of the initial thread with starting index being equal to `7x(N-1)`. `s1` is the exact same thread, `s2` is the thread starting at index 7, and so on.

These results are sufficient enough for our task as we just copy paste some of this threads in a predefined Excel spreadsheet and suggest this new planning to the management. (See `data/template*.xlsx` file for more info)

# Tools

Theses scripts are simple tools that can help when tweaking constraints, adjusting scripts.

## print_single_set.py

Print a single set in a human readable format:

```
$ ./print_single_set.py
which set: ooooJoo

L M M J V S D
o o o o J o o
days worked: 1
```

## print_sets.py

Print a whole file of variants in a human readable format.

```
$ ./print_sets.py
which input file: output/variants_12w/1-week.txt

L M M J V S D
J J o o o J J
days worked: 4

L M M J V S D
J o o o J J J
days worked: 4

[...]
```
