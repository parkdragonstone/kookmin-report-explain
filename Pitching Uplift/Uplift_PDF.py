from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from detecta import detect_peaks, detect_onset

class PDF(FPDF):
    def create_table(self, table_data, title='', data_size = 10, title_size=12, align_data='L', align_header='L', cell_width='even', x_start='x_default',emphasize_data=[], emphasize_style=None,emphasize_color=(0,0,0)): 
        """
        table_data: 
                    list of lists with first element being list of headers
        title: 
                    (Optional) title of table (optional)
        data_size: 
                    the font size of table data
        title_size: conda install -c conda-forge fpdf
                    the font size fo the title of the table
        align_data: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        align_header: 
                    align table data
                    L = left align
                    C = center align
                    R = right align
        cell_width: 
                    even: evenly distribute cell/column width
                    uneven: base cell size on lenght of cell/column items
                    int: int value for width of each cell/column
                    list of ints: list equal to number of columns with the widht of each cell / column
        x_start: 
                    where the left edge of table should start
                    'C' - center
        emphasize_data:  
                    which data elements are to be emphasized - pass as list 
                    emphasize_style: the font style you want emphaized data to take
                    emphasize_color: emphasize color (if other than black) 
        
        """
        default_style = self.font_style
        if emphasize_style == None:
            emphasize_style = default_style
        # default_font = self.font_family
        # default_size = self.font_size_pt
        # default_style = self.font_style
        # default_color = self.color # This does not work

        # Get Width of Columns
        def get_col_widths():
            col_width = cell_width
            if col_width == 'even':
                col_width = self.epw / len(data[0]) - 1  # distribute content evenly   # epw = effective page width (width of page not including margins)
            elif col_width == 'uneven':
                col_widths = []

                # searching through columns for largest sized cell (not rows but cols)
                for col in range(len(table_data[0])): # for every row
                    longest = 0 
                    for row in range(len(table_data)):
                        cell_value = str(table_data[row][col])
                        value_length = self.get_string_width(cell_value)
                        if value_length > longest:
                            longest = value_length
                    col_widths.append(longest + 4) # add 4 for padding
                col_width = col_widths



                        ### compare columns 

            elif isinstance(cell_width, list):
                col_width = cell_width  # TODO: convert all items in list to int        
            else:
                # TODO: Add try catch
                col_width = int(col_width)
            return col_width

        # Convert dict to lol
        # Why? because i built it with lol first and added dict func after
        # Is there performance differences?
        if isinstance(table_data, dict):
            header = [key for key in table_data]
            data = []
            for key in table_data:
                value = table_data[key]
                data.append(value)
            # need to zip so data is in correct format (first, second, third --> not first, first, first)
            data = [list(a) for a in zip(*data)]

        else:
            header = table_data[0]
            data = table_data[1:]

        line_height = self.font_size * 2.5

        col_width = get_col_widths()
        self.set_font(family='Arial', style='B', size=title_size)

        # Get starting position of x
        # Determin width of table to get x starting point for centred table
        if x_start == 'C':
            table_width = 0
            if isinstance(col_width, list):
                for width in col_width:
                    table_width += width
            else: # need to multiply cell width by number of cells to get table width 
                table_width = col_width * len(table_data[0])
            # Get x start by subtracting table width from pdf width and divide by 2 (margins)
            margin_width = self.w - table_width
            # TODO: Check if table_width is larger than pdf width

            center_table = margin_width / 2 # only want width of left margin not both
            x_start = center_table
            self.set_x(x_start)
        elif isinstance(x_start, int):
            self.set_x(x_start)
        elif x_start == 'x_default':
            x_start = self.set_x(self.l_margin)


        # TABLE CREATION #

        # add title
        if title != '':
            self.multi_cell(0, line_height, title, border=0, align='j', ln=3, max_line_height=self.font_size)
            self.ln(line_height)  # Move the cursor down by 3 units after multi_cell

        self.set_font(size=data_size)
        # add header
        y1 = self.get_y()
        if x_start:
            x_left = x_start
        else:
            x_left = self.get_x()
        x_right = self.epw + x_left
        if  not isinstance(col_width, list):
            if x_start:
                self.set_x(x_start)
            for datum in header:
                self.multi_cell(col_width, line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)

            for row in data:
                if x_start: # not sure if I need this
                    self.set_x(x_start)
                for datum in row:
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        
        else:
            if x_start:
                self.set_x(x_start)
            for i in range(len(header)):
                datum = header[i]
                self.multi_cell(col_width[i], line_height, datum, border=0, align=align_header, ln=3, max_line_height=self.font_size)
                x_right = self.get_x()
            self.ln(line_height) # move cursor back to the left margin
            y2 = self.get_y()
            self.line(x_left,y1,x_right,y1)
            self.line(x_left,y2,x_right,y2)


            for i in range(len(data)):
                if x_start:
                    self.set_x(x_start)
                row = data[i]
                for i in range(len(row)):
                    datum = row[i]
                    if not isinstance(datum, str):
                        datum = str(datum)
                    adjusted_col_width = col_width[i]
                    if datum in emphasize_data:
                        self.set_text_color(*emphasize_color)
                        self.set_font(style=emphasize_style)
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size)
                        self.set_text_color(0,0,0)
                        self.set_font(style=default_style)
                    else:
                        self.multi_cell(adjusted_col_width, line_height, datum, border=0, align=align_data, ln=3, max_line_height=self.font_size) # ln = 3 - move cursor to right with same vertical offset # this uses an object named self
                self.ln(line_height) # move cursor back to the left margin
        y3 = self.get_y()
        self.line(x_left,y3,x_right,y3)
        
