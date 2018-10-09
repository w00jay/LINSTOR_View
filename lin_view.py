"""
   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import os
from time import sleep
from random import randint
import pprint
import remi.gui as gui
from remi import start, App
import linstor
from linlin import Linlin

LVM = 'Lvm'
LVM_THIN = 'LvmThin'

DEFAULT_LINSTOR_URI = 'linstor://localhost'
DEFAULT_VOL_GROUP = 'vol_group'
DEFAULT_POOL = 'DfltStorPool'
DEFAULT_RSC = 'new_rsc'
DEFAULT_RSC_SIZE = 97657 # KiB = Just over 100MB
DEFAULT_DRIVER = LVM_THIN


cluster = Linlin()

class MyApp(App):
    def __init__(self, *args):

        self.count = 0
        self.rsc_count = 0
        #custom additional html head tags
        my_html_head = """
            """

        #custom css
        my_css_head = """
            <link rel="stylesheet" href="" type="text/css">
            """

        #custom js
        my_js_head = """
            <script></script>
            """

        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
        #static_file_path can be an array of strings allowing to define
        #  multiple resource path in where the resources will be placed
        super(MyApp, self).__init__(*args, static_file_path=res_path, html_head=my_html_head, css_head=my_css_head, js_head=my_js_head)

    def idle(self):
        """ Idle loop, you can place here custom code,
             avoid to use infinite iterations, it would stop gui update.
            This is a Thread safe method where you can update the
             gui with information from external Threads.
        """
        pass

    def main(self):

        # main viewport / window
        main_container = gui.Widget(width=800, height=600, style={'padding':'10px', 'margin':'10px auto'})

        self.lbl = gui.Label('LINSTOR View', style={'padding':'10px', 'font-size': '2.0em'})
        self.bt_show_rsc = gui.Button('Show Resources', style={'padding':'10px', 'margin':'10px'})
        self.bt_show_snap = gui.Button('Show Snapshots', style={'padding':'10px', 'margin':'10px'})
        self.bt_show_nodes = gui.Button('Show Nodes', style={'padding':'10px', 'margin':'10px'})
        self.bt_show_storage = gui.Button('Show Storage', style={'padding':'10px', 'margin':'10px'})
        self.bt_clear_view = gui.Button('Clear View', style={'padding':'10px', 'margin':'10px'})

        # sub-option widgets
        self.txt_rsc_create = gui.TextInput(width=200, height=30, margin='10px')
        self.txt_rsc_create.set_text('new_rsc')

        # display window for tasks
        self.view_container = gui.Widget(style={'display': 'block', 'overflow': 'auto', 'margin':'10px', 'text-align':'left', 'align':'left'})

        # display and resource assets
        self.disp_rsc_row = []
        self.disp_rsc_row_count = 0
        self.rscs = []
        self.nodes = []

        # event callbacks
        self.bt_show_rsc.onclick.connect(self.on_button_show_rsc)
        self.bt_show_snap.onclick.connect(self.on_button_show_snap)
        self.bt_show_nodes.onclick.connect(self.on_button_show_nodes)
        self.bt_show_storage.onclick.connect(self.on_button_show_storage)
        self.bt_clear_view.onclick.connect(self.on_button_view_clear)

        # Add menu buttons and task view to the main viewport
        main_container.append([self.lbl, self.bt_show_rsc, self.bt_show_snap,
                               self.bt_show_nodes, self.bt_show_storage,
                               self.bt_clear_view])
        main_container.append(self.view_container, 'rscs')

        # returning the root widget
        return main_container

    def view_clear(self):
        # reset view
        self.view_container.empty()
        self.disp_rsc_row_count = 0
        self.disp_rsc_row = []

    def action_wait(self):

        self.view_clear()

        # A display row for message
        lbl_msg = 'Waiting for response...'
        self.add_view_line(lbl_msg)

    def add_view_line(self, msg):
        # A display row for message
        row = gui.HBox(style={'border':'1px solid gray', 'margin':'10px', 'text-align':'left'})
        self.disp_rsc_row.append(row)

        # add message label to container
        lbl = gui.Label(msg)
        self.disp_rsc_row[self.disp_rsc_row_count].append(lbl, 'action_msg')

        self.disp_rsc_row_count += 1

        # Add the row to the display
        self.view_container.redraw()
        self.view_container.append(self.disp_rsc_row, 'msg')

    def rsc_create(self, emitter):
        new_rsc_name = self.txt_rsc_create.get_value()
        print('rsc_name: '+ str(new_rsc_name))

        self.action_wait()

        cluster.build_rsc(rsc_name = new_rsc_name, rsc_size=DEFAULT_RSC_SIZE,
                          vg=DEFAULT_VOL_GROUP, driver=DEFAULT_DRIVER)

        msg = 'Deployed resource ' + str(self.txt_rsc_create.get_value())
        self.add_view_line('Deployed resource ')

    def on_button_show_snap(self, emitter):

        # Clear view w/ message
        self.action_wait()

        # get data
        self.snap = cluster.get_snap()

        # Clear wait message
        self.view_clear()

        index = 0

        if self.snap:
            # TODO
            for node in self.nodes:

                lbl_msg = str(node['node_name']) + ' @ ' + str(node['node_address'])
                self.add_view_line(lbl_msg)
                print(str(index) + ' ' + lbl_msg)
        else:
            lbl_msg = 'No LINSTOR Snapshots found'
            self.add_view_line(lbl_msg)

        print('Nodes count: ' + str(index))

    def on_button_show_rsc(self, emitter):

        # Clear view w/ message
        self.action_wait()

        # get data
        self.rscs = cluster.get_rd()

        # Clear wait message
        self.view_clear()

        if self.rscs:
            for rsc in self.rscs:
                # A display row for each resources
                row = gui.HBox(style={'border':'1px solid gray', 'margin':'10px', 'text-align':'left'})
                self.disp_rsc_row.append(row)

                # Add row heading
                lbl_msg = str(self.disp_rsc_row_count) + '. Resource: ' + rsc['rsc_name']
                lbl = gui.Label(lbl_msg)
                self.disp_rsc_row[self.disp_rsc_row_count].append(lbl, 'rsc_name')
                print(lbl_msg)

                # Populate the row w/ resource nodes
                rsc_nodes = cluster.get_rsc_by_rsc(rsc['rsc_name'])
                self.rsc_row_add(rsc_nodes, row=self.disp_rsc_row_count)

                self.disp_rsc_row_count += 1
                print('Rsc count: ' + str(self.disp_rsc_row_count))
        else:
            lbl_msg = 'No LINSTOR Resources found'
            self.add_view_line(lbl_msg)

        # Add widgets for Resource Create
        row = gui.HBox(style={'border':'1px solid gray', 'margin':'10px', 'text-align':'left'})
        self.disp_rsc_row.append(row)

        lbl_rsc_create_msg = 'Create a new resource volume'
        lbl_rsc_create = gui.Label(lbl_rsc_create_msg)
        bt_rsc_create = gui.Button('Proceed', width=200, height=30, margin='10px')
        bt_rsc_create.onclick.connect(self.rsc_create)

        self.disp_rsc_row[self.disp_rsc_row_count].append(lbl_rsc_create, 'lbl')
        # text window is global for proper live look up
        self.disp_rsc_row[self.disp_rsc_row_count].append(self.txt_rsc_create, 'new_rsc')
        self.disp_rsc_row[self.disp_rsc_row_count].append(bt_rsc_create, 'btn')
        self.disp_rsc_row_count += 1
        self.view_container.append(self.disp_rsc_row, 'rsc_list')

    def rsc_row_add(self, rsc_nodes, row):
        index = 0
        for node in rsc_nodes:
            # key = node['node_uuid']
            lbl_msg = node['node_name']
            lbl = gui.Label(lbl_msg,
                    style={'border':'1px dashed green', 'padding':'5px', 'margin':'5px'})
            self.disp_rsc_row[row].append(lbl, str(index))
            index += 1
            print(str(index) + ' ' + lbl_msg)

        def rsc_close_btn(self, rsc_disp, rsc_count):
            target_rsc_name = rsc_disp.get_child('rsc_name').get_text().split(':')[1][1:]
            print('Removing ' + str(rsc_count) + ' resources.')
            print('on resource named: ' + str(target_rsc_name))

            # Remove backend resources
            cluster.destroy_rsc(rsc_name_target=target_rsc_name)

            # rsc_disp.empty()
            for key in range(rsc_count):
                print('removing ' + str(key))
                rsc_disp.remove_child(rsc_disp.get_child(str(key)))
            #rsc_disp.remove_child(rsc_disp.get_child('rsc_name'))
            rsc_disp.remove_child(rsc_disp.get_child('destroy'))

        # Add row clear button
        close_btn = gui.Button('Destroy', style={'padding':'5px'})
        close_btn.onclick.connect(rsc_close_btn, self.disp_rsc_row[row], index)
        self.disp_rsc_row[row].append(close_btn, 'destroy')

    def on_button_show_nodes(self, emitter):

        # Clear view w/ message
        self.action_wait()

        # get data
        self.nodes = cluster.get_nodes()

        # Clear wait message
        self.view_clear()

        index = 0
        if self.nodes:
            for node in self.nodes:

                lbl_msg = str(node['node_name']) + ' @ ' + str(node['node_address'])
                self.add_view_line(lbl_msg)
                print(str(index) + ' ' + lbl_msg)
        else:
            lbl_msg = 'No LINSTOR Resources found'
            self.add_view_line(lbl_msg)
        print('Nodes count: ' + str(index))

    def on_button_show_storage(self, emitter):

        # Clear view w/ message
        self.action_wait()

        # get data
        self.sp = cluster.get_sp()

        # Clear wait message
        self.view_clear()

        index = 0
        for node in self.sp:
            lbl_msg = str(node['sp_name']) + ' @ ' + str(node['node_name'])

            if node['driver_name'] == 'DisklessDriver':
                lbl_msg += ' | No storage with Diskless Node'
            else:
                lbl_msg += ' | ' + str(node['driver_name'])
                lbl_msg += ' | Max Capacity: ' + str(node['sp_cap']) + 'MB'
                lbl_msg += ' | Free ' + str(node['sp_free']) + 'MB'

            self.add_view_line(lbl_msg)
            index += 1
            print(str(index) + ' ' + lbl_msg)

        print('Nodes count: ' + str(index))

    def on_button_view_clear(self, emitter):
        self.view_clear()

    def on_close(self):
        """ Overloading App.on_close event allows to perform some
             activities before app termination.
        """
        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=8008, start_browser=True, username=None, password=None)

