from flask import Flask, render_template, jsonify, request
import requests
from core import DijkstraAlgorithm
from data import init_graph

app = Flask(__name__)

# Inisialisasi
print("⏳ Memuat data...")
graph = init_graph()
dijkstra = DijkstraAlgorithm()
total_edges = sum(len(e) for e in graph.adjacency_list.values()) // 2
print(f"✅ {len(graph.nodes)} node, {total_edges} edge")


def osrm_dist(lat1, lon1, lat2, lon2):
    """Jarak real-time via OSRM API"""
    url = f"http://router.project-osrm.org/route/v1/driving/{lon1},{lat1};{lon2},{lat2}?overview=false"
    try:
        r = requests.get(url, timeout=10).json()
        if 'routes' in r and r['routes']:
            return {
                'distance_km': round(r['routes'][0]['distance'] / 1000, 2),
                'duration_min': round(r['routes'][0]['duration'] / 60, 1),
                'status': 'success'
            }
    except Exception as e:
        print(f"OSRM Error: {e}")
    return {'distance_km': None, 'duration_min': None, 'status': 'error'}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/debug')
def debug():
    first = list(graph.nodes.values())[0]
    return jsonify({
        'status': 'ok',
        'nodes': len(graph.nodes),
        'edges': total_edges,
        'sample': {'id': first.id, 'name': first.name, 'type': first.node_type},
    })


@app.route('/api/nodes')
def get_nodes():
    return jsonify([{
        'id': n.id, 'name': n.name, 'type': n.node_type,
        'latitude': n.lat, 'longitude': n.lng
    } for n in graph.nodes.values()])


@app.route('/api/edges')
def get_edges():
    edges, seen = [], set()
    for fid, el in graph.adjacency_list.items():
        for e in el:
            tid = e.to_node.id
            k = tuple(sorted([fid, tid]))
            if k not in seen:
                seen.add(k)
                edges.append({'from_id': fid, 'to_id': tid, 'weight': e.weight})
    return jsonify(edges)


@app.route('/api/nearest-hospital')
def api_nearest():
    s = request.args.get('start')
    if not s or s not in graph.nodes:
        return jsonify({'error': 'Titik awal tidak valid'}), 400

    path, dist, rid = dijkstra.find_nearest_hospital(graph, s)
    if not path:
        return jsonify({'error': 'Tidak ada RS terjangkau'}), 404

    return jsonify({
        'path': [n.id for n in path],
        'path_details': [{'id': n.id, 'name': n.name, 'latitude': n.lat, 'longitude': n.lng, 'type': n.node_type} for n in path],
        'distance': dist,
        'hospital_id': rid,
        'hospital_name': graph.nodes[rid].name,
    })


@app.route('/api/shortest-path')
def api_path():
    s, e = request.args.get('start'), request.args.get('end')
    if not s or not e:
        return jsonify({'error': 'Pilih titik awal dan tujuan'}), 400
    if s not in graph.nodes or e not in graph.nodes:
        return jsonify({'error': 'ID tidak valid'}), 400

    path, dist = dijkstra.find_path(graph, s, e)
    if not path:
        return jsonify({'error': 'Jalur tidak ditemukan'}), 404

    return jsonify({
        'path': [n.id for n in path],
        'path_details': [{'id': n.id, 'name': n.name, 'latitude': n.lat, 'longitude': n.lng, 'type': n.node_type} for n in path],
        'distance': dist,
    })


@app.route('/api/compare-distances')
def api_compare():
    s = request.args.get('start')
    if not s or s not in graph.nodes:
        return jsonify({'error': 'Titik awal tidak valid'}), 400

    hs = graph.get_hospitals()
    res = []
    for h in hs:
        p, d = dijkstra.find_path(graph, s, h.id)
        if p:
            res.append({
                'rs_id': h.id, 'rs_name': h.name, 'distance': d,
                'path': [n.id for n in p],
                'path_details': [{'id': n.id, 'name': n.name, 'latitude': n.lat, 'longitude': n.lng, 'type': n.node_type} for n in p],
            })

    res.sort(key=lambda x: x['distance'])
    sn = graph.nodes[s]

    return jsonify({
        'start_id': s, 'start_name': sn.name,
        'start_lat': sn.lat, 'start_lng': sn.lng,
        'total_rs': len(res), 'results': res,
    })


@app.route('/api/osrm-distance')
def api_osrm():
    try:
        lat1 = float(request.args.get('lat1'))
        lon1 = float(request.args.get('lon1'))
        lat2 = float(request.args.get('lat2'))
        lon2 = float(request.args.get('lon2'))
    except (TypeError, ValueError):
        return jsonify({'error': 'Koordinat tidak valid'}), 400

    return jsonify(osrm_dist(lat1, lon1, lat2, lon2))


if __name__ == '__main__':
    print("\n🚀 http://localhost:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
