STATE:       KILLED
OBJECT:      P2a Human Delta portable-core transplant package
EXACT_REF:   human-delta@e972da48f7b1334bdd9e8b393aeb492989d095c9
EVIDENCE:    The applied provenance listed nine portable files, but transplanted `scripts/sabotage_test.py` imports `scripts/transplant.py`, which was absent from the portable manifest; the target state and failing output are preserved at the exact target commit.
PROGRESS:    MEASUREMENT
EFFECT:      killed portable identity e46361e and required a new preregistered transplant candidate including its complete refutation surface
BLOCKED_ON:  none
NEXT_OWNER:  P2b registration against a new portable identity; do not repair or relabel P2a.
