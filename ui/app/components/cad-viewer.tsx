"use client";
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
  cadShapes?: any;
  stlFileUrl?: string;
}

export default function CadViewer({
  cadShapes = [],
  stlFileUrl,
}: CadViewerProps) {
  const ref = useRef(null);
  const { innerWidth: width, innerHeight: height } = window;

  const viewerOptions = {
    theme: "light",
    ortho: true,
    control: "trackball", // "orbit",
    normalLen: 0,
    cadWidth: width,
    height: height * 0.85,
    ticks: 10,
    ambientIntensity: 0.9,
    directIntensity: 0.12,
    transparent: false,
    blackEdges: false,
    axes: true,
    grid: [false, false, false],
    timeit: false,
    rotateSpeed: 1,
    tools: false,
    glass: false,
  };

  const renderOptions = {
    ambientIntensity: 1.0,
    directIntensity: 1.1,
    metalness: 0.3,
    roughness: 0.65,
    edgeColor: 0x707070,
    defaultOpacity: 0.5,
    normalLen: 0,
    up: "Z",
  };

  useEffect(() => {
    const container = ref.current;

    if (stlFileUrl) {
      const viewer = new Viewer(container, viewerOptions, nc);
      fetch(stlFileUrl)
        .then((response) => response.arrayBuffer())
        .then((data) => {
          const blob = new Blob([data], { type: "application/octet-stream" });
          const url = URL.createObjectURL(blob);
          viewer.clear();
          viewer.loadSTL(url);
          viewer.render();
        })
        .catch((error) => console.error(error));
    }
  }, [stlFileUrl]);

  useEffect(() => {
    const container = ref.current;

    if (cadShapes && cadShapes.length > 0) {
      const viewer = new Viewer(container, viewerOptions, nc);

      render("input", ...cadShapes);
      function render(name: string, shapes, states) {
        viewer?.clear();
        const [unselected, selected] = viewer.renderTessellatedShapes(
          shapes,
          states,
          renderOptions
        );
        console.log(unselected);
        console.log(selected);

        viewer.render(unselected, selected, states, renderOptions);
      }
    }
  }, [cadShapes]);

  return <div ref={ref} style={{ width: "100%", height: "100%" }}></div>;
}
