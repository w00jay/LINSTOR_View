import linstor
import pprint
from google.protobuf.json_format import MessageToDict

DEFAULT_LINSTOR_URI = 'linstor://localhost'

class Linlin(object):
    def __init__(self):
        pass

    def get_nodes(self):
        try:
            with linstor.Linstor(DEFAULT_LINSTOR_URI) as lin:
                if not lin.connected:
                    lin.connect()

                node_list_reply = lin.node_list()[0].proto_msg

                node_list = []
                if not node_list_reply:
                    print("No LINSTOR nodes found on the network.")
                else:
                    for node in node_list_reply.nodes:
                        #print('NODE: '+node.name+' = '+node.uuid+' = '+node.net_interfaces[0].address+'\n')
                        node_item = {}
                        node_item['node_name'] = node.name
                        node_item['node_uuid'] = node.uuid
                        node_item['node_address'] = node.net_interfaces[0].address
                        node_list.append(node_item)

                lin.disconnect()
                return node_list
        except Exception as e:
            print(str(e))

    def get_rd(self):
        try:
            with linstor.Linstor("linstor://localhost") as lin:
                if not lin.connected:
                    lin.connect()

                rd_list = []
                rd_reply = lin.resource_dfn_list()[0].proto_msg

                if not rd_reply:
                    print("No LINSTOR Resource Definitions found")
                else:
                    for rsc in rd_reply.rsc_dfns:
                        rsc_item = {}
                        rsc_item['rsc_name'] = rsc.rsc_name
                        rd_list.append(rsc_item)

                lin.disconnect()
                return rd_list  # First entry is the node list proto msg

        except Exception as e:
            print(str(e))

    def get_spd(self):
        try:
            with linstor.Linstor("linstor://localhost") as lin:
                if not lin.connected:
                    lin.connect()

                # Storage Pool Definition List
                spd_reply = lin.storage_pool_dfn_list()[0].proto_msg
                if not spd_reply:
                    print("No LINSTOR Storage Pool Definition found")

                spd_list = []
                for node in spd_reply.stor_pool_dfns:
                    spd_item = {}
                    # spd_item['spd_uuid'] = node.uuid
                    spd_item['spd_name'] = node.stor_pool_name
                    spd_list.append(spd_item)

                lin.disconnect()
                return spd_list

        except Exception as e:
            print(str(e))

    def get_sp(self):
        try:
            with linstor.Linstor("linstor://localhost") as lin:
                if not lin.connected:
                    lin.connect()

                # Fetch Storage Pool List
                sp_reply = lin.storage_pool_list()[0].proto_msg
                if not sp_reply:
                    print("No LINSTOR Storage Pool found")

                sp_list = []
                node_count = 0
                for node in sp_reply.stor_pools:
                    sp_node = {}
                    sp_node['node_uuid'] = node.node_uuid
                    sp_node['node_name'] = node.node_name
                    sp_node['sp_uuid'] = node.stor_pool_uuid
                    sp_node['sp_name'] = node.stor_pool_name

                    print(str(node.node_name))
                    for prop in node.props:
                        if "Vg" in prop.key:
                            sp_node['vg_name'] = prop.value
                        if "ThinPool" in prop.key:
                            print("... is a thinpool")

                    if 'Diskless' in node.driver:
                        print("... is diskless")
                        sp_node['sp_free'] = -1.0
                        sp_node['sp_cap'] = 0.0
                    else:
                        # / 1048576 => to GiB
                        # / 976.5625 => to MB
                        sp_node['sp_free'] = round(
                            int(node['freeSpace']['freeCapacity']) / 976.5625,
                            2)
                        sp_node['sp_cap'] = round(
                            int(node['freeSpace']['totalCapacity']) / 976.5625,
                            2)

                    if node.driver == "LvmDriver":
                        sp_node['driver_name'] = "Lvm"
                    else:
                        sp_node['driver_name'] = node.driver

                    if node.vlms:
#                         print(node.vlms[0].backing_disk)
                        print(node.vlms[0].device_path)
                    else:
                        print('No volumes')

                    sp_list.append(sp_node)

                lin.disconnect()
                return sp_list

        except Exception as e:
            print(str(e))

    def get_rsc(self):
        try:
            with linstor.Linstor("linstor://localhost") as lin:
                if not lin.connected:
                    lin.connect()

                rsc_reply = lin.resource_list()[0].proto_msg
                if not rsc_reply:
                    print("No LINSTOR Resources found")

                rsc_list = []
                for rsc in rsc_reply.resources:
                    rsc_item = {}
                    # spd_item['spd_uuid'] = node.uuid
                    rsc_item['rsc_name'] = rsc.name
                    rsc_item['node_name'] = rsc.node_name
                    rsc_list.append(rsc_item)

                lin.disconnect()
                return rsc_list

        except Exception as e:
            print(str(e))

    def get_rsc_by_rsc(self, rsc_name):
        resources = self.get_rsc()
        if not resources:
            print("Empty Resource list")

        rsc_list = list(filter(lambda rsc: rsc['rsc_name'] == rsc_name, resources))
        return rsc_list

    def get_rsc_by_node(self, node_name):
        resources = self.get_rsc()
        if not resources:
            print("Empty Resource list")

        rsc_list = list(filter(lambda rsc: rsc['node_name'] == node_name, resources))
        return rsc_list

    def get_snap(self):
        try:
            with linstor.Linstor(DEFAULT_LINSTOR_URI) as lin:
                if not lin.connected:
                    lin.connect()

                snap_list_reply = lin.snapshot_dfn_list()[0].proto_msg
                snap_list = []
                if not len(str(snap_list_reply)):
                    print("No LINSTOR snapshots found on the network.")
                else:
                    for snap in snap_list_reply:
                        #print('NODE: '+node.name+' = '+node.uuid+' = '+node.net_interfaces[0].address+'\n')
                        snap_item = {}
                        # TODO
                        snap_item['node_uuid'] = snap.uuid
                        snap_item['node_address'] = snap.net_interfaces[0].address
                        snap_list.append(snap_item)

                lin.disconnect()
                return snap_list
        except Exception as e:
            print(str(e))

if __name__ == "__main__":
    foo = Linlin()
    pprint.pprint(foo.get_snap())
#    pprint.pprint(foo.get_nodes())
#    pprint.pprint(foo.get_rd())
#    pprint.pprint(foo.get_spd())
    pprint.pprint(foo.get_sp())
#    pprint.pprint(foo.get_rsc())
#    pprint.pprint(foo.get_rsc_by_rsc(rsc_name='a1'))
#    pprint.pprint(foo.get_rsc_by_node(node_name='osboxes'))
