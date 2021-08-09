import configparser

config = configparser.ConfigParser()
config.read('dependencies\\settings.ini')
temp_cmd_loc = config['DEFAULT']['temp_cmd_loc']
config_loc = config['DEFAULT']['config_loc']
targets_loc = config['DEFAULT']['targets_loc']
combobox_loc = config['DEFAULT']['combobox_loc']
logo_loc = config['DEFAULT']['logo_loc']
psexec_loc = config['DEFAULT']['psexec_loc']
buttonnext = config['DEFAULT']['buttonnext']
buttonclear = config['DEFAULT']['buttonclear']
buttonback = config['DEFAULT']['buttonback']
buttongo = config['DEFAULT']['buttongo']
logs = config['DEFAULT']['logs']
min_button_width = int(config['DEFAULT']['min_button_width'])
test_pings = int(config['DEFAULT']['test_pings'])
default_workers = int(config['DEFAULT']['default_workers'])
bg_one = config['DEFAULT']['bg_one']
fg_one = config['DEFAULT']['fg_one']
bg_two = config['DEFAULT']['bg_two']
fg_two = config['DEFAULT']['fg_two']
err_color = config['DEFAULT']['err_color']
suc_color = config['DEFAULT']['suc_color']
start_frame = config['DEFAULT']['start_frame']
width_perc = float(config['DEFAULT']['width_perc'])
height_perc = float(config['DEFAULT']['height_perc'])
min_width = int(config['DEFAULT']['min_width'])
min_height = int(config['DEFAULT']['min_height'])
max_output_length = int(config['DEFAULT']['max_output_length'])
max_output = int(config['DEFAULT']['max_output'])

install_state = None
installations = None
deletions = None
text = None
logger = None