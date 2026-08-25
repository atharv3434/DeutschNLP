import spacy
from textblob_de import TextBlobDE
from .compound_splitter import split_german_compound

class GermanNLPEngine:
    def __init__(self):
        # Load standard German model, fallback to blank German model if not yet downloaded
        try:
            self.nlp = spacy.load("de_core_news_sm")
        except OSError:
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "de_core_news_sm"])
            self.nlp = spacy.load("de_core_news_sm")

    def analyze(self, text: str) -> dict:
        if not text.strip():
            return {}

        doc = self.nlp(text)
        
        # 1. Morphological & Lexical Analysis
        tokens_data = []
        compounds = []

        for token in doc:
            morph_dict = token.morph.to_dict()
            
            # Check for German compound noun splitting
            compound_parts = []
            if token.pos_ in ["NOUN", "PROPN"] and len(token.text) > 7:
                split_res = split_german_compound(token.text)
                if len(split_res) > 1:
                    compound_parts = split_res
                    compounds.append({
                        "original": token.text,
                        "components": split_res
                    })

            tokens_data.append({
                "text": token.text,
                "lemma": token.lemma_,
                "pos": token.pos_,
                "tag": token.tag_,
                "dep": token.dep_,
                "head": token.head.text,
                "gender": morph_dict.get("Gender", "N/A"),
                "case": morph_dict.get("Case", "N/A"),
                "number": morph_dict.get("Number", "N/A"),
                "is_stop": token.is_stop,
                "compound_parts": compound_parts
            })

        # 2. Named Entity Recognition (NER)
        entities = [
            {
                "text": ent.text,
                "label": ent.label_,
                "start": ent.start_char,
                "end": ent.end_char
            }
            for ent in doc.ents
        ]

        # 3. Sentiment Analysis (using TextBlob-DE)
        blob = TextBlobDE(text)
        sentiment_score = round(blob.sentiment.polarity, 3)
        subjectivity_score = round(blob.sentiment.subjectivity, 3)

        if sentiment_score > 0.1:
            sentiment_label = "Positiv"
        elif sentiment_score < -0.1:
            sentiment_label = "Negativ"
        else:
            sentiment_label = "Neutral"

        # 4. Summary Statistics
        num_tokens = len(tokens_data)
        num_sentences = len(list(doc.sents))
        num_nouns = sum(1 for t in tokens_data if t["pos"] in ["NOUN", "PROPN"])
        num_verbs = sum(1 for t in tokens_data if t["pos"] == "VERB")

        return {
            "text": text,
            "statistics": {
                "token_count": num_tokens,
                "sentence_count": num_sentences,
                "noun_count": num_nouns,
                "verb_count": num_verbs
            },
            "sentiment": {
                "label": sentiment_label,
                "polarity": sentiment_score,
                "subjectivity": subjectivity_score
            },
            "tokens": tokens_data,
            "entities": entities,
            "compounds": compounds
        }