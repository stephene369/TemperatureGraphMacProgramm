from hobo import HoboCSVReader

def read_hobo_file(file_path):
    """
    Read a HOBO data file using the hobo library
    
    Args:
        file_path (str): Path to the HOBO data file (CSV format)
        
    Returns:
        list: List of data records from the HOBO file
    """
    data_records = []
    
    with HoboCSVReader(file_path) as reader:
        print('Reading %s ...' % reader.fname)
        print('Serial Number: %s  Title: %s' % (reader.sn, reader.title))
        
        # Collect all data records
        for record in reader:
            data_records.append(record)
            
        # Print summary
        print(f"Read {len(data_records)} records from {file_path}")
        
        # Print first few records as example
        if data_records:
            print("\nSample data (first 5 records):")
            for i, (timestamp, temperature, rh, battery) in enumerate(data_records[:5]):
                print('%s   %03.1f F   %02.1f %%   %.1f V' % (timestamp, temperature, rh, battery))
    
    return data_records




read_hobo_file(r"C:\Users\steph\Documents\Project\temperatureProgramm\21027238 Nord 2023-09-07 11_42_55 CET (Data CET).hobo")




if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter the path to your HOBO data file (.csv): ")
    
    try:
        data = read_hobo_file(file_path)
        
        # Example of how to work with the data
        if data:
            # Calculate average temperature
            avg_temp = sum(record[1] for record in data) / len(data)
            # print(f"\nAverage temperature: {avg_temp:.1f} F")
            
            # Find min and max temperature
            min_temp = min(record[1] for record in data)
            max_temp = max(record[1] for record in data)
            # print(f"Temperature range: {min_temp:.1f} F to {max_temp:.1f} F")
            
            # Calculate average humidity
            avg_rh = sum(record[2] for record in data) / len(data)
            # print(f"Average relative humidity: {avg_rh:.1f} %")
    except Exception as e:
        print(f"Error: {e}")
