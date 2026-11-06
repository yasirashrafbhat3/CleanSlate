# CleanSlate Test Cases

Run the automated tests from the project root with:

```bash
python3 -m unittest discover -s tests -v
```

| ID | Input condition | Expected result |
|---|---|---|
| TC01 | Valid email | Accepted |
| TC02 | Email with `@@` | Invalid email issue |
| TC03 | Valid 10-digit Indian mobile number | Accepted |
| TC04 | Phone with fewer than 10 digits | Invalid phone issue |
| TC05 | Valid past date in YYYY-MM-DD | Accepted |
| TC06 | Impossible or future date | Invalid DOB issue |
| TC07 | Empty required field | Missing-field issue |
| TC08 | Email repeated with different letter case/spaces | Duplicate email issue |
| TC09 | Name/city with extra spaces and mixed case | Trimmed and title-cased |
| TC10 | CSV missing a required header | CSV loading error |
| TC11 | CSV row with extra values | CSV loading error |
| TC12 | Empty CSV file | CSV loading error |

The application retains all input records in the cleaned output. It reports invalid values and duplicate email addresses separately instead of deleting records automatically.
