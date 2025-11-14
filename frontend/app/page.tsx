"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";
import { useSearch } from "@/context/SearchContext";
import Sidebar from "@/components/SideBar";

export default function Home() {
  const { startCoords, endCoords, startPoint, endPoint } = useSearch();
  const Map = useMemo(
    () =>
      dynamic(() => import("@/components/Map"), {
        ssr: false,
        loading: () => <p className="text-gray-500">Đang tải bản đồ...</p>,
      }),
    []
  );
  return (
    <main className="flex flex-col md:flex-row h-screen">
      <Sidebar />
      <div className="flex-1 relative">
        <Map
          startCoords={startCoords}
          endCoords={endCoords}
          startPointName={startPoint}
          endPointName={endPoint}
        />
      </div>
    </main>
  );
}