class report_data():
    def high(data, cols, time, k_kh_time, k_fc_time, k_mer_time, k_br_time):
        hig = {
            'kh_time' : {},
            'fc_time' : {},
            'mer_time': {},
            'bc_time' : {},
            'max'     : {},
            'max_time': {},
            'min'     : {},
            'min_time': {}
            }
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            hig['kh_time'][col] = round(data[col][k_kh_time], 2)
            hig['fc_time'][col] = round(data[col][k_fc_time], 2)
            hig['mer_time'][col] = round(data[col][k_mer_time], 2)
            hig['bc_time'][col] = round(data[col][k_br_time], 2)
            hig['max'][col] = round(data[col].iloc[k_fc_time:k_br_time+1].max(), 2)
            hig['max_time'][col] = np.where(data[col] == data[col].iloc[k_fc_time:k_br_time+1].max())[0][0]
            hig['min'][col] = round(data[col].iloc[k_fc_time:k_br_time+1].min(), 2)
            hig['min_time'][col] = np.where(data[col] == data[col].iloc[k_fc_time:k_br_time+1].min())[0][0]
        
        m = data[cols.keys()].max().max()
        
        plt.ylabel('Distance [cm]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[k_kh_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_mer_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_br_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)
        plt.text(time[k_kh_time],y = m, s='Knee High',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_mer_time],y = m, s='Max SER',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_br_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='left')
        plt.legend()
        plt.tight_layout()
        plt.title('Distance')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/hig.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return hig

    def one_angle(data, cols, time, k_kh_time, k_fc_time, k_mer_time, k_br_time):
        ang = {
            'max'       : {},
            'max_frame' : {},
            'min'       : {},
            'min_frame' : {},
            'fc_time'   : {},
            'fp_time'   : {},
            'mer_time'  : {},
            'br_time'   : {},
            'fc_br'     : {},
            'fc_br_min'   : {},
            'fc_br_max'   : {},
            'kh_time'   : {},
            }
        
        for col in cols:
            
            df = data[col]
            if 'velcoity' in col:
                ylb = 'Angular Velocity [deg/s]'
            elif col == 'head_hand_distance':
                ylb = 'Distance [cm]'
            else:
                ylb = 'Angle [deg]'
                
            fig, ax = plt.subplots()
            plt.plot(time, np.array(df), color = 'firebrick')
            
            ang['kh_time'][col]   = round(df[k_kh_time], 2)
            ang['fc_time'][col]   = round(df[k_fc_time], 2)
            ang['mer_time'][col]  = round(df[k_mer_time], 2)
            ang['br_time'][col]   = round(df[k_br_time], 2)
            ang['max'][col]       = round(df.max(), 2)
            ang['max_frame'][col] = np.where(df == df.max())[0][0]
            ang['min'][col]       = round(df.min(), 2)
            ang['min_frame'][col] = np.where(df == df.min())[0][0]
            
            ang['fc_br'][col] = df[k_fc_time:k_br_time+1]
            ang['fc_br_max'][col] = np.where(df == ang['fc_br'][col].max())[0][0]
            ang['fc_br_min'][col] = np.where(df == ang['fc_br'][col].min())[0][0]
        
                        
            m = df.max()
            
            plt.ylabel(ylb)
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[k_fc_time]  ,color='k' ,linestyle = '--' ,alpha=0.5)
            plt.axvline(time[k_mer_time] ,color='k' ,linestyle = '--' ,alpha=0.5)
            plt.axvline(time[k_br_time]  ,color='k' ,linestyle = '--' ,alpha=0.5)

            plt.axhline(0,color='k',lw=0.9)
            
            plt.text(time[0]          ,y = m, s='Knee High'    ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_fc_time]  ,y = m, s='Foot Contact'   ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            #plt.text(time[k_fc_time]  ,y = m, s='Foot Plant'   ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_mer_time] ,y = m, s='MER'          ,rotation = 90, verticalalignment='top',horizontalalignment='left')
            plt.text(time[k_br_time]  ,y = m, s='Ball Release' ,rotation = 90, verticalalignment='top',horizontalalignment='left')

            plt.tight_layout()
            plt.title(f'{cols[col]}')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"figure/{cols[col]}.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        return ang
    
    def kinematic_sequence(data, ks_cols, time, k_fc_time, k_mer_time,k_br_time):
        ks = {
            'peak' : {},
            'time' : {},
            }
        fig, ax = plt.subplots()
        
        for col in ks_cols:
            plt.plot(time, np.array(data[col]), color = ks_cols[col][-1], label=ks_cols[col][0])
            ks['peak'][col] = round(data[col].max(), 2)
            ks['time'][col] = np.where(data[col] == data[col].max())[0][0]
            
            if col == 'lead_shoulder_external_rotation_velocity':
                ks['peak'][col] = round(data[col].iloc[k_fc_time:k_br_time+20].max(), 2)
                ks['time'][col] = np.where(data[col] == data[col].iloc[k_fc_time:k_br_time+60].max())[0][0]

            plt.axvline(time[ks['time'][col]], color = ks_cols[col][-1], linestyle ='-', alpha= 0.7)
            
        plt.ylabel('Angular Velocity [Deg/s]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[k_fc_time], color='k',linestyle = '--',alpha=0.5)
        #plt.axvline(time[k_fp_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_mer_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_br_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)
        plt.text(time[0]         ,y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Knee High' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_fc_time] ,y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Foot Contact' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        #plt.text(time[k_fp_time] ,y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Foot Plant' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_mer_time],y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='MER',rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_br_time] ,y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Ball Release' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.legend()
        plt.tight_layout()
        plt.title('KINEMATIC SEQUENCE')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/kinematic.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return ks
    
    def create_bullet_chart(nm, title, actual_value, min_value, target_value1, target_value2, max_value, unit=''):
        fig, ax = plt.subplots(figsize=(10, 0.8))
        ax.axis('off')

        if actual_value < min_value:
            min_value = actual_value
        elif actual_value > max_value:
            max_value = actual_value

        plt.barh(0, max_value, height=0.5, left=min_value, color='white')

        plt.fill_betweenx([-0.05, 0.05], min_value, max_value, color='dimgray', alpha=0.8)
        plt.fill_betweenx([-0.18, 0.18], target_value1, target_value2, color='crimson', alpha=0.5)

        plt.plot(actual_value, 0, marker=7, color='black', markersize=13)

        ax.text(actual_value, 0.4, f"{actual_value}{unit}", horizontalalignment='center', verticalalignment='bottom', fontsize=10)
        ax.text(target_value1, -0.3, f"{target_value1}{unit}", horizontalalignment='center', verticalalignment='top', fontsize=10)
        ax.text(target_value2, -0.3, f"{target_value2}{unit}", horizontalalignment='center', verticalalignment='top', fontsize=10)
        ax.text(0, 1, title, transform=ax.transAxes, horizontalalignment='left', verticalalignment='top', fontsize=12)

        plt.xlim(min_value, max_value)
        plt.ylim(-0.8, 0.5)
        
        plt.savefig(f'figure/bar/{nm}_bar.png')
        plt.close()
    
    '''
    def kinematic_sequence_comparison_radar_individual(df):
        # Define the data for each category, swapping 'Me' and '90+ mph Pitchers'
        categories = ['90+ mph Pitchers', 'Me', 'KBO', 'High School Pitchers']
        data = {
            'Pelvic': [840, df['PELVIS_ANGLUAR_VELOCITY_Z'].max(), 740, 596],
            'Torso': [1174, df['TORSO_ANGLUAR_VELOCITY_Z'].max(), 1068, 831],
            'Elbow': [2710, df['LEAD_ELBOW_ANGULAR_VELOCITY_X'].max(), 2710, 2327],
            'Shoulder': [4884, df['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), 5523, 6019]
        }

        # Define colors for each body part
        colors = {
            'Pelvic': 'red',
            'Torso': 'green',
            'Elbow': 'blue',
            'Shoulder': 'y'
        }

        # Create a radar chart for each body part
        for part, values in data.items():
            angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
            values = values + [values[0]]  # Complete the loop
            angles += angles[:1]

            fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
            ax.plot(angles, values, color=colors[part], linewidth=2, label=part)
            ax.fill(angles, values, color=colors[part], alpha=0.25)
            ax.set_xticks(angles[:-1])
            ax.set_xticklabels(categories)
            plt.title(f'{part} velo', fontsize=16, fontweight='bold')

            plt.legend(loc='upper right')
            plt.tight_layout()
            plt.savefig(f"figure/{part}_kinevelo.jpg")
            '''
            
    def kinematic_sequence_comparison_bar_individual(df):
        # Define the data for each category, swapping 'Me' and '90+ mph Pitchers'
        categories = ['Pro range', 'Me']
        data = {
            'Pelvic': [550, df['pelvis_rotational_velocity_with_respect_to_ground'].max()],
            'Torso': [800, df['trunk_rotational_velocity_with_respect_to_ground'].max()],
            'Elbow': [4500, df['lead_arm_rotational_velocity_with_respect_to_ground'].max()]
        }

        # Define colors for each body part
        colors = {
            'Pelvic': 'darkred',
            'Torso': 'darkgreen',
            'Elbow': 'royalblue'
        }
        
        # Number of categories
        n_categories = len(categories)

        # Bar width
        bar_width = 0.5  # Adjust this value for desired bar width
        fig_width = 6   # Adjust this value for desired figure width
        fig_height = 4   # Adjust this value for desired figure height

        # Create a bar chart for each body part
        for part, values in data.items():
            # Create a new figure with a narrower width
            fig, ax = plt.subplots(figsize=(fig_width, fig_height))

            # Calculate the bar positions
            bar_positions = np.arange(n_categories)

            # Plot bars for each category
            for i in range(n_categories):
                if categories[i] == 'Me':
                    # Emphasize the 'Me' bar
                    ax.bar(bar_positions[i], values[i], color=colors[part], width=bar_width, label=part if i == 0 else "", hatch='/')
                else:
                    # Regular bar for other categories
                    ax.bar(bar_positions[i], values[i], color=colors[part], width=bar_width, label=part if i == 0 else "")

            # Set the position and labels for x-ticks
            ax.set_xticks(bar_positions)
            ax.set_xticklabels(categories)

            # Adding labels and title
            plt.ylabel('Velocity (Deg/s)',fontsize=18)
            plt.title(f'{part} Angular Velocity Comparison', fontsize=18, fontweight='bold')

            plt.xticks(fontsize=14,rotation=25)
            plt.yticks(fontsize=14,rotation=25)
            
            plt.legend()
            plt.tight_layout()
            plt.savefig(f"figure/{part}_kinevelo.jpg")
            plt.close()