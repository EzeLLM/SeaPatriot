import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')
def create_custom_map(lat, lon, address, status, from_location, to_location, direction, eta, last_report):
    # Create a new figure and axis with a specific projection
    fig, ax = plt.subplots(figsize=(12, 8), subplot_kw={'projection': ccrs.PlateCarree()})

    # Set the extent of the map (min_lon, max_lon, min_lat, max_lat)
    ax.set_extent([lon-2, lon+2, lat-2, lat+2], crs=ccrs.PlateCarree())

    # Add natural earth feature for a more detailed map
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='face', facecolor='lightgreen'))
    ax.add_feature(cfeature.NaturalEarthFeature('physical', 'ocean', '10m', edgecolor='face', facecolor='lightblue'))

    # Add coastlines and borders
    ax.add_feature(cfeature.COASTLINE, linewidth=0.5)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)

    # Plot the specific point with a prettier marker
    ax.plot(lon, lat, 'wo', markersize=14, transform=ccrs.PlateCarree(), zorder=5)  # White outer circle
    ax.plot(lon, lat, 'ro', markersize=10, transform=ccrs.PlateCarree(), zorder=6)  # Red inner circle

    arrow_length = 0.1  # in degrees
    dx = arrow_length * np.cos(np.radians(direction))
    dy = arrow_length * np.sin(np.radians(direction))
    ax.arrow(lon, lat, dx, dy, head_width=0.05, head_length=0.05, fc='blue', ec='blue', 
             transform=ccrs.PlateCarree(), zorder=7)

    info_text = f"Coordinates: {lat}°N, {lon}°E\nStatus: {status}\nFrom: {from_location}\nTo: {to_location}\nDirection: {direction}°\n{eta}\nLast Report: {last_report}"
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes, fontsize=10, verticalalignment='top', 
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

    plt.title(f"{address}", fontsize=16, fontweight='bold')

    ax.axis('off')

    plt.savefig('enhanced_map_with_direction.png', dpi=500, bbox_inches='tight')
    print("Enhanced map with direction has been created and saved as 'enhanced_map_with_direction.png'")

# Usage
if __name__ == '__main__':
    create_custom_map(
        lat=37.94802, 
        lon=23.59683, 
        address="Aegean Sea, East of Greece", 
        status="In Transit", 
        from_location="Port of Piraeus", 
        to_location="Port of Istanbul",
        direction=23,
        eta="2021-08-15 14:30 UTC",
        last_report="2021-08-15 10:00 UTC"
    )