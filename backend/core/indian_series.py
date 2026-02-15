
# Static mapping for Indian Mobile Number Series
# Format: First 4 digits (excluding +91) -> State/Circle

INDIAN_SERIES_MAP = {
    # Rajasthan
    "8949": "Rajasthan",
    "9414": "Rajasthan",
    "9413": "Rajasthan",
    "9829": "Rajasthan",
    "9828": "Rajasthan",
    "9460": "Rajasthan",
    "9461": "Rajasthan",
    "9462": "Rajasthan",
    "9001": "Rajasthan",
    "9772": "Rajasthan",
    "9660": "Rajasthan",
    
    # Delhi
    "9810": "Delhi",
    "9818": "Delhi",
    "9871": "Delhi",
    "9873": "Delhi",
    "9811": "Delhi",
    "9899": "Delhi",
    
    # Mumbai
    "9820": "Mumbai",
    "9821": "Mumbai",
    "9833": "Mumbai",
    "9867": "Mumbai",
    
    # Maharashtra
    "9422": "Maharashtra",
    "9423": "Maharashtra",
    "9822": "Maharashtra",
    "9850": "Maharashtra",
    "9890": "Maharashtra",
    
    # UP East
    "9415": "UP East",
    "9450": "UP East",
    "9451": "UP East",
    "9452": "UP East",
    "9453": "UP East",
    "9454": "UP East",
    "9455": "UP East",
    
    # UP West
    "9412": "UP West",
    "9411": "UP West",
    "9837": "UP West",
    "9897": "UP West",
    
    # Andhra Pradesh / Telangana
    "9440": "Andhra Pradesh",
    "9441": "Andhra Pradesh",
    "9490": "Andhra Pradesh",
    "9491": "Andhra Pradesh",
    "9492": "Andhra Pradesh",
    "9493": "Andhra Pradesh",
    "9494": "Andhra Pradesh",
    "9154": "Andhra Pradesh", # User's first number
    
    # Tamil Nadu
    "9442": "Tamil Nadu",
    "9443": "Tamil Nadu",
    "9486": "Tamil Nadu",
    "9487": "Tamil Nadu",
    "9488": "Tamil Nadu",
    "9489": "Tamil Nadu",
    
    # Karnataka
    "9448": "Karnataka",
    "9449": "Karnataka",
    "9480": "Karnataka",
    "9481": "Karnataka",
    "9482": "Karnataka",
    "9483": "Karnataka",
    
    # Gujarat
    "9426": "Gujarat",
    "9427": "Gujarat",
    "9428": "Gujarat",
    "9429": "Gujarat",
    "9824": "Gujarat",
    "9825": "Gujarat",
    "9879": "Gujarat",
    
    # Punjab
    "9417": "Punjab",
    "9463": "Punjab",
    "9464": "Punjab",
    "9465": "Punjab",
    "9814": "Punjab",
    "9815": "Punjab",
    "9872": "Punjab",
    "9876": "Punjab",
    "9878": "Punjab"
}

def get_circle_from_series(number):
    # Expects formatted number string e.g. "9810012345" or "+919810..."
    clean = number.replace("+", "").strip()
    
    # Try with and without country code (Assuming 91 mainly)
    local_part = clean
    if clean.startswith("91") and len(clean) == 12:
        local_part = clean[2:]
        
    if len(local_part) < 4: return None
    
    prefix_4 = local_part[:4]
    
    return INDIAN_SERIES_MAP.get(prefix_4)
