# Qulu - Movie Recommender System 🎬

**Qulu** is a premium, Netflix-style movie recommendation web application. It suggests movies based on content similarity using machine learning, presented in a sleek, dark-themed user interface with horizontal scrolling shelves.

## 🌟 Features

-   **Netflix-Inspired UI**: Dark theme, edge-to-edge layout, and premium typography.
-   **Smart Recommendations**: Uses **Content-Based Filtering** (Cosine Similarity) to recommend movies similar to your selection.
-   **Interactive "Shelf"**: A custom-built horizontal scroll view for browsing recommendations.
-   **Rich Metadata**: Fetches high-quality movie posters via the **TMDB API**.

## 🛠️ Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/) (Python) + Custom CSS/HTML
-   **Backend Logic**: Python, Pandas, Numpy
-   **Machine Learning**: Scikit-Learn (Cosine Similarity)
-   **Data Source**: TMDB 5000 Movie Dataset + TMDB API for posters

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/shrutikaingole15/Qulu-Movie-Recommender-System.git
cd Qulu-Movie-Recommender-System
```

### 2. Create a Virtual Environment (Optional but Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up Environment Variables
This app uses the TMDB API to fetch posters. You can set your API key in an environment variable `TMDB_API_KEY`.

**PowerShell:**
```powershell
$env:TMDB_API_KEY = "your_tmdb_api_key_here"
```

**Bash:**
```bash
export TMDB_API_KEY="your_tmdb_api_key_here"
```

*(Note: If no key is set, the app may fall back to a hardcoded key if present in `recommender.py` or fail to load images.)*

### 5. Run the App
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.


## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.
