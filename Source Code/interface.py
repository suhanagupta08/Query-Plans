import tkinter
from tkinter import *
import Pmw
from tkinter import ttk
import json
from preprocessing import *
from annotation import *
from tkinter import messagebox

x2 = Preprocessor()
global aqp

def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("500x500")
    main_screen.title("Account Login")

    global username_verify
    global password_verify
    global db_verify

    username_verify = StringVar()
    password_verify = StringVar()
    db_verify = StringVar()

    global username_entry
    global password_entry
    global db_entry
    Label(main_screen, text="CASE SENSITIVE", width="300", height="2", font=("Courier", 14)).pack(padx=2)
    Label(main_screen, text="Username:", width="300", height="2", font=("Courier", 14)).pack()
    main_screen.update()
    username_entry = Entry(main_screen, textvariable=username_verify)
    username_entry.pack()

    Label(main_screen, text="Password:", width="300", height="2", font=("Courier", 14)).pack()
    password_entry = Entry(main_screen, textvariable=password_verify, show='*',)
    password_entry.pack()

    Label(main_screen, text="Database Name:", width="300", height="2", font=("Courier", 14)).pack()
    db_entry = Entry(main_screen, textvariable=db_verify)
    db_entry.pack()

    Button(main_screen, text="Login", width=10, height=1, command=validatelogin).pack(pady=10)

    main_screen.mainloop()

#validate the user input in the main login
def validatelogin():
    username1 = username_verify.get()
    password1 = password_verify.get()
    db1 = db_verify.get()
    #x1 = Preprocessor()
    result = x2.establish_connection( db1, username1, password1)
    x2.connect()
    if result:
        guiforSQL()
    else:
        login_fail()

