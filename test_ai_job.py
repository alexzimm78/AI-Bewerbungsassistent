from utils.ai_generator import analyze_job

job_text = """
IT Support Specialist

Ihre Aufgaben:
- Unterstützung von Anwendern
- Microsoft 365
- Ticketsystem
- Service Desk
- Fehleranalyse
"""

result = analyze_job(job_text)

print(result)