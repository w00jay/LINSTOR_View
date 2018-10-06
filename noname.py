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
from random import randint
import pprint
import remi.gui as gui
from remi import start, App
import linstor
from linlin import Linlin

DEFAULT_LINSTOR_URI = 'linstor://localhost'
DEFAULT_POOL = 'DfltStorPool'

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
        #creating a container VBox type, vertical (you can use also HBox or Widget)
        main_container = gui.Widget(width=800, height=600, style={'margin':'10px auto'})

        self.lbl = gui.Label('Hello world!')
        self.bt = gui.Button('Press me!')
        self.lbls_container = gui.Widget(style={'display': 'block', 'overflow': 'auto', 'margin':'10px', 'text-align':'left', 'align':'left'})

        self.rsc_row = []
        self.rsc = []
        for i in range(5):
            print(i)
            row = gui.HBox(style={'border':'1px solid gray', 'margin':'10px', 'text-align':'left'})
            self.rsc_row.append(row)

            key = str(i)
            lbl = gui.Label('Row' + ' ' + key)
            self.rsc_row[i].append(lbl, 0)

        # setting the listener for the onclick event of the button
        # self.bt.onclick.connect(self.on_button_pressed)
        self.bt.onclick.connect(self.on_button_rsc_add)

        # appending a widget to another, the first argument is a string key
        main_container.append([self.lbl, self.bt])
        main_container.append(self.lbls_container, 'open')
        main_container.append(self.rsc_row)

        # returning the root widget
        return main_container

    def on_button_rsc_add(self, emitter):
        nodes = cluster.get_nodes()

        # TODO
        for node in nodes:
            self.rsc_row_add(emitter, nodes, row=self.rsc_count)
            self.rsc_count += 1
            print('rsc count: ' + str(self.rsc_count))
            print(str(node))

    def rsc_row_add(self, emitter, nodes, row):
        index = 0
        for node in nodes:
            # key = node['node_uuid']
            lbl = gui.Label(str(row) + ' ' + node['node_name'] + ' ' + node['node_address'], 
                    style={'border':'1px dashed green', 'padding':'5px', 'margin':'5px'})
            index += 1
            self.rsc_row[row].append(lbl, index)

        close_btn = gui.Button('Close')
        close_btn.onclick.connect(self.rsc_button_close)
        self.rsc_row[row].append(close_btn, 'close')

    def rsc_button_close(self, emitter):
        lbl = gui.Label('More')
        key = 86

        self.rsc_row[0].empty()
        # for i in range(len(self.rsc_row[0])):
        #     self.rsc_row[0].remove_child(self.rsc_row[0].children[str(i)])
        #
        # self.rsc_row[0].remove_child(self.rsc_row[0].children['close'])

    def on_close(self):
        """ Overloading App.on_close event allows to perform some
             activities before app termination.
        """
        super(MyApp, self).on_close()


if __name__ == "__main__":
    # starts the webserver
    start(MyApp, address='0.0.0.0', port=0, start_browser=True, username=None, password=None)

