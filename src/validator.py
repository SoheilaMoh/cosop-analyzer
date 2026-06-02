import re


EXCLUDED_TERMS = [
    # Generic / non-partner entities
    "government",
    "government of indonesia",
    "republic of indonesia",
    "government of cambodia",
    "kingdom of cambodia",
    "royal government of cambodia",
    "gokc",
    "ifad",
    "international fund for agricultural development",
    "cosop",
    "country strategic opportunities programme",
    "executive board",
    "un resident coordinator",

    # Generic groups / roles
    "regional director",
    "country director",
    "regional economist",
    "technical specialist",
    "finance officer",
    "project director",
    "project manager",
    "ministries",
    "districts",
    "village authorities",
    "pmu",
    "pmus",
    "project management units",

    # Frameworks / broad categories
    "undaf",
    "unsdcf",
    "united nations development assistance framework",
    "united nations sustainable development cooperation framework",
    "rome-based united nations agencies",
    "rome-based agencies",
    "un agencies",
    "smallholders",
    "smallholder farmers",
    "farmers",
    "producer organizations",
    "producers organisations",
    "agriculture cooperatives",
    "agricultural cooperative",
    "agricultural cooperatives",
    "private companies",
    "private sector",
    "private sector coordination platform",
    "development partners",
    "financial institutions",

    # People
    "reehana raza",
    "ivan cossio cortez",
    "francisco pichon",
    "abdelkarim sma",
    "mylene kherallah",
    "mark biriukov",

    # Country names when extracted alone
    "indonesia",
    "cambodia",
    "republic of korea",
    "finland",
    "netherlands",
    "united kingdom",
    "kingdom of norway",

    # Other non-partner terms
    "economic intelligence unit",
    "world bank group",
    "technical working group on agriculture and water",
    "twg-aw",
    "indonesia’s national environmental quality index",
    "national environmental quality index",
    "kredit usaha rakyat",
    "secap",
    "camgap",
    "cambodian good agriculture practice",
    "ministry of agriculture and development planning commission",
]


PROGRAM_TERMS = [
    # Cambodia programmes
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

    # Indonesia programmes / projects
    "yess",
    "tekad",
    "readsi",
    "upland",
    "uplands",
    "ipdmip",
    "hddap",
    "iard",
    "copli",
    "impli",
    "clpe",
    "mahfsa",
    "rural empowerment and agricultural development scaling-up initiative",
    "youth entrepreneurship and employment support services programme",
    "integrated village economic transformation project",
    "uplands agriculture productivity and markets project",
    "integrated participatory development and management of irrigation project",
    "horticulture development in dryland areas project",
    "integrated agriculture regional development project",
    "sustainable management of peatland ecosystems",
    "integrated management of peatland landscapes",
    "measurable action for haze-free sustainable land management",
]


INVALID_PARTNER_TYPES = [
    "project",
    "programme",
    "program",
    "strategy",
    "framework",
    "initiative",
    "risk",
    "indicator",
    "policy",
    "plan",
]


PERSON_TITLES = [
    "director",
    "economist",
    "manager",
    "specialist",
    "officer",
    "advisor",
    "consultant",
    "minister",
]


GENERIC_PHRASES = [
    "smallholder",
    "small-scale producer",
    "farmer",
    "producer organization",
    "producer organisation",
    "agriculture cooperative",
    "agricultural cooperative",
    "private companies",
    "private sector",
    "un agencies",
    "development partners",
    "financial institutions",
    "local governments",
    "district governments",
    "village authorities",
]


def normalize_text(text):
    return (
        str(text)
        .strip()
        .lower()
        .replace("’", "'")
        .replace("–", "-")
        .replace("—", "-")
    )


def contains_any(text, terms):
    text = normalize_text(text)
    return any(term in text for term in terms)


def is_exact_excluded_name(name):
    key = normalize_text(name)
    return key in [normalize_text(term) for term in EXCLUDED_TERMS]


