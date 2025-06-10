def generate_prompt(template_type: str, content: str) -> str:
    """
    Generate vulnerability assessment prompt for Ollama based on the content type.

    Parameters:
    - template_type (str): one of ['code', 'logs', 'json', 'shell', 'config', 'reasoning', 'threat', 'owasp']
    - content (str): the actual code, logs, or JSON input

    Returns:
    - str: Full prompt to be sent to the LLM
    """

    templates = {
        "code": (
            "You're a security expert. Analyze the following code for security vulnerabilities, especially from the OWASP Top 10 list. "
            "Return a list of identified issues, how they can be exploited, and how to fix them.\n\n```python\n{data}\n```"
        ),
        "logs": (
            "Analyze the following application logs for signs of security issues such as SQL Injection, XSS, CSRF, command injection, or SSRF. "
            "Highlight suspicious patterns and suggest mitigations.\n\n```log\n{data}\n```"
        ),
        "json": (
            "Given this vulnerability report in JSON format, assess the risk severity and suggest remediation steps for each vulnerability. "
            "Use OWASP, CVSS, and CWE references where applicable.\n\n```json\n{data}\n```"
        ),
        "shell": (
            "Check the following shell commands/configs for any signs of command injection, privilege escalation, or insecure configurations.\n\n```sh\n{data}\n```"
        ),
        "config": (
            "Review the following application or server configuration for security misconfigurations (e.g., weak headers, open permissions, missing CSP, TLS issues). "
            "Provide suggestions to improve hardening.\n\n```conf\n{data}\n```"
        ),
        "reasoning": (
            "Given this vulnerability data, perform reasoning to identify potential chaining of vulnerabilities (e.g., IDOR + XSS). "
            "Provide steps an attacker might take, and how to mitigate such an attack path.\n\n```json\n{data}\n```"
        ),
        "threat": (
            "Given the following system architecture and code snippets, identify threat vectors. Use STRIDE (Spoofing, Tampering, Repudiation, "
            "Information Disclosure, Denial of Service, Elevation of Privilege) model and give potential mitigation strategies.\n\n```yaml\n{data}\n```"
        ),
        "owasp": (
            "Review the following code and identify vulnerabilities based on the OWASP Top 10. For each, list: "
            "1. OWASP category (e.g., A1: Broken Access Control), 2. Description of the vulnerability, 3. Exploitation method, 4. Fix recommendation.\n\n```js\n{data}\n```"
        ),
    }

    if template_type not in templates:
        raise ValueError("Invalid template type. Must be one of: " + ", ".join(templates.keys()))

    return templates[template_type].format(data=content.strip())
