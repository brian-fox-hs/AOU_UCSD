# EHR's sample truth table 

| person_id | first_name | last_name | dob      | sex      | address  | phone_number | email    | algorithm_validation | manual_validation |
|-----------|------------|-----------|----------|----------|----------|--------------|----------|----------------------|-------------------|
| XX        | match      | match     | match    | match    | match    | missing      | excluded | yes                  | no                |
| XX        | no_match   | no_match  | no_match | no_match | no_match | no_match     | excluded | no                   | yes               |
| XX        | match      | match     | match    | match    | match    | match        | excluded | yes                  | no                |
| XX        | match      | match     | match    | match    | match    | match        | excluded | yes                  | no                |
| XX        | no_match   | no_match  | no_match | match    | no_match | no_match     | excluded | no                   | yes               |
| XX        | match      | match     | match    | match    | missing  | match        | excluded | no                   | yes               | 


# Our truth table

## Quick successful match (algorithmic)

As of 10/7/2022 - this gives us about 5000 matches

There is an algorithm match if ALL of these are true:

- first_name matches
- last_name matches
- normalized dob matches
- normalized sex matches
- first 10 letters of addr1 match
- first 5 letters of zip matches

## Fuzzy successful match (algorithmic) 

There is an algorithm match if ALL of these are true:

- fuzzy first_name matches
- fuzzy last_name matches
- normalized dob matches
- normalized sex matches
- fuzzy first 10 letters of addr1 match
- first 5 letters of zip matches

## Manual matches to be inspected by a human (not yet matched)

There is manual POTENTIAL match if this is true:

- Both the Quick and Fuzzy matches FAILED (described above)

AND 

One of these are true

- The first name is an exact match
- The last name is an exact match

AND 

Any THREE of these are true:

- fuzzy first_name matches
- fuzzy last_name matches
- fuzzy normalized dob matches
- fuzzy first 10 letters of address line 1 matches
- fuzzy normalized phone_number matches
- fuzzy normalized email matches

## Manual confirmed match (manual match):

There is a manuel CONFIRMED match if:

-the manual potential match has been inspected and confirmed by a human

## Duplicate match error

There is a duplicate match error if any of these are true:

- One HealthPro row matches to multiple HPO patients
- One HPO patient matches multiple HealthPro rows


## No match

The HealthPro row doesn't match any patients at all if this is true:

- The patient hasn't matched using the criteria above.