from components.participant_drawer.prefixes import EVENTS_PREFIX


class EventsPrefixes:
    PREFIX = f"{EVENTS_PREFIX}main_"


class CommitteePrefixes:
    PREFIX = f"{EVENTS_PREFIX}committee_"
    EDIT = f"{PREFIX}committee_edit_"
    EDIT_CHOOSE_MEMBER = f"{EDIT}_member_"
    EDIT_CHOOSE_FIELD = f"{EDIT}_field_"
