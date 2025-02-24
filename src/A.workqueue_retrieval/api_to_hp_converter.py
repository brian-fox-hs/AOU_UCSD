import pandas as pd
import json


# Moves data from All of Us API format to HealthPro web download format.

# The following fields are converted:

# "Date of Birth"
# "State"
# "Sex"
# "Gender Identity"
# "Race/Ethnicity"
# "Withdrawal Status"
# "Primary Consent Status"
# "EHR Consent Status"
# "Patient Status: Yes"
# "Patient Status: No"
# "Patient Status: No Access"
# "Patient Status: Unknown"
# "Deceased"

# The rest are passed thru as-is



# CaBOR is missing...
"""
ELIGIBILITY:

See email from REDACTED sent on 2/10/2025

Hi All,
 
The new participant list files have been dropped to your folder under /ops_data_api_awardee with all WorkQueue columns added on Feb 6th.
 
You can use the following criteria to find your participants at your organization:
 
Paired Organization = “Your organization’s acronym name”
AND
Primary Consent Status = “SUBMITTED”
AND
EHR Consent Status = “SUBMITTED”
AND
Withdrawal Status = “NOT_WITHDRAWN”
 
For sites who used to use WorkQueue export, the field values might look different than what you had. For example, the “Primary Consent Status” was 1 in WorkQueue export file instead of “SUBMITTED” in current file. This is because the current values were extracted from Ops Data API and not mapped to WorkQueue values.
 
You can use the aou confluence page to create a mapping from Ops Data API values to WorkQueue values.
https://www.aoucollaborations.net/pages/viewpage.action?spaceKey=DRC&title=Data+Dictionary+%7C+Ops+Data+API
 
The pdf version is also attached in case you don’t have access to the website.
 
Let us know if you have any questions.
 
Best,
EHR Ops team
 """

# UTILITY CLASS
# Forces all data typing to strings
class StringConverter(dict):
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return str

    def get(self, default=None):
        return str


def convert_date(original):
    try:
        # Convert to datetime, automatically handling multiple formats
        date_obj = pd.to_datetime(original, errors='coerce')

        # If conversion failed (NaT), return original
        if pd.isna(date_obj):
            return original

        # Format as MM/DD/YYYY
        return date_obj.strftime('%m/%d/%Y')

    except Exception as e:
        raise Exception(f"Unhandled Date: {original}")

def convert_state(original):
    state_abbreviations = [
        "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
        "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
        "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
        "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
        "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
        "PR",  # Puerto Rico?
        "DC",  # Washington DC?
        "GU",  # Guam?
        "FM",  # Federated States of Micronesia?
        "AS",  # American Samoa?
        "VI",  # U.S. Virgin Islands?
    ]

    tokens = original.split("_")
    if original.upper() == "UNSET":
        return original
    elif len(tokens) != 2:
        return "STATE_ERROR"
    elif tokens[1] not in state_abbreviations:
        return f"{original} STATE_ERROR"
    return tokens[1]


def convert_sex(original):
    sexes = [
        "Male", "Female", "Intersex",
        "Skip",  # NOT IN DATA DICTIONARY
    ]
    convert = {
        "SexAtBirth_None".upper(): "Other",
        "SexAtBirth_SexAtBirthNoneOfThese".upper(): "Other"
    }
    tokens = original.split("_")
    if original.upper() == "UNSET":
        return original
    elif original.upper() == "PMI_SKIP":
        return "Skip"
    elif original.upper() == "PMI_PREFERNOTTOANSWER":
        return "Prefer Not to Answer"
    elif original.upper() in convert:
        return convert[original.upper()]
    elif len(tokens) != 2:
        return "SEX_ERROR"
    elif tokens[1] not in sexes:
        return f"{original} SEX_ERROR"
    return tokens[1]


def convert_gender(original):
    sexes = [
        "Man", "Woman", "NonBinary", "Transgender",
        "Skip",  # NOT IN DATA DICTIONARY
    ]
    convert = { "MoreThanOne" : "More Than One Gender Identity", "AdditionalOptions" : "Other" }

    tokens = original.split("_")
    if original.upper() == "UNSET":
        return original
    if original.upper() == "PMI_SKIP":
        return "Skip"
    if original.upper() == "PMI_PREFERNOTTOANSWER":
        return "Prefer Not to Answer"
    elif tokens[1] in convert:
        return convert[tokens[1]]
    elif len(tokens) != 2:
        return "GENDER_ERROR"
    elif tokens[1] not in sexes:
        return f"{original} GENDER_ERROR"
    return tokens[1]

def convert_race(original):
    conversion_map = {
        "AMERICAN_INDIAN_OR_ALASKA_NATIVE": "American Indian /Alaska Native",
        "BLACK_OR_AFRICAN_AMERICAN": "Black or African American",
        "ASIAN": "Asian",
        "NATIVE_HAWAIIAN_OR_OTHER_PACIFIC_ISLANDER": "Native Hawaiian or Other Pacific Islander",
        "WHITE": "White",
        "HISPANIC_LATINO_OR_SPANISH": "Hispanic, Latino, or Spanish",
        "MIDDLE_EASTERN_OR_NORTH_AFRICAN": "Middle Eastern or North African",
        "HLS_AND_WHITE": r"H/L/S and White",
        "HLS_AND_BLACK": r"H/L/S and Black",
        "HLS_AND_ONE_OTHER_RACE": r"H/L/S and one other race",
        "HLS_AND_MORE_THAN_ONE_OTHER_RACE": r"H/L/S and more than one race",
        "UNSET": "Other",
        "UNMAPPED": "Other",
        "MORE_THAN_ONE_RACE": "Other",
        "OTHER_RACE": "Other",
        "PREFER_NOT_TO_SAY": "Other",
        "Skip": "Skip",
    }
    tokens = original.split("_")
    if original.upper() in conversion_map:
        return conversion_map[original.upper()]
    elif tokens[1] in conversion_map:
        return conversion_map[tokens[1]]
    elif len(tokens) != 2:
        return "RACE_ERROR"
    elif tokens[1] not in conversion_map:
        return f"{original} RACE_ERROR"
    raise Exception(f"Unhandled Race: {original}")


