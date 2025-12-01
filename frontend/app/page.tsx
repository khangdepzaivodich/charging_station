"use client";

import dynamic from "next/dynamic";
import { useMemo } from "react";
import { useSearch } from "@/context/SearchContext";
import Sidebar from "@/components/SideBar";
import { useState } from "react";
import Route from "@/interfaces/Route";
import { LatLngExpression } from "leaflet";
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
  const [route, setRoute] = useState<LatLngExpression[] | null>(null);

  return (
    <main className="flex flex-col md:flex-row h-screen">
      <Sidebar onRouteFound={setRoute} />
      <div className="flex-1 relative">
        <Map
          startCoords={startCoords}
          endCoords={endCoords}
          startPointName={startPoint}
          endPointName={endPoint}
          path={route}
        />
      </div>
    </main>
  );
}
