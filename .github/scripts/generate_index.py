# Adaptation pour tutoriels iPhone 
import os
import re
import glob
from bs4 import BeautifulSoup
from datetime import datetime

EXCLUDE_FILES = ['index.html', 'README.html', '404.html']

# Catégories définies pour l'organisation
CATEGORIES = {
    'reglages': {'name': 'Réglages essentiels', 'icon': '⚙️'},
    'communication': {'name': 'Communication', 'icon': '📱'},
    'meta': {'name': 'Applications Meta', 'icon': '👥'},
    'photos': {'name': 'Photos et souvenirs', 'icon': '📸'},
    'organisation': {'name': 'Organisation', 'icon': '📅'},
    'google': {'name': 'Google Drive', 'icon': '📁'}
}

# CSS adapté 
CSS = """
:root {
    --primary-color: #007AFF;  /* Bleu iOS */
    --secondary-color: #5AC8FA;
    --background-color: #F2F2F7;
    --text-color: #000;
    --card-bg: #fff;
    --border-radius: 16px;
    --text-size-base: 20px;  /* Plus grand */
    --heading-size: 28px;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif;
    font-size: var(--text-size-base);
    line-height: 1.6;
    color: var(--text-color);
    background-color: var(--background-color);
    padding: 20px;
}

.container {
    max-width: 800px;
    margin: 0 auto;
}

header {
    text-align: center;
    margin-bottom: 30px;
    padding: 25px;
    background-color: var(--primary-color);
    color: white;
    border-radius: var(--border-radius);
}

h1 {
    font-size: var(--heading-size);
    font-weight: 600;
}

.category-section {
    margin-bottom: 40px;
}

.category-header {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 20px;
    padding: 15px;
    background-color: var(--secondary-color);
    color: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.tutoriel-card {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
}

.tutoriel-card:active {
    transform: scale(0.98);
}

.tutoriel-title {
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--primary-color);
}

.tutoriel-description {
    font-size: 18px;
    color: #666;
    margin-bottom: 15px;
}

.tutoriel-meta {
    display: flex;
    gap: 20px;
    font-size: 16px;
    color: #999;
    margin-bottom: 15px;
}

.tutoriel-link {
    display: inline-block;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    padding: 12px 24px;
    border-radius: 22px;
    font-weight: 600;
    font-size: 18px;
}

@media (max-width: 428px) {  /* iPhone 14 Pro Max width */
    .container {
        padding: 10px;
    }
    
    h1 {
        font-size: 24px;
    }
    
    .category-header {
        font-size: 20px;
    }
}
"""

# Fonction pour extraire les métadonnées
def extract_metadata(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extraire le titre
        title = soup.find('h1').text.strip() if soup.find('h1') else filename.replace('.html', '')
        
        # Extraire la catégorie (via meta tag ou classe CSS)
        category = 'autre'
        meta_category = soup.find('meta', {'name': 'category'})
        if meta_category:
            category = meta_category.get('content', 'autre')
        
        # Extraire la description
        description = "Tutoriel pour iPhone"
        objectif = soup.find(class_='objectif')
        if objectif:
            description = objectif.text.strip()
        
        # Extraire la difficulté et durée (optionnel)
        difficulty = soup.find('meta', {'name': 'difficulty'})
        difficulty = difficulty.get('content') if difficulty else 'Facile'
        
        duration = soup.find('meta', {'name': 'duration'})
        duration = duration.get('content') if duration else '5 minutes'
        
        return {
            'filename': filename,
            'title': title,
            'category': category,
            'description': description,
            'difficulty': difficulty,
            'duration': duration
        }

# Générer l'index
html_files = glob.glob('*.html')
tutoriels = []

for filename in html_files:
    if filename in EXCLUDE_FILES:
        continue
    try:
        metadata = extract_metadata(filename)
        tutoriels.append(metadata)
    except Exception as e:
        print(f"Erreur avec {filename}: {str(e)}")

# Organiser par catégories
tutoriels_by_category = {}
for cat_key in CATEGORIES:
    tutoriels_by_category[cat_key] = [t for t in tutoriels if t['category'] == cat_key]

# Générer le HTML
sections_html = ""
for cat_key, cat_info in CATEGORIES.items():
    if tutoriels_by_category[cat_key]:
        sections_html += f"""
        <div class="category-section">
            <h2 class="category-header">
                <span>{cat_info['icon']}</span>
                {cat_info['name']}
            </h2>
            <div class="tutoriels-list">
        """
        
        for tuto in tutoriels_by_category[cat_key]:
            sections_html += f"""
            <div class="tutoriel-card">
                <h3 class="tutoriel-title">{tuto['title']}</h3>
                <p class="tutoriel-description">{tuto['description']}</p>
                <div class="tutoriel-meta">
                    <span>⏱️ {tuto['duration']}</span>
                    <span>📊 {tuto['difficulty']}</span>
                </div>
                <a href="{tuto['filename']}" class="tutoriel-link">Voir le tutoriel</a>
            </div>
            """
        
        sections_html += """
            </div>
        </div>
        """

# Template HTML principal
index_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide iPhone pour Maman</title>
    <style>
{CSS}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📱 Guide iPhone</h1>
            <p>Tutoriels simples et détaillés</p>
        </header>
        {sections_html}
        <div style="text-align: center; margin: 40px 0; color: #666;">
            <p>{len(tutoriels)} tutoriels disponibles</p>
            <p><small>Dernière mise à jour: {datetime.now().strftime("%d/%m/%Y")}</small></p>
        </div>
    </div>
</body>
</html>"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(index_html)
