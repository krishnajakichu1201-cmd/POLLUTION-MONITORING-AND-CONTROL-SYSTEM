import pandas as pd
import os

def clean_water_pollution(input_path, output_path):
    print(f"Cleaning {input_path}...")
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    # Fix header typo 'ear' -> 'Year'
    if lines[0].startswith('ear,'):
        lines[0] = 'Year,' + lines[0][4:]
    else:
        # If no header, add it
        header = "Year,Quarter,River,State,pH,DO(mg/L),BOD(mg/L),COD(mg/L),Turbidity(NTU),TDS(mg/L),Nitrates(mg/L),Phosphates(mg/L),Fecal_Coliform(MPN/100mL),Heavy_Metals(mg/L),Water_Quality_Class\n"
        lines.insert(0, header)
    
    with open(output_path, 'w') as f:
        f.writelines(lines)
    print(f"Saved to {output_path}")

def clean_soil_pollution(input_path, output_path):
    print(f"Cleaning {input_path}...")
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    cleaned_lines = []
    header = "Year,District,Land_Use,State,pH,EC(dS/m),Organic_Matter(%),Lead(mg/kg),Cadmium(mg/kg),Chromium(mg/kg),Arsenic(mg/kg),Mercury(mg/kg),Pesticide_Residue(mg/kg),Nitrogen(kg/ha),Phosphorus(kg/ha),Soil_Quality_Class\n"
    cleaned_lines.append(header)
    
    for i, line in enumerate(lines):
        parts = line.strip().split(',')
        
        # Row 1 fix (corrupted start)
        if i == 0 and parts[0] == 'kulam':
            parts = ['2022', 'Ernakulam'] + parts[1:]
            line = ','.join(parts) + '\n'
        
        # Row 8 fix (embedded header mess) - Drop it
        if (i == 7 and 'IYear' in line) or ('Year' in line and 'District' in line):
            print(f"Dropping corrupted header row or duplicate header at line {i+1}")
            continue
            
        # Row 13 fix (merged Ernandustrial)
        if i == 12 and parts[1] == 'Ernandustrial':
            parts = [parts[0], 'Ernakulam', 'Industrial'] + parts[2:]
            line = ','.join(parts) + '\n'
            
        cleaned_lines.append(line)
        
    with open(output_path, 'w') as f:
        f.writelines(cleaned_lines)
    print(f"Saved to {output_path}")

def main():
    data_dir = 'data'
    output_dir = 'outputs'
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Clean water pollution
    clean_water_pollution(os.path.join(data_dir, 'waterpollution.csv'), 
                          os.path.join(output_dir, 'waterpollution.csv'))
    
    # Clean soil pollution
    clean_soil_pollution(os.path.join(data_dir, 'soilpollution.csv'), 
                         os.path.join(output_dir, 'soilpollution.csv'))
    
    # Air pollution (just copy for now as it seems okay, or we could just leave it)
    import shutil
    shutil.copy2(os.path.join(data_dir, 'airpollution.csv'), 
                 os.path.join(output_dir, 'airpollution.csv'))
    print("Copied airpollution.csv to outputs")

if __name__ == "__main__":
    main()
