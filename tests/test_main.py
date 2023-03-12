import json
from typing import Optional
from src.main import get_diff, main
from pydantic import BaseModel


def test_get_diff_finds_differences_in_nested_dictionaries():
    sentinel = object()
    dictionary_1 = {"a": 123, "b": {"c": "zzz", "d": "xxx", "e": {"f": None, "g": 6, "h": 5}}, "i": 456, "j": 1}
    dictionary_2 = {"a": 123, "b": {"c": "zzz", "d": "yyy", "e": {"f": 4, "g": 6}}, "i": 789, "k": 2}

    difference = get_diff(dictionary_1, dictionary_2, sentinel)
    expected_difference = {
        "b": {
            "d": ("xxx", "yyy"),
            "e": {
                "f": (None, 4),
                "h": (5, sentinel),
            },
        },
        "i": (456, 789),
        "j": (1, sentinel),
        "k": (sentinel, 2),
    }
    assert difference == expected_difference


def test_get_diff_finds_differences_in_json_objects():
    sentinel = object()

    json_1 = json.dumps(
        {
            "a": "abc",
            "b": {
                "c": "def",
                "d": 123,
                "e": "xxx"
            }
        }
    )
    json_2 = json.dumps(
        {
            "a": "tuv",
            "b": {
                "c": "ghi",
                "d": 123
            }
        }
    )

    difference = get_diff(json_1, json_2, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", sentinel)
        }
    }
    assert difference == expected_difference

def test_get_diff_finds_differences_in_nested_pydantic_objects():
    sentinel = object()
    class SomeNestedClass(BaseModel):
        c: str
        d: int
        e: Optional[str]

    class SomeClass(BaseModel):
        a: str
        b: SomeNestedClass
    obj_1 = SomeClass(a="abc", b=SomeNestedClass(c="def", d=123, e="xxx"))
    obj_2 = SomeClass(a="tuv", b=SomeNestedClass(c="ghi", d=123))

    difference = get_diff(obj_1, obj_2, sentinel)
    expected_difference = {
        "a": ("abc", "tuv"),
        "b": {
            "c": ("def", "ghi"),
            "e": ("xxx", None)
        }
    }
    assert difference == expected_difference


def test_get_diff_finds_differences_in_strings():
    sentinel = object()

    str_1 = "abcdefghijklmnop12345"
    str_2 = "abcdexghiyzlmnop23345"
    difference = get_diff(str_1, str_2, sentinel)
    assert difference == [
        ["abcde", "abcde"],
        ["f", "x"],
        ["ghi", "ghi"],
        ["jk", "yz"],
        ["lmnop", "lmnop"],
        ["12", "23"],
        ["345", "345"]
    ]