#a pop up wil appear if login fail
def login_fail():
    global login_fail_screen
    login_fail_screen = Toplevel(main_screen)
    login_fail_screen.title("Fail")
    login_fail_screen.geometry("300x100")
    Label(login_fail_screen, text="Incorrect login credential",font=("Courier", 14)).pack()
    Button(login_fail_screen, text="OK", command=delete_login_fail, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000').pack()

#delete the popup
def delete_login_fail():
    login_fail_screen.destroy()
#delete the popup
def delete_main():
    main_screen.destroy()
#delete the popup
def delete_guiforSQL():
    window.destroy()
#delete the popup
def delete_empty_string():
    empty_string_screen.destroy()

class QEP_visaulizer:
    def __init__(self, window2, query_statement, more_info, plan_tree, cost_info, aqp):
        self.root = plan_tree.head
        self.window2 = window2
        self.query_statement = query_statement
        self.more_info = more_info
        self.cost_info = cost_info
        self.aqp = aqp

        # create window
        if aqp == True:
            self.window2.title('AQP Query Plan Visualizer')
        else:
            self.window2.title('Optimal Query Plan Visualizer')

        screen_width = self.window2.winfo_screenwidth()  # get width of the current computer screen
        screen_height = self.window2.winfo_screenheight() # get height of the current computer screen
        # calculate center coordinates
        x_center = (screen_width/2) - (self.WINDOW2_WIDTH/2)
        y_center = (screen_height/2) - (self.WINDOW2_HEIGHT/2)

        # set default window size and centralize
        self.window2.geometry('%dx%d+%d+%d' % (self.WINDOW2_WIDTH, self.WINDOW2_HEIGHT, x_center, y_center))
        

        # create frame to contain the canvas for flowchart
        flowchart_frame = Frame(self.window2, bg="#D3D3D3", height=self.FLOWCHART_CANVAS_HEIGHT_MAX, width=self.FLOWCHART_CANVAS_WIDTH_MAX)
        query_frame = Frame(self.window2, bg="#bababa", height=self.JSON_EXPLAIN_HEIGHT, width=self.JSON_WINDOW2_WIDTH)
        explain_frame = Frame(self.window2, bg="#bababa", height=self.JSON_QUERY_HEIGHT, width=self.JSON_WINDOW2_WIDTH)
     
        flowchart_canvas = Canvas(flowchart_frame, bg="#D3D3D3", height=self.FLOWCHART_CANVAS_HEIGHT_MAX-50, width=self.FLOWCHART_CANVAS_WIDTH_MAX, highlightthickness=0)
        query_canvas = Canvas(query_frame, bg="#bababa", height=self.JSON_QUERY_HEIGHT, width=self.JSON_WINDOW2_WIDTH, highlightthickness=0)
        more_info_canvas = Canvas(explain_frame, bg="#bababa", height=self.JSON_EXPLAIN_HEIGHT, width=self.JSON_WINDOW2_WIDTH, highlightthickness=0)
        
        # flowchart_canvas.grid(row=0, columnspan=2)
        flowchart_frame.pack(side=LEFT, fill=BOTH, expand=True)
        query_frame.pack(side=TOP, fill=BOTH, expand=True)
        explain_frame.pack(side=BOTTOM, fill=BOTH, expand=True)
       
        flowchart_canvas.pack(side=LEFT,fill=BOTH, pady=25, padx=25, expand=True)
        query_canvas.pack(side=RIGHT, fill=Y, expand=True, pady=22, padx=10)
        more_info_canvas.pack(side=RIGHT, fill=Y, expand=True, pady=22, padx=10)

        # setting style with ttk package
        style=ttk.Style()
        style.theme_use('default')
        # style.configure("Vertical.TScrollbar", background="gray", arrowcolor="white")

        # creating horizontal scrollbar binded to flowchart canvas
        flowchart_canvas_scrollbar_h = ttk.Scrollbar(flowchart_frame, orient="horizontal", command=flowchart_canvas.xview)
        flowchart_canvas_scrollbar_h.place(x=0.001, rely=0.98, relwidth=0.98)
        # flowchart_canvas_scrollbar_h.pack(side="bottom", fill="x")
        # creating vertical scrollbar binded to flowchart canvas
        flowchart_canvas_scrollbar_v = ttk.Scrollbar(flowchart_frame, orient="vertical", command=flowchart_canvas.yview)
        flowchart_canvas_scrollbar_v.pack(side="right", fill="y")
        flowchart_canvas.configure(xscrollcommand=flowchart_canvas_scrollbar_h.set, yscrollcommand=flowchart_canvas_scrollbar_v.set)
        flowchart_canvas.bind('<Configure>', lambda e: flowchart_canvas.configure(scrollregion=flowchart_canvas.bbox("all")))
        # scrollbars for query canvas
        query_canvas_scrollbar_h = ttk.Scrollbar(query_frame, orient="horizontal", command=query_canvas.xview)
        query_canvas_scrollbar_h.place(x=0.001, rely=0.96, relwidth=0.99)
        query_canvas_scrollbar_v = ttk.Scrollbar(query_frame, orient="vertical", command=query_canvas.yview)
        query_canvas_scrollbar_v.place(relx=0.93, rely=0.001, relheight=0.97)
        query_canvas.configure(xscrollcommand=query_canvas_scrollbar_h.set, yscrollcommand=query_canvas_scrollbar_v.set)
        query_canvas.bind('<Configure>', lambda e: query_canvas.configure(scrollregion=query_canvas.bbox("all")))
        # scrollbars for explain canvas
        explain_canvas_scrollbar_h = ttk.Scrollbar(explain_frame, orient="horizontal", command=more_info_canvas.xview)
        explain_canvas_scrollbar_h.place(x=0.001, rely=0.96, relwidth=0.99)
        explain_canvas_scrollbar_v = ttk.Scrollbar(explain_frame, orient="vertical", command=more_info_canvas.yview)
        explain_canvas_scrollbar_v.place(relx=0.93, rely=0.001, relheight=0.99)
        more_info_canvas.configure(xscrollcommand=explain_canvas_scrollbar_h.set, yscrollcommand=explain_canvas_scrollbar_v.set)
        more_info_canvas.bind('<Configure>', lambda e: more_info_canvas.configure(scrollregion=more_info_canvas.bbox("all")))
        
        if aqp == True:
            # back button
            backbtn = Button(flowchart_canvas, text="Back to Enter Query", relief=RIDGE, font=("Courier", 10, "bold"), width=20,command= lambda: backToQuery(self.window2), bg='#D3D3D3', fg='#000000', activebackground='#D3D3D3',
                    activeforeground='#D3D3D3')
            backbtn.place(relx=0.01, rely=0.01)
        else:
            # back button
            backbtn = Button(flowchart_canvas, text="Back to Enter Query", relief=RIDGE, font=("Courier", 10, "bold"), width=20,command= lambda: backToQuery(self.window2), bg='#D3D3D3', fg='#000000', activebackground='#D3D3D3',
                    activeforeground='#D3D3D3')
            backbtn.place(relx=0.01, rely=0.01)
            # aqp button
            aqpbtn = Button(flowchart_canvas, text="View AQP Tree", relief=RIDGE, font=("Courier", 10, "bold"), width=20,command= lambda: displayAQP(self.query_statement, self.window2), bg='#D3D3D3', fg='#000000', activebackground='#D3D3D3',
                    activeforeground='#D3D3D3')
            aqpbtn.place(relx=0.78, rely=0.01)
            

        formatted_query_statement = self.format_query()
        # display formatted query
        query_canvas.create_text(self.json_title_X, self.json_title_Y, fill=self.title_fill, font=self.json_title_font, text="QUERY STATEMENT", anchor=self.json_anchor, width = self.JSON_WINDOW2_WIDTH-120)
        query_canvas.create_text(self.json_subtitle_X, self.json_subtitle_Y, fill=self.json_fill, font=self.json_subtitle_font, text=formatted_query_statement, anchor=self.json_anchor, width = self.JSON_WINDOW2_WIDTH-120)
        # display formatted json
        formatted_more_info = self.format_more_info()
        more_info_canvas.create_text(17, 20, fill=self.title_fill, font=self.json_title_font, text="MORE INFO ON QUERY PLAN", anchor=self.json_anchor, width = self.JSON_WINDOW2_WIDTH-120)
        more_info_canvas.create_text(18, 45+27, fill=self.json_fill, font=self.json_subtitle_font, text=formatted_more_info, anchor=self.json_anchor, width = self.JSON_WINDOW2_WIDTH-120)

        drawing = draw_chart(flowchart_canvas)
        drawing.draw_query_flowchart(self.cost_info, self.default_line_length, self.switch, self.root, self.default_rect_X1, self.default_rect_Y1, self.default_rect_X2, self.default_rect_Y2, self.title_pos_height, self.title_pos_width, self.subtitle_pos_width, self.subtitle_pos_height)

    WINDOW2_WIDTH = 1000 # main window width 
    WINDOW2_HEIGHT = 800 # main window height
    FLOWCHART_CANVAS_WIDTH_MAX = 0.7*WINDOW2_WIDTH    # flowchart canvas width   
    FLOWCHART_CANVAS_HEIGHT_MAX = WINDOW2_HEIGHT   # flowchart canvas height
    JSON_WINDOW2_WIDTH = WINDOW2_WIDTH-FLOWCHART_CANVAS_WIDTH_MAX
    JSON_WINDOW2_HEIGHT = WINDOW2_HEIGHT
    JSON_QUERY_HEIGHT = 0.5*JSON_WINDOW2_HEIGHT
    JSON_EXPLAIN_HEIGHT = WINDOW2_HEIGHT-JSON_QUERY_HEIGHT

    # default settings for flowchart
    default_middle = FLOWCHART_CANVAS_WIDTH_MAX/2   # default middle of canvas
    # rect
    rect_padding = 30
    # starting coordiantes of top left corner of rect
    default_rect_X1 = 150   # LHS of rect has 150 space, RHS of rect has equal 150 space
    default_rect_Y1 = 30
    default_rect_width = 400
    # starting coordinates of bottom right corner of rect
    default_rect_X2 = default_rect_X1+default_rect_width    # starting X2 coordinate of bottom right corner of rect
    default_rect_height = 120
    default_rect_Y2 = 120   # rect height is dynamic and will change later according to subtitle size/height
    # title
    pad_title_width = (default_rect_X2-default_rect_X1)/2
    pad_title_height = default_rect_height/3
    # mid_of_rect_width 
    title_pos_width = default_rect_X1+pad_title_width
    # mid of rect height
    title_pos_height = default_rect_Y1+pad_title_height
    # subtitle
    pad_subtitle_width = (default_rect_X2-default_rect_X1)/8
    pad_subtitle_height = 2.5*(default_rect_Y2-default_rect_Y1)/3
    # starting point for subtitle
    subtitle_pos_width = default_rect_X1+pad_subtitle_width
    # ending height for subtitle
    subtitle_pos_height = default_rect_Y1+pad_subtitle_height
    subtitle_overflow = default_rect_width-pad_subtitle_width
    # line
    default_line_length = 50
    line_fill = "black"
    line_width = 3
    # default settings for text
    title_anchor = "center"
    title_fill = "black"
    title_font = "Calibri 20 bold"
    subtitle_anchor = "nw"
    subtitle_fill = "#5A5A5A"
    subtilte_font = "Calibri 15"
    node_outline_colour = "white"
    node_fill_colour = "white"
    json_fill = "black"
    json_title_font = "Calibri 18 bold"
    json_subtitle_font = "Calibri 12"
    json_anchor = "nw"
    json_title_X = 17
    json_title_Y = 20
    json_subtitle_X = 18
    json_subtitle_Y = 45

    # dummy to alternate between short and long lines
    switch = 0

    def format_query(self):
        formatted_query_statement = ""
        for text in self.query_statement.lower().split(' '):
            if 'select' in text:
                formatted_query_statement += text.upper() + " "
            elif 'from' in text or  "where" in text or 'order by' in text or "group by" in text or "limit" in text:
                formatted_query_statement += '\n' + text.upper() + " "
            elif 'and' in text or  "or" in text:
                formatted_query_statement += '\n\t' + text.upper() + " "
            else:
                formatted_query_statement += text + " "
        return formatted_query_statement 

    def format_more_info(self):
        formatted_more_info = "Reason for difference in final node's actual cost and estimated cost: " + "\n"
        more_info = str(self.more_info)
        more_info = more_info.replace("[", "")
        more_info = more_info.replace("]", "")
        more_info = more_info.replace("'", "")
        return formatted_more_info+more_info

class draw_chart:
    def __init__(self, canvas):
        self.flowchart_canvas = canvas
    
    WINDOW2_WIDTH = 1000 # main window width 
    WINDOW2_HEIGHT = 800 # main window height
    FLOWCHART_CANVAS_WIDTH_MAX = 0.7*WINDOW2_WIDTH    # flowchart canvas width   
    FLOWCHART_CANVAS_HEIGHT_MAX = WINDOW2_HEIGHT   # flowchart canvas height
    JSON_WINDOW2_WIDTH = WINDOW2_WIDTH-FLOWCHART_CANVAS_WIDTH_MAX
    JSON_WINDOW2_HEIGHT = WINDOW2_HEIGHT
    JSON_QUERY_HEIGHT = 0.5*JSON_WINDOW2_HEIGHT
    JSON_EXPLAIN_HEIGHT = WINDOW2_HEIGHT-JSON_QUERY_HEIGHT
    # default settings for flowchart
    default_middle = FLOWCHART_CANVAS_WIDTH_MAX/2   # default middle of canvas
    # rect
    rect_padding = 30
    # starting coordiantes of top left corner of rect
    default_rect_X1 = 150   # LHS of rect has 150 space, RHS of rect has equal 150 space
    default_rect_Y1 = 30
    default_rect_width = 400
    # starting coordinates of bottom right corner of rect
    default_rect_X2 = default_rect_X1+default_rect_width    # starting X2 coordinate of bottom right corner of rect
    default_rect_height = 120
    default_rect_Y2 = 120   # rect height is dynamic and will change later according to subtitle size/height
    # title
    pad_title_width = (default_rect_X2-default_rect_X1)/2
    pad_title_height = default_rect_height/3
    # mid_of_rect_width 
    title_pos_width = default_rect_X1+pad_title_width
    # mid of rect height
    title_pos_height = default_rect_Y1+pad_title_height
    # subtitle
    pad_subtitle_width = (default_rect_X2-default_rect_X1)/8
    pad_subtitle_height = 2.5*(default_rect_Y2-default_rect_Y1)/3
    # starting point for subtitle
    subtitle_pos_width = default_rect_X1+pad_subtitle_width
    # ending height for subtitle
    subtitle_pos_height = default_rect_Y1+pad_subtitle_height
    subtitle_overflow = default_rect_width-pad_subtitle_width
    # line
    default_line_length = 50
    line_fill = "black"
    line_width = 3
    # default settings for text
    title_anchor = "center"
    title_fill = "black"
    title_font = "Calibri 20 bold"
    subtitle_anchor = "nw"
    subtitle_fill = "#5A5A5A"
    subtilte_font = "Calibri 15"
    node_outline_colour = "white"
    node_fill_colour = "white"
    json_fill = "black"
    json_title_font = "Calibri 18 bold"
    json_subtitle_font = "Calibri 12"
    json_anchor = "nw"
    json_title_X = 17
    json_title_Y = 20
    json_subtitle_X = 18
    json_subtitle_Y = 45

    # dummy to alternate between short and long lines
    switch = 0

    nodeList = []

    # def onClick(self, event):
    #     self.flowchart_canvas.itemconfigure(event.num, fill="black")
    #     messagebox.showinfo("showinfo", "Information")

    def format_cost_info(self, cost_info):
        formatted_cost_info = "Estimated Total Cost: "
        for i in range(2):
            formatted_cost_info += str(cost_info[i])
            if i == 0:
                formatted_cost_info += "\nActual Total Time Taken: "
        cost_info.pop(0)
        cost_info.pop(0)
        return formatted_cost_info, cost_info

    def draw_node(self, cost_info, default_line_length, title, subtitle, default_rect_X1, default_rect_Y1, default_rect_X2, default_rect_Y2, title_pos_height, title_pos_width, subtitle_pos_width, subtitle_pos_height):
        node = self.flowchart_canvas.create_rectangle(default_rect_X1, default_rect_Y1, default_rect_X2, default_rect_Y2, outline = self.node_outline_colour, fill = self.node_fill_colour)
        node_type_title = self.flowchart_canvas.create_text(title_pos_width, title_pos_height, anchor = self.title_anchor, fill=self.title_fill, font=self.title_font, text=title)
        node_type_subtitle = self.flowchart_canvas.create_text(subtitle_pos_width, subtitle_pos_height, fill=self.subtitle_fill, font=self.subtilte_font, text=subtitle, anchor=self.subtitle_anchor, width = self.subtitle_overflow)
        subtitle_size = self.flowchart_canvas.bbox(node_type_subtitle)
        final_rect_height = subtitle_size[3]+self.rect_padding
        # only height of rect changes
        self.flowchart_canvas.coords(node, default_rect_X1, default_rect_Y1, default_rect_X2, final_rect_height)

        # # make node expand when clicked
        # button = Button(flowchart_canvas, width=6, height=2, text="click for more info", command=onClick)
        # button.place(x=int(default_rect_X1+default_rect_width/20), y=default_rect_Y1-20)

        # self.flowchart_canvas.tag_bind(node, '<Button-1>', self.onClick)
        formatted_cost_info, cost_info = self.format_cost_info(cost_info)
        formatted_cost_info += '\nNode Type Explanation: ' + subtitle
        # ballon tooltip (hover message)
        tip = Pmw.Balloon()
        # # tooltip hover message
        tip.tagbind(self.flowchart_canvas, node, formatted_cost_info)
        
        
        # update variables
        default_rect_Y1 = final_rect_height+default_line_length
        default_rect_Y2 = default_rect_Y1+self.default_rect_height
        title_pos_height = default_rect_Y1+self.pad_title_height
        subtitle_pos_height = default_rect_Y1+self.pad_subtitle_height

        return default_rect_Y1, default_rect_Y2, title_pos_height, subtitle_pos_height, final_rect_height, cost_info

    # pass in binary tree storing annotation information
    def draw_query_flowchart(self, cost_info, default_line_length, switch, root, default_rect_X1, default_rect_Y1, default_rect_X2, default_rect_Y2, title_pos_height, title_pos_width, subtitle_pos_width, subtitle_pos_height):
        if root:
            # get current plan, title and subtitle
            # plan = root.plan
            # title = root.title
            # subtitle = root.subtitle
            title = root.get_node_type()
            subtitle = root.explain_node_type()
            childrenList = []
            for child in root.children:
                childrenList.append(child)

            # draw current node
            default_rect_Y1, default_rect_Y2, title_pos_height, subtitle_pos_height, final_rect_height, cost_info = self.draw_node(cost_info, default_line_length,title, subtitle, default_rect_X1, default_rect_Y1, default_rect_X2, default_rect_Y2, title_pos_height, title_pos_width, subtitle_pos_width, subtitle_pos_height)
            # if leaf node (no child nodes), return
            if len(root.children) == 0:
                return
            # if root.plan == 0:
            #     return

            # if 1 child, straight down
            if len(root.children) == 1:
                # update variables according to varying line length
                default_line_length = default_line_length+25
                default_rect_Y1 = final_rect_height+default_line_length
                default_rect_Y2 = default_rect_Y1+self.default_rect_height
                title_pos_height = default_rect_Y1+self.pad_title_height
                subtitle_pos_height = default_rect_Y1+self.pad_subtitle_height
                # draw line arrow
                line_arrow_Y = default_line_length+final_rect_height
                line = self.flowchart_canvas.create_line(title_pos_width, line_arrow_Y, title_pos_width, final_rect_height, fill=self.line_fill, width=self.line_width, arrow='first')
                default_rect_Y1 = final_rect_height+default_line_length
                self.draw_query_flowchart(cost_info, default_line_length, switch, childrenList[0], default_rect_X1, default_rect_Y1, default_rect_X2, default_rect_Y2, title_pos_height, title_pos_width, subtitle_pos_width, subtitle_pos_height)
            # if 2 child, split
            if len(root.children) == 2:
                if switch == 0:
                    line_offset, line_arrow_Y = self.shorter_slant_lines(final_rect_height, default_line_length-50)
                    switch = 1
                else:
                    line_offset, line_arrow_Y = self.longer_slant_lines(final_rect_height, default_line_length+50)
                    switch = 0
                # line_offset = default_rect_width/4
                # line_arrow_Y = default_line_length+final_rect_height+default_line_length+default_line_length+default_line_length
                # draw left arrow
                left_arrow_X = title_pos_width-line_offset
                left_line = self.flowchart_canvas.create_line(left_arrow_X, line_arrow_Y-3, title_pos_width, final_rect_height, fill=self.line_fill, width=self.line_width, arrow='first')
                # update variables for left child node
                left_rect_offset = 2.5*self.default_rect_width/4  # offset to shift rect left for left child
                # left_rect_offset = default_rect_width
                left_temp_X1 = default_rect_X1-left_rect_offset   # default rect Y1 can use same as the updated one in draw_node function
                left_temp_X2 = default_rect_X2-left_rect_offset   # default rect Y2 can use same as the updated one in draw_node function
                left_temp_title_pos_width = title_pos_width-left_rect_offset
                left_temp_subtitle_pos_width = subtitle_pos_width-left_rect_offset
                # update variables
                temp_rect_Y1 = line_arrow_Y
                temp_rect_Y2 = temp_rect_Y1+self.default_rect_height
                temp_title_pos_height = temp_rect_Y1+self.pad_title_height
                temp_subtitle_pos_height = temp_rect_Y1+self.pad_subtitle_height
                # draw all left childs
                self.draw_query_flowchart(cost_info, default_line_length,switch, childrenList[0], left_temp_X1, temp_rect_Y1, left_temp_X2, temp_rect_Y2, temp_title_pos_height, left_temp_title_pos_width, left_temp_subtitle_pos_width, temp_subtitle_pos_height)
                # draw right arrow
                if switch == 0:
                    line_offset, line_arrow_Y = self.longer_slant_lines(final_rect_height, default_line_length+50)
                    switch = 1
                else:
                    line_offset, line_arrow_Y = self.shorter_slant_lines(final_rect_height, default_line_length-50)
                    switch = 0
                # line_offset = default_rect_width/4
                # line_arrow_Y = default_line_length-60+final_rect_height

                right_arrow_X = title_pos_width+line_offset
                right_line = self.flowchart_canvas.create_line(right_arrow_X, line_arrow_Y-3, title_pos_width, final_rect_height, fill=self.line_fill, width=self.line_width, arrow='first')
                # update variables for right child
                right_rect_offset = 2.5*self.default_rect_width/4  # offset to shift rect left for left child
                # right_rect_offset = 1.2*default_rect_width/4
                right_temp_X1 = default_rect_X1+right_rect_offset   # default rect Y1 can use same as the updated one above
                right_temp_X2 = default_rect_X2+right_rect_offset   # default rect Y2 can use same as the updated one above
                right_temp_title_pos_width = title_pos_width+right_rect_offset
                right_temp_subtitle_pos_width = subtitle_pos_width+right_rect_offset
                # update variables
                temp_rect_Y1 = line_arrow_Y
                temp_rect_Y2 = temp_rect_Y1+self.default_rect_height
                temp_title_pos_height = temp_rect_Y1+self.pad_title_height
                temp_subtitle_pos_height = temp_rect_Y1+self.pad_subtitle_height
                # draw all right childs
                self.draw_query_flowchart(cost_info, default_line_length,switch, childrenList[1], right_temp_X1, temp_rect_Y1, right_temp_X2, temp_rect_Y2, temp_title_pos_height, right_temp_title_pos_width, right_temp_subtitle_pos_width, temp_subtitle_pos_height)
        
    def longer_slant_lines(self, final_rect_height, default_line_length):
        line_offset = self.default_rect_width/7
        line_arrow_Y = default_line_length+final_rect_height+default_line_length
        return line_offset, line_arrow_Y

    def shorter_slant_lines(self, final_rect_height, default_line_length):
        line_offset = self.default_rect_width/4
        line_arrow_Y = default_line_length+final_rect_height
        return line_offset, line_arrow_Y

#a pop up wil appear if login fail
def empty_string():
    global empty_string_screen
    empty_string_screen = Toplevel(window)
    empty_string_screen.title("Empty String")
    empty_string_screen.geometry("300x100")
    Label(empty_string_screen, text="No SQL Query Text Entered",font=("Courier", 14)).pack()
    Button(empty_string_screen, text="OK", command=delete_empty_string, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000').pack()


def displayAQP(q2, window):
    aqp = True
    #p = Preprocessor()
    #alter = True

    query_plan = x2.execute_query_aqp(q2)

    print("=========================")
    if query_plan:
        plan_tree = PlanTree(query_plan)
        # plan_tree.print_tree()
        more_info = plan_tree.get_more_info()
        cost_info = plan_tree.get_cost_info()
        window.destroy()
        window2 = Tk()
        GUI = QEP_visaulizer(window2, q2, more_info, plan_tree, cost_info, aqp)
        window2.mainloop()
    else:
        print("Error.")

def executeAltQuery(q2):
    aqp = True
    #p = Preprocessor()
    #alter = True

    query_plan = x2.execute_query_aqp(q2)

    print("=========================")
    if query_plan:
        plan_tree = PlanTree(query_plan)
        # plan_tree.print_tree()
        more_info = plan_tree.get_more_info()
        cost_info = plan_tree.get_cost_info()
        delete_guiforSQL()
        window2 = Tk()
        GUI = QEP_visaulizer(window2, q2, more_info, plan_tree, cost_info, aqp)
        window2.mainloop()
    else:
        print("Error.")

def executeQuery(q2):
    aqp = False
    #p = Preprocessor()
    query_plan = x2.execute_query_qep(q2)
    # print("changing settings")
    print("=========================")
    if query_plan:
        plan_tree = PlanTree(query_plan)
        # plan_tree.print_tree()
        more_info = plan_tree.get_more_info()
        cost_info = plan_tree.get_cost_info()
        delete_guiforSQL()
        window2 = Tk()
        GUI = QEP_visaulizer(window2, q2, more_info, plan_tree, cost_info, aqp)
        window2.mainloop()
    else:
        print("Error.")

#Submit function to test if it is empty and also the result
def submitsql():
    text = userinput.get("1.0", "end-1c")
    #userinput.configure(state='normal')
    #userinput.delete('1.0', END)
    query = text
    if not query:
        empty_string()
    
    else:
        executeQuery(query)

#Submit function to test if it is empty and also the result
def submitAltSql():
    text = userinput.get("1.0", "end-1c")
    #userinput.configure(state='normal')
    #userinput.delete('1.0', END)
    query = text
    if not query:
        empty_string()
    
    else:
        executeAltQuery(query)




#gui for the main application
def guiforSQL():
    delete_main()
    global window
    global userinput
    window = Tk()
    window.geometry("1030x750")
    window.title("Enter Query Statement")


    #create panel1 for the user input
    inputpanel = PanedWindow()
    inputpanel_label = Label(inputpanel, text="User input")
    inputpanel_label.config(font=("Courier", 14))
    inputpanel_label.pack(pady=5)
    inputpanel.pack()
    #scrollbar
    scrollbar = Scrollbar(inputpanel)
    scrollbar.pack(side=RIGHT, fill=Y)
    #textarea for the user to write their sql statement
    userinput = Text(inputpanel,height=10, relief='groove', wrap='word', font=('courier',10),yscrollcommand=scrollbar.set)
    userinput.pack()
    scrollbar.config(command=userinput.yview)


    #a div/panel to hold the two button which allow it to be side bvy side
    div = PanedWindow()
     #to execute the query - currently connects to function to check if Query text box is empty or not, can add execution function as an if statement of submitsql
    submitbtn = Button(div, text="View Optimal QEP Tree", relief=RIDGE, font=("Courier", 12, "bold"), width=20, command=submitsql, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    submitbtn.pack(side=LEFT, padx=5)
    
    #to display the QEP - currently same function as submitsql
    aqptreebtn = Button(div, text="View AQP Tree", relief=RIDGE, font=("Courier", 12, "bold"), width=20,command=submitAltSql, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    aqptreebtn.pack(side=LEFT, padx=5)
    
    #Quit the window
    quitbtn = Button(div, text="Quit", relief=RIDGE, font=("Courier", 12, "bold"), width=20, command=delete_guiforSQL, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    quitbtn.pack()
    div.pack(pady=10)

def backToQuery(window2):
    window2.destroy()
    global window
    global userinput
    window = Tk()
    window.geometry("1030x750")
    window.title("CZ4031")


    #create panel1 for the user input
    inputpanel = PanedWindow()
    inputpanel_label = Label(inputpanel, text="User input")
    inputpanel_label.config(font=("Courier", 14))
    inputpanel_label.pack(pady=5)
    inputpanel.pack()
    #scrollbar
    scrollbar = Scrollbar(inputpanel)
    scrollbar.pack(side=RIGHT, fill=Y)
    #textarea for the user to write their sql statement
    userinput = Text(inputpanel,height=10, relief='groove', wrap='word', font=('courier',10),yscrollcommand=scrollbar.set)
    userinput.pack()
    scrollbar.config(command=userinput.yview)


    #a div/panel to hold the two button which allow it to be side bvy side
    div = PanedWindow()
     #to execute the query - currently connects to function to check if Query text box is empty or not, can add execution function as an if statement of submitsql
    submitbtn = Button(div, text="View Optimal QEP Tree", relief=RIDGE, font=("Courier", 12, "bold"), width=20, command=submitsql, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    submitbtn.pack(side=LEFT, padx=5)
    
    #to display the QEP - currently same function as submitsql
    aqptreebtn = Button(div, text="View AQP Tree", relief=RIDGE, font=("Courier", 12, "bold"), width=20,command=submitAltSql, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    aqptreebtn.pack(side=LEFT, padx=5)
    
    #Quit the window
    quitbtn = Button(div, text="Quit", relief=RIDGE, font=("Courier", 12, "bold"), width=20, command=delete_guiforSQL, bg='#0052cc', fg='#000000', activebackground='#0052cc',
                   activeforeground='#000000')
    quitbtn.pack()
    div.pack(pady=10)


    window.mainloop()






