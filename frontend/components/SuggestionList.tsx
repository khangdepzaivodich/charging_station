"use client";
import { useSearch } from "@/context/SearchContext";
export default function SuggestionsList() {
  const { suggestions, handleSelectSuggestion } = useSearch();

  if (!suggestions || suggestions.length === 0) return null;

  return (
    <ul className="absolute z-10 bg-white border border-gray-300 mt-1 rounded-lg shadow-md max-h-48 overflow-y-auto w-full">
      {suggestions.map((item: any, idx: number) => (
        <li
          key={idx}
          className="px-3 py-2 hover:bg-blue-100 cursor-pointer text-sm"
          onClick={() => handleSelectSuggestion(item)}
        >
          {item.display_name}
        </li>
      ))}
    </ul>
  );
}
