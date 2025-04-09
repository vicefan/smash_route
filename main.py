import json
import heapq
import streamlit as st

# 데이터 로드
with open("./match_history/data.json", "r", encoding="utf-8") as f:
    match_dict = json.load(f)

winner = list(match_dict.keys())
all_players = sorted(list(set(list(match_dict.keys()) + [player for players in match_dict.values() for player in players])))

# 그래프 생성 함수
def build_win_graph(win_data):
    graph = {}
    for winner, losers in win_data.items():
        if winner not in graph:
            graph[winner] = set()
        for loser in losers:
            if loser not in graph:
                graph[loser] = set()  # 패배한 선수도 그래프에 추가
            graph[winner].add(loser)
    return graph

# 다익스트라 알고리즘으로 승리 경로 찾기
def find_win_path(graph, start, end):
    if start not in graph or end not in graph:
        return None

    priority_queue = [(0, start, [start])]
    visited = set()

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)

        if current_node in visited:
            continue
        visited.add(current_node)

        if current_node == end:
            return path

        for neighbor in graph[current_node]:
            if neighbor not in visited:
                heapq.heappush(priority_queue, (current_distance + 1, neighbor, path + [neighbor]))

    return None

def is_subsequence(query, name):
    query = query.lower()
    name = name.lower()
    i = 0
    for char in name:
        if i < len(query) and char == query[i]:
            i += 1
    return i == len(query)

# Streamlit UI
st.set_page_config(page_title="How to Smash", page_icon=":trophy:")
st.title(":trophy: Find the path to victory!")

# 그래프 생성
win_graph = build_win_graph(match_dict)

# 사용자 입력
cols = st.columns(2)
with cols[0]:
    start_player = st.selectbox("Select a fighter:", winner, key="start_list", index=None)
with cols[1]:
    end_player = st.selectbox("Select a fighter:", all_players, key="all_players", index=None)

# 경로 찾기 버튼
if st.button("Find Path"):
    if start_player and end_player and start_player != end_player:
        path = find_win_path(win_graph, start_player, end_player)
        if path:
            result = ' -> '.join(path)
            st.code(result, language="python", wrap_lines=True)
        else:
            st.error("No path found between the players.")
    else:
        st.warning("Please enter both the starting and target players.")