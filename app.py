from flask import Flask, render_template, request, jsonify, redirect, url_for, session, send_file
import os
import json
import uuid
from datetime import datetime
import io
import base64
from PIL import Image

# Import your existing gallery system
try:
    from main import VirtualGalleryManager, UserProfile, Artwork
except ImportError:
    print("Make sure main.py is in the same directory!")
    exit(1)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize the gallery manager
gallery_manager = VirtualGalleryManager()

def create_html_templates():
    """Create HTML template files"""
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')

    # Main index template
    index_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Curated Virtual Art Gallery</title>
    <style>
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
            background-size: cover;
            background-position: center;
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
        }
    </style>
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
    <script>
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
                    <div class="artwork-image" style="background-image: url('${artwork.image_data || artwork.image_url || ''}'); background-size: cover; background-position: center;">
                        ${artwork.image_data || artwork.image_url ? '' : '🎨'}
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
        window.onclick = function(event) {
            const modal = document.getElementById('generateModal');
            if (event.target === modal) {
                hideGenerateModal();
            }
        }
        window.onload = function() {
            loadRecommendations();
        }
    </script>
</body>
</html>'''

    # Admin template
    admin_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gallery Admin Dashboard</title>
    <style>
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
        }
    </style>
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

    # Error templates
    error_404_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Not Found - Art Gallery</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .error-container {
            background: white;
            padding: 3rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            max-width: 500px;
        }
        .error-code {
            font-size: 4rem;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 1rem;
        }
        .error-message {
            font-size: 1.2rem;
            color: #718096;
            margin-bottom: 2rem;
        }
        .back-btn {
            background: #667eea;
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">404</div>
        <div class="error-message">Oops! This artwork seems to have wandered off...</div>
        <a href="/" class="back-btn">🎨 Return to Gallery</a>
    </div>
</body>
</html>'''

    error_500_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Server Error - Art Gallery</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
        }
        .error-container {
            background: white;
            padding: 3rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            max-width: 500px;
        }
        .error-code {
            font-size: 4rem;
            font-weight: bold;
            color: #e53e3e;
            margin-bottom: 1rem;
        }
        .error-message {
            font-size: 1.2rem;
            color: #718096;
            margin-bottom: 2rem;
        }
        .back-btn {
            background: #667eea;
            color: white;
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .back-btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-code">500</div>
        <div class="error-message">Something went wrong with our AI curator... Let's try again!</div>
        <a href="/" class="back-btn">🎨 Return to Gallery</a>
    </div>
</body>
</html>'''

    # Write template files with UTF-8 encoding
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)
    with open('templates/404.html', 'w', encoding='utf-8') as f:
        f.write(error_404_html)
    with open('templates/500.html', 'w', encoding='utf-8') as f:
        f.write(error_500_html)

    print("HTML templates created successfully!")

# Create HTML templates
create_html_templates()

@app.route('/')
def index():
    """Main gallery page"""
    # Create a demo user if none exists in session
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        # Create a demo user profile
        demo_user = UserProfile(
            user_id=session['user_id'],
            preferred_styles=["digital", "abstract"],
            preferred_colors=["vibrant", "cool"],
            liked_artworks=[],
            viewing_history=[],
            interaction_weights={"style": 0.4, "color": 0.3, "tags": 0.3}
        )
        gallery_manager.add_user(demo_user)
    return render_template('index.html')

@app.route('/api/recommendations')
def get_recommendations():
    """Get AI recommendations for current user"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user session'}), 400
    count = request.args.get('count', 12, type=int)
    recommendations = gallery_manager.get_recommendations(user_id, count)
    # Add base64 image data for each artwork
    for rec in recommendations:
        if rec.get('image_url'):
            img = gallery_manager.art_generator.generate_abstract_art(
                width=400, height=300, color_scheme=rec['color_palette'][0]
            )
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            rec['image_data'] = f'data:image/png;base64,{img_str}'
    return jsonify({
        'status': 'success',
        'recommendations': recommendations,
        'total': len(recommendations)
    })

@app.route('/api/artworks')
def get_all_artworks():
    """Get all artworks in the gallery"""
    artworks = []
    for artwork in gallery_manager.artworks:
        # Generate base64 image data for each artwork
        img = gallery_manager.art_generator.generate_abstract_art(
            width=400, height=300, color_scheme=artwork.color_palette[0]
        )
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        artwork_dict = {
            'id': artwork.id,
            'title': artwork.title,
            'artist': artwork.artist,
            'style': artwork.style,
            'color_palette': artwork.color_palette,
            'tags': artwork.tags,
            'description': artwork.description,
            'image_url': artwork.image_url,
            'image_data': f'data:image/png;base64,{img_str}',
            'created_date': artwork.created_date,
            'ai_generated': artwork.ai_generated
        }
        artworks.append(artwork_dict)
    return jsonify({
        'status': 'success',
        'artworks': artworks,
        'total': len(artworks)
    })

@app.route('/api/generate-artwork', methods=['POST'])
def generate_artwork():
    """Generate a new AI artwork"""
    try:
        data = request.get_json()
        style = data.get('style', 'vibrant')
        title = data.get('title', None)
        # Generate the artwork
        artwork = gallery_manager.generate_ai_artwork(style, title)
        # Generate a placeholder image data (base64 encoded)
        img = gallery_manager.art_generator.generate_abstract_art(
            width=400, height=300, color_scheme=style
        )
        # Convert PIL image to base64 for display
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return jsonify({
            'status': 'success',
            'artwork': {
                'id': artwork.id,
                'title': artwork.title,
                'artist': artwork.artist,
                'style': artwork.style,
                'tags': artwork.tags,
                'description': artwork.description,
                'ai_generated': artwork.ai_generated,
                'image_data': f'data:image/png;base64,{img_str}'
            }
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/interact', methods=['POST'])
def user_interaction():
    """Record user interaction with artwork"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user session'}), 400
    try:
        data = request.get_json()
        artwork_id = data.get('artwork_id')
        interaction_type = data.get('type')  # 'view', 'like', 'unlike'
        if interaction_type == 'like':
            gallery_manager.update_user_interaction(user_id, artwork_id, 'like')
        elif interaction_type == 'unlike':
            if user_id in gallery_manager.users:
                user = gallery_manager.users[user_id]
                if artwork_id in user.liked_artworks:
                    user.liked_artworks.remove(artwork_id)
        elif interaction_type == 'view':
            gallery_manager.update_user_interaction(user_id, artwork_id, 'view')
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/api/user-profile')
def get_user_profile():
    """Get current user's profile and preferences"""
    user_id = session.get('user_id')
    if not user_id or user_id not in gallery_manager.users:
        return jsonify({'error': 'User not found'}), 404
    user = gallery_manager.users[user_id]
    return jsonify({
        'status': 'success',
        'profile': {
            'user_id': user.user_id,
            'preferred_styles': user.preferred_styles,
            'preferred_colors': user.preferred_colors,
            'liked_artworks': user.liked_artworks,
            'viewing_history': user.viewing_history,
            'total_interactions': len(user.viewing_history) + len(user.liked_artworks)
        }
    })

@app.route('/api/update-preferences', methods=['POST'])
def update_preferences():
    """Update user preferences"""
    user_id = session.get('user_id')
    if not user_id or user_id not in gallery_manager.users:
        return jsonify({'error': 'User not found'}), 404
    try:
        data = request.get_json()
        user = gallery_manager.users[user_id]
        if 'preferred_styles' in data:
            user.preferred_styles = data['preferred_styles']
        if 'preferred_colors' in data:
            user.preferred_colors = data['preferred_colors']
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/export-artsteps')
def export_artsteps():
    """Export gallery for Artsteps integration"""
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'No user session'}), 400
    gallery_data = gallery_manager.export_gallery_for_artsteps(user_id)
    # Create a temporary file for download
    buffer = io.StringIO()
    json.dump(gallery_data, buffer)
    buffer.seek(0)
    return send_file(
        io.BytesIO(buffer.getvalue().encode('utf-8')),
        mimetype='application/json',
        as_attachment=True,
        download_name=f'artsteps_export_{user_id}.json'
    )

@app.route('/admin')
def admin_dashboard():
    """Simple admin dashboard to view gallery stats"""
    stats = {
        'total_artworks': len(gallery_manager.artworks),
        'total_users': len(gallery_manager.users),
        'ai_generated_count': len([a for a in gallery_manager.artworks if a.ai_generated]),
        'styles': list(set([a.style for a in gallery_manager.artworks]))
    }
    return render_template('admin.html', stats=stats)

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("Starting AI-Curated Virtual Art Gallery Web Server...")
    print(f"Gallery contains {len(gallery_manager.artworks)} artworks")
    print("Access your gallery at: http://localhost:5000")
    print("Admin dashboard at: http://localhost:5000/admin")
    app.run(debug=True, host='0.0.0.0', port=5000)