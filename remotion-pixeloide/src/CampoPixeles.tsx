import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { PX, RGB } from "./marca";

const CELDA = 8 * PX; // celda de 8 px lógicos
const PASO = 10 * PX; // con 2 px lógicos de separación (igual que pixel_field_bg del motor)

type Props = {
  readonly focoX: number; // 0..1 del ancho
  readonly focoY: number; // 0..1 del alto
  readonly entradaSeg: number; // cuánto tarda en encenderse
};

// Campo de píxeles reactivo de la marca: se ilumina de Cyan (arriba) a Magenta (abajo) alrededor del foco.
export const CampoPixeles: React.FC<Props> = ({ focoX, focoY, entradaSeg }) => {
  const frame = useCurrentFrame();
  const { width, height, fps } = useVideoConfig();
  const t = frame / fps;
  const brillo = Math.min(1, t / Math.max(0.01, entradaSeg));
  const cols = Math.ceil(width / PASO);
  const filas = Math.ceil(height / PASO);
  const radio = Math.max(width, height) * 0.48;
  const cx = focoX * width;
  const cy = focoY * height;

  const celdas: React.ReactNode[] = [];
  for (let fy = 0; fy < filas; fy++) {
    for (let fx = 0; fx < cols; fx++) {
      const x = fx * PASO + (PASO - CELDA) / 2;
      const y = fy * PASO + (PASO - CELDA) / 2;
      const d = Math.hypot(x - cx, y - cy);
      const onda = Math.max(0, 1 - d / radio) ** 1.6;
      const pulso = 0.5 + 0.5 * Math.sin(d * 0.0125 - t * 3.5);
      const k = Math.min(1, onda * (0.72 + 0.28 * pulso) * brillo);
      const m = Math.min(1, Math.max(0, y / height));
      const canal = (i: 0 | 1 | 2, ganancia: number) =>
        Math.min(255, Math.round(RGB.fondo[i] + k * (RGB.cyan[i] * (1 - m) + RGB.magenta[i] * m - RGB.fondo[i]) * ganancia));
      celdas.push(
        <rect
          key={`${fx}-${fy}`}
          x={x}
          y={y}
          width={CELDA}
          height={CELDA}
          fill={`rgb(${canal(0, 0.65)},${canal(1, 0.55)},${canal(2, 0.75)})`}
        />,
      );
    }
  }

  return (
    <svg width={width} height={height} style={{ position: "absolute", left: 0, top: 0 }} shapeRendering="crispEdges">
      {celdas}
    </svg>
  );
};
