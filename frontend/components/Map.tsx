"use client";
import L from "leaflet";
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import { LatLngExpression } from "leaflet";
import { useEffect } from "react";
import { FaMapMarkerAlt } from "react-icons/fa";
import { renderToStaticMarkup } from "react-dom/server";
import MapInteraface from "../interfaces/Map";
const defaultPosition: LatLngExpression = [21.0285, 105.8542];

const markerIcon = L.divIcon({
  html: renderToStaticMarkup(<FaMapMarkerAlt size={32} color="red" />),
  className: "",
  iconSize: [32, 32],
});

const FlyToMarker = ({ coords }: { coords: LatLngExpression | null }) => {
  const map = useMap();
  useEffect(() => {
    if (coords) {
      map.flyTo(coords, 13, { duration: 1.5 });
    }
  }, [coords]);
  return null;
};

const Map = ({
  startCoords,
  endCoords,
  startPointName,
  endPointName,
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

      {startCoords && (
        <>
          <Marker position={startCoords} icon={markerIcon}>
            <Popup>Điểm đi: {startPointName}</Popup>
          </Marker>
          <FlyToMarker coords={startCoords} />
        </>
      )}

      {endCoords && (
        <>
          <Marker position={endCoords} icon={markerIcon}>
            <Popup>Điểm đến: {endPointName}</Popup>
          </Marker>
          <FlyToMarker coords={endCoords} />
        </>
      )}
    </MapContainer>
  );
};
export default Map;
