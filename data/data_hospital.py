from core import Node, Graph

def init_graph() -> Graph:
    """Inisialisasi graf jaringan jalan Magelang"""
    g = Graph()

    #TITIK AWAL
    starts = [
        Node("A", "Alun-Alun Magelang", -7.477033641653756, 110.21869229757661, "start"),
        Node("B", "Taman Kyai Langgeng", -7.484118219242825, 110.21052473647646, "start"),
        Node("C", "Museum Diponegoro", -7.473576264657655, 110.21294936618276, "start"),
        Node("D", "Pasar Rejowinangun", -7.485922919483384, 110.22200822113354, "start"),
        Node("E", "Stasiun Magelang", -7.464551782684127, 110.22256720949046, "start"),
        Node("F", "Terminal Kebonpolo", -7.4643000825374415, 110.22233679414762, "start"),
        Node("G", "Taman Tuguran", -7.457017800002813, 110.22198769690947, "start"),
        Node("H", "Kantor Pos Jagoan", -7.4843816499496185, 110.21221282046425, "start"),
    ]

    #RUMAH SAKIT -7.4787455,110.2161794
    hospitals = [
        Node("RS1", "Prof.Dr. Soerojo", -7.441166630599607, 110.22571678065435, "hospital"),
        Node("RS2", "Magelang Islamic", -7.450866214286509, 110.2217575216037, "hospital"),
        Node("RS3", "Dr.Soedjono Army", -7.467602035796992, 110.2260369788048, "hospital"),
        Node("RS4", "RSUD Tidar Magelang", -7.483892362135311, 110.21856645228941, "hospital"),
        Node("RS5", "Lestari Raharja", -7.4787112674583245, 110.21608753862849, "hospital"),
        Node("RS6", "Gladiool", -7.482476830087648, 110.21524285579063, "hospital"),
        Node("RS7", "Harapan Magelang", -7.486575245025097, 110.21183569414796, "hospital"),
        Node("RS8", "Budi Rahayu", -7.463237868300863, 110.22447956611462, "hospital"),
        Node("RS9", "Merah Putih", -7.535954113805623, 110.23414225182024, "hospital"),
        Node("RS10", "Muntilan Regional", -7.582780022157282, 110.29111648065685, "hospital"),
        Node("RS11", "Aisyiyah Muntilan", -7.584598383289827, 110.28518900764256, "hospital"),
        Node("RS12", "N-21 Gemilang", -7.571470286601765, 110.2593505518209, "hospital"),
        Node("RS13", "Padma Lalita", -7.587350859534551, 110.27765470764263, "hospital"),
    ]

    for n in starts + hospitals:
        g.add_node(n)

    #EDGE
    edges = [
        # Jaringan Titik Awal
        ("A","B",1.9),("A","C",0.75),("A","D",1.3),("A","H",2.4),
        ("B","E",3.6),("B","F",3.6),("B","H",0.7),
        ("C","D",2.1),("C","G",2.4),("C","H",2.0),
        ("D","G",4.2),("E","F",0.18),("E","H",3.8),
        ("F","G",0.8),("G","H",4.7),
        # Titik Awal ke RS
        ("A","RS1",5.0),("A","RS2",3.7),("A","RS3",3.1),("A","RS4",1.4),
        ("B","RS4",1.3),("B","RS5",1.3),("B","RS6",0.7),
        ("C","RS1",4.4),("C","RS2",3.2),
        ("D","RS3",3.2),("D","RS4",0.55),
        ("E","RS4",2.8),("E","RS5",3.0),("E","RS6",3.00),
        ("F","RS6",3.1),("F","RS7",3.4),("F","RS8",0.3),
        ("G","RS2",0.7),("G","RS3",1.5),
        ("H","RS4",1.0),("H","RS5",1.6),
        # Antar RS
        ("RS1","RS2",1.7),("RS2","RS3",2.1),("RS3","RS4",3.6),
        ("RS4","RS5",1.2),("RS5","RS6",0.55),("RS6","RS7",0.8),
        ("RS7","RS8",3.7),("RS8","RS9",8.9),
        # Ke Muntilan
        ("RS9","RS10",10.0),("RS10","RS11",0.8),
        ("RS11","RS12",3.8),("RS12","RS13",4.9),
    ]

    for f, t, w in edges:
        g.add_edge(f, t, w, True)

    return g
