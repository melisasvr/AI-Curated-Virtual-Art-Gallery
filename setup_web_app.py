# setup_web_app.py
"""
Setup script for AI-Curated Virtual Art Gallery Web Application
Run this script to create all necessary files and directories
"""

import os

def create_directory_structure():
    """Create necessary directories"""
    directories = [
        'templates',
        'static',
        'static/css',
        'static/js', 
        'static/images'
    ]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def create_templates():
    """Create HTML template files"""
    
    # Main index template (emojis replaced with HTML entities where needed)
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Curated Virtual Art Gallery</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <div class="header">
        <h1>🎨 AI-Curated Virtual Art Gallery</h1>
        <p>Discover personalized art recommendations powered by artificial intelligence</p>
    </div>
    
    <div class="controls">
        <button class="btn btn-primary" onclick="loadRecommendations()">🤖 Get AI Recommendations</button>
        <button class="btn btn-secondary" onclick="loadAllArtworks()">🖼️ Browse All Artworks</button>
        <button class="btn btn-secondary" onclick="showGenerateModal()">✨ Generate AI Art</button>
        <a href="/admin" class="btn btn-secondary">📊 Gallery Stats</a>
        <a href="/export-artsteps" class="btn btn-secondary" target="_blank">📤 Export for Artsteps</a>
    </div>
    
    <div class="gallery-section">
        <h2 class="section-title" id="section-title">Welcome to Your Personalized Gallery</h2>
        <div class="artwork-grid" id="artwork-grid">
            <div class="loading">Click "Get AI Recommendations" to see your personalized art collection!</div>
        </div>
    </div>
    
    <!-- Generate Art Modal -->
    <div id="generateModal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="hideGenerateModal()">&times;</span>
            <h2>Generate AI Artwork</h2>
            <div class="form-group">
                <label for="artTitle">Title (optional):</label>
                <input type="text" id="artTitle" placeholder="Enter artwork title...">
            </div>
            <div class="form-group">
                <label for="colorScheme">Color Scheme:</label>
                <select id="colorScheme">
                    <option value="vibrant">Vibrant</option>
                    <option value="pastel">Pastel</option>
                    <option value="monochrome">Monochrome</option>
                    <option value="earth">Earth Tones</option>
                </select>
            </div>
            <button class="btn btn-primary" onclick="generateArt()">Generate Artwork</button>
        </div>
    </div>
    
    <script src="/static/js/gallery.js"></script>
</body>
</html>'''

    # Admin template
    admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery Admin Dashboard</title>
    <link rel="stylesheet" href="/static/css/admin.css">
</head>
<body>
    <div class="dashboard">
        <a href="/" class="back-btn">← Back to Gallery</a>
        
        <div class="header">
            <h1>📊 Gallery Admin Dashboard</h1>
            <p>Overview of your AI-Curated Virtual Art Gallery</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_artworks }}</div>
                <div class="stat-label">Total Artworks</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{{ stats.ai_generated_count }}</div>
                <div class="stat-label">AI Generated</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{{ stats.total_users }}</div>
                <div class="stat-label">Active Users</div>
            </div>
            
            <div class="stat-card">
                <div class="stat-number">{{ stats.styles|length }}</div>
                <div class="stat-label">Art Styles</div>
            </div>
        </div>
        
        <div class="styles-list">
            <h3>Available Art Styles:</h3>
            {% for style in stats.styles %}
                <span class="style-tag">{{ style }}</span>
            {% endfor %}
        </div>
    </div>
</body>
</html>'''

    # Write template files with UTF-8 encoding
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    print("✅ Created templates/index.html")
    
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)
    print("✅ Created templates/admin.html")

