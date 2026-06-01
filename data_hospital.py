"""
data/magelang.py - Data Jaringan Jalan Magelang
=================================================
Berisi inisialisasi node (titik awal + RS) dan edge (jalan).
Bisa diganti dengan data kota lain (Surabaya, Jakarta, dll).
"""

from core import Node, Graph

def init_graph() -> Graph:
    """Inisialisasi graf jaringan jalan Magelang"""
    g = Graph()

    # === 8 TITIK AWAL (Landmark Kota Magelang) ===
    starts = [
        Node("A", "Alun-Alun Magelang", -7.4797, 110.2177, "start"),
        Node("B", "Taman Kyai Langgeng", -7.4856, 110.2224, "start"),
        Node("C", "Museum Pemuda", -7.4703, 110.2186, "start"),
        Node("D", "Pasar Rejowinangun", -7.4822, 110.2133, "start"),
        Node("E", "Stasiun Magelang", -7.4769, 110.2227, "start"),
        Node("F", "Terminal Kebonpolo", -7.4811, 110.2267, "start"),
        Node("G", "Taman Bunga", -7.4733, 110.2156, "start"),
        Node("H", "Kantor Pos Magelang", -7.4789, 110.2194, "start"),
    ]

    # === 13 RUMAH SAKIT ===
    hospitals = [
        Node("RS1", "Prof.Dr. Soerojo", -7.4708, 110.2183, "hospital"),
        Node("RS2", "Magelang Islamic", -7.4722, 110.2194, "hospital"),
        Node("RS3", "Dr.Soedjono Army", -7.4744, 110.2208, "hospital"),
        Node("RS4", "Tidar Regional", -7.4767, 110.2222, "hospital"),
        Node("RS5", "Lestari Raharja", -7.4783, 110.2233, "hospital"),
        Node("RS6", "Gladiool", -7.4797, 110.2247, "hospital"),
        Node("RS7", "Harapan Magelang", -7.4811, 110.2261, "hospital"),
        Node("RS8", "Budi Rahayu", -7.4825, 110.2275, "hospital"),
        Node("RS9", "Merah Putih", -7.4842, 110.2289, "hospital"),
        Node("RS10", "Muntilan Regional", -7.5803, 110.2936, "hospital"),
        Node("RS11", "Aisyiyah Muntilan", -7.5817, 110.2950, "hospital"),
        Node("RS12", "N-21 Gemilang", -7.5831, 110.2964, "hospital"),
        Node("RS13", "Padma Lalita", -7.5844, 110.2978, "hospital"),
    ]

    for n in starts + hospitals:
        g.add_node(n)

    # === 48 EDGE (Jalan Dua Arah) ===
    edges = [
        # Jaringan Titik Awal
        ("A","B",0.9),("A","C",0.7),("A","D",1.1),("A","H",0.5),
        ("B","E",0.8),("B","F",1.2),("B","H",0.6),
        ("C","D",1.3),("C","G",0.4),("C","H",0.8),
        ("D","G",1.5),("E","F",0.7),("E","H",0.4),
        ("F","G",1.8),("G","H",1.0),
        # Titik Awal ke RS
        ("A","RS1",0.8),("A","RS2",1.2),("A","RS3",1.5),("A","RS4",2.1),
        ("B","RS4",0.9),("B","RS5",1.3),("B","RS6",1.8),
        ("C","RS1",0.5),("C","RS2",0.7),
        ("D","RS3",1.1),("D","RS4",1.4),
        ("E","RS4",0.6),("E","RS5",0.9),("E","RS6",1.2),
        ("F","RS6",0.8),("F","RS7",1.1),("F","RS8",1.5),
        ("G","RS2",0.9),("G","RS3",1.2),
        ("H","RS4",0.7),("H","RS5",1.0),
        # Antar RS
        ("RS1","RS2",0.5),("RS2","RS3",0.6),("RS3","RS4",0.7),
        ("RS4","RS5",0.4),("RS5","RS6",0.5),("RS6","RS7",0.6),
        ("RS7","RS8",0.7),("RS8","RS9",0.8),
        # Ke Muntilan
        ("RS9","RS10",12.5),("RS10","RS11",0.8),
        ("RS11","RS12",0.9),("RS12","RS13",1.0),
    ]

    for f, t, w in edges:
        g.add_edge(f, t, w, True)

    return g
