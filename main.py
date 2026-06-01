#!/usr/bin/env python3
"""Entry point - Jalankan server Flask"""

from app import app

if __name__ == '__main__':
    print("\n🏥 Sistem Rute RS Terdekat - Magelang")
    print("🌐 http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
