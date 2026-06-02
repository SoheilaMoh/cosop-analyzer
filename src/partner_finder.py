import re
from collections import defaultdict


PARTNER_KEYWORDS = {
    "ADB": "International Financial Institution",
    "Asian Development Bank": "International Financial Institution",
    "World Bank": "International Financial Institution",
    "World Bank Group": "International Financial Institution",
    "FAO": "UN Agency",
    "Food and Agriculture Organization": "UN Agency",
    "UNDP": "UN Agency",
    "UNICEF": "UN Agency",
    "WFP": "UN Agency",
    "European Union": "Donor / Development Partner",
    "EU": "Donor / Development Partner",
    "European Investment Bank": "International Financial Institution",
    "EIB": "International Financial Institution",
    "Asian Infrastructure Investment Bank": "International Financial Institution",
    "AIIB": "International Financial Institution",
    "Green Climate Fund": "Climate Fund",
    "GCF": "Climate Fund",
    "Global Environment Facility": "Climate Fund",
    "GEF": "Climate Fund",
    "Grow Asia": "Private Sector / Partnership Platform",
    "MAFF": "Government",
    "Ministry of Agriculture": "Government",
    "MEF": "Government",
    "Ministry of Economy and Finance": "Government",
    "MoWRAM": "Government",
    "Ministry of Water Resources": "Government",
}


def split_into_sentences(text):
    return re.split(r"(?<=[.!?])\s+", text)


def find_partner_mentions(pages):
    raw_results = []

    for page in pages:
        page_number = page["page"]
        text = page["text"]
        sentences = split_into_sentences(text)

        for sentence in sentences:
            for partner_name, partner_type in PARTNER_KEYWORDS.items():
                if partner_name.lower() in sentence.lower():
                    raw_results.append({
                        "partner_name": partner_name,
                        "partner_type": partner_type,
                        "page_number": page_number,
                        "evidence_sentence": sentence.strip()
                    })

    return raw_results


def summarize_partners(partner_mentions):
    grouped = defaultdict(lambda: {
        "partner_name": "",
        "partner_type": "",
        "mention_count": 0,
        "pages": set(),
        "sample_evidence": ""
    })

    for mention in partner_mentions:
        name = mention["partner_name"]
        grouped[name]["partner_name"] = name
        grouped[name]["partner_type"] = mention["partner_type"]
        grouped[name]["mention_count"] += 1
        grouped[name]["pages"].add(mention["page_number"])

        if not grouped[name]["sample_evidence"]:
            grouped[name]["sample_evidence"] = mention["evidence_sentence"]

    summary = []

    for item in grouped.values():
        summary.append({
            "partner_name": item["partner_name"],
            "partner_type": item["partner_type"],
            "mention_count": item["mention_count"],
            "pages": ", ".join(str(p) for p in sorted(item["pages"])),
            "sample_evidence": item["sample_evidence"]
        })

    return sorted(summary, key=lambda x: x["mention_count"], reverse=True)