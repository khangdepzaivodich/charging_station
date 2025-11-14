"use client";

import {
  createContext,
  useContext,
  useState,
  useCallback,
  useEffect,
} from "react";
import { LatLngExpression } from "leaflet";

const SearchContext = createContext<any>(null);

export function SearchProvider({ children }: { children: React.ReactNode }) {
  const [startPoint, setStartPoint] = useState("");
  const [endPoint, setEndPoint] = useState("");
  const [startCoords, setStartCoords] = useState<LatLngExpression | null>(null);
  const [endCoords, setEndCoords] = useState<LatLngExpression | null>(null);

  const [suggestions, setSuggestions] = useState<any[]>([]);
  const [activeInput, setActiveInput] = useState<"start" | "end" | null>(null);
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  // Fetch suggestions
  const fetchSuggestions = useCallback(
    async (text: string) => {
      if (text.trim().length < 1 || activeInput === null) {
        setSuggestions([]);
        return;
      }
      setIsSearching(true);

      try {
        const res = await fetch(
          `https://nominatim.openstreetmap.org/search?format=json&addressdetails=1&countrycodes=vn&limit=5&q=${encodeURIComponent(
            text
          )}`
        );
        const data = await res.json();
        setSuggestions(data);
      } finally {
        setIsSearching(false);
      }
    },
    [activeInput]
  );

  // Debounce search
  useEffect(() => {
    if (!query) {
      setSuggestions([]);
      return;
    }
    const timer = setTimeout(() => fetchSuggestions(query), 500);
    return () => clearTimeout(timer);
  }, [query, fetchSuggestions]);

  // Select suggestion
  const handleSelectSuggestion = (item: any) => {
    const coords: LatLngExpression = [
      parseFloat(item.lat),
      parseFloat(item.lon),
    ];

    if (activeInput === "start") {
      setStartPoint(item.display_name);
      setStartCoords(coords);
    }

    if (activeInput === "end") {
      setEndPoint(item.display_name);
      setEndCoords(coords);
    }

    setSuggestions([]);
    setActiveInput(null);
    setQuery(item.display_name);
  };

  return (
    <SearchContext.Provider
      value={{
        startPoint,
        endPoint,
        startCoords,
        endCoords,

        suggestions,
        activeInput,
        query,
        isSearching,

        setStartPoint,
        setEndPoint,
        setActiveInput,
        setQuery,

        fetchSuggestions,
        handleSelectSuggestion,
      }}
    >
      {children}
    </SearchContext.Provider>
  );
}

export const useSearch = () => useContext(SearchContext);
