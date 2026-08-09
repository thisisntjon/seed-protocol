STATE:       DONE
OBJECT:      Encode and test the distinction between verified progress and infrastructure activity
EXACT_REF:   d609ef97845a0cdfbf414cef007124d2fb2d16be
EVIDENCE:    `python scripts/sabotage_test.py` returned 14/14, including independent assertions that an infrastructure receipt leaves verified loops at zero and a measurement receipt increments them to one; `python scripts/onboard_check.py` returned 0 errors.
PROGRESS:    MEASUREMENT
EFFECT:      confirmed that the status surface distinguishes one measured loop from infrastructure-only completion
BLOCKED_ON:  none
NEXT_OWNER:  P2 transplant uses this progress contract; P3 tests whether it improves real project outcomes.