def normalize_partner_name(name):
    clean_name = str(name).strip()
    key = normalize_text(clean_name)

    # =====================
    # Multilateral / IFI partners
    # =====================

    if key == "adb" or "asian development bank" in key:
        return "Asian Development Bank"

    if key == "world bank" or "world bank" in key:
        return "World Bank"

    if key == "eib" or "european investment bank" in key:
        return "European Investment Bank"

    if key == "aiib" or "asian infrastructure investment bank" in key:
        return "Asian Infrastructure Investment Bank"

    if (
        key == "isdb"
        or key == "islamic development bank"
        or "islamic development bank" in key
    ):
        return "Islamic Development Bank"

    if key == "eu" or "european union" in key:
        return "European Union"

    if key == "ofid" or "opec fund" in key:
        return "OPEC Fund"

    if "food and agricultural organization" in key:
        return "Food and Agriculture Organization of the United Nations"

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

    if key in ["un women", "un-women"] or "un women" in key or "un-women" in key:
        return "UN Women"

    if key == "unicef" or "unicef" in key:
        return "UNICEF"

    if key == "uncdf" or "united nations capital development fund" in key:
        return "United Nations Capital Development Fund"

    if key == "ilo" or "international labour organization" in key:
        return "International Labour Organization"

    # =====================
    # Bilateral / development partners
    # =====================

    if key == "usaid" or "united states agency for international development" in key:
        return "United States Agency for International Development"

    if key == "sdc" or "swiss agency for development and cooperation" in key:
        return "Swiss Agency for Development and Cooperation"

    if key == "dfat" or "department of foreign affairs and trade" in key:
        return "DFAT"

    if (
        key == "afd"
        or "agence française de développement" in key
        or "agence francaise de developpement" in key
    ):
        return "AFD"

    if key == "kfw" or "kfw" in key:
        return "KFW"

    if key == "giz" or key == "gtz" or "deutsche gesellschaft" in key:
        return "GIZ"

    # =====================
    # Indonesia government / public institutions
    # =====================

    if (
        key == "bappenas"
        or "bappenas" in key
        or "ministry for national development planning" in key
        or "ministry of national development planning" in key
        or "national development planning agency" in key
    ):
        return "Bappenas"

    if key == "mof" or "ministry of finance" in key:
        return "Ministry of Finance"

    if (
        key == "moa"
        or "ministry of agriculture" in key
        or "indonesian ministry of agriculture" in key
    ):
        return "Ministry of Agriculture"

    if (
        key == "moef"
        or "moef" in key
        or "ministry of environment and forestry" in key
        or "ministry of environment" in key
        or "ministry of forestry" in key
    ):
        return "Ministry of Environment and Forestry"

    if (
        key == "mov"
        or "ministry of villages" in key
        or "ministry of village" in key
        or "ministry of villages, development of disadvantaged regions and transmigration" in key
        or "ministry of villages development of disadvantaged regions and transmigration" in key
    ):
        return "Ministry of Villages, Development of Disadvantaged Regions and Transmigration"

    if key == "moha" or "ministry of home affairs" in key:
        return "Ministry of Home Affairs"

    if (
        key == "ojk"
        or "indonesia financial services authority" in key
        or "financial services authority" in key
    ):
        return "Indonesia Financial Services Authority"

    if key == "bi" or "bank indonesia" in key or "bank of indonesia" in key:
        return "Bank Indonesia"

    if key == "bps" or "statistics indonesia" in key:
        return "Statistics Indonesia"

    # =====================
    # Cambodia government / public institutions
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
    # ASEAN / regional bodies
    # =====================

    if key == "asean" or "association of southeast asian nations" in key:
        return "Association of Southeast Asian Nations"

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

    if key == "mars" or key == "mars inc" or key == "mars inc." or "mars inc" in key:
        return "Mars Inc."

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
    clean_type = str(partner_type).strip()
    key = normalize_text(clean_type)

    if not key:
        return "Other"

    if "ministry" in key or "government" in key or "public institution" in key:
        return "Government / Public Institution"

    if "funding" in key or "co-financing" in key or "financing partner" in key:
        return "Funding Partner"

    if "climate fund" in key or "environmental fund" in key or "fund" in key:
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

    if (
        "development partner" in key
        or "international organization" in key
        or "bilateral" in key
        or "multilateral" in key
    ):
        return "Development Partner"

    return clean_type