def create_css_files():
    """Create CSS files"""
    
    # Main stylesheet
    main_css = '''/* Main Gallery Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    color: #333;
}

.header {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    padding: 1rem 2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.1);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header h1 {
    color: #4a5568;
    font-size: 2rem;
    text-align: center;
    margin-bottom: 0.5rem;
}

.header p {
    text-align: center;
    color: #718096;
}

.controls {
    background: rgba(255, 255, 255, 0.9);
    padding: 1.5rem;
    margin: 2rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    display: flex;
    gap: 1rem;
    flex-wrap: wrap;
    align-items: center;
    justify-content: center;
}

.btn {
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}

.btn-primary {
    background: linear-gradient(45deg, #667eea, #764ba2);
    color: white;
}

.btn-secondary {
    background: #e2e8f0;
    color: #4a5568;
}

.btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.gallery-section {
    margin: 2rem;
}

.section-title {
    color: white;
    font-size: 1.5rem;
    margin-bottom: 1rem;
    text-align: center;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.artwork-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 1.5rem;
    margin-top: 1rem;
}

.artwork-card {
    background: white;
    border-radius: 15px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    cursor: pointer;
}

.artwork-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.15);
}

.artwork-image {
    width: 100%;
    height: 200px;
    background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #999;
    font-size: 3rem;
    position: relative;
}

.artwork-info {
    padding: 1.5rem;
}

.artwork-title {
    font-size: 1.2rem;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 0.5rem;
}

.artwork-artist {
    color: #718096;
    margin-bottom: 0.5rem;
}

.artwork-style {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.8rem;
    margin-bottom: 0.5rem;
}

.artwork-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tag {
    background: #e2e8f0;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.7rem;
    color: #4a5568;
}

.artwork-actions {
    display: flex;
    gap: 0.5rem;
}

.like-btn {
    background: #e53e3e;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.like-btn.liked {
    background: #c53030;
}

.like-btn:hover {
    background: #c53030;
}

.loading {
    text-align: center;
    color: white;
    font-size: 1.2rem;
    margin: 2rem;
}

.score {
    position: absolute;
    top: 10px;
    right: 10px;
    background: rgba(0,0,0,0.8);
    color: white;
    padding: 0.25rem 0.5rem;
    border-radius: 12px;
    font-size: 0.7rem;
}

.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.8);
    backdrop-filter: blur(5px);
}

.modal-content {
    background: white;
    margin: 10% auto;
    padding: 2rem;
    border-radius: 15px;
    width: 90%;
    max-width: 500px;
}

.close {
    color: #999;
    float: right;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover {
    color: #333;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
}

.form-group input, .form-group select {
    width: 100%;
    padding: 0.75rem;
    border: 2px solid #e2e8f0;
    border-radius: 8px;
    font-size: 1rem;
}

@media (max-width: 768px) {
    .controls {
        flex-direction: column;
        align-items: stretch;
    }
    
    .btn {
        width: 100%;
        text-align: center;
    }
    
    .artwork-grid {
        grid-template-columns: 1fr;
    }
}'''

    # Admin stylesheet
    admin_css = '''/* Admin Dashboard Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    margin: 0;
    padding: 2rem;
}

.dashboard {
    max-width: 1200px;
    margin: 0 auto;
}

.header {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-card {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.stat-number {
    font-size: 2.5rem;
    font-weight: bold;
    color: #667eea;
    margin-bottom: 0.5rem;
}

.stat-label {
    color: #718096;
    font-size: 1rem;
}

.styles-list {
    background: white;
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.style-tag {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 0.5rem 1rem;
    margin: 0.25rem;
    border-radius: 20px;
    font-size: 0.9rem;
}

.back-btn {
    background: #667eea;
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 8px;
    text-decoration: none;
    display: inline-block;
    margin-bottom: 2rem;
    transition: all 0.3s ease;
}

.back-btn:hover {
    background: #5a67d8;
    transform: translateY(-2px);
}'''

    # Write CSS files with UTF-8 encoding
    with open('static/css/style.css', 'w', encoding='utf-8') as f:
        f.write(main_css)
    print("✅ Created static/css/style.css")
    
    with open('static/css/admin.css', 'w', encoding='utf-8') as f:
        f.write(admin_css)
    print("✅ Created static/css/admin.css")

