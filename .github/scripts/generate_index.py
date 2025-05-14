# Script de génération avec navigation complète
import os
import re
import glob
from bs4 import BeautifulSoup
from datetime import datetime

EXCLUDE_FILES = ['index.html', 'README.html', '404.html']

# Catégories définies pour l'organisation
CATEGORIES = {
    'reglages': {'name': 'Réglages essentiels', 'icon': '⚙️', 'description': 'Volume, luminosité, Wi-Fi et paramètres de base'},
    'communication': {'name': 'Communication', 'icon': '📱', 'description': 'Appels, messages et emails'},
    'meta': {'name': 'Applications Meta', 'icon': '👥', 'description': 'Facebook, WhatsApp et Instagram'},
    'photos': {'name': 'Photos et souvenirs', 'icon': '📸', 'description': 'Prendre et partager des photos'},
    'organisation': {'name': 'Organisation', 'icon': '📅', 'description': 'Calendrier, rappels et notes'},
    'google': {'name': 'Google Drive', 'icon': '📁', 'description': 'Accès et synchronisation des fichiers'}
}

# CSS pour toutes les pages
CSS = """
:root {
    --primary-color: #007AFF;
    --secondary-color: #5AC8FA;
    --background-color: #F2F2F7;
    --text-color: #000;
    --card-bg: #fff;
    --border-radius: 16px;
    --text-size-base: 20px;
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

.breadcrumb {
    margin-bottom: 20px;
    font-size: 16px;
    color: #666;
}

.breadcrumb a {
    color: var(--primary-color);
    text-decoration: none;
}

.category-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 40px;
}

.category-card {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 30px;
    text-align: center;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
    text-decoration: none;
    color: var(--text-color);
}

.category-card:active {
    transform: scale(0.98);
}

.category-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.category-name {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
    color: var(--primary-color);
}

.category-description {
    font-size: 18px;
    color: #666;
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

.nav-link {
    display: inline-block;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    padding: 12px 24px;
    border-radius: 22px;
    font-weight: 600;
    font-size: 18px;
    margin: 10px;
}

.nav-bottom {
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid #E0E0E0;
    text-align: center;
}

@media (max-width: 428px) {
    .container {
        padding: 10px;
    }
    
    h1 {
        font-size: 24px;
    }
    
    .category-grid {
        grid-template-columns: 1fr;
    }
}
"""

def extract_metadata(filepath):
    """Extrait les métadonnées d'un fichier HTML de tutoriel"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        
        title = soup.find('h1').text.strip() if soup.find('h1') else os.path.basename(filepath).replace('.html', '')
        
        category = 'autre'
        meta_category = soup.find('meta', {'name': 'category'})
        if meta_category:
            category = meta_category.get('content', 'autre')
        
        description = "Tutoriel pour iPhone"
        objectif = soup.find(class_='objectif')
        if objectif:
            description = objectif.text.strip()
        
        difficulty = soup.find('meta', {'name': 'difficulty'})
        difficulty = difficulty.get('content') if difficulty else 'Facile'
        
        duration = soup.find('meta', {'name': 'duration'})
        duration = duration.get('content') if duration else '5 minutes'
        
        return {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'title': title,
            'category': category,
            'description': description,
            'difficulty': difficulty,
            'duration': duration
        }

def create_homepage():
    """Crée la page d'accueil avec les catégories"""
    categories_html = ""
    for cat_key, cat_info in CATEGORIES.items():
        categories_html += f"""
        <a href="categories/{cat_key}/index.html" class="category-card">
            <div class="category-icon">{cat_info['icon']}</div>
            <div class="category-name">{cat_info['name']}</div>
            <div class="category-description">{cat_info['description']}</div>
        </a>
        """
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide iPhone - Tutoriels simples</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📱 Guide iPhone</h1>
            <p>Tutoriels simples et détaillés</p>
        </header>
        
        <h2 style="text-align: center; margin-bottom: 30px;">Choisissez une catégorie</h2>
        
        <div class="category-grid">
            {categories_html}
        </div>
        
        <div style="text-align: center; margin: 40px 0; color: #666;">
            <p><small>Dernière mise à jour: {datetime.now().strftime("%d/%m/%Y")}</small></p>
        </div>
    </div>
</body>
</html>"""
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)

def create_category_page(category_key, tutoriels):
    """Crée une page pour chaque catégorie"""
    cat_info = CATEGORIES[category_key]
    
    tutoriels_html = ""
    for tuto in tutoriels:
        tutoriels_html += f"""
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
    
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_info['name']} - Guide iPhone</title>
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <div class="breadcrumb">
            <a href="../../index.html">Accueil</a> > {cat_info['name']}
        </div>
        
        <header>
            <h1>{cat_info['icon']} {cat_info['name']}</h1>
            <p>{cat_info['description']}</p>
        </header>
        
        <div class="tutoriels-list">
            {tutoriels_html}
        </div>
        
        <div class="nav-bottom">
            <a href="../../index.html" class="nav-link">← Retour à l'accueil</a>
        </div>
    </div>
</body>
</html>"""
    
    # Créer le répertoire si nécessaire
    category_dir = f"categories/{category_key}"
    os.makedirs(category_dir, exist_ok=True)
    
    with open(f"{category_dir}/index.html", 'w', encoding='utf-8') as f:
        f.write(html)

def update_tutorial_navigation(filepath, category, next_tutorial=None, prev_tutorial=None):
    """Met à jour la navigation dans un tutoriel existant"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Supprimer la navigation existante si présente
    nav_bottom = soup.find(class_='nav-bottom')
    if nav_bottom:
        nav_bottom.decompose()
    
    # Créer la nouvelle navigation
    nav_html = f"""
    <div class="nav-bottom">
        <a href="index.html" class="nav-link">← {CATEGORIES[category]['name']}</a>
        <a href="../../index.html" class="nav-link">🏠 Accueil</a>
    </div>
    """
    
    # Ajouter la navigation à la fin du tutoriel
    container = soup.find(class_='container')
    if container:
        nav_soup = BeautifulSoup(nav_html, 'html.parser')
        container.append(nav_soup)
    
    # Sauvegarder le fichier modifié
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

def main():
    """Fonction principale"""
    # Créer la page d'accueil
    create_homepage()
    
    # Parcourir toutes les catégories
    for cat_key in CATEGORIES:
        category_dir = f"categories/{cat_key}"
        if os.path.exists(category_dir):
            # Trouver tous les tutoriels de cette catégorie
            html_files = glob.glob(f"{category_dir}/*.html")
            tutoriels = []
            
            for filepath in html_files:
                if os.path.basename(filepath) not in EXCLUDE_FILES + ['index.html']:
                    try:
                        metadata = extract_metadata(filepath)
                        tutoriels.append(metadata)
                        
                        # Mettre à jour la navigation du tutoriel
                        update_tutorial_navigation(filepath, cat_key)
                    except Exception as e:
                        print(f"Erreur avec {filepath}: {str(e)}")
            
            # Créer la page de catégorie
            if tutoriels:
                create_category_page(cat_key, tutoriels)
    
    print("Génération terminée!")

if __name__ == "__main__":
    main()
