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
        title_size: 
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
    def grf(data, cols, time, kh_time, fc_time, mer_time, br_time, f_rear_peak_z_time, f_lead_peak_z_time,f_rear_peak_y_time,f_lead_min_y_time, axis):
        if axis == 'ap':
            title = 'GROUND REACTION FORCE (AP-AXIS)'
        else:
            title = 'GROUND REACTION FORCE (Vertical)'
        y = {
            'max'       : {},
            'max_frame' : {},
            'min'       : {},
            'min_frame' : {},
            'kh_time'   : {},
            'fc_time'   : {},
            'mer_time'  : {},
            'br_time'   : {},
            }
        
        fig, ax = plt.subplots()
        for col in cols:
            df = data[col]
            plt.plot(time, np.array(df), color = cols[col][-1], label = cols[col][0])
            
            y['kh_time'][col]   = round(df[kh_time], 2)
            y['fc_time'][col]   = round(df[fc_time], 2)
            y['mer_time'][col]  = round(df[mer_time], 2)
            y['br_time'][col]   = round(df[br_time], 2)
            y['max'][col]       = round(df.max(), 2)
            y['max_frame'][col] = np.where(df == df.max())[0][0]
            y['min'][col]       = round(df.min(), 2)
            y['min_frame'][col] = np.where(df == df.min())[0][0]
            
        if axis == 'vt':
            plt.axvline(time[f_rear_peak_z_time], color = cols['REAR_FORCE_Z'][-1], linestyle ='--',alpha = 0.7)
            if col in ['LEAD_FORCE_Z']:
                plt.axvline(time[f_lead_peak_z_time], color = cols['LEAD_FORCE_Z'][-1], linestyle ='--',alpha = 0.7)
                y['max'][col]       = round(df[fc_time:br_time].max(), 2)
                y['max_frame'][col] = np.where(df == df[fc_time:br_time].max())[0][0]
                plt.axvline(time[y['max_frame'][col]], color = cols['LEAD_FORCE_Z'][-1], linestyle ='--',alpha = 0.7)

        if axis == 'ap':
            plt.axvline(time[f_rear_peak_y_time], color = cols['REAR_FORCE_Y'][-1], linestyle ='--',alpha = 0.7)
            if col in ['LEAD_FORCE_Y']:
                plt.axvline(time[f_lead_min_y_time], color = cols['LEAD_FORCE_Y'][-1], linestyle ='--',alpha = 0.7)
            

        m = data[cols.keys()].max().max()    
        
        plt.ylabel('Force [% BW]')
        plt.xlabel('Time [s]')

        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[fc_time]  ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[mer_time] ,color='k' ,linestyle = '--' ,alpha=0.5)
        plt.axvline(time[br_time]  ,color='k' ,linestyle = '--' ,alpha=0.5)

        plt.axhline(0,color='k',lw=0.9)
        
        plt.text(time[0]        ,y = m, s='Knee High'    ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[fc_time]  ,y = m, s='Foot Contact' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[mer_time] ,y = m, s='MER'          ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[br_time]  ,y = m, s='Ball Release' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.legend()
        plt.tight_layout()
        plt.title(title)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/grf_{axis}.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return y

    def one_angle(data, cols, time, k_kh_time, k_fc_time, k_mer_time, k_br_time):
        ang = {
            'max'       : {},
            'max_frame' : {},
            'min'       : {},
            'min_frame' : {},
            'kh_time'   : {},
            'fc_time'   : {},
            'fp_time'   : {},
            'mer_time'  : {},
            'br_time'   : {},
            }
        
        for col in cols:
            
            df = data[col]
            if 'VELOCITY' in col:
                ylb = 'Angular Velocity [deg/s]'
            else:
                ylb = 'Angle [deg]'
                
            fig, ax = plt.subplots()
            plt.plot(time, np.array(df), color = 'firebrick')

            ang['kh_time'][col]   = round(df[k_kh_time], 2)
            ang['fc_time'][col]   = round(df[k_fc_time], 2)
            #ang['fp_time'][col]   = round(df[k_fp_time], 2)
            ang['mer_time'][col]  = round(df[k_mer_time], 2)
            ang['br_time'][col]   = round(df[k_br_time], 2)
            ang['max'][col]       = round(df.max(), 2)
            ang['max_frame'][col] = np.where(df == df.max())[0][0]
            ang['min'][col]       = round(df.min(), 2)
            ang['min_frame'][col] = np.where(df == df.min())[0][0]
        
            
            if col in ['TORSO_PELVIS_ANGLE_Z','LEAD_SHOULDER_ANGLE_X']:
                plt.axvline(time[np.where(df == df.min())[0][0]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            elif col in ['TORSO_ANGLE_Y','LEAD_ELBOW_ANGLE_X','LEAD_SHOULDER_ANGLE_Y','LEAD_SHOULDER_ANGLE_Z','LEAD_KNEE_ANGULAR_VELOCITY_X']:
                ang['max'][col]  = round(df[k_fc_time-40:k_br_time+15].max(), 2)
                ang['max_frame'][col] = np.where(df == df[k_fc_time-40:k_br_time+15].max())[0][0]
                plt.axvline(time[ang['max_frame'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)       

            elif col in ['LEAD_KNEE_ANGLE_X']:
                ang['max'][col]  = round(df[k_fc_time:k_br_time+1].max(), 2)
                ang['max_frame'][col] = np.where(df == df[k_fc_time:k_br_time+1].max())[0][0]
                plt.axvline(time[ang['max_frame'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
                
                        
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

            if col == 'LEAD_SHOULDER_ANGULAR_VELOCITY_Z':
                ks['peak'][col] = round(data[col].iloc[k_fc_time:k_br_time+20].max(), 2)
                ks['time'][col] = np.where(data[col] == data[col].iloc[k_fc_time:k_br_time+20].max())[0][0]

            
            plt.axvline(time[ks['time'][col]], color = ks_cols[col][-1], linestyle ='-', alpha= 0.7)
                
        plt.ylabel('Angular Velocity [Deg/s]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[k_fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_mer_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[k_br_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)
        plt.text(time[0]         ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Knee High' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        # plt.text(time[k_fc_time] ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='FC' ,rotation = 90, verticalalignment='top',horizontalalignment='right')
        plt.text(time[k_fc_time] ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Foot Contact' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_mer_time],y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='MER',rotation = 90, verticalalignment='top',horizontalalignment='left')
        plt.text(time[k_br_time] ,y = data['LEAD_SHOULDER_ANGULAR_VELOCITY_Z'].max(), s='Ball Release' ,rotation = 90, verticalalignment='top',horizontalalignment='left')
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
        fig, ax = plt.subplots(figsize=(10, 0.6))
        ax.axis('off')

        if actual_value < min_value:
            min_value = actual_value
        elif actual_value > max_value:
            max_value = actual_value

        plt.barh(0, max_value, height=0.05, left=min_value, color='white')

        plt.fill_betweenx([-0.05, 0.05], min_value, max_value, color='dimgray', alpha=0.8)
        plt.fill_betweenx([-0.18, 0.18], target_value1, target_value2, color='crimson', alpha=0.5)

        plt.plot(actual_value, 0, marker=7, color='black', markersize=8)

        ax.text(actual_value, 0.2, f"{actual_value}{unit}", horizontalalignment='center', verticalalignment='bottom', fontsize=9)
        ax.text(target_value1, -0.3, f"{target_value1}{unit}", horizontalalignment='center', verticalalignment='top', fontsize=9)
        ax.text(target_value2, -0.3, f"{target_value2}{unit}", horizontalalignment='center', verticalalignment='top', fontsize=9)
        ax.text(0, 0.5, title, transform=ax.transAxes, horizontalalignment='left', verticalalignment='top', fontsize=9)

        plt.xlim(min_value, max_value)
        plt.ylim(-0.8, 0.5)
        
        plt.savefig(f'figure/bar/{nm}_bar.png')
        plt.close()
