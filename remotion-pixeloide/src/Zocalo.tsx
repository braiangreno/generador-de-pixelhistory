import React from "react";
import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { COLOR, FUENTE_PIXEL, FUENTE_SILK, PX, aPixel, esquinasRecortadas } from "./marca";

export type ZocaloProps = {
  readonly nombre: string;
  readonly rol: string;
  readonly acento: "cyan" | "dorado";
};

const BORDE = {
  cyan: { luz: COLOR.cyan, sombra: "#188486" },
  dorado: { luz: COLOR.dorado, sombra: "#8C7449" },
} as const;

const fijo = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Zócalo (lower third) con la ventana RPG del motor: fondo transparente para usar encima de cualquier video.
// Exportarlo con alfa: ProRes 4444 (.mov) o secuencia PNG (ver README del agente).
export const PixeloideZocalo: React.FC<ZocaloProps> = ({ nombre, rol, acento }) => {
  const frame = useCurrentFrame();
  const { fps, width, height, durationInFrames } = useVideoConfig();
  const b = BORDE[acento];
  const entra = interpolate(frame, [0, 0.35 * fps], [-width * 0.6, 0], { ...fijo, easing: Easing.out(Easing.cubic) });
  const sale = interpolate(frame, [durationInFrames - 0.35 * fps, durationInFrames - 1], [0, -width * 0.6], {
    ...fijo,
    easing: Easing.in(Easing.cubic),
  });
  const letras = Math.max(0, Math.min(nombre.length, Math.floor((frame / fps - 0.3) * 24)));

  return (
    <AbsoluteFill>
      <div
        style={{
          position: "absolute",
          left: 16 * PX,
          top: height - 60 * PX,
          translate: `${aPixel(entra + sale)}px 0px`,
          padding: `${6 * PX}px ${10 * PX}px ${7 * PX}px`,
          minWidth: 200 * PX,
          backgroundImage: "linear-gradient(to bottom, #141834 0 25%, #181C38 25% 50%, #1C203C 50% 75%, #202440 75% 100%)",
          border: `${PX}px solid ${COLOR.tinta}`,
          boxShadow: `inset ${PX}px ${PX}px 0 0 ${b.luz}, inset -${PX}px -${PX}px 0 0 ${b.sombra}, inset ${2 * PX}px ${2 * PX}px 0 0 ${COLOR.ventanaLinea}`,
          clipPath: esquinasRecortadas,
        }}
      >
        <div style={{ fontFamily: FUENTE_PIXEL, fontSize: 8 * PX, color: COLOR.paper, lineHeight: 1.6 }}>
          {nombre.toUpperCase().slice(0, letras)}
          <span style={{ opacity: 0 }}>{nombre.toUpperCase().slice(letras)}</span>
        </div>
        <div
          style={{
            fontFamily: FUENTE_SILK,
            fontSize: 8 * PX,
            color: b.luz,
            marginTop: 2 * PX,
            opacity: interpolate(frame, [0.5 * fps, 0.8 * fps], [0, 1], fijo),
          }}
        >
          {rol.toUpperCase()}
        </div>
      </div>
    </AbsoluteFill>
  );
};
