from langid.langid import LanguageIdentifier, model
identifier = LanguageIdentifier.from_modelstring(model, norm_probs=True)

def detect_language(text):
    text = text.strip().replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')  
    lang, confidence  = identifier.classify(text)
    return lang, confidence

# # Example usage
# text = "सड़क पर गड्ढा है, कृपया इसे ठीक करें।"  # French text
# language, confidence = detect_language(text)

# print(f"Detected Language: {language} (Confidence: {confidence:.2f})")
# print(text)