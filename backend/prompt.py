"""Prompt generator and response format for AI-driven security analysis."""


def prompt_string() -> str:
    """
    Returns the AI system prompt for assessing vulnerabilities and misconfigurations.

    This prompt instructs the AI to:
    - Analyze structured/unstructured data for security flaws.
    - Use OWASP Top 10 categories.
    - Provide detailed summary, table, and explanations in structured JSON format.
    """
    return """
You are a senior security analyst. Carefully review the following input (which may be a dictionary, JSON object, or unstructured text) for any potential security vulnerabilities, misconfigurations, or exposures.

For complex or nested data, analyze all levels and relationships between fields. Identify vulnerabilities that may arise from combinations of fields, inherited permissions, or contextual misconfigurations. If the data includes code, configuration, or embedded secrets, audit those as well.

When identifying vulnerabilities, ensure you consider all relevant OWASP Top 10 categories (such as injection, broken authentication, sensitive data exposure, XML external entities, broken access control, security misconfiguration, cross-site scripting, insecure deserialization, using components with known vulnerabilities, insufficient logging & monitoring) and reference the specific OWASP category in your findings where applicable.

If vulnerabilities are found, provide:
- A concise summary of the most critical findings at the top in `summary`.
- Provide technical explanation, as senior developer.
- A table listing each vulnerability with these fields: field_key, vulnerability_type, severity, justification, recommended_fix, reference_standard, related_context.
- The table should clearly associate each finding with the relevant data and context, including cross-field or cross-object issues.
- Add a score (0–10) based on severity.
- For complex findings, include affected_software, weakness, severity, mitigations, and related_attack_patterns.
- Include references to public advisories or sources.
- If no issues are found, explain why the data is secure.

Return the results in a well-structured JSON format containing cve_id, title, description, severity, cvss, summary, vulnerabilities, score, complex_findings, and references.
"""


def response_format_json() -> dict:
    """
    Returns the expected response format for AI vulnerability analysis.

    This ensures consistent structure for parsing and UI rendering.
    """
    return {
        "cve_id": "",
        "title": "",
        "description": "",
        "summary": "",
        "severity": "",
        "cvss_score": "",
        "technical_explanation": "",
        "vulnerabilities": [
            {
                "field_key": "",
                "vulnerability_type": "",
                "justification": "",
                "severity": "",
                "recommended_fix": "",
                "reference_standard": "",
                "related_context": ""
            }
        ],
        "complex_findings": {
            "affected_software": "",
            "weakness": "",
            "potential_mitigations": [
                ""
            ],
            "related_attack_patterns": [
                "",
            ]
        },
        "references": [
            ""
        ]
    }


def ollama_prompt() -> str:
    return """
            You are a senior security analyst. Carefully review the following input (which may be a dictionary, JSON object, or unstructured text) for any potential security vulnerabilities, misconfigurations, or exposures.
            Return the results always in a consistent well-structured JSON format containing cve_id, title, description, severity, cvss_score,technical_explanation, summary, vulnerabilities, score, complex_findings, and references"""