from components.participant_drawer.prefixes import ACTIVITIES_PREFIX


class AcktivitiesPrefixes:
    PREFIX = f"{ACTIVITIES_PREFIX}main_"


class CommitteePrefixes:
    PREFIX = f"{ACTIVITIES_PREFIX}committee_"
    EDIT = f"{PREFIX}committee_edit_"
    EDIT_CHOOSE_MEMBER = f"{EDIT}_member_"
    EDIT_CHOOSE_FIELD = f"{EDIT}_field_"
