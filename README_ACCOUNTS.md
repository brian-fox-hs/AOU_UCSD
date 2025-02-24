# Accounts

All of Us is spread across various tools.  Confluence.  Google.  PMI Ops.  ZenDesk.  And so forth.

This is a partial list.  Please add stuff (or correct) as you find it.

### To get access to google groups: 

Contact AoU EHR Operations Group <aou-ehr-operations-group@googlegroups.com>
 
### To get all purpose general support for the EHR submission: 

Contact DRC Support <drcsupport@vumc.org>
 
### To get access to ZenDesk

Contact support@aou-ehr-ops.zendesk.com

### Other accounts

TODO: I'm pretty sure this is a partial list.  But time is fleeting.  Add them here when you find more please.


# Noise

Google groups and the EHR weekly meeting notes tend to be NOISY.  It's very difficult to coalesce the big picture 
from either of these sources.

# Good coalesced documentation for data submissions

From a technical standpoint, you should be aware of a few pieces of crucial documentation.  

### Data stewrdship

The first bit of documentation explains how to gain credentials to even submit data.  EHR Ops calls these 
credentials `data stewardship`.  At the moment, each participating org gets two stewards and there's an 
application process to gain access.

The application process is documented.  You can find it here:

https://aou-ehr-ops.zendesk.com/hc/en-us/categories/1500001782581-Making-File-Submission

### OMOP Data Format

The second piece of documentation explains how to format files with some decent amount of granularity.
It covers things like file names, typing, and so on.

https://aou-ehr-ops.zendesk.com/hc/en-us/sections/1500002391122-OMOP-v-5-3-1-

### Patient matching

Make sure you have an established algorithm describing exactly how to match patients between HealthPro and local
EHR/EMRs (in our case, managed by Epic).  

Apparently WE (as a participating organization, meaning UCSD) have the obligation to define the algorithm WE
are going to us:

```
Ultimately each partner HPO determines the criteria that are acceptable to their organization to validate 
EHR data is linked with the correct participant IDs prior to sending the data to the DRC. 

Organizations have adopted a number of different approaches to validate this linkage. The role 
of the DRC, to ensure data quality, is to conduct independent identity validation checks and 
inform sites in instances in which a validation status appears incorrect
```

So EHR dodges and punts on the exact algorith.

But they do provide an example truth table of sorts.  You can find it here:

#### Patient matching docs in Google Docs (link will be finicky)

https://docs.google.com/document/d/1eA815KpS3Qro8BhLcx8KZv-impNgHi9GsHsGjU-cbtA/edit

#### Patient matching docs in ZenDesk

https://aou-ehr-ops.zendesk.com/hc/en-us/articles/1500012461361-Participant-Tables

Scroll down to the `Participant Match Table` section.

#### OUR algorithm

We define OUR algorithm in README_PATIENT_MATCHING.md
