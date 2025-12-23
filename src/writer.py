import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class ContentWriter:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            pass
        self.client = OpenAI(api_key=self.api_key)

    def draft_article(self, plan: str, synthesis: str) -> str:
        """
        Drafts an article based on the provided plan and synthesis.
        """
        system_prompt = """
Tu es un Conseiller d'orientation pédagogique expert.
Ton style est humain, direct, orienté vers l'action.
Tu évites les fioritures ("il est crucial de", "dans cet article nous allons voir").
Tu t'adresses directement au lecteur ("votre dossier", "préparez-vous").
Ne reformule pas les contenus des concurrents, mais utilise les faits pour rédiger du neuf.
Suis scrupuleusement le plan fourni.
"""
        user_prompt = f"""
Rédige un article complet basé sur les éléments suivants :

--- SYNTHÈSE & PLAN ---
{synthesis}

--- DERNIÈRE INSTRUCTION ---
Utilise le balisage Markdown (H1 pour le titre, H2, H3).
Sois exhaustif mais concis.
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error drafting article: {e}"

    def optimize_seo(self, article_content: str, keywords: list = [], external_links: list = []) -> str:
        """
        Optimizes the article with Meta tags, FAQ, and strategic links.
        """
        keywords_str = ", ".join(
            keywords) if keywords else "parcoursup, orientation, concours"
        links_str = "\n".join(
            f"- {link}" for link in external_links) if external_links else "Aucun lien spécifique fourni, utilise des sources d'autorité générales."

        system_prompt = """
Tu es un expert SEO. Ton rôle est d'optimiser un article pour le référencement naturel.
Tu dois ajouter :
1. Une section META au tout début (Title < 60 chars, Meta Description < 160 chars).
2. Des suggestions de maillage interne et externe à des endroits pertinents.
3. Une section FAQ type "People Also Ask" à la fin (3 questions/réponses).
"""
        user_prompt = f"""
Voici l'article rédigé :

{article_content}

--- RESSOURCES ---
Voici une liste de liens identifiés lors de la recherche. Choisis-en UN pertinent (de préférence une source officielle ou d'autorité) pour l'intégrer comme [LIEN EXTERNE] dans le texte.
{links_str}

--- TÂCHE ---
Renvoie l'article complet avec :
1. En haut : un bloc de métadonnées (Title, Description).
2. Dans le corps : 
   - Insère 2-3 marqueurs [LIEN INTERNE: sujet connexe].
   - Intègre intelligemment 1 lien externe choisi dans la liste ci-dessus (ou une source officielle connue si la liste n'est pas pertinente). Le format doit être Markdown : [Ancre du lien](URL).
3. En bas : Une section ## FAQ avec 3 questions pertinentes pour la position zéro (basées sur les mots-clés : {keywords_str}).
"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error optimizing SEO: {e}"
