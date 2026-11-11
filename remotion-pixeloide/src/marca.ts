import { loadFont } from "@remotion/fonts";
import { staticFile } from "remotion";

// Manual de marca Pixeloide Studios (mismos valores que engine/outro.py y engine/core.py del motor Python).
export const COLOR = {
  ink: "#070A1F",
  surface: "#0D1132",
  paper: "#F4F3EE",
  cyan: "#28DCE0",
  magenta: "#E732B6",
  muted: "#A5ACC4",
  borde: "#32385C",
  // paleta de las escenas del motor
  dorado: "#E9C27A",
  doradoOscuro: "#A87034",
  crema: "#F5F2EB",
  tinta: "#0E0C18",
  ventana: "#141834",
  ventanaLinea: "#3C4682",
} as const;

export const RGB = {
  cyan: [40, 220, 224],
  magenta: [231, 50, 182],
  fondo: [11, 15, 42],
} as const;

// 1 píxel del lienzo del motor (480x270) = 4 píxeles reales en 1920x1080.
// Todo lo que se mueve o se dibuja usa múltiplos de PX para que se vea pixel art de verdad.
export const PX = 4;
export const aPixel = (v: number) => Math.round(v / PX) * PX;

export const FUENTE_PIXEL = "PressStart2P";
export const FUENTE_SILK = "Silkscreen";

// loadFont usa delayRender: el render espera a que las fuentes estén cargadas.
loadFont({ family: FUENTE_PIXEL, url: staticFile("fonts/PressStart2P-Regular.ttf") });
loadFont({ family: FUENTE_SILK, url: staticFile("fonts/Silkscreen-Regular.ttf") });

export type Idioma = "es" | "en" | "pt";

// «JUGAMOS EN SERIO.»: JUGAMOS en Paper, EN SERIO en Cyan y el punto en Magenta.
export const CLAIM: Record<Idioma, readonly [string, string, string]> = {
  es: ["JUGAMOS", "EN SERIO", "."],
  en: ["WE PLAY", "SERIOUSLY", "."],
  pt: ["JOGAMOS", "A SÉRIO", "."],
};

// Esquinas recortadas de 1 píxel lógico, como las ventanas RPG del motor.
export const esquinasRecortadas = `polygon(${PX}px 0, calc(100% - ${PX}px) 0, calc(100% - ${PX}px) ${PX}px, 100% ${PX}px, 100% calc(100% - ${PX}px), calc(100% - ${PX}px) calc(100% - ${PX}px), calc(100% - ${PX}px) 100%, ${PX}px 100%, ${PX}px calc(100% - ${PX}px), 0 calc(100% - ${PX}px), 0 ${PX}px, ${PX}px ${PX}px)`;
