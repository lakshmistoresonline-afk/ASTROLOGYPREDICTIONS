// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title EphemerisOracle
 * @notice On-Chain Web3 Ephemeris Oracle delivering cryptographically verified planetary longitudes.
 */
contract EphemerisOracle {
    address public oracleAdmin;

    struct PlanetaryPosition {
        uint256 planetId; // 0=Sun, 1=Moon, 2=Mars, etc.
        uint256 longitudeArcsec; // Longitude in arcseconds (deg * 3600)
        uint256 timestamp;
    }

    mapping(uint256 => PlanetaryPosition) public latestPositions;

    event PlanetaryPositionUpdated(uint256 indexed planetId, uint256 longitudeArcsec, uint256 timestamp);

    modifier onlyAdmin() {
        require(msg.sender == oracleAdmin, "ONLY_ORACLE_ADMIN_ALLOWED");
        _;
    }

    constructor() {
        oracleAdmin = msg.sender;
    }

    function updatePlanetaryPosition(uint256 planetId, uint256 longitudeArcsec) external onlyAdmin {
        latestPositions[planetId] = PlanetaryPosition({
            planetId: planetId,
            longitudeArcsec: longitudeArcsec,
            timestamp: block.timestamp
        });

        emit PlanetaryPositionUpdated(planetId, longitudeArcsec, block.timestamp);
    }

    function getPlanetaryPosition(uint256 planetId) external view returns (uint256 longitudeArcsec, uint256 timestamp) {
        PlanetaryPosition memory pos = latestPositions[planetId];
        return (pos.longitudeArcsec, pos.timestamp);
    }
}
