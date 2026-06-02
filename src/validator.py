EXCLUDED_TERMS = [
    "government",
    "government of cambodia",
    "kingdom of cambodia",
    "royal government of cambodia",
    "gokc",
    "ifad",
    "international fund for agricultural development",
    "undaf",
    "united nations development assistance framework",
    "rome-based united nations agencies",
    "un agencies",
    "smallholders",
    "farmers",
    "producer organizations",
    "producers organisations",
    "agriculture cooperatives",
    "agricultural cooperative",
    "agricultural cooperatives",
    "private companies",
    "private sector coordination platform",
    "regional director",
    "country director",
    "regional economist",
    "reehana raza",
    "francisco pichon",
    "abdelkarim sma",
    "camgap",
    "cambodian good agriculture practice",
    "ministry of agriculture and development planning commission",
    "republic of korea",
    "finland",
    "economic intelligence unit",
    "world bank group",
    "technical working group on agriculture and water",
    "twg-aw",
]

PROGRAM_TERMS = [
    "asmp",
    "aspire",
    "aspire-at",
    "ifad-aspire",
    "aspire programme",
    "aspire secretariat",
    "aims",
    "caisar",
    "saambat",
    "sstc",
    "s-ret",
    "s-ret ii",
    "tssd",
    "nurture",
    "casdp",
    "selas",
    "bram",
    "asap",
    "spa",
    "ac/uac",
    "acs",
    "pos",
    "nso",
]

INVALID_PARTNER_TYPES = [
    "project",
    "programme",
    "program",
    "strategy",
    "framework",
    "initiative",
]

PERSON_TITLES = [
    "director",
    "economist",
    "manager",
    "specialist",
    "officer",
    "advisor",
    "consultant",
]

GENERIC_PHRASES = [
    "smallholder",
    "producer organization",
    "producer organisation",
    "agriculture cooperative",
    "agricultural cooperative",
    "private companies",
    "private sector",
    "un agencies",
    "development partners",
    "financial institutions",
]


