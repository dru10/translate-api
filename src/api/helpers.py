LANGUAGE_MAPPING = {
    "en": "english",
    "fr": "french",
    "de": "german",
    "ro": "romanian",
}


def convert_language_to_iso(language: str) -> str:
    language = language.lower()
    iso_mapping = {v: k for k, v in LANGUAGE_MAPPING.items()}
    try:
        return iso_mapping[language]
    except KeyError as e:
        raise ValueError(
            f"{language} is not supported, supported languages are: {', '.join(iso_mapping.keys())}"
        ) from e
