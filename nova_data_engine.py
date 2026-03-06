import requests
import pandas as pd
from datetime import datetime

class NovaDataEngine:
    def __init__(self):
        # Endpoints officiels du satellite GOES-16 via la NOAA
        self.XRAY_URL = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
        self.PROTON_URL = "https://services.swpc.noaa.gov/json/goes/primary/protons-1-day.json"

    def fetch_live_xray(self):
        """Récupère le flux de rayons X (Spectre Long 0.1-0.8nm)"""
        try:
            response = requests.get(self.XRAY_URL)
            data = response.json()
            # On filtre pour ne garder que le flux long (0.1-0.8nm)
            df = pd.DataFrame(data)
            df_long = df[df['energy'] == '0.1-0.8nm'].tail(1) 
            
            current_flux = df_long['flux'].values[0]
            timestamp = df_long['time_tag'].values[0]
            
            return {"flux": current_flux, "time": timestamp, "status": "SUCCESS"}
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

    def fetch_proton_density(self):
        """Récupère la densité de protons (>10 MeV)"""
        try:
            response = requests.get(self.PROTON_URL)
            data = response.json()
            df = pd.DataFrame(data)
            # On prend la dernière mesure d'énergie haute
            latest = df.tail(1)
            
            return {
                "proton_flux": latest['flux'].values[0],
                "energy_level": latest['energy'].values[0],
                "status": "SUCCESS"
            }
        except Exception as e:
            return {"status": "ERROR", "message": str(e)}

# --- TEST DU MOTEUR ---
if __name__ == "__main__":
    engine = NovaDataEngine()
    print("🛰️ Connexion au satellite GOES-16...")
    
    xray = engine.fetch_live_xray()
    if xray["status"] == "SUCCESS":
        print(f"✅ Flux X-Ray (0.1-0.8nm): {xray['flux']} W/m²")
    
    protons = engine.fetch_proton_density()
    if protons["status"] == "SUCCESS":
        print(f"✅ Flux Protons (>10 MeV): {protons['proton_flux']} pfu")