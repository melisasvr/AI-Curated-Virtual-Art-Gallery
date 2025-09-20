# AI-Curated Virtual Art Gallery

- This project is a web-based virtual art gallery that uses artificial intelligence to generate abstract artwork and provide personalized recommendations to users.
- Built with Python, Flask, and PIL, it features a recommendation engine, AI art generation, and user interaction tracking. The gallery allows users to browse artworks, generate new pieces, like artworks, and export their curated collection for Artsteps integration.
- Note: This is my first attempt at building an AI art gallery, so the generated images are simple and not particularly fancy. They use basic geometric shapes and gradients to create abstract art.

## Features
- AI Art Generation: Generate abstract artworks with customizable color schemes (vibrant, pastel, monochrome, earth tones).
- Personalized Recommendations: A recommendation engine that suggests artworks based on user preferences for styles, colors, and interaction history.
- User Interaction Tracking: Track user views and likes to improve recommendations.
- Web Interface: A responsive Flask-based web interface for browsing, generating, and interacting with artworks.
- Artsteps Export: Export curated gallery data in JSON format for integration with Artsteps.
- Admin Dashboard: View gallery statistics, including total artworks, AI-generated pieces, and available art styles.

## Technologies Used
- Python: Core programming language.
- Flask: Web framework for the user interface and API.
- PIL (Pillow): For generating abstract artworks.
- NumPy: For vector calculations in the recommendation engine.
- HTML/CSS/JavaScript: For the front-end interface.
- JSON: For data storage and export.

## Installation
- Clone the Repository:
- `git clone <repository-url>`
- `cd <repository-folder>`

## Install Dependencies:
- `pip install flask pillow numpy`
1. Ensure Required Files:
- Make sure `main.py` and `app.py` are in the project root.
2. The templates folder will be automatically created with HTML templates when you run `app.py`.

## Usage
1. Run the Application:
- `python app.py`
- This will start the Flask server at `http://localhost:5000`.
2. Access the Gallery:
- Visit `http://localhost:5000` to explore the gallery.
- Click "Get AI Recommendations" for personalized artwork suggestions.
- Click "Browse All Artworks" to view all available pieces.
- Use "Generate AI Art" to create new artwork with a chosen color scheme.
- Access the admin dashboard at http://localhost:5000/admin to view gallery statistics.
- Export your curated gallery for Artsteps using the "Export for Artsteps" button.


## Interacting with Artworks:
- Click the "Like" button to add an artwork to your favorites.
- Generated artworks are simple abstract pieces created with geometric shapes and gradients.


## Project Structure: 
- `main.py`: Core logic for the virtual gallery, including the recommendation engine and AI art generation.
- `app.py`: Flask web application for the user interface and API endpoints.
- templates/: Contains HTML templates (index.html, admin.html, 404.html, 500.html) for the web interface.
- `gallery_data.json`: Generated file storing gallery data (artworks and user profiles).

## Notes
- Image Quality: The generated images are basic abstract compositions using geometric shapes and gradients, as this is a first attempt at AI art generation. Future iterations could enhance image complexity.
- Session Management: The application uses Flask sessions to track user interactions. A demo user is created automatically on the first visit.
- Artsteps Export: The export feature generates a JSON file compatible with Artsteps for virtual gallery integration.
- Error Handling: Custom 404 and 500 error pages are included for a better user experience.


## Contributing
- Contributions are welcome! Please submit a pull request or open an issue for bug reports or feature suggestions.

## License
- This project is licensed under the MIT License.
