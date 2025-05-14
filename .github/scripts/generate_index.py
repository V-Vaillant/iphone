#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import glob
from bs4 import BeautifulSoup
from datetime import datetime

# Configuration
CATEGORIES = {
    'reglages': {'name': 'Réglages essentiels', 'icon': '⚙️'},
    'communication': {'name': 'Communication', 'icon': '📱'},
    'meta': {'name': 'Applications Meta', 'icon': '👥'},
    'photos': {'name': 'Photos et souvenirs', 'icon': '📸'},
    'organisation': {'name': 'Organisation', 'icon': '📅'},
    'google': {'name': 'Google Drive', 'icon': '📁'}
}

# CSS commun
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

.tutoriel-card {
    background-color: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: transform 0.2s ease;
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

.nav-top, .nav-bottom {
    display: flex;
    gap: 15px;
    align-items: center;
    justify-content: center;
    margin: 20px 0;
}

.nav-link {
    display: inline-block;
    padding: 12px 24px;
    background-color: var(--primary-color);
    color: white;
    text-decoration: none;
    border-radius: 22px;
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
    text-decoration: none;
    color: var(--text-color);
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

.empty-state {
    text-align: center;
    color: #666;
    padding: 40px;
    font-size: 18px;
}

@media (max-width: 428px) {
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

def find_project_root():
    """Trouve la racine du projet (où se trouve le dossier categories)"""
    current = os.getcwd()
    while current != '/':
        if os.path.exists(os.path.join(current, 'categories')):
            return current
        current = os.path.dirname(current)
    return None

def extract_metadata(filepath):
    """Extrait les métadonnées d'un fichier tutoriel"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Si le fichier est vide, utiliser des valeurs par défaut
        if not content.strip():
            basename = os.path.basename(filepath).replace('.html', '')
            return {
                'title': basename.replace('-', ' ').title(),
                'description': 'Tutoriel pour iPhone',
                'difficulty': 'Facile',
                'duration': '5 minutes'
            }
            
        soup = BeautifulSoup(content, 'html.parser')
        
        # Extraire le titre
        title = None
        if soup.find('h1'):
            title = soup.find('h1').text.strip()
        
        if not title:
            title = os.path.basename(filepath).replace('.html', '').replace('-', ' ').title()
        
        # Extraire la description
        description = "Tutoriel pour iPhone"
        objectif = soup.find(class_='objectif')
        if objectif:
            description = objectif.text.strip()
        
        # Extraire difficulté et durée
        difficulty = 'Facile'
        duration = '5 minutes'
        
        difficulty_meta = soup.find('meta', {'name': 'difficulty'})
        if difficulty_meta:
            difficulty = difficulty_meta.get('content', 'Facile')
            
        duration_meta = soup.find('meta', {'name': 'duration'})
        if duration_meta:
            duration = duration_meta.get('content', '5 minutes')
        
        return {
            'title': title,
            'description': description,
            'difficulty': difficulty,
            'duration': duration
        }
        
    except Exception as e:
        print(f"Erreur lors de la lecture de {filepath}: {e}")
        basename = os.path.basename(filepath).replace('.html', '')
        return {
            'title': basename.replace('-', ' ').title(),
            'description': 'Tutoriel pour iPhone',
            'difficulty': 'Facile',
            'duration': '5 minutes'
        }

def generate_category_index(category, tutoriels):
    """Génère le HTML pour l'index d'une catégorie"""
    cat_info = CATEGORIES[category]
    
    tutoriels_html = ""
    if not tutoriels:
        tutoriels_html = '<p class="empty-state">Aucun tutoriel disponible dans cette catégorie pour le moment.</p>'
    else:
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
    
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{cat_info['name']} - Guide iPhone</title>
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
            {tutoriels_html}
        </div>
        
        <nav class="nav-bottom">
            <a href="../../index.html" class="nav-link">🏠 Retour à l'accueil</a>
        </nav>
    </div>
</body>
</html>"""

def generate_main_index(stats):
    """Génère l'index principal avec les catégories"""
    categories_html = ""
    
    for cat_key, cat_info in CATEGORIES.items():
        count = stats.get(cat_key, 0)
        categories_html += f"""
        <a href="categories/{cat_key}/index.html" class="category-card">
            <div class="category-icon">{cat_info['icon']}</div>
            <div class="category-name">{cat_info['name']}</div>
            <div class="category-count">{count} tutoriel{"s" if count > 1 else ""}</div>
        </a>
        """
    
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guide iPhone</title>
    <style>{CSS}</style>
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
            <p><small>Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y')}</small></p>
        </div>
    </div>
</body>
</html>"""

def main():
    """Fonction principale"""
    print("🚀 Génération des index du site iPhone")
    print("=" * 40)
    
    # Trouver la racine du projet
    root = find_project_root()
    if not root:
        print("❌ Erreur: Impossible de trouver le dossier 'categories'")
        print("Assurez-vous d'être dans le bon répertoire")
        return 1
        
    os.chdir(root)
    print(f"📂 Répertoire de travail: {root}")
    
    # Statistiques
    stats = {}
    total_generated = 0
    
    # Traiter chaque catégorie
    for category in CATEGORIES:
        print(f"\n📁 Traitement de la catégorie: {category}")
        category_dir = f"categories/{category}"
        
        # Créer le répertoire s'il n'existe pas
        if not os.path.exists(category_dir):
            os.makedirs(category_dir, exist_ok=True)
            print(f"  ✓ Créé le répertoire {category_dir}")
        
        # Trouver tous les tutoriels dans cette catégorie
        tutoriels = []
        html_files = glob.glob(f"{category_dir}/*.html")
        
        for filepath in html_files:
            filename = os.path.basename(filepath)
            if filename == 'index.html':
                continue
                
            print(f"  → Analyse de {filename}")
            metadata = extract_metadata(filepath)
            metadata['filename'] = filename
            tutoriels.append(metadata)
        
        # Générer l'index de la catégorie
        index_content = generate_category_index(category, tutoriels)
        index_path = f"{category_dir}/index.html"
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
            
        print(f"  ✓ Généré: {index_path} ({len(tutoriels)} tutoriels)")
        stats[category] = len(tutoriels)
        total_generated += 1
    
    # Générer l'index principal
    print(f"\n📄 Génération de l'index principal")
    main_index = generate_main_index(stats)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(main_index)
        
    print(f"  ✓ Généré: index.html")
    total_generated += 1
    
    # Résumé
    print("\n" + "=" * 40)
    print("✅ Génération terminée avec succès!")
    print(f"📊 Statistiques:")
    print(f"  - {total_generated} fichiers index générés")
    print(f"  - {sum(stats.values())} tutoriels au total")
    
    for cat, count in stats.items():
        print(f"  - {CATEGORIES[cat]['name']}: {count} tutoriels")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
