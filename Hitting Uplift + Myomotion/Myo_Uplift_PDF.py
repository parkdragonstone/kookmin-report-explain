from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np

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
        self.set_font(size=title_size)

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
            self.ln(line_height) # move cursor back to the left margin

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
    def one_force(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        sr = 1000
        
        rear = {
            'max_at_loading' : {},
            'to_time'        : {},
            'fc_time'        : {},
            'max_grf_time'   : {},
            'bc_time'        : {}
            }

        lead_tq = {
            'max'  : [],
            'time' : []
        }
        
        lead_z = {
            'fc_time' : [],
            'max'     : [],
            'fc-max_time' : [],
            'loading_rate' : []
        }
        rear_leg_y = {
            'max' : [],
            'max_timing' : [],
        }
        for col in cols:
            fig, ax = plt.subplots()
            plt.plot(time, np.array(data[col]),color = 'firebrick')    
            
            if col in ['rear_force_z','rear_moment_z']:
                rear['max_at_loading'][col] = round(data[col].iloc[to_time:fc_time].max(),2)
                loading_time = np.where(data[col] == data[col].iloc[to_time:fc_time].max())[0][0]
                rear['to_time'][col] = round(data[col][to_time], 2)
                rear['fc_time'][col] = round(data[col][fc_time], 2)
                rear['max_grf_time'][col] = round(data[col][max_grf_time], 2)
                rear['bc_time'][col] = round(data[col][bc_time], 2)
                plt.axvline(time[loading_time], color='firebrick',linestyle = '--',alpha=0.5)
                if col == 'rear_force_z':
                    yl = 'Force [% BW]'
                else:
                    yl = 'Moment [Nm]'
                    
            elif col in ['lead_moment_z']:
                lead_tq['max'] = round(data[col].min(), 2)
                lead_tq['time'] = np.where(data[col] == data[col].min())[0][0]
                plt.axvline(time[lead_tq['time']], color='firebrick',linestyle = '--',alpha=0.5)
                yl = 'Moment [Nm]'
                
            elif col in ['lead_force_z']:
                lead_z['fc_time'] = round(data[col][fc_time], 2)
                lead_z['max'] = round(data[col].max(), 2)
                max_time = np.where(data[col] == data[col].max())[0][0]
                lead_z['fc-max_time'] = (max_time - fc_time) / sr
                lead_z['loading_rate'] = round(( lead_z['max'] - lead_z['fc_time'] ) / lead_z['fc-max_time'], 2)
                plt.axvline(time[max_time], color='firebrick',linestyle = '--',alpha=0.5)
                yl = 'Force [% BW]'
            
            elif col in ['rear_force_x']:
                rear_leg_y['max'] = round(data[col].min(), 2)
                rear_leg_y['max_timing'] = np.where(data[col] == data[col].min())[0][0]
                plt.axvline(time[rear_leg_y['max_timing']], color='firebrick',linestyle = '--',alpha=0.5)
                yl = 'Force [% BW]'
                
            m = data[col].max()
            
            plt.ylabel(yl)
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[max_grf_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
            
            plt.axhline(0,color='k',lw=0.9)  
            plt.text(time[to_time],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='right')
            plt.text(time[fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='right')
            plt.text(time[max_grf_time],y = m, s='Max GRF',rotation = 90,verticalalignment='top',horizontalalignment='right')
            plt.text(time[bc_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='right')
            # plt.legend()
            plt.tight_layout()
            plt.title(f'{cols[col]}')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"figure/{col}.png", dpi=300, bbox_inches='tight')
            plt.close()
            
        return rear, lead_tq, lead_z, rear_leg_y
    def xfactor(data,col, time, to_time, fc_time, max_grf_time, bc_time):
        sr = 1000
        xf = {
                'to_time'  : {},
                'max_grf_time'  : {},
                'fc_time'  : {},
                'bc_time'  : {},
                'max'      : {},
                'max_time' : {},
                'min'      : {},
                'min_time' : {},
                }
        
        fig, ax = plt.subplots()
        plt.plot(time, np.array(data[col]), color = 'firebrick')
        xf['to_time'][col] = round(data[col][to_time], 2)
        xf['fc_time'][col] = round(data[col][fc_time], 2)
        xf['max_grf_time'][col] = round(data[col][max_grf_time], 2)
        xf['bc_time'][col] = round(data[col][bc_time], 2)
        xf['min'][col] = round(data[col].min(),2)
        xf['min_time'][col] = np.where(data[col] == data[col].min())[0][0]
        plt.axvline(time[xf['min_time'][col]], color='firebrick',linestyle = '--',alpha=0.5)
        m = data[col].max()
        
        plt.ylabel('Angle [Deg]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[max_grf_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)  
        plt.text(time[to_time],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[max_grf_time],y = m, s='Max GRF',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[bc_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='right')
        # plt.legend()
        plt.tight_layout()
        plt.title(f'X FACTOR')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/{col}.png", dpi=300, bbox_inches='tight')
        plt.close()
        return xf
    
    def grf_y(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        sr = 1000
        y = {
        'max'      : {},
        'lead_max'      : {},
        'x_axis_time' : []
        }
        max_time = data['peak_lead_grf_y'][0]
        fig, ax = plt.subplots()
        for col in cols:
            if col in 'lead_force_y':
                plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
                y['max'][col] = round(data[col].max(), 2)
                y['lead_max'][col] = round(data[col].max(),2)
                lead_max_time = np.where(data[col] == data[col].max())[0][0]
                plt.axvline(time[lead_max_time], color = 'firebrick', linestyle='--', alpha=0.5)
                plt.axvline(time[max_time],color = 'firebrick', linestyle='--', alpha=0.5)
                
            else:
                plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
                y['max'][col] = round(data[col].min())
                y['lead_max'][col] = round(data[col][max_time], 2)
                rear_max_time = np.where(data[col] == data[col].min())[0][0]
                y['x_axis_time'] = round(100 * ( y['lead_max'][col] / y['max'][col] ),2)
                plt.axvline(time[rear_max_time],color = 'firebrick', linestyle='--', alpha=0.5)

        
        m = data['lead_force_y'].max()  
        
        plt.ylabel('Force [% BW]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[max_grf_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)
        
        plt.text(time[to_time],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[max_grf_time],y = m, s='Max GRF',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[bc_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='right')
        plt.legend()
        plt.tight_layout()
        plt.title('GROUND REACTION FORCE (AP axis)')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/grf_ap.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return y
    def elbow_height(data, cols, time, to_time, kh_time, fc_time, bc_time):
        sr = 240
        arm = {
            'to_time' : {},
            'kh_time' : {},
            'fc_time' : {},
            'bc_time' : {},
            'max'     : {},
            'max_time': {},
            'min'     : {},
            'min_time': {}
            }
        off_set = data['rear_ankle_jc_3d_y'].min()
        fig, ax = plt.subplots()
        for col in cols:
            data[col] = data[col] - off_set
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            arm['to_time'][col] = round(data[col][to_time], 2)
            arm['kh_time'][col] = round(data[col][kh_time], 2)
            arm['fc_time'][col] = round(data[col][fc_time], 2)
            arm['bc_time'][col] = round(data[col][bc_time], 2)
            arm['max'][col] = round(data[col].iloc[fc_time:bc_time+1].max(), 2)
            arm['max_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].max())[0][0]
            arm['min'][col] = round(data[col].iloc[fc_time:bc_time+1].min(), 2)
            arm['min_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].min())[0][0]
        
        m = data[cols.keys()].max().max()
        
        plt.ylabel('Angle [Deg]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[kh_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
        
        # plt.axhline(0,color='k',lw=0.9)
        plt.text(time[to_time],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[kh_time],y = m, s='Knee High',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[bc_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='left')
        plt.legend()
        plt.tight_layout()
        plt.title('LEAD & REAR ELBOW HEIGHT')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/elbow_height.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return arm
    def lead_arm(data, cols, time, to_time, kh_time, fc_time, bc_time):
        sr = 240
        arm = {
            'to_time' : {},
            'kh_time' : {},
            'fc_time' : {},
            'bc_time' : {},
            'max'     : {},
            'max_time': {},
            'min'     : {},
            'min_time': {}
            }
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            arm['to_time'][col] = round(data[col][to_time], 2)
            arm['kh_time'][col] = round(data[col][kh_time], 2)
            arm['fc_time'][col] = round(data[col][fc_time], 2)
            arm['bc_time'][col] = round(data[col][bc_time], 2)
            arm['max'][col] = round(data[col].iloc[fc_time:bc_time+1].max(), 2)
            arm['max_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].max())[0][0]
            arm['min'][col] = round(data[col].iloc[fc_time:bc_time+1].min(), 2)
            arm['min_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].min())[0][0]
        
        m = data[cols.keys()].max().max()
        
        plt.ylabel('Angle [Deg]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[kh_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
        
        # plt.axhline(0,color='k',lw=0.9)
        plt.text(time[to_time],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[kh_time],y = m, s='Knee High',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[fc_time],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[bc_time], y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='left')
        plt.legend()
        plt.tight_layout()
        plt.title('LEAD SHOULDER ROTATION & ELBOW FLEXION')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/Lead Arm.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return arm
    
    
    def one_angle(data, cols, time, to_time, kh_time, fc_time, bc_time,uplift_pel_initial_time):
        ang = {
            'to_time'  : {},
            'kh_time'  : {},
            'fc_time'  : {},
            'bc_time'  : {},
            'max'      : {},
            'max_time' : {},
            'min'      : {},
            'min_time' : {},
        }
        
        for col in cols:
            fig, ax = plt.subplots()
            plt.plot(time, np.array(data[col]),color = 'firebrick')
            ang['to_time'][col] = round(data[col][to_time], 2)
            ang['kh_time'][col] = round(data[col][kh_time], 2)
            ang['fc_time'][col] = round(data[col][fc_time], 2)
            ang['bc_time'][col] = round(data[col][bc_time], 2)
            ang['max'][col] = round(data[col].iloc[fc_time:bc_time+1].max(),2)
            ang['min'][col] = round(data[col].iloc[fc_time:bc_time+1].min(),2)
            ang['max_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].max())[0][0]
            ang['min_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time+1].min())[0][0]
            
            if col in ['pelvis_rotational_velocity_with_respect_to_ground']:
                ang['max'][col] = round(data[col].max(), 2)
                ang['max_time'][col] = np.where(data[col] == data[col].max())[0][0]
                plt.axvline(time[uplift_pel_initial_time], color = 'firebrick', linestyle = '--',alpha=0.7)
                
            if col in ['lead_knee_extension']:
                ang['max'][col] = round(data[col].max(),2)
                ang['max_time'][col] = np.where(data[col] == data[col].max())[0][0]
            
            if col in ['rear_shoulder_adduction']:
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
                
            if col in ['trunk_lateral_flexion']:
                ang['max'][col] = round(data[col].max(),2)
                ang['max_time'][col] = np.where(data[col] == data[col].max())[0][0]
                plt.axvline(time[ang['max_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if col in ['trunk_twist_clockwise']:
                ang['min'][col] = round(data[col].min(),2)
                ang['min_time'][col] = np.where(data[col] == data[col].min())[0][0]  
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if col in ['lead_knee_extension_velocity', 'lead_hip_flexion_with_respect_to_trunk','lead_elbow_flexion']:
                plt.axvline(time[ang['max_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if col in ['shank_angle']:
                ang['min'][col] = round(data[col].iloc[to_time:fc_time].min(),2)
                ang['min_time'][col] = np.where(data[col] == data[col].iloc[to_time:fc_time+1].min())[0][0]
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if col in ['hand_shoulder_distance']:
                ang['min'][col] = round(data[col].min(),2)
                ang['min_time'][col] = np.where(data[col] == data[col].min())[0][0]
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
                
            if col in ['hip_elbow_loss_space']:
                ang['min'][col] = round(data[col].iloc[:bc_time].min(),2)
                ang['min_time'][col] = np.where(data[col] == data[col].iloc[:bc_time].min())[0][0]
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if col in ['shoulder_hand_loss_space']:
                ang['min'][col] = round(data[col].iloc[fc_time:bc_time].min(),2)
                ang['min_time'][col] = np.where(data[col] == data[col].iloc[fc_time:bc_time].min())[0][0]
                plt.axvline(time[ang['min_time'][col]], color = 'firebrick', linestyle = '--',alpha=0.7)
            
            if 'velocity' in col:
                ylb = 'Angular Velocity [deg/s]'
            elif col in ['hip_elbow_loss_space','shoulder_hand_loss_space','hand_shoulder_distance']:
                ylb = 'Distance [m]'
            else:
                ylb = 'Angle [deg]'
                
            m = data[col].max()
            
            plt.ylabel(ylb)
            plt.xlabel('Time [s]')
            plt.autoscale(axis='x', tight=True)
            plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[kh_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
            plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
            
            # plt.axhline(0,color='k',lw=0.9)  
            plt.text(time[to_time+1],y = m, s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='left')
            plt.text(time[kh_time+1],y = m, s='Knee High',rotation = 90,verticalalignment='top',horizontalalignment='left')
            plt.text(time[fc_time+1],y = m, s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='left')
            plt.text(time[bc_time+1],y = m,s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='left')
            # plt.legend()
            plt.tight_layout()
            plt.title(f'{cols[col]}')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"figure/{cols[col]}.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        return ang
    
    def kinematic_sequence(data, cols, time, to, kh, fc, bc):
        ks = {
            'max' : {},
            'time' : {},
        }
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]), color = cols[col][-1],label=cols[col][0])
            ks['max'][col] = round(data[col].iloc[:bc].max(),2)
            ks['time'][col] = np.where(data[col] ==data[col].iloc[:bc].max())[0][0]
            plt.axvline(time[ks['time'][col]], color = cols[col][-1], linestyle = '--',alpha=0.7)

        plt.ylabel('Angular Velocity [Deg/s]')
        plt.xlabel('TIME [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[kh], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc], color='k',linestyle = '--',alpha=0.5)
        
        # plt.axhline(0,color='k',lw=0.9)        
        
        plt.text(time[to+1],y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[kh+1],y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Knee High',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[fc+1],y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='left')
        plt.text(time[bc+1],y = data['lead_arm_rotational_velocity_with_respect_to_ground'].max(), s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='left')
        plt.title(f"KINEMATIC SEQUENCE")
        
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.tight_layout()
        plt.legend()
        plt.savefig(f"figure/KINEMATIC SEQUENCE.png", dpi=300, bbox_inches="tight")
        plt.close()
        
        return ks