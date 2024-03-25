# config for pc-3vrl06, cyclone X
server_address = ('169.254.28.129', 20000)
upld_jpg_path='/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/images/upload_image.jpg'
upld_jpg_default_path='/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/images/default/upload_image.jpg'
upld_jpg_error_path='/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/images/default/image_upload_jpeg_error.jpg'
output_jpg_path="/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/output_images/C_X/output.jpg"
prog_default='quartus_pgm -z -m JTAG -o "P;/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/edupow_default_cyc-10.sof"'
prog_file='quartus_pgm -z -m JTAG -o "P;/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/bit_file.sof"'
prog_invert='quartus_pgm -z -m JTAG -o "P;/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/edupow_invert_cyc-10.sof"'
prog_filter='quartus_pgm -z -m JTAG -o "P;/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/edupow_filter_cyc-10.sof"'
prog_edge='quartus_pgm -z -m JTAG -o "P;/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/edupow_lane_cyc-10.sof"'
prog_file_path="/home/vrlab/FPGA_Vision_Remote_Lab_experiment/Experiment_files/programs/C_X/bit_file.sof"
fpga_name="CX2"