def create_javascript():
    """Create JavaScript file"""
    
    gallery_js = '''// Gallery JavaScript functionality
let likedArtworks = new Set();

async function loadRecommendations() {
    document.getElementById('section-title').textContent = 'AI Recommendations For You';
    document.getElementById('artwork-grid').innerHTML = '<div class="loading">Loading your personalized recommendations...</div>';
    
    try {
        const response = await fetch('/api/recommendations');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayArtworks(data.recommendations, true);
        } else {
            document.getElementById('artwork-grid').innerHTML = '<div class="loading">Error loading recommendations</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('artwork-grid').innerHTML = '<div class="loading">Error loading recommendations</div>';
    }
}

async function loadAllArtworks() {
    document.getElementById('section-title').textContent = 'All Gallery Artworks';
    document.getElementById('artwork-grid').innerHTML = '<div class="loading">Loading all artworks...</div>';
    
    try {
        const response = await fetch('/api/artworks');
        const data = await response.json();
        
        if (data.status === 'success') {
            displayArtworks(data.artworks, false);
        } else {
            document.getElementById('artwork-grid').innerHTML = '<div class="loading">Error loading artworks</div>';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('artwork-grid').innerHTML = '<div class="loading">Error loading artworks</div>';
    }
}

function displayArtworks(artworks, showScores = false) {
    const grid = document.getElementById('artwork-grid');
    
    if (artworks.length === 0) {
        grid.innerHTML = '<div class="loading">No artworks found</div>';
        return;
    }
    
    grid.innerHTML = '';
    
    artworks.forEach(artwork => {
        const isLiked = likedArtworks.has(artwork.id);
        const score = artwork.recommendation_score;
        
        const artworkCard = document.createElement('div');
        artworkCard.className = 'artwork-card';
        artworkCard.innerHTML = `
            <div class="artwork-image">
                🎨
                ${showScores && score ? `<div class="score">Score: ${score.toFixed(2)}</div>` : ''}
            </div>
            <div class="artwork-info">
                <div class="artwork-title">${artwork.title}</div>
                <div class="artwork-artist">by ${artwork.artist}</div>
                <div class="artwork-style">${artwork.style}</div>
                <div class="artwork-tags">
                    ${artwork.tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                </div>
                <div class="artwork-actions">
                    <button class="like-btn ${isLiked ? 'liked' : ''}" onclick="toggleLike('${artwork.id}', this)">
                        ${isLiked ? '❤️ Liked' : '🤍 Like'}
                    </button>
                </div>
            </div>
        `;
        
        artworkCard.addEventListener('click', (e) => {
            if (e.target.tagName !== 'BUTTON') {
                viewArtwork(artwork.id);
            }
        });
        grid.appendChild(artworkCard);
    });
}

async function toggleLike(artworkId, button) {
    event.stopPropagation();
    const isLiked = likedArtworks.has(artworkId);
    const action = isLiked ? 'unlike' : 'like';
    
    try {
        const response = await fetch('/api/interact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                artwork_id: artworkId,
                type: action
            })
        });
        
        if (response.ok) {
            if (isLiked) {
                likedArtworks.delete(artworkId);
                button.innerHTML = '🤍 Like';
                button.classList.remove('liked');
            } else {
                likedArtworks.add(artworkId);
                button.innerHTML = '❤️ Liked';
                button.classList.add('liked');
            }
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function viewArtwork(artworkId) {
    try {
        await fetch('/api/interact', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                artwork_id: artworkId,
                type: 'view'
            })
        });
        console.log('Viewed artwork:', artworkId);
    } catch (error) {
        console.error('Error recording view:', error);
    }
}

function showGenerateModal() {
    document.getElementById('generateModal').style.display = 'block';
}

function hideGenerateModal() {
    document.getElementById('generateModal').style.display = 'none';
    document.getElementById('artTitle').value = '';
    document.getElementById('colorScheme').value = 'vibrant';
}

async function generateArt() {
    const title = document.getElementById('artTitle').value;
    const colorScheme = document.getElementById('colorScheme').value;
    
    const generateButton = event.target;
    generateButton.disabled = true;
    generateButton.textContent = 'Generating...';
    
    try {
        const response = await fetch('/api/generate-artwork', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title || null,
                style: colorScheme
            })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            alert(`Successfully generated: ${data.artwork.title}`);
            hideGenerateModal();
            loadAllArtworks();
        } else {
            alert('Error generating artwork: ' + data.message);
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error generating artwork');
    } finally {
        generateButton.disabled = false;
        generateButton.textContent = 'Generate Artwork';
    }
}

// Close modal when clicking outside of it
window.onclick = function(event) {
    const modal = document.getElementById('generateModal');
    if (event.target === modal) {
        hideGenerateModal();
    }
}

// Load recommendations on page load
window.onload = function() {
    loadRecommendations();
}'''

    with open('static/js/gallery.js', 'w', encoding='utf-8') as f:
        f.write(gallery_js)
    print("✅ Created static/js/gallery.js")

def create_requirements_file():
    """Create requirements.txt file"""
    requirements = '''Flask==2.3.3
Pillow==10.0.1
numpy==1.24.3
'''
    
    with open('requirements.txt', 'w', encoding='utf-8') as f:
        f.write(requirements)
    print("✅ Created requirements.txt")

def create_run_script():
    """Create a simple run script"""
    run_script = '''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run the AI-Curated Virtual Art Gallery Web Application
"""

from app import app

if __name__ == '__main__':
    print("Starting AI-Curated Virtual Art Gallery...")
    print("Access your gallery at: http://localhost:5000")
    print("Admin dashboard at: http://localhost:5000/admin")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
'''
    
    with open('run.py', 'w', encoding='utf-8') as f:
        f.write(run_script)
    print("✅ Created run.py")

def main():
    """Main setup function"""
    print("Setting up AI-Curated Virtual Art Gallery Web Application")
    print("=" * 60)
    
    # Create directory structure
    create_directory_structure()
    print()
    
    # Create template files
    print("Creating HTML templates...")
    create_templates()
    print()
    
    # Create CSS files
    print("Creating CSS files...")
    create_css_files()
    print()
    
    # Create JavaScript files
    print("Creating JavaScript files...")
    create_javascript()
    print()
    
    # Create requirements file
    create_requirements_file()
    
    # Create run script
    create_run_script()
    
    print()
    print("=" * 60)
    print("Setup complete! Your web application is ready.")
    print()
    print("Next steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Make sure you have your main.py file in the same directory")
    print("3. Run the Flask app: python app.py")
    print("4. Open your browser to: http://localhost:5000")
    print()
    print("Enjoy your AI-Curated Virtual Art Gallery!")

if __name__ == "__main__":
    main()