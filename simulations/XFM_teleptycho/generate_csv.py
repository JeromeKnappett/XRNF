import csv
import numpy as np
import usefulWavefield_old as UW
output_csv_file = '/user/home/opt/xl/xl/experiments/XFM_teleptycho/scan_positions_med_wballs.csv'
titles = ['name','fdir','op_pinhole_x','op_pinhole_y']

dx,dy = 9.905302137876412e-09, 9.907279315837693e-09

# Define scanning parameters
xmin = -2.08e-6   # Minimum x position
xmax = 2.08e-6    # Maximum x position
x_step =26*dx # Step size in x direction

ymin = -2.08e-6      # Minimum y position
ymax = 2.08e-6     # Maximum y position
y_step = 26*dy   # Step size in y direction

# Base file location path (modify as needed)
base_file_location = '/user/home/opt/xl/xl/experiments/XFM_teleptycho/medium_scan_wBalls/'

# Generate x and y positions
x_positions = np.arange(xmin, xmax + x_step, x_step)
y_positions = np.arange(ymin, ymax + y_step, y_step)
# print(x_positions)
print("Number of positions: ", len(x_positions)*len(y_positions))

# fig, ax = plt.subplots()   
# Open CSV file for writing
with open(output_csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header with additional columns
    writer.writerow(titles)#['x', 'y', 'file_location', 'position_name'])  

    # Generate scanning pattern
    for i,y in enumerate(y_positions):
        for ii,x in enumerate(x_positions):
            # Define file location and position name strings
            file_location = f"{base_file_location}pos_x{ii}_y{i}/"
            position_name = f"Position_x{ii}_y{i}"
            
            # if abs(x) < 9.0e-9:
            #     x = 0.0
            # else:
            #     x = UW.round_sig(x,3)            
            
            # if abs(y) < 9.0e-9:
            #     y = 0.0
            # else:
            #     y = UW.round_sig(y,3)      
            # Write row to CSV file
            writer.writerow([position_name, file_location, x, y,x,y])
            
            # ax.plot(x,y,':x')#,label='Sample positions')np.deg2rad(15))