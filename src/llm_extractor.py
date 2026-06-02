import json
import re


import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def test_openai_connection():
    response = client.responses.create(
        model="gpt-4o-mini",
        input="Reply only with: Connection successful"
    )

    return response.output_text


def extract_partners_with_gpt(text, page_number=None):
    prompt = f"""
    You are an IFAD COSOP partner extraction system.

    Your task is to extract only specifically named organizations that have an active role in the COSOP document.

    Extract organizations only if they are clearly acting as one of the following:

    - Funding partner
    - Co-financing partner
    - Development partner
    - Implementing partner
    - Government counterpart
    - Ministry or public institution
    - UN agency
    - NGO
    - Private sector organization
    - Financial institution
    - Climate fund
    - Producer association or formally named cooperative
    - Stakeholder organization with a clearly defined role

    Do NOT extract:

    - Countries
    - National governments as generic entities
    - Government of Cambodia
    - Authors
    - Publications
    - Reports
    - Footnotes
    - Citations
    - Bibliography entries
    - Academic references
    - Research institutions mentioned only as sources
    - IFAD itself, unless it is explicitly described as partnering with another organization
    - Generic groups, sectors, or stakeholder labels

    Examples of generic labels to ignore:

    - Farmers
    - Smallholders
    - Producer Organizations
    - Agriculture cooperatives
    - Farmer Water User Communities
    - Stakeholder Groups
    - Development Partners
    - Government Agencies
    - Private Sector Partners
    - Financial Institutions
    - Civil Society Organizations
    - Major agribusinesses
    - Agribusiness sector
    - Private sector
    - Commercial actors
    
    The extracted entity must be a legally identifiable organization or institution.

    Reject any entity that is:

    - A country
    - A government as a whole
    - A population group
    - A beneficiary group
    - A geographic region
    - A stakeholder category
    - A generic collective term

    Examples to reject:

    - Kingdom of Cambodia
    - Government of Cambodia
    - Smallholders
    - Farmers
    - Rural youth
    - Women
    - Producer organizations
    - Rome-based United Nations agencies
    - Development partners
    - Financial institutions
    - Private sector
    
    Only extract formally named organizations, institutions, ministries, banks, funds, companies, NGOs, or associations.

    The organization must have a clearly described active function in the COSOP, such as:

    - Funding
    - Co-financing
    - Technical assistance
    - Project implementation
    - Policy coordination
    - Capacity building
    - Knowledge support
    - Climate finance
    - Irrigation investment
    - Extension services
    - Stakeholder representation

    The role field must describe a concrete function.

    Avoid vague roles such as:

    - Partnership
    - Collaboration
    - Support
    - Involvement
    - Participation

    Use specific role descriptions whenever possible, such as:

    - Co-financing irrigation investments
    - Providing climate finance
    - Technical assistance for agricultural value chains
    - Policy coordination for rural development
    - Capacity building for producer organizations
    - Implementation of agricultural development activities
    - Financing private sector partnerships

    For each partner, provide:

    - partner_name
    - partner_type
    - role
    - evidence_sentence

    Return ONLY valid JSON.
    Do not include markdown.
    Do not include explanations.

    Format:

    [
      {{
        "partner_name": "",
        "partner_type": "",
        "role": "",
        "evidence_sentence": ""
      }}
    ]

    TEXT:
    {text}
    """


    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        temperature=0
    )

    raw_output = response.output_text

    cleaned_output = re.sub(r"```json|```", "", raw_output).strip()

    try:
        partners = json.loads(cleaned_output)
    except json.JSONDecodeError:
        partners = []

    if page_number is not None:
        for partner in partners:
            partner["page_number"] = page_number

    return partners