def test_main():
    sentinel = object()
    expected_body = {
        "uid": "79da3ec3-d5bb-49f1-842a-8561b02bf006",
        "created_at": "2022-05-10T14:00:10.961047+00:00",
        "updated_at": "2022-10-25T15:15:33.075228+00:00",
        "company": {
            "uid": "2a6ff18b-6646-43a5-bdc4-a450893db097",
            "location": {
                "address": "Neue Grünstraße 27, Berlin, Deutschland",
                "street_name": "Neue Grünstraße",
                "street_number": "27",
                "city": "Berlin",
                "country_code": "de",
                "postal_code": "10179",
                "coordinates": {"lat": 52.5102559, "lon": 13.405686100000025},
            },
            "logo_url": "https://d2nk66epwbpimf.cloudfront.net/images/a64610cd-29e1-454b-b92c-0d101b611c6f/b3dc238c-1ea4-4830-bba1-35916c273267.png",
            "name": "EIGENSONNE GmbH",
            "seo_whitelisted": False,
            "subdomain": ["eigensonne"],
            "is_client": True,
        },
        "salary": {
            "period": "year",
            "currency": "EUR",
            "amount": None,
            "range_min": None,
            "range_max": None,
            "incentive": None,
            "is_salary_available": False,
        },
        "cpc": 0,
        "description": {"en": None, "de": "something different"},
        "language": "de",
        "link_out_type": None,
        "location": {
            "address": "Berlin, Deutschland",
            "street_name": None,
            "street_number": None,
            "city": "Berlin",
            "country_code": "de",
            "postal_code": "10178",
            "coordinates": {"lat": 52.52000659999999, "lon": 13.404954},
        },
        "posting_publish_time": "2022-06-10T14:01:11.969763+00:00",
        "source": None,
        "title": {"en": None, "de": "Data Engineer (m/f/d)", "suggest_search_as_you_type": "Data Engineer (m/f/d)"},
        "description_vector_128": None,
        "description_vector_512": None,
        "title_vector_128": None,
        "title_vector_512": None,
        "talent_platform_weight": 1.0,
        "talent_platform_status": "published",
        "allow_easy_apply": True,
        "employment_types": ["permanent_employment"],
        "open_for_career_changers": False,
        "required_education": None,
        "required_experience": None,
        "schedule_type": None,
        "shift": None,
        "working_hours_type": "full_time",
        "working_from_home": None,
        "job_type": {"codename": "other", "localized_keywords": None, "localized_synonyms": None, "localized_name": "Andere"},
    }

    actual = {
        "uid": "736c5eaf-1bab-48e0-8319-b379fc87f7ca",
        "created_at": "2022-08-02T10:00:20.187576+00:00",
        "updated_at": "2022-10-25T15:54:55.110791+00:00",
        "company": {
            "uid": "902bbdff-8ac2-448f-84d3-83f7e1e104df",
            "location": {
                "address": "Vulkanstraße 1, 10367 Berlin, Deutschland",
                "street_name": "Vulkanstraße",
                "street_number": "1",
                "city": "Berlin",
                "country_code": "de",
                "postal_code": "10367",
                "coordinates": {"lat": 52.5236864, "lon": 13.4863921},
            },
            "logo_url": "https://d2nk66epwbpimf.cloudfront.net/images/ba33ca98-ec4f-4de4-baf2-6526ae9b7faa/f387eb21-db2b-4b4d-851b-e2bcb3868b96.png",
            "name": "Digital Career Institute gGmbH",
            "seo_whitelisted": False,
            "subdomain": ["dci-jobs-personio"],
            "is_client": True,
        },
        "salary": {
            "period": "year",
            "currency": "EUR",
            "amount": None,
            "range_min": None,
            "range_max": None,
            "incentive": None,
            "is_salary_available": False,
        },
        "cpc": 0,
        "description": {
            "en": None,
            "de": "Deine AufgabenWir sind auf der Suche nach einem Daten- und Automatisierungsingenieur/in (w/m/d), der/die das Team beim weiteren Aufbau und der Pflege der zentralen Dateninfrastruktur vom DCI sowie der damit verbundenen Workflows zur Automatisierung von Geschäftsprozessen unterstützt. Da das DCI weiter wächst, möchten wir unsere Dateninfrastruktur der nächsten Generation auf AWS aufbauen.Du implementierst und verwaltest die Data Lake-Infrastruktur auf AWSAufbau und Pflege von ETL-Pipelines für verschiedene Datenquellen und -ziele gehören zu Deinen AufgabenDu entwickelst (Mikro-)Dienste zur ProzessautomatisierungDu bist für die kontinuierliche Verbesserung und Überwachung von Automatisierungs- und DatenprozessenDeine SkillsDu besitzt die Fähigkeit zur selbständigen Implementierung von Daten-/ETL-PipelinesDein fortgeschrittenes Verständnis von Konzepten für relationale Datenbanken, Verwaltung und SQL ist für uns essentiellDu bringst Kenntnisse und Verständnis für die Implementierung von Automatisierungs-(Mikro-)Diensten mitMit AWS und Data Lake-Konzepten bist du VertrautDu verfügst über Erfahrung in der Softwareentwicklung (entweder node.js/javascript, python und/oder go)Erfahrung mit PostgreSQL, SQL und relationalen Datenbankkonzepten und -verwaltung gehören zu Deinen FähigkeitenCI/CD, Überwachung und Alarmierung sind für Dich keine NeuheitDeine BenefitsViel Verantwortung und Gestaltungsspielraum in einem dynamischen Lernumfeld mit Startup-Atmosphäre in einem regional wachsendem Unternehmen.Zusammenarbeit mit einem internationalem Team, das Vielfalt, Humor, Teamspirit und gegenseitige Unterstützung sowie Wertschätzung \xa0groß schreibt.Intensive Einarbeitung und Weiterentwicklungsmöglichkeiten durch regelmäßige Feedbacks, Schulungen und Coaching.Sei Teil einer wertvollen Mission und verantwortungsvollen Aufgabe, denn durch Bildung bieten wir Menschen eine Perspektive.Diverse Team Events und Parties (auch virtuelle), Mitarbeiterrabatte (Corporate Benefits) und kostenlose Sportangebote erwarten dich natürlich ebenfalls. ",
        },
        "language": "de",
        "link_out_type": None,
        "location": {
            "address": "Berlin, Deutschland",
            "street_name": None,
            "street_number": None,
            "city": "Berlin",
            "country_code": "de",
            "postal_code": "10178",
            "coordinates": {"lat": 52.52000659999999, "lon": 13.404954},
        },
        "posting_publish_time": "2022-08-02T10:00:20.183385+00:00",
        "source": None,
        "title": {
            "en": None,
            "de": "Data & Automation Engineer (w/m/d)",
            "suggest_search_as_you_type": "Data & Automation Engineer (w/m/d)",
        },
        "title_vector_128": None,
        "title_vector_512": None,
        "talent_platform_weight": 1.0,
        "talent_platform_status": "published",
        "allow_easy_apply": True,
        "employment_types": ["permanent_employment"],
        "open_for_career_changers": False,
        "required_education": None,
        "required_experience": None,
        "schedule_type": None,
        "shift": None,
        "working_hours_type": "full_time",
        "working_from_home": None,
        "job_type": {"codename": "other", "localized_keywords": None, "localized_synonyms": None, "localized_name": "Andere"},
    }
    main(actual, expected_body, sentinel)
