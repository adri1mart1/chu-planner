# CHU planner

## _The Last Markdown Editor, Ever_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

CHU planner is about planning organization. Very recently, I had an opportunity to work with my wife to update employees'planning in the hospital, hence, CHU (french version of UHC - University Hospital Center).
With some feedback from nurses, logic and a bit of programming, the goal was to find some of the best combinations of work shift to match the needs.

Rules are simple:
 - A typical working day is 12 hours, either you work ('J' symbole) or you don't ('o' symbole)
 - The whole planning must be a thread over N weeks, that can be continuously restarted over time.
 - The same thread is shared between people in the same team, starting at different weeks.
 -

Example:

The example thread over 3 weeks is the following:
   MTWTFSS
w1 ooJooJJ
w2 oJooJJJ
w3 ooJoJoo

3 persons are in the same team, sharing the same thread, starting at different starting point in the thread:
Person_A (w1, w2, w3) -> ooJooJJoJooJJJooJoJoo
Person_B (w2, w3, w1) -> ooJoJooooJooJJoJooJJJ
Person_C (w3, w1, w2) -> oJooJJJooJoJooooJooJJ

Ideally, the management wants to have someone working every day so the thread AND the variants of the thread of each person must be well balanced.
Ex: the very first day, no one is working, while the last day, 2 persons are working.
This manual example is not very interesting then.

The goal of this project is to find good threads and find best combinations of this thread.

# Details of implementation

Base hypothesis:
 - Main thread is 12-weeks long
 - Number of employees in the team, 5 persons

The whole algorithm is based on two phases:
1- Generate all possible 12 weeks threads:
  1- generate 1-week all possible variants based on mathematical logic, then filter
  2- generate 2-weeks all possible variants based on all 1-week valid results, then filter
  3- generate 4-weeks all possible variants based on all 2-weeks valid results, then filter
  4- generate 8-weeks all possible variants based on all 4-weeks valid results, then filter
  5- generate 12-weeks all possible variants based on all 8-weeks and 4-weeks valid results, then filter
2- For each thread, generate all employees thread combinations and evaluate how well balanced it is

Why the generation of thread is like this ? why not mathematically generate all 12-weeks ?
12 weeks of 7 days each is 84 days.
84 days either worked or not is 2^84 ~= 2.10^25 possibilities.
This is far more than what a computer can process in a reasonable timeframe so the algorithm must prune some invalid threads as soon as possible.
## Generate all possible threads (or variants)
STEP 1:
Starting from nothing, we generate all one-week different threads.
One week is 7 days, each days is either worked or not, so one week is 2^7 = 128 possibilities.
```

$ cat output/variants_12w/1-week-all-variants.txt
ooooooo
oooooo1
ooooo1o
...
JJJJJJo
JJJJJJJ
```
In this file, we can filter results pruning invalid results. All pruning rules can be seen in the source code, function names are verbose enough to understand what it does.
Some example:
ooJJJJo -> Impossible because 4 working days in a row is not valid
oJoooJo -> Impossible because if a saturday is worked, sunday must be worked too (a weekend is a whole)

Valid results are saved into `output/variants_12w/1-week.txt` file.

STEP 2:
We retrieve all valid 1-week results and assemble them two by two to generate 2-weeks variants.
1-week variant number is 35 so there are 35² =  1225 2-weeks variant possibilities.
Again, we prune the variants following some rules.

Some new rules used when dealing with 2 weeks-variants:
- It's not possible to work 2 weekends in a row
- You can't work more than 4 days over 7 moving days

STEP 3:
Same process to generate 4-weeks variants based on 2-weeks valid results, then filter.

STEP 4:
Same process to generate 8-weeks variants based on 4-weeks valid results, then filter

STEP 5:
Same process to generate 12-weeks variants based on 8-weeks and 4-weeks valid results, then filter

## Memory management

On this project, I have used text files with either 'J' or 'o' character to represent data. Depending on which rules set to prune results, there may be a lot of results, so much that output files was several hundred of megabytes.
To manage this, the `assemble_variants_two_by_two` function computes how much the output file will be. If it is detected to be oversized by a factor N, the function will assemble every N frames two by two.
This is a good way to deal with a lot of data, quite simple, fair and we don't use any random or shuffle function which needs to load data into memory before mixing everything.

# How to use

## Generate all week variants

First, generate all week variants based on differents hypothesis

```
$ ./generate_week_variants.py
```

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
