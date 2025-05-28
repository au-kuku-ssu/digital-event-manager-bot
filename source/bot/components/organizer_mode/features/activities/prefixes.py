from components.organizer_mode.prefixes import ACTIVITIES_PREFIX



class ActivitiesPrefixes:
    PREFIX = f"{ACTIVITIES_PREFIX}main_"


class CommitteePrefixes:
    PREFIX = f"{ACTIVITIES_PREFIX}committee_"
    ADD = f"{ACTIVITIES_PREFIX}committee_add_"
    EDIT = f"{PREFIX}committee_edit_"
    EDIT_CHOOSE_PARTICIPANT= f"{EDIT}_member_"
    EDIT_CHOOSE_FIELD = f"{EDIT}_field_"
