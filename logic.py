import sqlite3
import matplotlib
matplotlib.use('Agg')  # Pencere açmadan grafik kaydetmek için
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature  # Kıyılar, sınırlar vs için
import io

class DB_Map():
    def __init__(self, database):
        self.database = database  # Veri tabanı dosya yolu

    # -----------------------------
    # Kullanıcı tabloları
    # -----------------------------
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    # -----------------------------
    # Şehir ekleme / seçme
    # -----------------------------
    def add_city(self, user_id, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                              FROM users_cities  
                              JOIN cities ON users_cities.city_id = cities.id
                              WHERE users_cities.user_id = ?''', (user_id,))
            cities = [row[0] for row in cursor.fetchall()]
            return cities

    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                              FROM cities  
                              WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    # -----------------------------
    # Harita oluşturma
    # -----------------------------
    def create_graph(self, path, cities, marker_color='red'):
        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())

        # Kara, okyanus, dağlar, nehirler ve göller
        ax.add_feature(cfeature.LAND, facecolor='lightgreen')
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        ax.add_feature(cfeature.LAKES, facecolor='blue', alpha=0.5)
        ax.add_feature(cfeature.RIVERS)
        ax.add_feature(cfeature.MOUNTAINS, facecolor='brown', alpha=0.3)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')

        for city in cities:
            coords = self.get_coordinates(city)
            if coords:
                lat, lng = coords
                ax.plot(lng, lat, 'o', color=marker_color, markersize=10, transform=ccrs.Geodetic())
                ax.text(lng + 0.3, lat + 0.3, city, transform=ccrs.Geodetic(), fontsize=9)

        plt.savefig(path)
        plt.close()

    # -----------------------------
    # Mesafeyi çizme
    # -----------------------------
    def draw_distance(self, city1, city2):
        coords1 = self.get_coordinates(city1)
        coords2 = self.get_coordinates(city2)

        if not coords1 or not coords2:
            print("❌ Şehir bulunamadı.")
            return

        lat1, lng1 = coords1
        lat2, lng2 = coords2

        fig = plt.figure(figsize=(10, 6))
        ax = plt.axes(projection=ccrs.PlateCarree())

        ax.add_feature(cfeature.LAND, facecolor='lightgreen')
        ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
        ax.add_feature(cfeature.LAKES, facecolor='blue', alpha=0.5)
        ax.add_feature(cfeature.RIVERS)
        ax.add_feature(cfeature.MOUNTAINS, facecolor='brown', alpha=0.3)
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')

        ax.plot([lng1, lng2], [lat1, lat2], color='blue', linewidth=2, marker='o', transform=ccrs.Geodetic())
        ax.text(lng1 + 0.3, lat1 + 0.3, city1, transform=ccrs.Geodetic(), fontsize=9)
        ax.text(lng2 + 0.3, lat2 + 0.3, city2, transform=ccrs.Geodetic(), fontsize=9)

        plt.savefig("distance_map.png")
        plt.close()
        print("✅ distance_map.png dosyası oluşturuldu.")

# -----------------------------
# Harita tamponu oluşturmak (bot noktaları için)
# -----------------------------
def harita_olustur(points=[], marker_color='red'):
    fig = plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())

    # Kara, okyanus, dağlar, nehirler ve göller
    ax.add_feature(cfeature.LAND, facecolor='lightgreen')
    ax.add_feature(cfeature.OCEAN, facecolor='lightblue')
    ax.add_feature(cfeature.LAKES, facecolor='blue', alpha=0.5)
    ax.add_feature(cfeature.RIVERS)
    ax.add_feature(cfeature.MOUNTAINS, facecolor='brown', alpha=0.3)
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    for lat, lon in points:
        ax.plot(lon, lat, 'o', color=marker_color, markersize=10, transform=ccrs.Geodetic())

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf

# -----------------------------
# Ana kontrol
# -----------------------------
if __name__ == "__main__":
    m = DB_Map("database.db")
    m.create_user_table()