def normalize_partner_name(name):
    clean_name = name.strip()
    key = clean_name.lower()

    # =====================
    # Multilateral / IFI partners
    # =====================

    if key == "adb" or "asian development bank" in key:
        return "Asian Development Bank"

    if key == "eib" or "european investment bank" in key:
        return "European Investment Bank"

    if key == "aiib" or "asian infrastructure investment bank" in key:
        return "Asian Infrastructure Investment Bank"

    if key == "world bank" or "world bank" in key:
        return "World Bank"

    if key == "eu" or "european union" in key:
        return "European Union"

    # =====================
    # Climate / environmental funds
    # =====================

    if key == "gcf" or "green climate fund" in key:
        return "Green Climate Fund"

    if (
        key == "gef"
        or "global environment fund" in key
        or "global environment facility" in key
    ):
        return "Global Environment Fund"

    # =====================
    # UN agencies
    # =====================

    if key == "fao" or "food and agriculture" in key:
        return "Food and Agriculture Organization of the United Nations"

    if key == "undp" or "united nations development programme" in key:
        return "United Nations Development Programme"

    if key == "wfp" or "world food programme" in key:
        return "World Food Programme"

    if key == "un women" or "un women" in key:
        return "UN Women"

    if key == "unicef" or "unicef" in key:
        return "UNICEF"

    if key == "uncdf" or "united nations capital development fund" in key:
        return "United Nations Capital Development Fund"

    # =====================
    # Bilateral / development partners
    # =====================

    if key == "sdc" or "swiss agency for development and cooperation" in key:
        return "Swiss Agency for Development and Cooperation"

    if key == "usaid" or "united states agency for international development" in key:
        return "United States Agency for International Development"

    if key == "dfat" or "department of foreign affairs and trade" in key:
        return "DFAT"

    if key == "afd" or "agence française de développement" in key or "agence francaise de developpement" in key:
        return "AFD"

    if key == "kfw" or "kfw" in key:
        return "KFW"

    # =====================
    # Cambodian government / public institutions
    # =====================

    if key == "mef" or "ministry of economy and finance" in key:
        return "Ministry of Economy and Finance"

    if key == "maff" or "ministry of agriculture, forestry and fisheries" in key:
        return "Ministry of Agriculture, Forestry and Fisheries"

    if key == "mowram" or "ministry of water resources and meteorology" in key:
        return "Ministry of Water Resources and Meteorology"

    if (
        key == "mrd"
        or "ministry of rural development" in key
        or "ministry for rural development" in key
    ):
        return "Ministry of Rural Development"

    if key == "moc" or "ministry of commerce" in key:
        return "Ministry of Commerce"

    if key == "mowa" or "ministry of women" in key:
        return "Ministry of Women’s Affairs"

    if (
        "ministry of industry and handicraft" in key
        or "ministry of industry and handicrafts" in key
    ):
        return "Ministry of Industry and Handicraft"

    if key == "moe" or "ministry of environment" in key:
        return "Ministry of Environment"

    if "ministry of planning" in key:
        return "Ministry of Planning"

    if key == "mosvy" or "ministry of social affairs" in key:
        return "Ministry of Social Affairs, Veterans and Youth Rehabilitation"

    if key == "card" or "council for agriculture and rural development" in key:
        return "Council for Agriculture and Rural Development"

    if key == "ncdd-s" or "national committee for sub-national democratic development" in key:
        return "National Committee for Sub-National Democratic Development Secretariat"

    if key == "snec" or "supreme national economic council" in key:
        return "Supreme National Economic Council"

    if key == "nbc" or "national bank of cambodia" in key:
        return "National Bank of Cambodia"

    if key == "gdpp" or "general department of public procurement" in key:
        return "General Department of Public Procurement"

    if key == "nis" or "national institute of statistics" in key:
        return "National Institute of Statistics"

    if (
        key == "cardi"
        or "cambodian agricultural research and development institute" in key
        or "cambodia agriculture research development institute" in key
        or "cambodia agricultural research and development institute" in key
    ):
        return "Cambodian Agricultural Research and Development Institute"

    # =====================
    # Financial institutions
    # =====================

    if (
        key == "ardb"
        or key == "arbd"
        or "agriculture and rural development bank" in key
        or "agricultural and rural development bank" in key
    ):
        return "Agricultural and Rural Development Bank"

    if key == "sme bank" or "sme bank" in key:
        return "SME Bank"

    if key == "amk" or "amk microfinance" in key:
        return "AMK Microfinance Plc"

    if key == "cma" or "cambodia microfinance association" in key:
        return "Cambodia Microfinance Association"

    if key == "cgcc" or "credit guarantee corporation of cambodia" in key:
        return "Credit Guarantee Corporation of Cambodia"

    # =====================
    # Farmer / producer organizations
    # =====================

    if key == "fnn" or "farmer and nature net" in key:
        return "Farmer and Nature Net"

    if (
        key == "cfap"
        or "cambodia farmer federation" in key
        or "cambodian farmer federation" in key
        or "cambodia farmer federation association" in key
        or "cambodian farmer federation association" in key
        or "cambodian farmer association federation" in key
    ):
        return "Cambodia Farmer Federation Association of Agricultural Producers"

    if key == "cacc" or "cacc" in key:
        return "CACC"

    # =====================
    # Research / knowledge / academic partners
    # =====================

    if (
        key == "ipsard"
        or "institute of policy and strategy for agriculture and rural development" in key
        or "policy and strategy for agriculture and rural development" in key
    ):
        return "Institute of Policy and Strategy for Agriculture and Rural Development"

    if key == "nardt" or "network for agriculture and rural development think-tanks" in key:
        return "Network for Agriculture and Rural Development Think-Tanks for Countries in Mekong Subregion"

    if "royal university of agriculture" in key:
        return "Royal University of Agriculture"

    if "prek leap national institute of agriculture" in key:
        return "Prek Leap National Institute of Agriculture"

    # =====================
    # Private sector / technology partners
    # =====================

    if key == "amru" or key == "amru rice" or "amru rice" in key:
        return "AMRU Rice"

    if "signature of asia" in key:
        return "Signature of Asia"

    if "natural agriculture village" in key:
        return "Natural Agriculture Village"

    if key == "remic" or "remic" in key:
        return "REMIC"

    if key == "agribuddy" or "agribuddy" in key:
        return "Agribuddy"

    if key == "bhaji" or key == "bhanji" or "bhanji" in key:
        return "BhanJi"

    if key == "angorsalad" or "angkor salad" in key or "angorsalad" in key:
        return "AngorSalad"

    if key == "kiu" or "kiu" in key:
        return "KiU"

    if key == "bronx" or "bronx technology" in key or key == "br0nx":
        return "Bronx Technology"

    if key == "tsc" or "techo startup center" in key:
        return "Techo Startup Center"

    # =====================
    # NGOs / civil society
    # =====================

    if "care cambodia" in key:
        return "CARE Cambodia"

    if key == "jci" or "jci" in key:
        return "JCI"

    if key == "cipo" or "cambodia indigenous peoples organization" in key:
        return "Cambodia Indigenous Peoples Organization"

    if "swisscontact" in key:
        return "SwissContact"

    if "cordaid" in key or "icco" in key:
        return "CordAid/ICCO"

    # =====================
    # Networks / platforms / certification
    # =====================

    if "grow asia" in key or "growasia" in key:
        return "Grow Asia"

    if "cambodia partnership for sustainable agriculture" in key:
        return "Cambodia Partnership for Sustainable Agriculture"

    if "smile khmer" in key:
        return "SMILE Khmer vegetable Network"

    if key == "ecocert" or "ecocert" in key:
        return "ECOCERT"

    if "camgap" in key or "cambodian good agriculture practice" in key:
        return "Cambodian Good Agriculture Practice"

    return clean_name


