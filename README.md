# VAST 2017: Mini-Challenge-1

## You can use the code in this repo to:
* see paths on the map
* use computed values seen in output files

* detect groups in paths (not yet- working on it)

## First time use (downloaded whole repo):
1. Edit config.py
2. Run Driver.py

### How does the `plotPath` function work?
Its input is a `VisitRecord`. `rowsToRecords` generates `VisitRecord`s.

### Ok, how do I use the `rowsToRecords` function?
Its input is the string path of the raw data downloaded from the VAST website.

The output of `rowsToRecords("path/to/raw/data")` is a map:
* `String` of a `car.id` -> a `list` of `VisitRecord`

Each element of the returned list is a separate visit to the park.
That is, the path field of a visit always begins and ends at an entrance or the ranger base
(Unless the data begins after they entered or before they left)

### Anything else I should know?
Not that I can think of atm.