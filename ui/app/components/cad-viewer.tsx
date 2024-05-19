"use client";

import { useEffect, useRef } from 'react';
import "../../dist/three-cad-viewer/three-cad-viewer.css";
import { Viewer, Display } from "../../dist/three-cad-viewer/three-cad-viewer.esm.js";

function nc(change) {
  console.log("NOTIFY:", JSON.stringify(change, null, 2));
}

export interface CadViewerProps {
  cadShapes?: any;
  stlFileUrl?: string;
}

export default function CadViewer({ cadShapes = {}, stlFileUrl }: CadViewerProps) {
  const ref = useRef<HTMLDivElement>(null);
  const { innerWidth: width, innerHeight: height } = window;

  const viewerOptions = {
    theme: "light",
    ortho: true,
    control: "trackball",
    normalLen: 0,
    cadWidth: width,
    height: height * 0.85,
    treeWidth: 240,
    ticks: 10,
    ambientIntensity: 0.9,
    directIntensity: 0.12,
    transparent: false,
    blackEdges: false,
    axes: true,
    grid: [false, false, false],
    timeit: false,
    rotateSpeed: 1,
  };

  useEffect(() => {
    const container = ref.current;

    if (container && stlFileUrl) {
      const display = new Display(container, viewerOptions);
      const viewer = new Viewer(display, true, viewerOptions, nc);
      fetch(stlFileUrl)
        .then(response => response.arrayBuffer())
        .then(data => {
          const blob = new Blob([data], { type: 'application/octet-stream' });
          const url = URL.createObjectURL(blob);
          viewer.clear();
          viewer.addModelFromURL(url); // Ensure this is the correct method name
          viewer.render();
        })
        .catch(error => console.error(error));
    }
  }, [stlFileUrl]);

  useEffect(() => {
    const container = ref.current;

    if (container && cadShapes && Object.keys(cadShapes).length > 0) {
      const display = new Display(container, viewerOptions);
      const viewer = new Viewer(display, true, viewerOptions, nc);
      viewer.render(cadShapes, {});
    }
  }, [cadShapes]);

  return (
    <div ref={ref} style={{ width: '100%', height: '100%' }}></div>
  );
}
