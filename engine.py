import json
from sentence_transformers import SentenceTransformer, util
import numpy as np
from googletrans import Translator
from language_detect import detect_language

threshold = 0.3

with open('./json_files/department_map.json', 'r') as file:
    department_map = json.load(file)

with open('./json_files/categories_map.json', 'r') as file:
    categories_map = json.load(file)
        

categories_with_context = list(categories_map.values())

model = SentenceTransformer('paraphrase-MiniLM-L6-v2') #('all-MiniLM-L6-v2') 

category_embeddings = model.encode(categories_with_context, convert_to_tensor=True)

def translate_text(text, target_language="en"):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    return translation.text

# Grievance categorization function
def categorize_grievance(grievance):
    grievance_embedding = model.encode(grievance, convert_to_tensor=True)
    similarities = util.pytorch_cos_sim(grievance_embedding, category_embeddings)[0]
    highest_similarity_idx = np.argmax(similarities.cpu().numpy())
    highest_similarity_score = similarities[highest_similarity_idx]
    
    if highest_similarity_score >= threshold:
        cat_id = 'CT'+str(highest_similarity_idx+1)
        return cat_id, highest_similarity_score
    
    else:
        print( categories_with_context[highest_similarity_idx])
        return "Uncategorized", highest_similarity_score


def predict_category(grievance_input):
    detected_lang_1, _ = detect_language(grievance_input)
    print('detected_lang ',grievance_input, detected_lang_1 )
    if detected_lang_1 == "en" or detected_lang_1 == "hi":
        translated_grievance = grievance_input
        if detected_lang_1 == 'hi':
            translated_grievance = translate_text(grievance_input, target_language="en")
            print("Presented in ", detected_lang_1, 'and translated text: ',translated_grievance)
    else:
        return 'Unrecognized language', None, 0.0

    cat_id, score = categorize_grievance(translated_grievance)
    
    if cat_id == "Uncategorized":
        return "Uncategorized", 'None', score
    
    suitable_department = ''
    for dept in department_map.keys():
        if cat_id in department_map[dept]:
            suitable_department = dept
            break
    
    return suitable_department, categories_map[cat_id], score