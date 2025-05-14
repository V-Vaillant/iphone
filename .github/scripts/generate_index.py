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

# CSS adapté pour 
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

.categories-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 30px;
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

.category-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.category-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.category-name {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 10px;
}

.category-count {
    font-size: 16px;
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

.nav-top {
    margin-bottom: 20px;
    display: flex;
    gap: 15px;
    align-items: center;
}

.nav-bottom {
    display: flex;
    justify-content: center;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 40px;
    padding-top: 20px;
    border-top: 2px solid #E0E0E0;
}

.nav-link {
    display: inline-block;
    padding: 12px 24px;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 22px;
    font-weight: 600;
    margin: 10px;
}

@media (max-width: 428px) {  /* iPhone 14 Pro Max width */
    .container {
        padding: 10px;
    }
    
    h1 {
        font-size: 24px;
    }
    
    .categories-grid {
        grid-template-columns: 1fr;
    }
    
    .nav-top, .nav-bottom {
        flex-direction: column;
    }
    
    .nav-link {
        width: 100%;
        text-align: center;
    }
}
"""

# Fonction pour extraire les métadonnées
def extract_metadata(filepath):
    # Extraire la catégorie du chemin du fichier
    path_parts = filepath.replace('\\', '/').split('/')
    if len(path_parts) >= 3 and path_parts[0] == 'categories':
        category = path_parts[1]
    else:
        category = 'autre'
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extraire le titre
            title = soup.find('h1').text.strip() if soup.find('h1') else os.path.basename(filepath).replace('.html', '')
            
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
                'filepath': filepath,
                'filename': os.path.basename(filepath),
                'title': title,
                'category': category,
                'description': description,
                'difficulty': difficulty,
                'duration': duration
            }
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
        # Retourner des valeurs par défaut si le fichier est vide ou corrompu
        return {
            'filepath': filepath,
            'filename': os.path.basename(filepath),
            'title': os.path.basename(filepath).replace('.html', '').replace('-', ' ').title(),
            'category': category,
            'description': 'Tutoriel pour iPhone',
            'difficulty': 'Facile',
            'duration': '5 minutes'
        }

# Générer les pages de catégories
def generate_category_pages(tutoriels_by_category):
    print("\n--- Génération des pages de catégories ---")
    
    for cat_key, cat_info in CATEGORIES.items():
        category_dir = f'categories/{cat_key}'
        category_index_path = f'{category_dir}/index.html'
        
        print(f"\nCatégorie: {cat_key} ({cat_info['name']})")
        print(f"Répertoire: {category_dir}")
        
        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(category_dir):
            print(f"  → Création du répertoire {category_dir}")
            os.makedirs(category_dir, exist_ok=True)
        
        # Récupérer les tutoriels de cette catégorie
        tutoriels = tutoriels_by_category.get(cat_key, [])
        print(f"  → {len(tutoriels)} tutoriels trouvés")
        
        # HTML de la page de catégorie
        category_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_info['name']} - Guide iPhone</title>
    <link rel="stylesheet" href="../../styles/tutoriel.css">
    <style>{CSS}</style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{cat_info['icon']} {cat_info['name']}</h1>
        </header>
        
        <nav class="nav-top">
            <a href="../../index.html" class="nav-link">← Retour à l'accueil</a>
        </nav>
        
        <div class="tutoriels-list">
"""
        
        if not tutoriels:
            category_html += """
            <p style="text-align: center; color: #666; padding: 40px;">
                Aucun tutoriel disponible dans cette catégorie pour le moment.
            </p>
            """
        else:
            for tuto in tutoriels:
                category_html += f"""
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
        
        category_html += """
        </div>
        
        <nav class="nav-bottom">
            <a href="../../index.html" class="nav-link">🏠 Retour à l'accueil</a>
        </nav>
    </div>
</body>
</html>"""
        
        # Écrire le fichier
        try:
            with open(category_index_path, 'w', encoding='utf-8') as f:
                f.write(category_html)
            print(f"  ✓ Créé: {category_index_path}")
        except Exception as e:
            print(f"  ✗ Erreur lors de la création de {category_index_path}: {e}")

# Script principal
print("Génération de l'index et des pages de catégories...")
print(f"Répertoire de travail: {os.getcwd()}")

# Rechercher tous les fichiers HTML dans les catégories
html_files = glob.glob('categories/*/*.html')
print(f"\nFichiers HTML trouvés: {len(html_files)}")

tutoriels = []

for filepath in html_files:
    filename = os.path.basename(filepath)
    if filename in EXCLUDE_FILES:
        continue
    try:
        metadata = extract_metadata(filepath)
        tutoriels.append(metadata)
        print(f"Traité: {filepath}")
    except Exception as e:
        print(f"Erreur avec {filepath}: {str(e)}")

# Organiser par catégories
tutoriels_by_category = {}
for cat_key in CATEGORIES:
    tutoriels_by_category[cat_key] = [t for t in tutoriels if t['category'] == cat_key]

# Générer les pages de catégories EN PREMIER
generate_category_pages(tutoriels_by_category)

# Générer le HTML de l'index principal - SEULEMENT LES CATÉGORIES
categories_html = ""
for cat_key, cat_info in CATEGORIES.items():
    count = len(tutoriels_by_category.get(cat_key, []))
    # Afficher toutes les catégories, même vides
    categories_html += f"""
        <a href="categories/{cat_key}/index.html" class="category-card">
            <div class="category-icon">{cat_info['icon']}</div>
            <div class="category-name">{cat_info['name']}</div>
            <div class="category-count">{count} tutoriel{"s" if count > 1 else ""}</div>
        </a>
        """

# Template HTML principal - UNIQUEMENT LES CATÉGORIES
index_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide iPhone pour Denise</title>
    <style>
{CSS}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📱 Guide iPhone</h1>
            <p>Tutoriels simples et détaillés pour maîtriser votre iPhone</p>
        </header>
        
        <div class="categories-grid">
            {categories_html}
        </div>
        
        <div style="text-align: center; margin: 40px 0; color: #666;">
            <p>Choisissez une catégorie pour voir les tutoriels</p>
            <p><small>Dernière mise à jour: {datetime.now().strftime("%d/%m/%Y")}</small></p>
        </div>
    </div>
</body>
</html>"""

# Écrire l'index principal
try:
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("\n✓ Généré: index.html")
except Exception as e:
    print(f"\n✗ Erreur lors de la création de index.html: {e}")

print(f"\nGénération terminée!")
print(f"Total: {len(tutoriels)} tutoriels traités")
print(f"Catégories créées: {len(CATEGORIES)}")

# Vérifier que les fichiers ont bien été créés
print("\n--- Vérification des fichiers créés ---")
for cat_key in CATEGORIES:
    index_path = f'categories/{cat_key}/index.html'
    if os.path.exists(index_path):
        print(f"✓ {index_path} existe")
    else:
        print(f"✗ {index_path} n'existe pas")
