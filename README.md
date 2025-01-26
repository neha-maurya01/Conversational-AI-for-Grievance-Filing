# Conversational-AI-for-Grievance-Filing

This project is a grievance filing system that utilizes machine learning models for categorizing and processing grievances, along with language detection and translation support. It allows users to file grievances in either English or Hindi, automatically categorizing them and suggesting the relevant department for action.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies](#technologies)
- [Installation](#installation)
- [Usage](#usage)
- [Code Structure](#code-structure)
- [Contributing](#contributing)

## Overview
The grievance filing system enables users to submit grievances in English or Hindi. The system categorizes the grievance, calculates a similarity score, and assigns it to an appropriate department. If the grievance is not in the supported languages, it returns an "Uncategorized" status.

## Features
- **Grievance Categorization**: Classifies grievances based on similarity to predefined categories.
- **Language Detection**: Detects the language of the input grievance using the `langid` library.
- **Translation Support**: If the input grievance is in Hindi, it is translated to English for categorization.
- **Streamlit Interface**: Provides a simple web interface to file grievances, view results, and check conversation history.

## Technologies
- **Python**: The core language used for implementing the system.
- **Sentence Transformers**: Used to compute similarity scores for grievance categorization.
- **Google Translate**: For translating grievances in Hindi to English.
- **Streamlit**: For the user interface (UI).
- **langid**: For language detection.
- **JSON**: For storing predefined mappings for departments and categories.

## Installation

### Prerequisites
Ensure you have Python 3.x installed. You will also need the following libraries:
- `streamlit`
- `sentence-transformers`
- `googletrans`
- `langid`
- `numpy`

To install the necessary libraries, run the following command:

```bash
pip install streamlit sentence-transformers googletrans langid numpy
```

### File Structure

```
.
├── engine.py              # Contains the logic for grievance categorization and language translation
├── language_detect.py     # Contains the logic for language detection
├── main.py                # Streamlit app to interact with the user
├── json_files
│   ├── department_map.json  # Department mapping file
│   └── categories_map.json  # Category mapping file
└── requirements.txt       # List of dependencies
```

## Usage

1. **Run the Streamlit Application**:
   Navigate to the project directory and run the following command to start the Streamlit app:

   ```bash
   streamlit run main.py
   ```

2. **File a Grievance**:
   - Enter a grievance in the text box.
   - Select the language of the grievance (English or Hindi).
   - Click the "File Grievance" button to submit.
   - The system will categorize the grievance and show the predicted category, similarity score, and the relevant department.
   
3. **Conversation History**:
   The system maintains a session-based history of previously filed grievances, displaying the grievance, assigned category, and similarity score.

## Code Structure

- **`engine.py`**: Contains the main logic for grievance categorization, language detection, and translation.
  - `categorize_grievance()`: Categorizes a grievance based on similarity to predefined categories.
  - `predict_category()`: Detects the language of the grievance, translates if necessary, and predicts the department and category.

- **`language_detect.py`**: Handles language detection using the `langid` library.
  - `detect_language()`: Detects the language of a given text and returns the language code along with the confidence score.

- **`main.py`**: Implements the Streamlit app UI for grievance filing and displays results and conversation history.
  - `add_to_conversation()`: Adds the grievance and its associated information to the conversation history.

## Example Usage

- **Filing a grievance in Hindi**: 
    - Grievance: "सड़क पर गड्ढा है, कृपया इसे ठीक करें।"
    - The system will translate the grievance to English and categorize it accordingly.

- **Filing a grievance in English**: 
    - Grievance: "There's a broken streetlight on Elm Street."
    - The system will directly categorize it without translation.

## Contributing

Feel free to fork the repository and submit pull requests with improvements, bug fixes, or new features. Contributions are welcome!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
