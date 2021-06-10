"""AWS Comprehend connectors."""

# Import from standard library
from typing import List, Dict
import json
from operator import itemgetter

# Import from 3rd party libraries
import boto3


class Comprehend:
    """Controller for requests to the AWS Comprehend API."""

    translater = boto3.client(service_name="translate")
    translater_languages = [
        "af",
        "sq",
        "am",
        "ar",
        "hy",
        "az",
        "bn",
        "bs",
        "bg",
        "ca",
        "zh",
        "zh-TW",
        "hr",
        "cs",
        "da",
        "fa-AF",
        "nl",
        "en",
        "et",
        "fa",
        "tl",
        "fi",
        "fr",
        "fr-CA",
        "ka",
        "de",
        "el",
        "gu",
        "ht",
        "ha",
        "he",
        "hi",
        "hu",
        "is",
        "id",
        "it",
        "ja",
        "kn",
        "kk",
        "ko",
        "lv",
        "lt",
        "mk",
        "ms",
        "ml",
        "mt",
        "mn",
        "no",
        "fa",
        "ps",
        "pl",
        "pt",
        "ro",
        "ru",
        "sr",
        "si",
        "sk",
        "sl",
        "so",
        "es",
        "es-MX",
        "sw",
        "sv",
        "tl",
        "ta",
        "te",
        "th",
        "tr",
        "uk",
        "ur",
        "uz",
        "vi",
        "cy",
    ]

    comprehender = boto3.client(service_name="comprehend")
    comprehender_languages = [
        "ar",
        "hi",
        "ko",
        "zh-TW",
        "ja",
        "zh",
        "de",
        "pt",
        "en",
        "it",
        "fr",
        "es",
    ]

    def language(self, text: str) -> str:
        """Detect language of text.

        Args:
            text: string to detect language for
        Returns:
            Language code for text
        """
        return self.comprehender.detect_dominant_language(Text=text)["Languages"][0][
            "LanguageCode"
        ]

    def translate(self, text: str, source: str, target: str = "en") -> str:
        """Translate text.

        Args:
            text: string to translate
            source: language code for text input
            target: language code for text output
        Returns:
            Translated text
        """
        return self.translater.translate_text(
            Text=text, SourceLanguageCode=source, TargetLanguageCode=target
        )["TranslatedText"]

    def entities(
        self,
        text: str,
        language: str = "en",
        types: List["str"] = ["PERSON", "ORGANIZATION"],
    ) -> List[Dict]:
        """Detect named entities in text.

        Args:
            text: string to detect entities for
            language: language code for text
        Returns:
            List of detected entities with type, text and count

        """
        for type in types:
            assert type in [
                "PERSON",
                "LOCATION",
                "ORGANIZATION",
                "COMMERCIAL_ITEM",
                "EVENT",
                "DATE",
                "QUANTITY",
                "TITLE",
                "OTHER",
            ]

        entities = self.comprehender.detect_entities(Text=text, LanguageCode=language)[
            "Entities"
        ]

        entity_counts: Dict[str, int] = {}
        for e in entities:
            if e["Type"] in types:
                key = json.dumps({"type": e["Type"], "text": e["Text"].lower()})
                if key in entity_counts.keys():
                    entity_counts[key] += 1
                else:
                    entity_counts[key] = 1

        return sorted(
            [{**json.loads(k), "count": v} for k, v in entity_counts.items()],
            key=itemgetter("count"),
            reverse=True,
        )
