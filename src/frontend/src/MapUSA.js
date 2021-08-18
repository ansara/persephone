import React, {useState} from 'react';
import { geoCentroid } from 'd3-geo';
import {
  ComposableMap,
  Geographies,
  Geography,
  Marker,
  Annotation,
  ZoomableGroup
} from "react-simple-maps";

import statesUSA from './data/states.json';

const geoUrl = 'https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json';

const wrapperStyles = {
  width: '100%',
  maxWidth: 980,
  margin: '0 auto'
};

const offsets = {
  VT: [50, -8],
  NH: [34, 2],
  MA: [30, -1],
  RI: [28, 2],
  CT: [35, 10],
  NJ: [34, 1],
  DE: [33, 0],
  MD: [47, 10],
  DC: [49, 21]
};

const selectColor = '#800020'

const fillStates = statesUSA.map(state => ({
  fill: '#DB7093',
  ...state
}));

function handleClick(stateSelected, activeGeo, geo) {
  if (stateSelected === true){
    if (geo.id === activeGeo){
      return [null, false];
    }
  }
  return [geo.id, true];
}
const MapUSA = () => {
  const [activeGeo, setActiveGeo] = useState("");
  var stateSelected = false;
  return (
    <ComposableMap projection="geoAlbersUsa">
      <Geographies geography={geoUrl}>
        {({ geographies }) => (
          <>
            {geographies.map(geo => {
              const cur = fillStates.find(s => s.val === geo.id);
              return (
                <Geography
                  key={geo.rsmKey}
                  geography={geo}
                  onClick={() => {
                    var values = handleClick(stateSelected, activeGeo ,geo);
                    stateSelected = values[1];
                    setActiveGeo(values[0]);
                  }}
                  onMouseEnter={() => {stateSelected === false ? setActiveGeo(geo.id): void 0}}
                  onMouseLeave={() => {stateSelected === false ? setActiveGeo(null): void 0}}

                  fill={geo.id === activeGeo  ? selectColor : cur.fill}
                  stroke="#FFFFFF"
                />
              );
            })}
            {geographies.map(geo => {
              const centroid = geoCentroid(geo);
              const cur = fillStates.find(s => s.val === geo.id);
              const textFill = '#000000';
              return (
                <g key={geo.rsmKey + "-name"}>
                  {cur &&
                    centroid[0] > -160 &&
                    centroid[0] < -67 &&
                    (Object.keys(offsets).indexOf(cur.id) === -1 ? (
                      <Marker coordinates={centroid}>
                        <text
                          y="2"
                          fontSize={14}
                          textAnchor="middle"
                          onClick={() => {
                            var values = handleClick(stateSelected, activeGeo ,geo);
                            stateSelected = values[1];
                            setActiveGeo(values[0]);
                          }}
                          onMouseEnter={() => {stateSelected === false ? setActiveGeo(geo.id): void 0}}
                          onMouseLeave={() => {stateSelected === false ? setActiveGeo(null): void 0}}
                          style={{ cursor: "pointer" }}
                          fill={geo.id === activeGeo ? "#FFFFFF" : textFill}
                        >
                          {cur.id}
                        </text>
                      </Marker>
                    ) : (
                      <Annotation
                        subject={centroid}
                        dx={offsets[cur.id][0]}
                        dy={offsets[cur.id][1]}
                      >
                        <text
                          x={4}
                          fontSize={14}
                          alignmentBaseline="middle"
                          onClick={() => {
                            var values = handleClick(stateSelected, activeGeo ,geo);
                            stateSelected = values[1];
                            setActiveGeo(values[0]);
                          }}
                          onMouseEnter={() => {stateSelected === false ? setActiveGeo(geo.id): void 0}}
                          onMouseLeave={() => {stateSelected === false ? setActiveGeo(null): void 0}}
                          style={{ cursor: "pointer" }}
                        >
                          {cur.id}
                        </text>
                      </Annotation>
                    ))}
                </g>
              );
            })}
          </>
        )}
      </Geographies>
    </ComposableMap>
  );
};

export default MapUSA;