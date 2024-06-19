from streamlit_react_flow import react_flow
import streamlit as st

st.title("React-Flow Test")

st.subheader("Friends Graph")


# nodes = [
#     {
#         'id': 'A',
#         'position': {'x': 100, 'y': 250},
#         'data': {'label': '<div><h3>标题A</h3><p>内容A</p></div>'}
#     },
#     {
#         'id': 'B',
#         'position': {'x': 100, 'y': 400},
#         'data': {'label': '<div><h3>标题B</h3><p>内容B</p></div>'}
#     },
#     {
#         'id': 'C',
#         'position': {'x': 300, 'y': 325},
#         'data': {'label': '<div><h3>标题C</h3><p>内容C</p></div>'}
#     },
#     {
#         'id': 'D',
#         'position': {'x': 500, 'y': 400},
#         'data': {'label': '<div><h3>标题D</h3><p>内容D</p></div>'}
#     },
#     {
#         'id': 'E',
#         'position': {'x': 700, 'y': 250},
#         'data': {'label': '<div><h3>标题E</h3><p>内容E</p></div>'}
#     },
#     {
#         'id': 'F',
#         'position': {'x': 500, 'y': 150},
#         'data': {'label': '<div><h3>标题F</h3><p>内容F</p></div>'}
#     },
# ]
#
# # 定义所有链接
# edges = [
#     { 'id': 'A-C', 'source': 'A', 'target': 'C' },
#     { 'id': 'B-C', 'source': 'B', 'target': 'C' },
#     { 'id': 'C-D', 'source': 'C', 'target': 'D' },
#     { 'id': 'B-D', 'source': 'B', 'target': 'D' },
#     { 'id': 'A-E', 'source': 'A', 'target': 'E' },
#     { 'id': 'D-E', 'source': 'D', 'target': 'E' },
#     { 'id': 'A-F', 'source': 'A', 'target': 'F' },
#     { 'id': 'C-F', 'source': 'C', 'target': 'F' },
# ]
#
# elements = nodes + edges

flowStyles = {"height": 500, "width": 1100, "background": "#f6f6f6"}

# Create an instance of our component with a constant `name` arg, and
# print its output value.
# react_flow("friends", elements=elements, flow_styles=flowStyles, mini_map=True)

plan = 'LogicalProject(monthh=[CAST(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0)))):INTEGER], yearr=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 12)):INTEGER])\n  LogicalTableScan(table=[[root, test]])\n'
plan = plan.strip(
    "\n")  # 'LogicalProject(ms=[*(CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 1000)):INTEGER, 1000000)], sec=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 1000)):INTEGER], minn=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 60000)):INTEGER], hr=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 3600000)):INTEGER], dayy=[CAST(/INT(Reinterpret(-(CAST($0):TIMESTAMP(0), CAST($1):TIMESTAMP(0))), 86400000)):INTEGER])\n  LogicalTableScan(table=[[root, test]])'
subplans = plan.split("\n")[::-1]
plan_elements = [{"id": f"{i}", "data": {"label": text}, "style": {"background": '#62c1f0', "width": 300, },
                  "position": {"x": 100, "y": 100 + i * 100}} for i, text in enumerate(subplans)]
plan_edges = [{"id": f"conn{i}_{1 + 1}", "source": i, "target": i + 1} for i in range(len(subplans) - 1)]
plan_elements.extend(plan_edges)
react_flow("dask-sql", elements=plan_elements, flow_styles=flowStyles)