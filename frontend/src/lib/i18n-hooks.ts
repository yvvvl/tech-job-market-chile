import { useContext } from "react";

import { I18nCtx } from "./i18n-context";

export const useI18n = () => useContext(I18nCtx);
export const useT = () => useContext(I18nCtx).t;
