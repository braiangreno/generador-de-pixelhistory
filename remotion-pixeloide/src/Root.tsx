import React from "react";
import { Composition, Folder } from "remotion";
import { PixeloideTitulo } from "./Titulo";
import { PixeloideZocalo } from "./Zocalo";

// Composiciones de marca Pixeloide Studios. Se previsualizan con `npm run dev` (Remotion Studio)
// y se exportan con `npx remotion render <id> out/<archivo>.mp4 --props=...` (ver README del agente).
export const RemotionRoot: React.FC = () => {
  return (
    <Folder name="Pixeloide">
      <Composition
        id="PixeloideTitulo"
        component={PixeloideTitulo}
        durationInFrames={150}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ titulo: "La historia de Dune", subtitulo: "1957 - 2026 · Documental 16-bit", idioma: "es" as const }}
      />
      <Composition
        id="PixeloideTituloVertical"
        component={PixeloideTitulo}
        durationInFrames={150}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{ titulo: "La historia de Dune", subtitulo: "1957 - 2026 · Documental 16-bit", idioma: "es" as const }}
      />
      <Composition
        id="PixeloideZocalo"
        component={PixeloideZocalo}
        durationInFrames={120}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ nombre: "Frank Herbert", rol: "Periodista y novelista · 1957", acento: "cyan" as const }}
      />
    </Folder>
  );
};
