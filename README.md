# Cornerstone

## Summary

Basic loan annotation use case to extract the following values:
- Borrower Name
- Mailing Address
- Property Address
- Lender Name
- Recording Date
- Document Number

## Process

    1. Generate teach task csv (scripts/create_teach_data.py)
    2. Generagte predictions after model has been trained (scripts/run_predictions.py)
    3. Post process predictions (scripts/format_predictions.py)