def infer_partner_type(partner_name, normalized_type):
    key = normalize_text(partner_name)

    if partner_name in [
        "Asian Development Bank",
        "Islamic Development Bank",
        "European Union",
        "United States Agency for International Development",
        "Swiss Agency for Development and Cooperation",
        "DFAT",
        "AFD",
        "KFW",
        "GIZ",
        "OPEC Fund",
    ]:
        return "Development Partner"

    if partner_name in [
        "World Bank",
        "European Investment Bank",
        "Asian Infrastructure Investment Bank",
        "Agricultural and Rural Development Bank",
        "SME Bank",
        "AMK Microfinance Plc",
        "Cambodia Microfinance Association",
        "Credit Guarantee Corporation of Cambodia",
        "Bank Indonesia",
    ]:
        return "Financial Institution"

    if partner_name in [
        "Green Climate Fund",
        "Global Environment Fund",
    ]:
        return "Climate / Environmental Fund"

    if partner_name in [
        "Food and Agriculture Organization of the United Nations",
        "United Nations Development Programme",
        "World Food Programme",
        "UN Women",
        "UNICEF",
        "United Nations Capital Development Fund",
        "International Labour Organization",
    ]:
        return "UN Agency"

    if partner_name in [
        "Bappenas",
        "Ministry of Finance",
        "Ministry of Agriculture",
        "Ministry of Environment and Forestry",
        "Ministry of Villages, Development of Disadvantaged Regions and Transmigration",
        "Ministry of Home Affairs",
        "Indonesia Financial Services Authority",
        "Statistics Indonesia",
        "Ministry of Economy and Finance",
        "Ministry of Agriculture, Forestry and Fisheries",
        "Ministry of Water Resources and Meteorology",
        "Ministry of Rural Development",
        "Ministry of Commerce",
        "Ministry of Women’s Affairs",
        "Ministry of Industry and Handicraft",
        "Ministry of Environment",
        "Ministry of Planning",
        "Ministry of Social Affairs, Veterans and Youth Rehabilitation",
        "Council for Agriculture and Rural Development",
        "National Committee for Sub-National Democratic Development Secretariat",
        "Supreme National Economic Council",
        "National Bank of Cambodia",
        "General Department of Public Procurement",
        "National Institute of Statistics",
        "Cambodian Agricultural Research and Development Institute",
    ]:
        return "Government / Public Institution"

    if partner_name in [
        "Mars Inc.",
        "AMRU Rice",
        "Signature of Asia",
        "Natural Agriculture Village",
        "REMIC",
        "Agribuddy",
        "BhanJi",
        "AngorSalad",
        "KiU",
        "Bronx Technology",
        "Techo Startup Center",
    ]:
        return "Private Sector"

    if partner_name in [
        "Association of Southeast Asian Nations",
        "Grow Asia",
        "Cambodia Partnership for Sustainable Agriculture",
        "SMILE Khmer vegetable Network",
    ]:
        return "Stakeholder / Coordination Platform"

    if partner_name in [
        "Farmer and Nature Net",
        "Cambodia Farmer Federation Association of Agricultural Producers",
        "CACC",
    ]:
        return "Producer / Farmer Organization"

    if partner_name in [
        "CARE Cambodia",
        "JCI",
        "Cambodia Indigenous Peoples Organization",
        "SwissContact",
        "CordAid/ICCO",
    ]:
        return "NGO / Civil Society"

    if partner_name in [
        "Institute of Policy and Strategy for Agriculture and Rural Development",
        "Network for Agriculture and Rural Development Think-Tanks for Countries in Mekong Subregion",
        "Royal University of Agriculture",
        "Prek Leap National Institute of Agriculture",
    ]:
        return "Research / Academic Institution"

    if partner_name in [
        "ECOCERT",
        "Cambodian Good Agriculture Practice",
    ]:
        return "Certification Body"

    return normalized_type


def validate_partners(partners):
    validated = []

    for partner in partners:
        raw_name = str(partner.get("partner_name", "")).strip()
        raw_partner_type = str(partner.get("partner_type", "")).strip()

        if not raw_name:
            continue

        normalized_name = normalize_partner_name(raw_name)
        normalized_type = normalize_partner_type(raw_partner_type)
        normalized_type = infer_partner_type(normalized_name, normalized_type)

        name_lower = normalize_text(normalized_name)
        raw_name_lower = normalize_text(raw_name)
        partner_type_lower = normalize_text(normalized_type)
        raw_partner_type_lower = normalize_text(raw_partner_type)

        if raw_partner_type_lower == "individual":
            continue

        if is_exact_excluded_name(normalized_name) or is_exact_excluded_name(raw_name):
            continue

        if contains_any(name_lower, PROGRAM_TERMS) or contains_any(raw_name_lower, PROGRAM_TERMS):
            continue

        if contains_any(partner_type_lower, INVALID_PARTNER_TYPES):
            continue

        if contains_any(raw_partner_type_lower, INVALID_PARTNER_TYPES):
            continue

        if contains_any(name_lower, INVALID_PARTNER_TYPES):
            continue

        if contains_any(name_lower, PERSON_TITLES):
            continue

        if contains_any(name_lower, GENERIC_PHRASES):
            continue

        partner["partner_name"] = normalized_name
        partner["partner_type"] = normalized_type

        validated.append(partner)

    return validated


def deduplicate_partners(partners):
    grouped = {}

    for partner in partners:
        name = str(partner.get("partner_name", "")).strip()

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
            grouped[name]["roles"].add(str(role).strip())

        if page:
            grouped[name]["pages"].add(page)

        if evidence:
            grouped[name]["evidence_sentences"].add(str(evidence).strip())

    final_results = []

    for item in grouped.values():
        evidence_list = sorted(item["evidence_sentences"])

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