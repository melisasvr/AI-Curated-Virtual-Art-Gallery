#!/usr/bin/env python3
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
