"use client";

import { useState } from "react";
import { useSearch } from "@/context/SearchContext";
import SuggestionsList from "./SuggestionList";
import SearchInput from "./SearchInput";
import { BatteryCharging, Settings, Navigation, Zap } from "lucide-react";
import axios from "axios";
import { stationsData } from "@/data/station";
import Vehicle from "@/interfaces/Vehicle";
import { LatLngExpression } from "leaflet";

export default function Sidebar({
  onRouteFound,
}: {
  onRouteFound: (route: LatLngExpression[] | null) => void;
}) {
  const {
    startPoint,
    endPoint,
    startCoords,
    endCoords,
    suggestions,
    activeInput,
    setStartPoint,
    setEndPoint,
    setActiveInput,
    setQuery,
  } = useSearch();

  const [vehicle, setVehicle] = useState<Vehicle>({
    batteryLevel: 80,
    maxRange: 300,
    safetyThreshold: 10,
    consumptionRate: 16.3,
    speed: 60,
    batteryCapacity: 75,
  });

  const [preference, setPreference] = useState("time");
  const [filters, setFilters] = useState<{
    avoidHighway?: boolean;
    avoidToll?: boolean;
  }>({});

  const [loading, setLoading] = useState(false);

  const handleSearchRoute = async () => {
    setLoading(true);
    try {
      const userInput = {
        start: [parseFloat(startCoords[0]), parseFloat(startCoords[1])],
        end: [parseFloat(endCoords[0]), parseFloat(endCoords[1])],
        vehicle,
        options: {
          preference: preference || null,
          ...(filters && Object.keys(filters).length > 0 ? { filters } : {}),
        },
        chargingStations: stationsData,
      };

      console.log("User Input:", userInput);

      const response = await axios.post(
        "http://localhost:8000/route",
        userInput,
        { headers: { "Content-Type": "application/json" } }
      );

      console.log("Route:", response.data);

      onRouteFound(response.data.path_geometry);
    } catch (err: any) {
      if (err.response) {
        console.error("Server responded with error:", err.response.status);
        console.error("Details:", err.response.data);
      } else {
        console.error("Request error:", err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full md:w-1/3 h-screen bg-white border-r border-gray-200 flex flex-col shadow-xl z-20">
      <div className="p-5 border-b border-gray-100 bg-blue-600 text-white">
        <h2 className="text-xl font-bold flex items-center gap-2">
          <Zap className="w-6 h-6 text-yellow-300" />
          Trạm sạc xe điện
        </h2>
        <p className="text-blue-100 text-sm mt-1">
          Tìm trạm sạc & Lộ trình tối ưu
        </p>
      </div>

      <div className="flex-1 overflow-y-auto p-5 space-y-6">
        {/* Lộ trình */}
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
            Lộ trình
          </h3>
          <div className="relative space-y-4">
            <div className="relative">
              <div className="pl-2 border-l-4 border-blue-500">
                <SearchInput
                  label="Điểm xuất phát"
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
                  placeholder="Nhập vị trí bắt đầu..."
                />
              </div>
              {activeInput === "start" && suggestions.length > 0 && (
                <div className="absolute top-full left-0 w-full z-50 mt-1">
                  <SuggestionsList />
                </div>
              )}
            </div>

            <div className="relative">
              <div className="pl-2 border-l-4 border-red-500">
                <SearchInput
                  label="Điểm đến"
                  value={endPoint}
                  onFocus={() => {
                    setActiveInput("end");
                    setQuery(endPoint);
                  }}
                  onChange={(e) => {
                    setEndPoint(e.target.value);
                    setActiveInput("end");
                    setQuery(e.target.value);
                  }}
                  placeholder="Nhập điểm đến..."
                />
              </div>
              {activeInput === "end" && suggestions.length > 0 && (
                <div className="absolute top-full left-0 w-full z-50 mt-1">
                  <SuggestionsList />
                </div>
              )}
            </div>
          </div>
        </section>

        <hr className="border-gray-100" />

        {/* Thông số xe điện */}
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
            <BatteryCharging className="w-4 h-4" />
            Thông số xe điện
          </h3>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Pin hiện tại (%)
              </label>
              <input
                type="number"
                value={vehicle.batteryLevel}
                onChange={(e) =>
                  setVehicle({
                    ...vehicle,
                    batteryLevel: Number(e.target.value),
                  })
                }
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                min={0}
                max={100}
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Max Range (km)
              </label>
              <input
                type="number"
                value={vehicle.maxRange}
                onChange={(e) =>
                  setVehicle({ ...vehicle, maxRange: Number(e.target.value) })
                }
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Mức tiêu thụ (kWh/100km)
              </label>
              <input
                type="number"
                value={vehicle.consumptionRate}
                onChange={(e) =>
                  setVehicle({
                    ...vehicle,
                    consumptionRate: Number(e.target.value),
                  })
                }
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Tốc độ trung bình (km/h)
              </label>
              <input
                type="number"
                value={vehicle.speed}
                onChange={(e) =>
                  setVehicle({ ...vehicle, speed: Number(e.target.value) })
                }
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                min={0}
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Dung lượng pin (kWh)
              </label>
              <input
                type="number"
                value={vehicle.batteryCapacity}
                onChange={(e) =>
                  setVehicle({
                    ...vehicle,
                    batteryCapacity: Number(e.target.value),
                  })
                }
                className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none text-sm"
                min={0}
              />
            </div>

            <div className="col-span-2">
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Ngưỡng an toàn (%)
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="range"
                  min={5}
                  max={30}
                  value={vehicle.safetyThreshold}
                  onChange={(e) =>
                    setVehicle({
                      ...vehicle,
                      safetyThreshold: Number(e.target.value),
                    })
                  }
                  className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
                />
                <span className="text-sm font-bold text-gray-600 w-8">
                  {vehicle.safetyThreshold}%
                </span>
              </div>
              <p className="text-[10px] text-gray-400 mt-1">
                Hệ thống sẽ tìm trạm sạc khi pin dưới mức này.
              </p>
            </div>
          </div>
        </section>

        <hr className="border-gray-100" />

        {/* Tùy chọn */}
        <section>
          <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-2">
            <Settings className="w-4 h-4" /> Tùy chọn
          </h3>

          <div className="space-y-3">
            <div>
              <label className="block text-xs font-medium text-gray-700 mb-1">
                Ưu tiên lộ trình
              </label>

              <select
                value={preference}
                onChange={(e) => setPreference(e.target.value)}
                className="w-full p-2 border rounded-lg bg-white text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              >
                <option value="time">Tổng thời gian ngắn nhất</option>
                <option value="distance">Quãng đường ngắn nhất</option>
                <option value="cost">Chi phí rẻ nhất</option>
              </select>
            </div>

            <div className="flex gap-4 mt-2">
              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.avoidHighway || false}
                  onChange={(e) =>
                    setFilters({ ...filters, avoidHighway: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600">Tránh cao tốc</span>
              </label>

              <label className="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={filters.avoidToll || false}
                  onChange={(e) =>
                    setFilters({ ...filters, avoidToll: e.target.checked })
                  }
                  className="w-4 h-4 text-blue-600 rounded focus:ring-blue-500"
                />
                <span className="text-sm text-gray-600">Tránh thu phí</span>
              </label>
            </div>
          </div>
        </section>
      </div>

      <div className="p-5 border-t border-gray-200 bg-gray-50">
        <button
          onClick={handleSearchRoute}
          disabled={loading}
          className={`w-full bg-blue-600 text-white font-semibold rounded-xl px-4 py-3 shadow-lg flex justify-center items-center gap-2 transition-all
            ${
              loading
                ? "opacity-60 cursor-not-allowed"
                : "hover:bg-blue-700 active:scale-95"
            }`}
        >
          {loading ? (
            <span>Đang tìm lộ trình...</span>
          ) : (
            <>
              <Navigation className="w-5 h-5" /> Tìm lộ trình tối ưu
            </>
          )}
        </button>
      </div>
    </div>
  );
}
