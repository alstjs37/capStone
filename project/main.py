from flask import Flask, request, render_template, jsonify
import osmnx as ox
import networkx as nx
from _kafka.web_producer import Producer

app = Flask(__name__)

producer = Producer()

# 뉴욕시 그래프 다운로드
newYork_graph = ox.graph_from_place('New York City, New York, USA', network_type='drive')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/save_coordinates', methods=['POST'])
def save_coordinates():
    data = request.json
    start = data.get('start')
    end = data.get('end')

    # 좌표를 터미널에 출력
    print(f"Start coordinates: {start}")
    print(f"End coordinates: {end}")

    # 출발지와 도착지의 노드 찾기
    orig_node = ox.distance.nearest_nodes(newYork_graph, X=start['lng'], Y=start['lat'])
    dest_node = ox.distance.nearest_nodes(newYork_graph, X=end['lng'], Y=end['lat'])

    # 최단 경로 계산
    shortest_path = nx.shortest_path(newYork_graph, orig_node, dest_node, weight='length')
    shortest_path_length = nx.shortest_path_length(newYork_graph, orig_node, dest_node, weight='length')
    
    # producer 통해 K8s로 보냄
    producer.publish_to_kafka(shortest_path_length)

    # 최단 경로의 좌표 리스트 생성
    path_coordinates = []
    for node in shortest_path:
        point = newYork_graph.nodes[node]
        path_coordinates.append([point['y'], point['x']])

    # 최단 경로 길이 출력
    print(f"\n[SUCCESS] Shortest path length: {shortest_path_length} meters\n")

    return jsonify({'status': 'success', 'path': path_coordinates, 'length': shortest_path_length})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)