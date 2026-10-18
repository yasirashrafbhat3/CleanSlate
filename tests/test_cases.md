# CleanSlate Test Cases

This file documents at least 10 test scenarios for the project. These are written as manual test cases and can later be converted into automated unit tests.

## 1. Valid record
Input:
- name: Alice Smith
- email: alice.smith@example.com
- phone: +1-202-555-0135
- date_of_birth: 1990-05-21
- city: New York

Expected:
- No validation issues
- Record is valid
- Not marked as duplicate

## 2. Invalid email
Input:
- email: eve.adams@@example.com

Expected:
- Invalid email issue
- Record marked invalid

## 3. Invalid phone
Input:
- phone: 12345

Expected:
- Invalid phone number issue

## 4. Invalid date of birth
Input:
- date_of_birth: 1995-02-30

Expected:
- Invalid date of birth issue

## 5. Duplicate exact record
Input:
- Same name, email, phone, and date_of_birth as an earlier record

Expected:
- Duplicate record detected
- Should be flagged in error report

## 6. Duplicate with case differences
Input:
- name: "ALICE SMITH"
- email: "ALICE.SMITH@EXAMPLE.COM"
- city: "NEW YORK"

Expected:
- Duplicate should still be detected after text normalization

## 7. Extra spaces in fields
Input:
- name: "  Diana Prince  "
- city: "  denver"

Expected:
- Spaces trimmed
- Cleaned version should be "Diana Prince" and "denver"

## 8. Mixed case values
Input:
- name: "bob jones"
- city: " san francisco "

Expected:
- Text is cleaned and standardized
- Not invalid just because of lowercase or spacing

## 9. Missing email
Input:
- email: ""

Expected:
- Missing/invalid email issue
- Record not valid

## 10. Missing city
Input:
- city: ""

Expected:
- Missing city issue
- Record not valid

## 11. Valid but whitespace-heavy row
Input:
- name: "  Grace Hall  "
- email: "grace.hall@example.com"
- phone: " +1 646 555 0138 "
- date_of_birth: "1985-12-05"
- city: " Seattle "

Expected:
- Cleaned values should strip spaces
- No validation issues

## 12. Duplicate with slightly different formatting
Input:
- name: "Bob Jones"
- email: "bob.jones@example.com"
- phone: "+1 (415) 555-0147"
- city: "San Francisco"

Expected:
- Detect as duplicate when normalized
