"use client";

import { useSearch } from "@/context/SearchContext";
import SuggestionsList from "./SuggestionList";
import SearchInput from "./SearchInput";
export default function Sidebar() {
  const {
    startPoint,
    endPoint,
    suggestions,
    activeInput,
    query,
    isSearching,
    setStartPoint,
    setEndPoint,
    setActiveInput,
    setQuery,
    fetchSuggestions,
  } = useSearch();
  return (
    <div className="w-full md:w-1/3 bg-gray-50 p-6 overflow-y-auto shadow-md relative">
      <h2 className="text-2xl font-semibold mb-4 text-blue-600">
        Tìm trạm sạc xe điện
      </h2>

      <div className="relative mb-4">
        <SearchInput
          label="Điểm đi"
          value={startPoint}
          onFocus={() => {
            setActiveInput("start");
            setQuery(startPoint);
          }}
          onChange={(e) => {
            setStartPoint(e.target.value);
            setActiveInput("start");
            setQuery(e.target.value);
          }}
          placeholder="Ví dụ: Trường Đại học Sư phạm"
        />

        {activeInput === "start" && suggestions.length > 0 && (
          <SuggestionsList />
        )}
      </div>

      <div className="relative mb-4">
        <SearchInput
          label="Điểm đến"
          value={endPoint}
          onFocus={() => {
            setActiveInput("end");
            setQuery(startPoint);
          }}
          onChange={(e) => {
            setEndPoint(e.target.value);
            setActiveInput("end");
            setQuery(e.target.value);
          }}
          placeholder="Ví dụ: Trường Đại học Sư phạm"
        />

        {activeInput === "end" && suggestions.length > 0 && <SuggestionsList />}
      </div>

      <button
        onClick={() => fetchSuggestions(query)}
        disabled={isSearching}
        className="bg-blue-600 text-white rounded-lg px-4 py-2 mt-2 hover:bg-blue-700 disabled:opacity-50"
      >
        {isSearching ? "Đang tìm..." : "🔍 Tìm kiếm"}
      </button>
    </div>
  );
}
