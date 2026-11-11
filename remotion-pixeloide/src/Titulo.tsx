import React from "react";
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { CampoPixeles } from "./CampoPixeles";
import { CLAIM, COLOR, FUENTE_PIXEL, FUENTE_SILK, Idioma, PX, aPixel } from "./marca";

export type TituloProps = {
  readonly titulo: string;
  readonly subtitulo: string;
  readonly idioma: Idioma;
};

const fijo = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;

// Barrido Cyan de 520 ms con la curva de la marca (cubic-bezier(.76, 0, .24, 1)).
const Barrido: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: COLOR.cyan,
        translate: `${aPixel(interpolate(frame, [0, 0.52 * fps], [-width, width], { ...fijo, easing: Easing.bezier(0.76, 0, 0.24, 1) }))}px 0px`,
      }}
    />
  );
};

// Isotipo «Una P que es un play» exportado del motor (engine/outro.py → public/marca/isotipo.png).
const Isotipo: React.FC<{ readonly desde: number }> = ({ desde }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <Img
      src={staticFile("marca/isotipo.png")}
      style={{
        width: 64 * PX,
        height: 64 * PX,
        imageRendering: "pixelated",
        scale: interpolate(frame, [desde * fps, (desde + 0.45) * fps], [0, 1], { ...fijo, easing: Easing.bezier(0.34, 1.56, 0.64, 1) }),
      }}
    />
  );
};

// Texto que se tipea letra por letra; el resto queda invisible para que el bloque no salte de lugar.
const Tipeado: React.FC<{ readonly texto: string; readonly desde: number; readonly letrasPorSeg: number; readonly style: React.CSSProperties }> = ({
  texto,
  desde,
  letrasPorSeg,
  style,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = Math.max(0, Math.min(texto.length, Math.floor((frame / fps - desde) * letrasPorSeg)));
  return (
    <div style={style}>
      {texto.slice(0, n)}
      <span style={{ opacity: 0 }}>{texto.slice(n)}</span>
    </div>
  );
};

// Aparición con subida en saltos de píxel.
const Aparece: React.FC<{ readonly desde: number; readonly children: React.ReactNode }> = ({ desde, children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        opacity: interpolate(frame, [desde * fps, (desde + 0.3) * fps], [0, 1], fijo),
        translate: `0px ${aPixel(interpolate(frame, [desde * fps, (desde + 0.3) * fps], [6 * PX, 0], { ...fijo, easing: Easing.out(Easing.cubic) }))}px`,
      }}
    >
      {children}
    </div>
  );
};

const FundidoSalida: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#000000",
        opacity: interpolate(frame, [durationInFrames - 0.45 * fps, durationInFrames - 1], [0, 1], fijo),
      }}
    />
  );
};

const sombraPixel = `${PX}px ${PX}px 0 ${COLOR.tinta}`;

// Placa de título con la marca Pixeloide. Sirve en 16:9 y 9:16 (se adapta al tamaño de la composición).
export const PixeloideTitulo: React.FC<TituloProps> = ({ titulo, subtitulo, idioma }) => {
  const { width, height } = useVideoConfig();
  const vertical = height > width;
  const anchoTexto = vertical ? 240 * PX : 400 * PX;
  const letrasPorLinea = Math.floor(anchoTexto / (16 * PX));
  const grande = titulo.length <= letrasPorLinea * (vertical ? 3 : 2);
  const [a, b, c] = CLAIM[idioma];

  return (
    <AbsoluteFill style={{ backgroundColor: COLOR.ink }}>
      <CampoPixeles focoX={0.5} focoY={vertical ? 0.36 : 0.42} entradaSeg={1.2} />
      <AbsoluteFill
        style={{
          alignItems: "center",
          justifyContent: "center",
          flexDirection: "column",
          gap: 12 * PX,
          textAlign: "center",
        }}
      >
        <Isotipo desde={0.25} />
        <Tipeado
          texto={titulo.toUpperCase()}
          desde={0.6}
          letrasPorSeg={20}
          style={{
            fontFamily: FUENTE_PIXEL,
            fontSize: (grande ? 16 : 8) * PX,
            lineHeight: 1.5,
            color: COLOR.paper,
            maxWidth: anchoTexto,
            textShadow: sombraPixel,
          }}
        />
        <Aparece desde={1.7}>
          <div style={{ fontFamily: FUENTE_SILK, fontSize: 8 * PX, color: COLOR.cyan, maxWidth: anchoTexto, textShadow: sombraPixel }}>
            {subtitulo.toUpperCase()}
          </div>
        </Aparece>
        <Aparece desde={2.5}>
          <div style={{ fontFamily: FUENTE_PIXEL, fontSize: 8 * PX, marginTop: 6 * PX, textShadow: sombraPixel }}>
            <span style={{ color: COLOR.paper }}>{a} </span>
            <span style={{ color: COLOR.cyan }}>{b}</span>
            <span style={{ color: COLOR.magenta }}>{c}</span>
          </div>
        </Aparece>
      </AbsoluteFill>
      <Barrido />
      <FundidoSalida />
    </AbsoluteFill>
  );
};
