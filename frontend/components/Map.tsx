"use client";
import L from "leaflet";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
  useMap,
} from "react-leaflet";
import { LatLngExpression } from "leaflet";
import { useEffect } from "react";
import { renderToStaticMarkup } from "react-dom/server";
import MapInteraface from "../interfaces/Map";
import { stationsData } from "../data/station";
import StationPopupInfo from "./StationPopupInfo";
import { HiLocationMarker, HiFlag } from "react-icons/hi";
import { MdEvStation } from "react-icons/md";

const defaultPosition: LatLngExpression = [10.762622, 106.660172];

// Icon riêng cho start
const startIcon = L.divIcon({
  html: renderToStaticMarkup(<HiLocationMarker size={36} color="#3b82f6" />),
  className: "custom-start-icon",
  iconSize: [36, 36],
  iconAnchor: [18, 36],
  popupAnchor: [0, -36],
});

// Icon riêng cho end
const endIcon = L.divIcon({
  html: renderToStaticMarkup(<HiFlag size={32} color="#ef4444" />),
  className: "custom-end-icon",
  iconSize: [32, 32],
  iconAnchor: [16, 32],
  popupAnchor: [0, -32],
});

// Icon trạm sạc
const stationIcon = L.divIcon({
  html: renderToStaticMarkup(<MdEvStation size={28} color="#22c55e" />),
  className: "custom-station-icon",
  iconSize: [30, 30],
  iconAnchor: [15, 30],
  popupAnchor: [0, -30],
});

const FlyToMarker = ({ coords }: { coords: LatLngExpression | null }) => {
  const map = useMap();
  useEffect(() => {
    if (coords) {
      map.flyTo(coords, 14, { duration: 1.5 });
    }
  }, [coords, map]);
  return null;
};

const FitBoundsToRoute = ({ route }: { route: LatLngExpression[] }) => {
  const map = useMap();
  useEffect(() => {
    if (route && route.length > 0) {
      const bounds = L.latLngBounds(route);
      map.fitBounds(bounds, { padding: [50, 50] });
    }
  }, [route, map]);
  return null;
};

const Map = ({
  startCoords,
  endCoords,
  startPointName,
  endPointName,
  path,
}: MapInteraface) => {
  return (
    <MapContainer
      center={defaultPosition}
      zoom={13}
      style={{ height: "100%", width: "100%" }}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {path && path.length > 0 && (
        <>
          <Polyline positions={path} color="blue" weight={4} opacity={0.7} />
          <FitBoundsToRoute route={path} />
        </>
      )}

      {startCoords && (
        <>
          <Marker position={startCoords} icon={startIcon}>
            <Popup>
              <div className="font-bold text-blue-600">Điểm đi:</div>{" "}
              {startPointName}
            </Popup>
          </Marker>
          <FlyToMarker coords={startCoords} />
        </>
      )}

      {endCoords && (
        <>
          <Marker position={endCoords} icon={endIcon}>
            <Popup>
              <div className="font-bold text-red-600">Điểm đến:</div>{" "}
              {endPointName}
            </Popup>
          </Marker>
          <FlyToMarker coords={endCoords} />
        </>
      )}

      {stationsData.map((station) => (
        <Marker
          key={station.id}
          position={[station.coords.lat, station.coords.lng]}
          icon={stationIcon}
        >
          <Popup maxWidth={300} minWidth={200}>
            <StationPopupInfo station={station} />
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
};

export default Map;
