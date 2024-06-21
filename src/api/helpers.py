def convert_language_to_iso(language: str) -> str:
    language = language.lower()
    iso_mapping = {
        "english": "en",
        "chinese": "zh",
        "french": "fr",
        "german": "de",
        "spanish": "es",
        "italian": "it",
        "portuguese": "pt",
        "romanian": "ro",
    }
    try:
        return iso_mapping[language]
    except KeyError as e:
        raise ValueError(
            f"{language} is not supported, supported languages are: {', '.join(iso_mapping.keys())}"
        ) from e
