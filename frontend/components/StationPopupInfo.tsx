import ChargingStation from "@/interfaces/ChargingStation";
import { FaBolt } from "react-icons/fa";
const StationPopupInfo = ({ station }: { station: ChargingStation }) => {
  return (
    <div className="min-w-[220px] p-1 font-sans">
      <h3 className="text-base font-bold text-blue-700 m-0 mb-1">
        {station.name}
      </h3>
      <p className="text-xs text-gray-600 mb-2 italic">{station.address}</p>

      <div className="bg-gray-50 p-2 rounded border border-gray-200 text-sm">
        <div className="flex items-center justify-between mb-1">
          <span className="font-semibold text-gray-700">Công suất:</span>
          <span className="flex items-center text-orange-600 font-bold">
            <FaBolt className="mr-1" /> {station.maximumPower} kW
          </span>
        </div>
        <div className="flex items-center justify-between mb-1">
          <span className="font-semibold text-gray-700">Cổng sạc:</span>
          <span>
            {station.chargingPorts} ({station.type})
          </span>
        </div>
        <div className="flex items-center justify-between border-t pt-1 mt-1">
          <span className="font-semibold text-gray-700">Giá:</span>
          <span className="text-green-600 font-bold">
            {station.pricePerKWh.toLocaleString()} đ/kWh
          </span>
        </div>
      </div>

      <button
        className="w-full mt-2 bg-blue-600 text-white text-xs py-1.5 rounded hover:bg-blue-700 transition"
        onClick={() => alert(`Đã chọn trạm: ${station.name}`)}
      >
        Đặt trạm sạc này
      </button>
    </div>
  );
};
export default StationPopupInfo;
