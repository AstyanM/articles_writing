import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ContentAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            # Client might find it in env automatically or fail later
            pass

        self.client = OpenAI(api_key=self.api_key)

    def analyze_competitors(self, contents: list[str], angle_focus: str = "Un nouvel angle original") -> str:
        """
        Analyzes competitor content to find commonalities and blind spots.
        """
        if not contents:
            return "No content to analyze."

        # Prepare the prompt
        system_prompt = "Tu es un expert en stratégie éditoriale. Ton rôle est d'analyser des articles concurrents pour proposer un plan d'article unique et pertinent pour des étudiants."

        # Simple truncation to avoid hitting token limits if many articles are passed.
        # Ideally, we would tokenize and truncate properly, or summarize each article first.
        # For now, we utilize a hard character limit as a safeguard.
        combined_content = ""
        for i, content in enumerate(contents):
            # Limit each article contribution
            combined_content += f"\n--- ARTICLE {i+1} ---\n{content[:6000]}"

        user_prompt = f"""
Analyse ces {len(contents)} articles. 
Identifie les informations manquantes ou les questions que se poserait un étudiant et auxquelles ils ne répondent pas. 
Propose un plan d'article qui couvre l'essentiel mais centre l'argumentaire sur : {angle_focus}.

--- CONTENU DES CONCURRENTS ---
{combined_content}
"""

        try:
            response = self.client.chat.completions.create(
                # Defaulting to gpt-4o as requested by 'OpenAI' choice usually implies best model
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error during analysis: {e}"
