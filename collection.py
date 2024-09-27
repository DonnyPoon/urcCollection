import pandas as pd
import os

def collect_data():
    # Collect quantitative inputs for site
    site_data = {}
    site_data['Test Site'] = input("Enter site number: ")
    site_data['Depth Category'] = int(input("Enter depth category (1 - 0-2 inches, 2 - 2-4 inches, 3 - 4-6 inches): "))
    site_data['Compaction Depth'] = float(input("Enter compaction depth (inch): "))
    site_data['Temperature'] = float(input("Enter temperature (Celsius): "))
    site_data['Moisture'] = float(input("Enter moisture(1-dry, 2-normal, 3-moist): "))
    site_data['pH'] = float(input("Enter pH value: "))
    return site_data

def save_to_csv(data, filename):
    # Create a DataFrame from the data
    df = pd.DataFrame([data])
    
    # Check if the CSV file exists
    if os.path.exists(filename):
        # Append to the existing CSV file, no header, no indexing
        df.to_csv(filename, mode='a', header=False, index=False)
    else:
        # Create a new CSV file with headers
        df.to_csv(filename, index=False)

def main():
    while True: # can manually exit with ctrl+e or stop program for now
        filename = 'urc_soil_data.csv'
        data = collect_data()
        save_to_csv(data, filename)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
