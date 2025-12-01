import ChargingStation from "@/interfaces/ChargingStation";

export const stationsData: ChargingStation[] = [
  {
    id: "vs-01",
    name: "VinFast 40 Chiến Lược",
    address: "40 Chiến Lược, P. Bình Trị Đông, Q. Bình Tân, TP. HCM",
    coords: { lat: 10.7625, lng: 106.6028 },
    chargingPorts: 20,
    maximumPower: 120,
    type: "DC/AC",
    pricePerKWh: 3858,
  },
  {
    id: "vs-02",
    name: "VinFast Aeon Mall Bình Tân",
    address: "Số 1 Đường Số 17A, P. Bình Trị Đông B, Q. Bình Tân",
    coords: { lat: 10.7431, lng: 106.6146 },
    chargingPorts: 10,
    maximumPower: 60,
    type: "DC",
    pricePerKWh: 3858,
  },
];
