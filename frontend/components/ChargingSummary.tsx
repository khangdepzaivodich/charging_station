// ChargingSummary.tsx
"use client";

import { FC } from "react";
import {
  FaRoad,
  FaClock,
  FaBatteryHalf,
  FaMoneyBillWave,
  FaCarSide,
  FaExclamationTriangle,
} from "react-icons/fa";

interface Station {
  stop: number;
  station: string;
  kwh: number;
  time: number; // giờ
  cost: number; // vnđ
}

interface Summary {
  charge_count: number;
  estimated_time_hours: number;
  final_battery_pct: number;
  remaining_range_km: number;
  total_charging_time_hours: number;
  total_cost: number;
  total_distance_km: number;
}

interface ChargingSummaryProps {
  stations: Station[];
  summary?: Summary;
  feasible: boolean;
  message?: string;
}

const ChargingSummary: FC<ChargingSummaryProps> = ({
  stations,
  summary,
  feasible,
  message,
}) => {
  return (
    <div className="p-5 border-t border-gray-200 bg-white">
      <h3 className="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">
        Các trạm sạc đã đi qua
      </h3>

      {!feasible && message && (
        <div className="mb-3 p-3 bg-yellow-100 border border-yellow-300 rounded-lg flex items-center gap-2 text-sm text-yellow-800">
          <FaExclamationTriangle /> {message}
        </div>
      )}

      {stations.length === 0 ? (
        <p className="text-gray-400 text-sm">
          {feasible ? "Không có trạm sạc nào trong lộ trình" : ""}
        </p>
      ) : (
        <ul className="space-y-3 max-h-60 overflow-y-auto">
          {stations.map((st, idx) => (
            <li
              key={idx}
              className="p-3 bg-gray-50 rounded-lg shadow border border-gray-200"
            >
              <p className="font-semibold text-gray-700">
                Trạm {st.stop}: {st.station}
              </p>
              <p className="text-xs text-gray-600 mt-1">
                Năng lượng sạc: <b>{st.kwh} kWh</b>
              </p>
              <p className="text-xs text-gray-600">
                Thời gian sạc:{" "}
                <b>
                  {st.time >= 1
                    ? `${st.time.toFixed(2)} giờ`
                    : `${(st.time * 60).toFixed(2)} phút`}
                </b>
              </p>
              <p className="text-xs text-gray-600">
                Chi phí: <b>{st.cost.toLocaleString()} đ</b>
              </p>
            </li>
          ))}
        </ul>
      )}

      {summary && feasible && (
        <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded-lg text-sm text-gray-700 space-y-1">
          <p className="flex items-center gap-2">
            <FaRoad /> Tổng quãng đường:{" "}
            <b>{summary.total_distance_km.toFixed(2)} km</b>
          </p>

          <p className="flex items-center gap-2">
            <FaBatteryHalf /> Số lần sạc: <b>{summary.charge_count}</b>
          </p>
          <p className="flex items-center gap-2">
            <FaClock /> Tổng thời gian sạc:{" "}
            <b>
              {summary.total_charging_time_hours >= 1
                ? `${summary.total_charging_time_hours.toFixed(2)} giờ`
                : `${(summary.total_charging_time_hours * 60).toFixed(2)} phút`}
            </b>
          </p>
          <p className="flex items-center gap-2">
            <FaMoneyBillWave /> Tổng chi phí:{" "}
            <b>{summary.total_cost.toLocaleString()} đ</b>
          </p>
          <p className="flex items-center gap-2">
            <FaBatteryHalf /> Pin còn lại:{" "}
            <b>{summary.final_battery_pct.toFixed(1)}%</b>
          </p>
        </div>
      )}
    </div>
  );
};

export default ChargingSummary;
