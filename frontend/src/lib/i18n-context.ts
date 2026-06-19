import { createContext } from "react";

export type Lang = "en" | "es";
export type Dict = Record<string, string>;
export type Ctx = {
  lang: Lang;
  setLang: (l: Lang) => void;
  t: (k: string) => string;
};

export const I18nCtx = createContext<Ctx>({
  lang: "en",
  setLang: () => {},
  t: (k) => k,
});
