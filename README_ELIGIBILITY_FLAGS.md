# Patient Eligibility

# Update

## This is an email sent from EHR Ops on 10/06/2022:

Hi Brian, thanks for your email.
 
I’ve “translated” those criteria into their field name equivalents.
 
The following criteria must be met in order to transfer participant EHR data to the DRC:

```
consentForStudyEnrollment = 1
AND consentForElectronicHealthRecords = 1
AND withdrawalStatus = 0
AND 
    (
        onsiteIdVerificationTime = NOT NULL 
        OR participant provided records via Sync 4 Science (Sync 4 Science is not a value on the WQ or WQ export)
    )
AND
If participant located in California,  consentForCABoR = 1

If you have any additional questions about these fields, there is extensive documentation provided in the Ops Data API Data Dictionary HERE (The Work Queue is essentially an in-application UI for the API)

Many thanks,
Keo
```


# Whose records can we upload?

See the link and document below.

This is the only document that I could find that came close to describing EHR upload eligibility.  I don't 
know what "General Consent" means.  It's not well paired to a field in HealthPro.

Dumping it here for now.  


----

# EHR Ops description
Copied 2022-10-05 from:
https://aou-ehr-ops.zendesk.com/hc/en-us/articles/1500012461741-Criteria-for-Participant-EHR-Data-Transfer

Criteria for Participant EHR Data Transfer
1 year ago Updated


The following criteria must be met in order to transfer participant EHR data to the DRC:

General Consent = Complete

General Consent = Yes

EHR Consent = Complete

EHR Consent = Yes

Withdrawn = No

California Bill of Rights (if in California) = Yes

ID proofed and linkage established to MRN | OR | participant provided records via S4S

For the use of the HealthPro Ops Data API:

Patients who

withdrawalStatus=NOT_WITHDRAWN
AND consentForStudyEnrollment=SUBMITTED
AND consentForElectronicHealthRecords=SUBMITTED
*For participants who are deactivated, we only submit their data prior to deactivation date.

The DRC is currently pursuing a more specific list of minimum requirements for participant 
ID verification with the Consortium. Currently it is up to sites to set these requirements.