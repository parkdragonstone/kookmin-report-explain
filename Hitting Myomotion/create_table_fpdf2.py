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
    def grf_y(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        y = {
        'max'      : {},
        'lead_max'      : {},
        'x_axis_time' : []
        }
        sr = 1000
        max_time = data['peak_lead_grf_y'][0]
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            if col in 'lead_force_y':
                y['max'][col] = round(data[col][max_time], 2)
                y['lead_max'][col] = round(data[col][max_time],2)
                plt.axvline(time[max_time],color = 'firebrick', linestyle='--', alpha=0.5)
            else:
                y['max'][col] = round(data[col].max())
                y['lead_max'][col] = round(data[col][max_time], 2)
                rear_max_time = np.where(data[col] == data[col].max())[0][0]
                y['x_axis_time'] = round(100 * ( y['lead_max'][col] / y['max'][col] ),2)
                plt.axvline(time[rear_max_time],color = 'firebrick', linestyle='--', alpha=0.5)

        
        m = data[cols.keys()].max().max()    
        
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

    def one_angle(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        ang = {
            'to_time'      : {},
            'fc_time'      : {},
            'max_grf_time' : {},
            'bc_time'      : {}
            }
        xf = {
            'peak'  : [],
            'time'  : []
        }
        
        for col in cols:
            fig, ax = plt.subplots()
            plt.plot(time, np.array(data[col]),color = 'firebrick')
            ang['to_time'][col] = round(data[col][to_time], 2)
            ang['fc_time'][col] = round(data[col][fc_time], 2)
            ang['max_grf_time'][col] = round(data[col][max_grf_time], 2)
            ang['bc_time'][col] = round(data[col][bc_time], 2)

            if col in 'x_factor':
                xf['peak'] = round(data[col].min(), 2)
                xf['time'] = np.where(data[col] == data[col].min())[0][0]
                plt.axvline(time[xf['time']], color='firebrick',linestyle = '--',alpha=0.5)
                
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
            plt.title(f'{cols[col]}')
            ax.spines['right'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)
            ax.grid(axis='y')
            plt.savefig(f"figure/{col}.png", dpi=300, bbox_inches='tight')
            plt.close()
        
        return ang, xf
    
    def kinematic_sequence(data, ks_cols, time, to_time, fc_time, max_grf_time, bc_time,peak_hand_time):
        ks = {
            'peak' : {},
            'time' : {},
            }
        fig, ax = plt.subplots()
        for col in ks_cols:
            if col not in 'forearm_angular_velo':
                plt.plot(time, np.array(data[col]),color = ks_cols[col][-1],label=ks_cols[col][0])
                ks['peak'][col] = round(data[col].max(), 2)
                ks['time'][col] = np.where(data[col] == data[col].max())[0][0]
                plt.axvline(time[ks['time'][col]], color = ks_cols[col][-1], linestyle ='--', alpha= 0.7)
            else:
                plt.plot(time, np.array(data[col]),color = ks_cols[col][-1],label=ks_cols[col][0])
                ks['peak'][col] = round(data[col][peak_hand_time], 2)
                ks['time'][col] = np.where(data[col] == data[col][peak_hand_time])[0][0]
                plt.axvline(time[ks['time'][col]], color = ks_cols[col][-1], linestyle ='--', alpha= 0.7)
                
        plt.ylabel('Angular Velocity [Deg/s]')
        plt.xlabel('Time [s]')
        plt.autoscale(axis='x', tight=True)
        plt.axvline(time[to_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[fc_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[max_grf_time], color='k',linestyle = '--',alpha=0.5)
        plt.axvline(time[bc_time], color='k',linestyle = '--',alpha=0.5)
        
        plt.axhline(0,color='k',lw=0.9)  
        plt.text(time[to_time],y = data['forearm_angular_velo'].max(), s='Toe Off',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[fc_time],y = data['forearm_angular_velo'].max(), s='Foot Contact',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[max_grf_time],y = data['forearm_angular_velo'].max(), s='Max GRF',rotation = 90,verticalalignment='top',horizontalalignment='right')
        plt.text(time[bc_time], y=data['forearm_angular_velo'].max(),s='Ball Contact', rotation=90,verticalalignment='top',horizontalalignment='right')
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

    def pelvic_angle(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        pel = {
            'to_time'      : {},
            'fc_time'      : {},
            'max_grf_time' : {},
            'bc_time'      : {}
            }
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            pel['to_time'][col] = round(data[col][to_time], 2)
            pel['fc_time'][col] = round(data[col][fc_time], 2)
            pel['max_grf_time'][col] = round(data[col][max_grf_time], 2)
            pel['bc_time'][col] = round(data[col][bc_time], 2)
        
        m = data[cols.keys()].max().max()
        
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
        plt.legend()
        plt.tight_layout()
        plt.title('PELVIC ANGLE')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/pelvic.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return pel

    def torso_angle(data, cols, time, to_time, fc_time, max_grf_time, bc_time):
        tor = {
            'to_time'      : {},
            'fc_time'      : {},
            'max_grf_time' : {},
            'bc_time'      : {}
            }
        fig, ax = plt.subplots()
        for col in cols:
            plt.plot(time, np.array(data[col]),color = cols[col][-1],label=cols[col][0])
            tor['to_time'][col] = round(data[col][to_time], 2)
            tor['fc_time'][col] = round(data[col][fc_time], 2)
            tor['max_grf_time'][col] = round(data[col][max_grf_time], 2)
            tor['bc_time'][col] = round(data[col][bc_time], 2)
        
        m = data[cols.keys()].max().max()
        
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
        plt.legend()
        plt.tight_layout()
        plt.title('TORSO ANGLE')
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.grid(axis='y')
        plt.savefig(f"figure/torso.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        return tor
    
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
            
        return rear, lead_tq, lead_z
        
        