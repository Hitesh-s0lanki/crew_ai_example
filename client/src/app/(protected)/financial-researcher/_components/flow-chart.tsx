import React, { useCallback } from "react";
import {
  ReactFlow,
  addEdge,
  MiniMap,
  Controls,
  Background,
  Connection,
  type Node,
  type Edge,
  useNodesState,
  useEdgesState,
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";

const initialNodes: Node[] = [
  {
    id: "user",
    type: "input",
    data: { label: "You" },
    position: { x: 0, y: 200 },
  },
  {
    id: "writer",
    data: { label: "Expert Writer" },
    position: { x: 250, y: 100 },
    style: { border: "1px solid #222", borderRadius: 8, padding: 10 },
  },
  {
    id: "researcher",
    data: { label: "Expert Researcher" },
    position: { x: 250, y: 250 },
    style: { border: "1px solid #222", borderRadius: 8, padding: 10 },
  },
  {
    id: "engineer",
    data: { label: "Expert Engineer" },
    position: { x: 250, y: 400 },
    style: { border: "1px solid #222", borderRadius: 8, padding: 10 },
  },
  {
    id: "result",
    type: "output",
    data: { label: "Result" },
    position: { x: 600, y: 250 },
  },
];

const initialEdges: Edge[] = [
  { id: "e-wr", source: "writer", target: "researcher", type: "smoothstep" },
  { id: "e-re", source: "researcher", target: "engineer", type: "smoothstep" },
  { id: "e-ew", source: "engineer", target: "writer", type: "smoothstep" },
  { id: "e-ur", source: "user", target: "writer", animated: true },
  { id: "e-er", source: "engineer", target: "result", animated: true },
];

const AICrewFlow: React.FC = () => {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges]
  );

  return (
    <div style={{ height: "100%", width: "100%" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        attributionPosition="bottom-right">
        <MiniMap zoomable pannable />
        <Controls />
        <Background gap={16} />
      </ReactFlow>
    </div>
  );
};

export default AICrewFlow;
