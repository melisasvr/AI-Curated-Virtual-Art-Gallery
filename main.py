import json
import random
import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import hashlib
from PIL import Image, ImageDraw, ImageFilter
import colorsys

@dataclass
class Artwork:
    id: str
    title: str
    artist: str
    style: str
    color_palette: List[str]
    tags: List[str]
    description: str
    image_url: str
    created_date: str
    ai_generated: bool = False

@dataclass
class UserProfile:
    user_id: str
    preferred_styles: List[str]
    preferred_colors: List[str]
    liked_artworks: List[str]
    viewing_history: List[str]
    interaction_weights: Dict[str, float]

class AIArtGenerator:
    """Simple AI art generator using procedural techniques"""
    
    @staticmethod
    def generate_abstract_art(width: int = 800, height: int = 600, 
                            color_scheme: str = "vibrant") -> Image.Image:
        """Generate abstract art using geometric shapes and gradients"""
        image = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(image)
        
        # Define color schemes
        color_schemes = {
            "vibrant": [(255, 59, 48), (255, 149, 0), (255, 204, 0), (52, 199, 89), (0, 122, 255)],
            "pastel": [(255, 214, 214), (255, 238, 214), (214, 255, 235), (214, 235, 255), (235, 214, 255)],
            "monochrome": [(0, 0, 0), (64, 64, 64), (128, 128, 128), (192, 192, 192), (255, 255, 255)],
            "earth": [(139, 69, 19), (160, 82, 45), (210, 180, 140), (222, 184, 135), (245, 245, 220)]
        }
        
        colors = color_schemes.get(color_scheme, color_schemes["vibrant"])
        
        # Create background gradient
        for y in range(height):
            r = int(255 * (y / height))
            g = int(200 * (1 - y / height))
            b = 150
            draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add geometric shapes
        for _ in range(random.randint(5, 15)):
            shape_type = random.choice(['circle', 'rectangle', 'polygon'])
            color = random.choice(colors)
            
            if shape_type == 'circle':
                x1, y1 = random.randint(0, width), random.randint(0, height)
                radius = random.randint(20, 100)
                draw.ellipse([x1-radius, y1-radius, x1+radius, y1+radius], 
                           fill=(*color, random.randint(100, 200)))
            elif shape_type == 'rectangle':
                x1, y1 = random.randint(0, width//2), random.randint(0, height//2)
                x2, y2 = x1 + random.randint(50, 200), y1 + random.randint(50, 200)
                draw.rectangle([x1, y1, x2, y2], 
                             fill=(*color, random.randint(100, 200)))
        
        # Apply blur effect
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
        return image

class RecommendationEngine:
    """AI-powered art recommendation system"""
    
    def __init__(self):
        self.style_vectors = self._create_style_vectors()
        self.color_vectors = self._create_color_vectors()
    
    def _create_style_vectors(self) -> Dict[str, List[float]]:
        """Create vector representations for art styles"""
        return {
            "abstract": [1.0, 0.8, 0.2, 0.9, 0.1],
            "impressionist": [0.7, 0.9, 0.8, 0.6, 0.7],
            "surreal": [0.9, 0.3, 0.7, 0.8, 0.9],
            "minimalist": [0.2, 0.1, 0.9, 0.3, 0.8],
            "pop_art": [0.9, 0.7, 0.3, 0.9, 0.4],
            "digital": [0.6, 0.4, 0.5, 0.9, 0.8],
            "classical": [0.3, 0.8, 0.9, 0.4, 0.6]
        }
    
    def _create_color_vectors(self) -> Dict[str, List[float]]:
        """Create vector representations for color preferences"""
        return {
            "warm": [1.0, 0.8, 0.2, 0.1, 0.3],
            "cool": [0.2, 0.3, 0.9, 0.8, 0.7],
            "neutral": [0.5, 0.5, 0.5, 0.6, 0.4],
            "vibrant": [0.9, 0.9, 0.8, 0.7, 0.9],
            "muted": [0.3, 0.4, 0.6, 0.3, 0.5]
        }
    
    def calculate_similarity(self, user_profile: UserProfile, artwork: Artwork) -> float:
        """Calculate similarity score between user preferences and artwork"""
        style_score = 0.0
        color_score = 0.0
        tag_score = 0.0
        
        # Style similarity
        if artwork.style in self.style_vectors:
            artwork_style_vec = self.style_vectors[artwork.style]
            for pref_style in user_profile.preferred_styles:
                if pref_style in self.style_vectors:
                    pref_vec = self.style_vectors[pref_style]
                    similarity = np.dot(artwork_style_vec, pref_vec) / (
                        np.linalg.norm(artwork_style_vec) * np.linalg.norm(pref_vec)
                    )
                    style_score = max(style_score, similarity)
        
        # Color similarity
        for color in user_profile.preferred_colors:
            if color in self.color_vectors:
                color_vec = self.color_vectors[color]
                # Simple color matching based on artwork's color palette
                color_score += 0.2  # Simplified for demo
        
        # Tag-based similarity
        user_tags = set(user_profile.liked_artworks)  # Simplified
        artwork_tags = set(artwork.tags)
        if artwork_tags:
            tag_score = len(user_tags.intersection(artwork_tags)) / len(artwork_tags)
        
        # Historical preference weighting
        history_boost = 1.0
        if artwork.id in user_profile.viewing_history:
            history_boost = 0.5  # Reduce recommendation for already viewed
        
        # Combine scores
        final_score = (0.4 * style_score + 0.3 * color_score + 0.3 * tag_score) * history_boost
        return min(final_score, 1.0)
    
    def recommend_artworks(self, user_profile: UserProfile, artworks: List[Artwork], 
                          count: int = 10) -> List[Tuple[Artwork, float]]:
        """Recommend artworks based on user profile"""
        scored_artworks = []
        
        for artwork in artworks:
            if artwork.id not in user_profile.viewing_history:
                score = self.calculate_similarity(user_profile, artwork)
                scored_artworks.append((artwork, score))
        
        # Sort by score and return top recommendations
        scored_artworks.sort(key=lambda x: x[1], reverse=True)
        return scored_artworks[:count]

class VirtualGalleryManager:
    """Main class for managing the AI-curated virtual art gallery"""
    
    def __init__(self):
        self.artworks: List[Artwork] = []
        self.users: Dict[str, UserProfile] = {}
        self.recommendation_engine = RecommendationEngine()
        self.art_generator = AIArtGenerator()
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample artworks and user data"""
        sample_artworks = [
            Artwork(
                id="art001",
                title="Digital Sunset",
                artist="AI Artist",
                style="abstract",
                color_palette=["#FF6B6B", "#4ECDC4", "#45B7D1"],
                tags=["sunset", "digital", "colorful"],
                description="A vibrant abstract representation of a digital sunset",
                image_url="/gallery/digital_sunset.jpg",
                created_date="2024-01-15",
                ai_generated=True
            ),
            Artwork(
                id="art002",
                title="Geometric Dreams",
                artist="Virtual Creator",
                style="minimalist",
                color_palette=["#2C3E50", "#ECF0F1", "#E74C3C"],
                tags=["geometric", "minimalist", "clean"],
                description="Clean geometric patterns in a minimalist composition",
                image_url="/gallery/geometric_dreams.jpg",
                created_date="2024-01-20",
                ai_generated=True
            ),
            Artwork(
                id="art003",
                title="Ocean Waves",
                artist="Nature AI",
                style="impressionist",
                color_palette=["#3498DB", "#2980B9", "#ECF0F1"],
                tags=["ocean", "waves", "nature"],
                description="Impressionistic interpretation of ocean waves",
                image_url="/gallery/ocean_waves.jpg",
                created_date="2024-02-01",
                ai_generated=True
            ),
            Artwork(
                id="art004",
                title="Neon Cityscape",
                artist="CyberArt AI",
                style="digital",
                color_palette=["#FF0080", "#00FF80", "#8000FF"],
                tags=["cyberpunk", "city", "neon", "futuristic"],
                description="A futuristic cityscape with vibrant neon lighting",
                image_url="/gallery/neon_cityscape.jpg",
                created_date="2024-02-05",
                ai_generated=True
            ),
            Artwork(
                id="art005",
                title="Zen Garden",
                artist="Peaceful Mind",
                style="minimalist",
                color_palette=["#F5F5DC", "#8FBC8F", "#696969"],
                tags=["zen", "peaceful", "nature", "meditation"],
                description="A serene minimalist interpretation of a zen garden",
                image_url="/gallery/zen_garden.jpg",
                created_date="2024-02-08",
                ai_generated=False
            ),
            Artwork(
                id="art006",
                title="Cosmic Dance",
                artist="StarField Studio",
                style="surreal",
                color_palette=["#4B0082", "#FF1493", "#FFD700"],
                tags=["space", "cosmic", "surreal", "dance"],
                description="Surreal interpretation of celestial bodies in motion",
                image_url="/gallery/cosmic_dance.jpg",
                created_date="2024-02-10",
                ai_generated=True
            ),
            Artwork(
                id="art007",
                title="Urban Pulse",
                artist="Street Vision",
                style="pop_art",
                color_palette=["#FF4500", "#32CD32", "#1E90FF"],
                tags=["urban", "street", "energy", "modern"],
                description="Pop art representation of urban energy and movement",
                image_url="/gallery/urban_pulse.jpg",
                created_date="2024-02-12",
                ai_generated=False
            ),
            Artwork(
                id="art008",
                title="Forest Whispers",
                artist="Natural Harmony",
                style="impressionist",
                color_palette=["#228B22", "#8FBC8F", "#F5F5DC"],
                tags=["forest", "nature", "peaceful", "organic"],
                description="Impressionistic capture of sunlight filtering through forest",
                image_url="/gallery/forest_whispers.jpg",
                created_date="2024-02-14",
                ai_generated=False
            ),
            Artwork(
                id="art009",
                title="Quantum Fragments",
                artist="Physics Art Lab",
                style="abstract",
                color_palette=["#00CED1", "#FF69B4", "#ADFF2F"],
                tags=["quantum", "science", "fragments", "energy"],
                description="Abstract visualization of quantum particle interactions",
                image_url="/gallery/quantum_fragments.jpg",
                created_date="2024-02-16",
                ai_generated=True
            ),
            Artwork(
                id="art010",
                title="Retro Synthwave",
                artist="Retro Future",
                style="digital",
                color_palette=["#FF006E", "#FB5607", "#8338EC"],
                tags=["retro", "synthwave", "80s", "nostalgic"],
                description="Nostalgic digital art inspired by 80s synthwave aesthetic",
                image_url="/gallery/retro_synthwave.jpg",
                created_date="2024-02-18",
                ai_generated=True
            ),
            Artwork(
                id="art011",
                title="Marble Dreams",
                artist="Classical Moderne",
                style="classical",
                color_palette=["#F8F8FF", "#D2B48C", "#A0522D"],
                tags=["marble", "classical", "sculpture", "elegant"],
                description="Digital interpretation of classical marble sculpture",
                image_url="/gallery/marble_dreams.jpg",
                created_date="2024-02-20",
                ai_generated=False
            ),
            Artwork(
                id="art012",
                title="Electric Storm",
                artist="Weather Dynamics",
                style="abstract",
                color_palette=["#9400D3", "#FFD700", "#FF4500"],
                tags=["storm", "electricity", "energy", "dynamic"],
                description="Abstract representation of electrical storm patterns",
                image_url="/gallery/electric_storm.jpg",
                created_date="2024-02-22",
                ai_generated=True
            ),
            Artwork(
                id="art013",
                title="Minimalist Horizon",
                artist="Simple Beauty",
                style="minimalist",
                color_palette=["#E6E6FA", "#FFE4E1", "#F0F8FF"],
                tags=["horizon", "minimal", "peaceful", "simplicity"],
                description="Clean, minimal interpretation of a distant horizon",
                image_url="/gallery/minimalist_horizon.jpg",
                created_date="2024-02-24",
                ai_generated=False
            )
        ]
        self.artworks.extend(sample_artworks)
        
        # Sample user profile
        sample_user = UserProfile(
            user_id="user001",
            preferred_styles=["abstract", "digital"],
            preferred_colors=["vibrant", "cool"],
            liked_artworks=["art001"],
            viewing_history=[],
            interaction_weights={"style": 0.4, "color": 0.3, "tags": 0.3}
        )
        self.users["user001"] = sample_user
    
    def add_user(self, user_profile: UserProfile):
        """Add a new user profile"""
        self.users[user_profile.user_id] = user_profile
    
    def add_artwork(self, artwork: Artwork):
        """Add a new artwork to the gallery"""
        self.artworks.append(artwork)
    
    def generate_ai_artwork(self, style_preference: str = "vibrant", 
                          title: str = None) -> Artwork:
        """Generate a new AI artwork"""
        # Generate the image
        image = self.art_generator.generate_abstract_art(color_scheme=style_preference)
        
        # Create artwork metadata
        artwork_id = hashlib.md5(f"{datetime.now()}{random.random()}".encode()).hexdigest()[:8]
        
        if not title:
            title = f"AI Generated Art #{len([a for a in self.artworks if a.ai_generated]) + 1}"
        
        artwork = Artwork(
            id=artwork_id,
            title=title,
            artist="AI Gallery Generator",
            style="abstract",
            color_palette=["#FF6B6B", "#4ECDC4", "#45B7D1"],  # Simplified
            tags=["ai_generated", "abstract", style_preference],
            description=f"AI-generated artwork with {style_preference} color scheme",
            image_url=f"/generated/{artwork_id}.jpg",
            created_date=datetime.now().strftime("%Y-%m-%d"),
            ai_generated=True
        )
        
        # Save image (in real implementation)
        # image.save(f"gallery_images/{artwork_id}.jpg")
        
        self.add_artwork(artwork)
        return artwork
    
    def get_recommendations(self, user_id: str, count: int = 10) -> List[Dict]:
        """Get personalized artwork recommendations for a user"""
        if user_id not in self.users:
            return []
        
        user_profile = self.users[user_id]
        recommendations = self.recommendation_engine.recommend_artworks(
            user_profile, self.artworks, count
        )
        
        return [{
            **asdict(artwork),
            "recommendation_score": score
        } for artwork, score in recommendations]
    
    def update_user_interaction(self, user_id: str, artwork_id: str, 
                              interaction_type: str):
        """Update user interaction data"""
        if user_id in self.users:
            user = self.users[user_id]
            
            if interaction_type == "view":
                if artwork_id not in user.viewing_history:
                    user.viewing_history.append(artwork_id)
            elif interaction_type == "like":
                if artwork_id not in user.liked_artworks:
                    user.liked_artworks.append(artwork_id)
    
    def export_gallery_for_artsteps(self, user_id: str) -> Dict:
        """Export gallery data in a format suitable for Artsteps integration"""
        recommendations = self.get_recommendations(user_id, count=20)
        
        gallery_data = {
            "gallery_info": {
                "title": f"AI-Curated Gallery for {user_id}",
                "description": "Personalized art collection curated by AI",
                "created_date": datetime.now().strftime("%Y-%m-%d"),
                "total_artworks": len(recommendations)
            },
            "artworks": recommendations,
            "user_preferences": asdict(self.users.get(user_id, UserProfile("", [], [], [], [], {})))
        }
        
        return gallery_data
    
    def save_gallery_data(self, filename: str = "gallery_data.json"):
        """Save all gallery data to JSON file"""
        data = {
            "artworks": [asdict(artwork) for artwork in self.artworks],
            "users": {uid: asdict(user) for uid, user in self.users.items()}
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Gallery data saved to {filename}")

# Example usage
if __name__ == "__main__":
    # Initialize the gallery
    gallery = VirtualGalleryManager()
    
    # Generate some AI artworks
    print("Generating AI artworks...")
    gallery.generate_ai_artwork("vibrant", "Colorful Dreams")
    gallery.generate_ai_artwork("pastel", "Soft Whispers")
    gallery.generate_ai_artwork("monochrome", "Shadow Play")
    
    # Get recommendations for user
    print("\nGetting recommendations for user001...")
    recommendations = gallery.get_recommendations("user001", count=5)
    
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec['title']} by {rec['artist']}")
        print(f"   Style: {rec['style']} | Score: {rec['recommendation_score']:.2f}")
        print(f"   Tags: {', '.join(rec['tags'])}")
        print()
    
    # Update user interaction
    gallery.update_user_interaction("user001", "art002", "like")
    gallery.update_user_interaction("user001", "art002", "view")
    
    # Export for Artsteps
    print("Exporting gallery data for Artsteps integration...")
    artsteps_data = gallery.export_gallery_for_artsteps("user001")
    
    # Save gallery data
    gallery.save_gallery_data()
    
    print(f"Gallery contains {len(gallery.artworks)} artworks")
    print(f"Generated Artsteps export with {len(artsteps_data['artworks'])} recommended pieces")