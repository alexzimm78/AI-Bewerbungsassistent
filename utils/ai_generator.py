def generate_bewerbung(job_title, skills, experience):
    try:
        prompt = f"""
        Schreibe ein professionelles deutsches Bewerbungsschreiben.

        Job: {job_title}
        Fähigkeiten: {skills}
        Erfahrung: {experience}

        Die Person macht aktuell eine Weiterbildung im Bereich AI Engineering.
        Der Stil soll freundlich, modern und professionell sein.
        """

        response = client.responses.create(
            model="gpt-4o-mini",
            input=prompt
        )

        return response.output_text

    except Exception:
        return f"""
Hallo,

hiermit möchte ich mich auf die Stelle als {job_title} bewerben.

Ich interessiere mich sehr für IT und absolviere aktuell eine Weiterbildung im Bereich AI Engineering.

Durch meine bisherigen Erfahrungen in den Bereichen {experience}
bringe ich Zuverlässigkeit, strukturiertes Arbeiten und Verantwortungsbewusstsein mit.

Zusätzlich verfüge ich über folgende Kenntnisse und Fähigkeiten:
{skills}

Mit freundlichen Grüßen
Alexander Zimmermann
"""
###

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def analyze_job(job_text):
    prompt = f"""
Du bist ein Bewerbungsassistent.

Analysiere diese Stellenanzeige:

{job_text}

Gib die Antwort in diesem Format:

Kategorie:
IT Support / Service Desk / Applikationsbetreuer / Andere

Gefundene Skills:
- Skill 1
- Skill 2
- Skill 3

Passung:
0-100 %

Empfohlenes Anschreiben:
support / servicedesk / application

Kurze Begründung:
maximal 3 Sätze
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    return response.output_text

###
def generate_ai_cover_letter(job_text, skills, experience):
    prompt = f"""
Du bist ein professioneller Bewerbungscoach für den deutschen Arbeitsmarkt.

Erstelle ein individuelles Bewerbungsschreiben auf Deutsch.
Wichtig:
Verwende am Ende:

Mit freundlichen Grüßen

Alexander Zimmermann

Verwende niemals "Vorname Nachname".

Profil des Bewerbers:
Skills: {skills}
Erfahrung: {experience}
Weiterbildung: AI Engineer an der AIT Technology School, 03/2026 bis 09/2026
Aktuelles Ziel: Einstieg in IT Support, Service Desk oder Applikationsbetreuung

Stellenanzeige:
{job_text}

Anforderungen:
- professionell
- glaubwürdig für einen IT-Quereinsteiger
- nicht übertreiben
- Logistik-Erfahrung sinnvoll mit IT verbinden
- maximal 250 Wörter
- mit Grußformel
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    result = response.output_text

    result = result.replace("Vorname Nachname", "Alexander Zimmermann")
    result = result.replace("■", "-")
    result = result.replace("–", "-")
    result = result.replace("—", "-")

    return result

