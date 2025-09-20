// Gallery JavaScript functionality
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
}