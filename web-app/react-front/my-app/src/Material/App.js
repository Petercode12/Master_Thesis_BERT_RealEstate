import React, { useState, createContext, useContext } from "react";
import "./App.css";
import MainPage from "./Page/MainPage";
import en from "./lang/en";
export const langContext = createContext({});

function App() {
  const [lang, setLang] = useState(en);
  return (
    <langContext.Provider value={{ lang, setLang }}>
      <MainPage />
    </langContext.Provider>
  );
}

export default App;