def normalize_partner_type(partner_type):
    clean_type = partner_type.strip()
    key = clean_type.lower()

    if not key:
        return "Other"

    if "ministry" in key or "government" in key or "public institution" in key:
        return "Government / Public Institution"

    if "funding" in key or "co-financing" in key or "financing partner" in key:
        return "Funding Partner"

    if "climate fund" in key or "fund" in key:
        return "Climate / Environmental Fund"

    if "financial institution" in key or "bank" in key or "microfinance" in key:
        return "Financial Institution"

    if "un agency" in key or "un " in key or "united nations" in key:
        return "UN Agency"

    if "ngo" in key or "civil society" in key:
        return "NGO / Civil Society"

    if "private" in key or "company" in key or "agritech" in key or "fintech" in key:
        return "Private Sector"

    if "producer" in key or "association" in key or "cooperative" in key:
        return "Producer / Farmer Organization"

    if "academic" in key or "research" in key or "university" in key:
        return "Research / Academic Institution"

    if "certification" in key:
        return "Certification Body"

    if "stakeholder" in key or "working group" in key or "coordination" in key:
        return "Stakeholder / Coordination Platform"

    if "development partner" in key or "international organization" in key:
        return "Development Partner"

    return clean_type


def validate_partners(partners):
    validated = []

    for partner in partners:
        raw_name = partner.get("partner_name", "").strip()
        raw_partner_type = partner.get("partner_type", "").strip()

        if not raw_name:
            continue

        normalized_name = normalize_partner_name(raw_name)
        normalized_type = normalize_partner_type(raw_partner_type)

        name_lower = normalized_name.lower()
        raw_name_lower = raw_name.lower()
        partner_type_lower = normalized_type.lower()
        raw_partner_type_lower = raw_partner_type.lower()

        if raw_partner_type_lower == "individual":
            continue

        if any(term in name_lower for term in EXCLUDED_TERMS):
            continue

        if any(term in raw_name_lower for term in EXCLUDED_TERMS):
            continue

        if any(term in name_lower for term in PROGRAM_TERMS):
            continue

        if any(term in raw_name_lower for term in PROGRAM_TERMS):
            continue

        if any(word in partner_type_lower for word in INVALID_PARTNER_TYPES):
            continue

        if any(word in raw_partner_type_lower for word in INVALID_PARTNER_TYPES):
            continue

        if any(word in name_lower for word in INVALID_PARTNER_TYPES):
            continue

        if any(title in name_lower for title in PERSON_TITLES):
            continue

        if any(phrase in name_lower for phrase in GENERIC_PHRASES):
            continue

        partner["partner_name"] = normalized_name
        partner["partner_type"] = normalized_type

        validated.append(partner)

    return validated


def deduplicate_partners(partners):
    grouped = {}

    for partner in partners:
        name = partner.get("partner_name", "").strip()

        if not name:
            continue

        if name not in grouped:
            grouped[name] = {
                "partner_name": name,
                "partner_type": partner.get("partner_type", ""),
                "roles": set(),
                "pages": set(),
                "evidence_sentences": set(),
            }

        role = partner.get("role", "")
        page = partner.get("page_number", "")
        evidence = partner.get("evidence_sentence", "")

        if role:
            grouped[name]["roles"].add(role)

        if page:
            grouped[name]["pages"].add(page)

        if evidence:
            grouped[name]["evidence_sentences"].add(evidence)

    final_results = []

    for item in grouped.values():
        evidence_list = list(item["evidence_sentences"])

        final_results.append({
            "partner_name": item["partner_name"],
            "partner_type": item["partner_type"],
            "mention_count": len(evidence_list),
            "pages": ", ".join(str(p) for p in sorted(item["pages"])),
            "roles": " | ".join(sorted(item["roles"])),
            "sample_evidence": evidence_list[0] if evidence_list else "",
            "all_evidence": " || ".join(evidence_list),
        })

    return sorted(
        final_results,
        key=lambda x: x["mention_count"],
        reverse=True
    )