def convert_withdrawal_status(original):
    if original == 0 or original == "NOT_WITHDRAWN":
        return 0
    elif original == 1 or original == "NO_USE":
        return 1
    raise Exception(f"Unhandled Withdrawal Status: {original}")


def convert_primary_consent_status(original):
    zero = ["UNSET", "SUBMITTED_NO_CONSENT", "SUBMITTED_INVALID"]
    one = ["SUBMITTED"]
    two = ["SUBMITTED_NOT_SURE"]
    if original in zero:
        return 0
    elif original in one:
        return 1
    elif original in two:
        return 2
    raise Exception(f"Unhandled Primary Consent Status: {original}")


def convert_ehr_consent_status(original):
    zero = ["UNSET", "SUBMITTED_NO_CONSENT", "SUBMITTED_NOT_VALIDATED", "SUBMITTED_INVALID"]
    one = ["SUBMITTED"]
    two = ["SUBMITTED_NOT_SURE"]
    if original in zero:
        return 0
    elif original in one:
        return 1
    elif original in two:
        return 2
    raise Exception(f"Unhandled EHR Consent Status: {original}")


def convert_cabor_consent_status(original):
    zero = ["UNSET", "SUBMITTED_NO_CONSENT", "SUBMITTED_INVALID"]
    one = ["SUBMITTED"]
    two = ["SUBMITTED_NOT_SURE"]
    if original in zero:
        return 0
    elif original in one:
        return 1
    elif original in two:
        return 2
    raise Exception(f"Unhandled EHR Consent Status: {original}")

def convert_campus(original, response):
    quote_fix = original.replace("'", "\"")
    j = json.loads(quote_fix)
    results = []
    for entry in j:
        status = entry['status'].upper()
        organization = entry['organization']
        if status == response.upper():
            results.append(organization)
    return '; '.join(results)


def convert_deceased(original):
    zero = ["UNSET"]
    one = ["PENDING"]
    two = ["APPROVED"]
    if original in zero:
        return 0
    elif original in one:
        return 1
    elif original in two:
        return 2
    raise Exception(f"Unhandled EHR Consent Status: {original}")


def convert_field(value, type):
    """ Calls the appropriate conversion function based on field type. """
    if type == 'Date':
        return convert_date(value)
    if type == 'State':
        return convert_state(value)
    if type == 'Sex':
        return convert_sex(value)
    if type == 'Gender':
        return convert_gender(value)
    if type == 'Race':
        return convert_race(value)
    if type == 'Withdrawal':
        return convert_withdrawal_status(value)
    if type == 'Primary Consent':
        return convert_primary_consent_status(value)
    if type == 'EHR Consent':
        return convert_ehr_consent_status(value)
    if type == 'CampusYes':
        return convert_campus(value, "yes")
    if type == 'CampusNo':
        return convert_campus(value, "no")
    if type == 'CampusUnknown':
        return convert_campus(value, "unknown")
    if type == 'CampusNoAccess':
        return convert_campus(value, "noaccess")
    if type == 'Deceased':
        return convert_deceased(value)
    return value  # Return value unchanged if type is not found

def api_to_hp(api_file, out_file):
    """ Reads a CSV, applies field conversions, and writes it back. """

    fields_convert = {
        "Date of Birth": "Date",
        "State": "State",
        "Sex": "Sex",
        "Gender Identity": "Gender",
        "Race/Ethnicity": "Race",
        "Withdrawal Status": "Withdrawal",
        "Primary Consent Status": "Primary Consent",
        "EHR Consent Status": "EHR Consent",
        "Patient Status: Yes": "CampusYes",
        "Patient Status: No": "CampusNo",
        "Patient Status: No Access": "CampusNoAccess",
        "Patient Status: Unknown": "CampusUnknown",
        "Deceased": "Deceased",
    }

    # Read CSV, forcing all data as string
    df = pd.read_csv(api_file, converters=StringConverter(), delimiter=',', skiprows=1)

    # Apply transformations
    for index, row in df.iterrows():
        for col_name in df.columns:
            if col_name in fields_convert:
                df.at[index, col_name] = convert_field(row[col_name], fields_convert[col_name])

    for row in df:
        print(row)
    # Write the modified DataFrame back to a new CSV file
    df.to_csv(out_file, index=False, header=True)

if __name__ == "__main__":
    file1 = r"F:\dev.brian\aou_submission\build\out.csv"
    file2 = r"F:\dev.brian\aou_submission\build\ops_data_api_awardee_chunk_1_63708_CAL_PMC.csv"
    api_to_hp(file2, file1)
