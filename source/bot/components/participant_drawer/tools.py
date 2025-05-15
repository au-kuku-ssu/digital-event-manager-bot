from os.path import dirname, join

from components.shared.locale import get_locale_str, load_locales

locale = load_locales(join(dirname(__file__), "locale"))
getstr = lambda lang, path: get_locale_str(locale, f"{lang}.{path}")


class CommitteeTools:
    def data_field_to_state(data_field: str):
        pass

    def state_to_data_field(state: str):
        pass
