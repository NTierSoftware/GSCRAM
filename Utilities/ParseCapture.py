# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = msg_from_dict(json.loads(json_string))
# IN_FILE = '../../captures/export.json'
# OUT_FILE_CSV = '../../captures/summary.csv'
# OUT_FILE_JSON = '../../captures/messageList.json'
# OUT_FILE_TXT = '../../captures/conversationOverview.txt'


import json

from dataclasses import dataclass
from typing import Optional, List, Union, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_none(x: Any) -> Any:
    assert x is None
    return x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Data:
    data_data_raw: Optional[List[Union[int, str]]]
    data_data: Optional[str]
    data_len: Optional[int]

    @staticmethod
    def from_dict(obj: Any) -> 'Data':
        assert isinstance(obj, dict)
        data_data_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("data.data_raw"))
        data_data = from_union([from_str, from_none], obj.get("data.data"))
        data_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("data.len"))
        return Data(data_data_raw, data_data, data_len)

    def to_dict(self) -> dict:
        result: dict = {}
        result["data.data_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.data_data_raw)
        result["data.data"] = from_union([from_str, from_none], self.data_data)
        result["data.len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.data_len)
        return result


@dataclass
class EthTree:
    eth_dst_resolved_raw: Optional[List[Union[int, str]]]
    eth_dst_resolved: Optional[str]
    eth_addr_raw: Optional[List[Union[int, str]]]
    eth_addr: Optional[str]
    eth_addr_resolved_raw: Optional[List[Union[int, str]]]
    eth_addr_resolved: Optional[str]
    eth_lg_raw: Optional[List[int]]
    eth_lg: Optional[int]
    eth_ig_raw: Optional[List[int]]
    eth_ig: Optional[int]
    eth_src_resolved_raw: Optional[List[Union[int, str]]]
    eth_src_resolved: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'EthTree':
        assert isinstance(obj, dict)
        eth_dst_resolved_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.dst_resolved_raw"))
        eth_dst_resolved = from_union([from_str, from_none], obj.get("eth.dst_resolved"))
        eth_addr_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.addr_raw"))
        eth_addr = from_union([from_str, from_none], obj.get("eth.addr"))
        eth_addr_resolved_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.addr_resolved_raw"))
        eth_addr_resolved = from_union([from_str, from_none], obj.get("eth.addr_resolved"))
        eth_lg_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("eth.lg_raw"))
        eth_lg = from_union([from_none, lambda x: int(from_str(x))], obj.get("eth.lg"))
        eth_ig_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("eth.ig_raw"))
        eth_ig = from_union([from_none, lambda x: int(from_str(x))], obj.get("eth.ig"))
        eth_src_resolved_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.src_resolved_raw"))
        eth_src_resolved = from_union([from_str, from_none], obj.get("eth.src_resolved"))
        return EthTree(eth_dst_resolved_raw, eth_dst_resolved, eth_addr_raw, eth_addr, eth_addr_resolved_raw, eth_addr_resolved, eth_lg_raw, eth_lg, eth_ig_raw, eth_ig, eth_src_resolved_raw, eth_src_resolved)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eth.dst_resolved_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_dst_resolved_raw)
        result["eth.dst_resolved"] = from_union([from_str, from_none], self.eth_dst_resolved)
        result["eth.addr_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_addr_raw)
        result["eth.addr"] = from_union([from_str, from_none], self.eth_addr)
        result["eth.addr_resolved_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_addr_resolved_raw)
        result["eth.addr_resolved"] = from_union([from_str, from_none], self.eth_addr_resolved)
        result["eth.lg_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.eth_lg_raw)
        result["eth.lg"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.eth_lg)
        result["eth.ig_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.eth_ig_raw)
        result["eth.ig"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.eth_ig)
        result["eth.src_resolved_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_src_resolved_raw)
        result["eth.src_resolved"] = from_union([from_str, from_none], self.eth_src_resolved)
        return result


@dataclass
class Eth:
    eth_dst_raw: Optional[List[Union[int, str]]]
    eth_dst: Optional[str]
    eth_dst_tree: Optional[EthTree]
    eth_src_raw: Optional[List[Union[int, str]]]
    eth_src: Optional[str]
    eth_src_tree: Optional[EthTree]
    eth_type_raw: Optional[List[Union[int, str]]]
    eth_type: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Eth':
        assert isinstance(obj, dict)
        eth_dst_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.dst_raw"))
        eth_dst = from_union([from_str, from_none], obj.get("eth.dst"))
        eth_dst_tree = from_union([EthTree.from_dict, from_none], obj.get("eth.dst_tree"))
        eth_src_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.src_raw"))
        eth_src = from_union([from_str, from_none], obj.get("eth.src"))
        eth_src_tree = from_union([EthTree.from_dict, from_none], obj.get("eth.src_tree"))
        eth_type_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth.type_raw"))
        eth_type = from_union([from_str, from_none], obj.get("eth.type"))
        return Eth(eth_dst_raw, eth_dst, eth_dst_tree, eth_src_raw, eth_src, eth_src_tree, eth_type_raw, eth_type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["eth.dst_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_dst_raw)
        result["eth.dst"] = from_union([from_str, from_none], self.eth_dst)
        result["eth.dst_tree"] = from_union([lambda x: to_class(EthTree, x), from_none], self.eth_dst_tree)
        result["eth.src_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_src_raw)
        result["eth.src"] = from_union([from_str, from_none], self.eth_src)
        result["eth.src_tree"] = from_union([lambda x: to_class(EthTree, x), from_none], self.eth_src_tree)
        result["eth.type_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_type_raw)
        result["eth.type"] = from_union([from_str, from_none], self.eth_type)
        return result


@dataclass
class FrameInterfaceIDTree:
    frame_interface_name: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'FrameInterfaceIDTree':
        assert isinstance(obj, dict)
        frame_interface_name = from_union([from_str, from_none], obj.get("frame.interface_name"))
        return FrameInterfaceIDTree(frame_interface_name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["frame.interface_name"] = from_union([from_str, from_none], self.frame_interface_name)
        return result


@dataclass
class Frame:
    frame_interface_id: Optional[int]
    frame_interface_id_tree: Optional[FrameInterfaceIDTree]
    frame_encap_type: Optional[int]
    frame_time: Optional[str]
    frame_offset_shift: Optional[str]
    frame_time_epoch: Optional[str]
    frame_time_delta: Optional[str]
    frame_time_delta_displayed: Optional[str]
    frame_time_relative: Optional[str]
    frame_number: Optional[int]
    frame_len: Optional[int]
    frame_cap_len: Optional[int]
    frame_marked: Optional[int]
    frame_ignored: Optional[int]
    frame_protocols: Optional[str]
    frame_coloring_rule_name: Optional[str]
    frame_coloring_rule_string: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Frame':
        assert isinstance(obj, dict)
        frame_interface_id = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.interface_id"))
        frame_interface_id_tree = from_union([FrameInterfaceIDTree.from_dict, from_none], obj.get("frame.interface_id_tree"))
        frame_encap_type = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.encap_type"))
        frame_time = from_union([from_str, from_none], obj.get("frame.time"))
        frame_offset_shift = from_union([from_str, from_none], obj.get("frame.offset_shift"))
        frame_time_epoch = from_union([from_str, from_none], obj.get("frame.time_epoch"))
        frame_time_delta = from_union([from_str, from_none], obj.get("frame.time_delta"))
        frame_time_delta_displayed = from_union([from_str, from_none], obj.get("frame.time_delta_displayed"))
        frame_time_relative = from_union([from_str, from_none], obj.get("frame.time_relative"))
        frame_number = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.number"))
        frame_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.len"))
        frame_cap_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.cap_len"))
        frame_marked = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.marked"))
        frame_ignored = from_union([from_none, lambda x: int(from_str(x))], obj.get("frame.ignored"))
        frame_protocols = from_union([from_str, from_none], obj.get("frame.protocols"))
        frame_coloring_rule_name = from_union([from_str, from_none], obj.get("frame.coloring_rule.name"))
        frame_coloring_rule_string = from_union([from_str, from_none], obj.get("frame.coloring_rule.string"))
        return Frame(frame_interface_id, frame_interface_id_tree, frame_encap_type, frame_time, frame_offset_shift, frame_time_epoch, frame_time_delta, frame_time_delta_displayed, frame_time_relative, frame_number, frame_len, frame_cap_len, frame_marked, frame_ignored, frame_protocols, frame_coloring_rule_name, frame_coloring_rule_string)

    def to_dict(self) -> dict:
        result: dict = {}
        result["frame.interface_id"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_interface_id)
        result["frame.interface_id_tree"] = from_union([lambda x: to_class(FrameInterfaceIDTree, x), from_none], self.frame_interface_id_tree)
        result["frame.encap_type"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_encap_type)
        result["frame.time"] = from_union([from_str, from_none], self.frame_time)
        result["frame.offset_shift"] = from_union([from_str, from_none], self.frame_offset_shift)
        result["frame.time_epoch"] = from_union([from_str, from_none], self.frame_time_epoch)
        result["frame.time_delta"] = from_union([from_str, from_none], self.frame_time_delta)
        result["frame.time_delta_displayed"] = from_union([from_str, from_none], self.frame_time_delta_displayed)
        result["frame.time_relative"] = from_union([from_str, from_none], self.frame_time_relative)
        result["frame.number"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_number)
        result["frame.len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_len)
        result["frame.cap_len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_cap_len)
        result["frame.marked"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_marked)
        result["frame.ignored"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.frame_ignored)
        result["frame.protocols"] = from_union([from_str, from_none], self.frame_protocols)
        result["frame.coloring_rule.name"] = from_union([from_str, from_none], self.frame_coloring_rule_name)
        result["frame.coloring_rule.string"] = from_union([from_str, from_none], self.frame_coloring_rule_string)
        return result


@dataclass
class IPDsfieldTree:
    ip_dsfield_dscp_raw: Optional[List[int]]
    ip_dsfield_dscp: Optional[int]
    ip_dsfield_ecn_raw: Optional[List[int]]
    ip_dsfield_ecn: Optional[int]

    @staticmethod
    def from_dict(obj: Any) -> 'IPDsfieldTree':
        assert isinstance(obj, dict)
        ip_dsfield_dscp_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.dsfield.dscp_raw"))
        ip_dsfield_dscp = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.dsfield.dscp"))
        ip_dsfield_ecn_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.dsfield.ecn_raw"))
        ip_dsfield_ecn = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.dsfield.ecn"))
        return IPDsfieldTree(ip_dsfield_dscp_raw, ip_dsfield_dscp, ip_dsfield_ecn_raw, ip_dsfield_ecn)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ip.dsfield.dscp_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_dsfield_dscp_raw)
        result["ip.dsfield.dscp"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_dsfield_dscp)
        result["ip.dsfield.ecn_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_dsfield_ecn_raw)
        result["ip.dsfield.ecn"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_dsfield_ecn)
        return result


@dataclass
class IPFlagsTree:
    ip_flags_rb_raw: Optional[List[int]]
    ip_flags_rb: Optional[int]
    ip_flags_df_raw: Optional[List[int]]
    ip_flags_df: Optional[int]
    ip_flags_mf_raw: Optional[List[int]]
    ip_flags_mf: Optional[int]
    ip_frag_offset_raw: Optional[List[int]]
    ip_frag_offset: Optional[int]

    @staticmethod
    def from_dict(obj: Any) -> 'IPFlagsTree':
        assert isinstance(obj, dict)
        ip_flags_rb_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.flags.rb_raw"))
        ip_flags_rb = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.flags.rb"))
        ip_flags_df_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.flags.df_raw"))
        ip_flags_df = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.flags.df"))
        ip_flags_mf_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.flags.mf_raw"))
        ip_flags_mf = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.flags.mf"))
        ip_frag_offset_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.frag_offset_raw"))
        ip_frag_offset = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.frag_offset"))
        return IPFlagsTree(ip_flags_rb_raw, ip_flags_rb, ip_flags_df_raw, ip_flags_df, ip_flags_mf_raw, ip_flags_mf, ip_frag_offset_raw, ip_frag_offset)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ip.flags.rb_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_flags_rb_raw)
        result["ip.flags.rb"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_flags_rb)
        result["ip.flags.df_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_flags_df_raw)
        result["ip.flags.df"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_flags_df)
        result["ip.flags.mf_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_flags_mf_raw)
        result["ip.flags.mf"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_flags_mf)
        result["ip.frag_offset_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_frag_offset_raw)
        result["ip.frag_offset"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_frag_offset)
        return result


@dataclass
class IP:
    ip_version_raw: Optional[List[int]]
    ip_version: Optional[int]
    ip_hdr_len_raw: Optional[List[int]]
    ip_hdr_len: Optional[int]
    ip_dsfield_raw: Optional[List[Union[int, str]]]
    ip_dsfield: Optional[str]
    ip_dsfield_tree: Optional[IPDsfieldTree]
    ip_len_raw: Optional[List[Union[int, str]]]
    ip_len: Optional[int]
    ip_id_raw: Optional[List[Union[int, str]]]
    ip_id: Optional[str]
    ip_flags_raw: Optional[List[int]]
    ip_flags: Optional[str]
    ip_flags_tree: Optional[IPFlagsTree]
    ip_ttl_raw: Optional[List[int]]
    ip_ttl: Optional[int]
    ip_proto_raw: Optional[List[Union[int, str]]]
    ip_proto: Optional[int]
    ip_checksum_raw: Optional[List[Union[int, str]]]
    ip_checksum: Optional[str]
    ip_checksum_status: Optional[int]
    ip_src_raw: Optional[List[Union[int, str]]]
    ip_src: Optional[str]
    ip_addr_raw: Optional[List[Union[int, str]]]
    ip_addr: Optional[str]
    ip_src_host_raw: Optional[List[Union[int, str]]]
    ip_src_host: Optional[str]
    ip_host_raw: Optional[List[Union[int, str]]]
    ip_host: Optional[str]
    ip_dst_raw: Optional[List[Union[int, str]]]
    ip_dst: Optional[str]
    ip_dst_host_raw: Optional[List[Union[int, str]]]
    ip_dst_host: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'IP':
        assert isinstance(obj, dict)
        ip_version_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.version_raw"))
        ip_version = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.version"))
        ip_hdr_len_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.hdr_len_raw"))
        ip_hdr_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.hdr_len"))
        ip_dsfield_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.dsfield_raw"))
        ip_dsfield = from_union([from_str, from_none], obj.get("ip.dsfield"))
        ip_dsfield_tree = from_union([IPDsfieldTree.from_dict, from_none], obj.get("ip.dsfield_tree"))
        ip_len_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.len_raw"))
        ip_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.len"))
        ip_id_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.id_raw"))
        ip_id = from_union([from_str, from_none], obj.get("ip.id"))
        ip_flags_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.flags_raw"))
        ip_flags = from_union([from_str, from_none], obj.get("ip.flags"))
        ip_flags_tree = from_union([IPFlagsTree.from_dict, from_none], obj.get("ip.flags_tree"))
        ip_ttl_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("ip.ttl_raw"))
        ip_ttl = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.ttl"))
        ip_proto_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.proto_raw"))
        ip_proto = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.proto"))
        ip_checksum_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.checksum_raw"))
        ip_checksum = from_union([from_str, from_none], obj.get("ip.checksum"))
        ip_checksum_status = from_union([from_none, lambda x: int(from_str(x))], obj.get("ip.checksum.status"))
        ip_src_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.src_raw"))
        ip_src = from_union([from_str, from_none], obj.get("ip.src"))
        ip_addr_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.addr_raw"))
        ip_addr = from_union([from_str, from_none], obj.get("ip.addr"))
        ip_src_host_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.src_host_raw"))
        ip_src_host = from_union([from_str, from_none], obj.get("ip.src_host"))
        ip_host_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.host_raw"))
        ip_host = from_union([from_str, from_none], obj.get("ip.host"))
        ip_dst_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.dst_raw"))
        ip_dst = from_union([from_str, from_none], obj.get("ip.dst"))
        ip_dst_host_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip.dst_host_raw"))
        ip_dst_host = from_union([from_str, from_none], obj.get("ip.dst_host"))
        return IP(ip_version_raw, ip_version, ip_hdr_len_raw, ip_hdr_len, ip_dsfield_raw, ip_dsfield, ip_dsfield_tree, ip_len_raw, ip_len, ip_id_raw, ip_id, ip_flags_raw, ip_flags, ip_flags_tree, ip_ttl_raw, ip_ttl, ip_proto_raw, ip_proto, ip_checksum_raw, ip_checksum, ip_checksum_status, ip_src_raw, ip_src, ip_addr_raw, ip_addr, ip_src_host_raw, ip_src_host, ip_host_raw, ip_host, ip_dst_raw, ip_dst, ip_dst_host_raw, ip_dst_host)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ip.version_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_version_raw)
        result["ip.version"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_version)
        result["ip.hdr_len_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_hdr_len_raw)
        result["ip.hdr_len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_hdr_len)
        result["ip.dsfield_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_dsfield_raw)
        result["ip.dsfield"] = from_union([from_str, from_none], self.ip_dsfield)
        result["ip.dsfield_tree"] = from_union([lambda x: to_class(IPDsfieldTree, x), from_none], self.ip_dsfield_tree)
        result["ip.len_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_len_raw)
        result["ip.len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_len)
        result["ip.id_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_id_raw)
        result["ip.id"] = from_union([from_str, from_none], self.ip_id)
        result["ip.flags_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_flags_raw)
        result["ip.flags"] = from_union([from_str, from_none], self.ip_flags)
        result["ip.flags_tree"] = from_union([lambda x: to_class(IPFlagsTree, x), from_none], self.ip_flags_tree)
        result["ip.ttl_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.ip_ttl_raw)
        result["ip.ttl"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_ttl)
        result["ip.proto_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_proto_raw)
        result["ip.proto"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_proto)
        result["ip.checksum_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_checksum_raw)
        result["ip.checksum"] = from_union([from_str, from_none], self.ip_checksum)
        result["ip.checksum.status"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.ip_checksum_status)
        result["ip.src_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_src_raw)
        result["ip.src"] = from_union([from_str, from_none], self.ip_src)
        result["ip.addr_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_addr_raw)
        result["ip.addr"] = from_union([from_str, from_none], self.ip_addr)
        result["ip.src_host_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_src_host_raw)
        result["ip.src_host"] = from_union([from_str, from_none], self.ip_src_host)
        result["ip.host_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_host_raw)
        result["ip.host"] = from_union([from_str, from_none], self.ip_host)
        result["ip.dst_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_dst_raw)
        result["ip.dst"] = from_union([from_str, from_none], self.ip_dst)
        result["ip.dst_host_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_dst_host_raw)
        result["ip.dst_host"] = from_union([from_str, from_none], self.ip_dst_host)
        return result


@dataclass
class TCPAnalysis:
    tcp_analysis_initial_rtt: Optional[str]
    tcp_analysis_bytes_in_flight: Optional[int]
    tcp_analysis_push_bytes_sent: Optional[int]
    tcp_analysis_acks_frame: Optional[int]
    tcp_analysis_ack_rtt: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'TCPAnalysis':
        assert isinstance(obj, dict)
        tcp_analysis_initial_rtt = from_union([from_str, from_none], obj.get("tcp.analysis.initial_rtt"))
        tcp_analysis_bytes_in_flight = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.analysis.bytes_in_flight"))
        tcp_analysis_push_bytes_sent = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.analysis.push_bytes_sent"))
        tcp_analysis_acks_frame = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.analysis.acks_frame"))
        tcp_analysis_ack_rtt = from_union([from_str, from_none], obj.get("tcp.analysis.ack_rtt"))
        return TCPAnalysis(tcp_analysis_initial_rtt, tcp_analysis_bytes_in_flight, tcp_analysis_push_bytes_sent, tcp_analysis_acks_frame, tcp_analysis_ack_rtt)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tcp.analysis.initial_rtt"] = from_union([from_str, from_none], self.tcp_analysis_initial_rtt)
        result["tcp.analysis.bytes_in_flight"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_analysis_bytes_in_flight)
        result["tcp.analysis.push_bytes_sent"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_analysis_push_bytes_sent)
        result["tcp.analysis.acks_frame"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_analysis_acks_frame)
        result["tcp.analysis.ack_rtt"] = from_union([from_str, from_none], self.tcp_analysis_ack_rtt)
        return result


@dataclass
class TCPFlagsTree:
    tcp_flags_res_raw: Optional[List[int]]
    tcp_flags_res: Optional[int]
    tcp_flags_ns_raw: Optional[List[int]]
    tcp_flags_ns: Optional[int]
    tcp_flags_cwr_raw: Optional[List[int]]
    tcp_flags_cwr: Optional[int]
    tcp_flags_ecn_raw: Optional[List[int]]
    tcp_flags_ecn: Optional[int]
    tcp_flags_urg_raw: Optional[List[int]]
    tcp_flags_urg: Optional[int]
    tcp_flags_ack_raw: Optional[List[int]]
    tcp_flags_ack: Optional[int]
    tcp_flags_push_raw: Optional[List[int]]
    tcp_flags_push: Optional[int]
    tcp_flags_reset_raw: Optional[List[int]]
    tcp_flags_reset: Optional[int]
    tcp_flags_syn_raw: Optional[List[int]]
    tcp_flags_syn: Optional[int]
    tcp_flags_fin_raw: Optional[List[int]]
    tcp_flags_fin: Optional[int]
    tcp_flags_str_raw: Optional[List[int]]
    tcp_flags_str: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'TCPFlagsTree':
        assert isinstance(obj, dict)
        tcp_flags_res_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.res_raw"))
        tcp_flags_res = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.res"))
        tcp_flags_ns_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.ns_raw"))
        tcp_flags_ns = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.ns"))
        tcp_flags_cwr_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.cwr_raw"))
        tcp_flags_cwr = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.cwr"))
        tcp_flags_ecn_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.ecn_raw"))
        tcp_flags_ecn = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.ecn"))
        tcp_flags_urg_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.urg_raw"))
        tcp_flags_urg = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.urg"))
        tcp_flags_ack_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.ack_raw"))
        tcp_flags_ack = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.ack"))
        tcp_flags_push_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.push_raw"))
        tcp_flags_push = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.push"))
        tcp_flags_reset_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.reset_raw"))
        tcp_flags_reset = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.reset"))
        tcp_flags_syn_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.syn_raw"))
        tcp_flags_syn = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.syn"))
        tcp_flags_fin_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.fin_raw"))
        tcp_flags_fin = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.flags.fin"))
        tcp_flags_str_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags.str_raw"))
        tcp_flags_str = from_union([from_str, from_none], obj.get("tcp.flags.str"))
        return TCPFlagsTree(tcp_flags_res_raw, tcp_flags_res, tcp_flags_ns_raw, tcp_flags_ns, tcp_flags_cwr_raw, tcp_flags_cwr, tcp_flags_ecn_raw, tcp_flags_ecn, tcp_flags_urg_raw, tcp_flags_urg, tcp_flags_ack_raw, tcp_flags_ack, tcp_flags_push_raw, tcp_flags_push, tcp_flags_reset_raw, tcp_flags_reset, tcp_flags_syn_raw, tcp_flags_syn, tcp_flags_fin_raw, tcp_flags_fin, tcp_flags_str_raw, tcp_flags_str)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tcp.flags.res_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_res_raw)
        result["tcp.flags.res"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_res)
        result["tcp.flags.ns_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_ns_raw)
        result["tcp.flags.ns"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_ns)
        result["tcp.flags.cwr_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_cwr_raw)
        result["tcp.flags.cwr"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_cwr)
        result["tcp.flags.ecn_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_ecn_raw)
        result["tcp.flags.ecn"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_ecn)
        result["tcp.flags.urg_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_urg_raw)
        result["tcp.flags.urg"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_urg)
        result["tcp.flags.ack_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_ack_raw)
        result["tcp.flags.ack"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_ack)
        result["tcp.flags.push_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_push_raw)
        result["tcp.flags.push"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_push)
        result["tcp.flags.reset_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_reset_raw)
        result["tcp.flags.reset"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_reset)
        result["tcp.flags.syn_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_syn_raw)
        result["tcp.flags.syn"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_syn)
        result["tcp.flags.fin_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_fin_raw)
        result["tcp.flags.fin"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_flags_fin)
        result["tcp.flags.str_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_str_raw)
        result["tcp.flags.str"] = from_union([from_str, from_none], self.tcp_flags_str)
        return result


@dataclass
class Timestamps:
    tcp_time_relative: Optional[str]
    tcp_time_delta: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'Timestamps':
        assert isinstance(obj, dict)
        tcp_time_relative = from_union([from_str, from_none], obj.get("tcp.time_relative"))
        tcp_time_delta = from_union([from_str, from_none], obj.get("tcp.time_delta"))
        return Timestamps(tcp_time_relative, tcp_time_delta)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tcp.time_relative"] = from_union([from_str, from_none], self.tcp_time_relative)
        result["tcp.time_delta"] = from_union([from_str, from_none], self.tcp_time_delta)
        return result


@dataclass
class TCP:
    tcp_srcport_raw: Optional[List[Union[int, str]]]
    tcp_srcport: Optional[int]
    tcp_dstport_raw: Optional[List[Union[int, str]]]
    tcp_dstport: Optional[int]
    tcp_port_raw: Optional[List[Union[int, str]]]
    tcp_port: Optional[int]
    tcp_stream: Optional[int]
    tcp_len_raw: Optional[List[int]]
    tcp_len: Optional[int]
    tcp_seq_raw: Optional[List[Union[int, str]]]
    tcp_seq: Optional[int]
    tcp_nxtseq: Optional[int]
    tcp_ack_raw: Optional[List[Union[int, str]]]
    tcp_ack: Optional[int]
    tcp_hdr_len_raw: Optional[List[int]]
    tcp_hdr_len: Optional[int]
    tcp_flags_raw: Optional[List[int]]
    tcp_flags: Optional[str]
    tcp_flags_tree: Optional[TCPFlagsTree]
    tcp_window_size_value_raw: Optional[List[Union[int, str]]]
    tcp_window_size_value: Optional[int]
    tcp_window_size_raw: Optional[List[Union[int, str]]]
    tcp_window_size: Optional[int]
    tcp_window_size_scalefactor_raw: Optional[List[Union[int, str]]]
    tcp_window_size_scalefactor: Optional[int]
    tcp_checksum_raw: Optional[List[Union[int, str]]]
    tcp_checksum: Optional[str]
    tcp_checksum_status: Optional[int]
    tcp_urgent_pointer_raw: Optional[List[Union[int, str]]]
    tcp_urgent_pointer: Optional[int]
    tcp_analysis: Optional[TCPAnalysis]
    timestamps: Optional[Timestamps]
    tcp_payload_raw: Optional[List[Union[int, str]]]
    tcp_payload: Optional[str]

    @staticmethod
    def from_dict(obj: Any) -> 'TCP':
        assert isinstance(obj, dict)
        tcp_srcport_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.srcport_raw"))
        tcp_srcport = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.srcport"))
        tcp_dstport_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.dstport_raw"))
        tcp_dstport = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.dstport"))
        tcp_port_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.port_raw"))
        tcp_port = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.port"))
        tcp_stream = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.stream"))
        tcp_len_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.len_raw"))
        tcp_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.len"))
        tcp_seq_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.seq_raw"))
        tcp_seq = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.seq"))
        tcp_nxtseq = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.nxtseq"))
        tcp_ack_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.ack_raw"))
        tcp_ack = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.ack"))
        tcp_hdr_len_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.hdr_len_raw"))
        tcp_hdr_len = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.hdr_len"))
        tcp_flags_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, lambda x: int(from_str(x))], x), x), from_none], obj.get("tcp.flags_raw"))
        tcp_flags = from_union([from_str, from_none], obj.get("tcp.flags"))
        tcp_flags_tree = from_union([TCPFlagsTree.from_dict, from_none], obj.get("tcp.flags_tree"))
        tcp_window_size_value_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.window_size_value_raw"))
        tcp_window_size_value = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.window_size_value"))
        tcp_window_size_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.window_size_raw"))
        tcp_window_size = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.window_size"))
        tcp_window_size_scalefactor_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.window_size_scalefactor_raw"))
        tcp_window_size_scalefactor = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.window_size_scalefactor"))
        tcp_checksum_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.checksum_raw"))
        tcp_checksum = from_union([from_str, from_none], obj.get("tcp.checksum"))
        tcp_checksum_status = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.checksum.status"))
        tcp_urgent_pointer_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.urgent_pointer_raw"))
        tcp_urgent_pointer = from_union([from_none, lambda x: int(from_str(x))], obj.get("tcp.urgent_pointer"))
        tcp_analysis = from_union([TCPAnalysis.from_dict, from_none], obj.get("tcp.analysis"))
        timestamps = from_union([Timestamps.from_dict, from_none], obj.get("Timestamps"))
        tcp_payload_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp.payload_raw"))
        tcp_payload = from_union([from_str, from_none], obj.get("tcp.payload"))
        return TCP(tcp_srcport_raw, tcp_srcport, tcp_dstport_raw, tcp_dstport, tcp_port_raw, tcp_port, tcp_stream, tcp_len_raw, tcp_len, tcp_seq_raw, tcp_seq, tcp_nxtseq, tcp_ack_raw, tcp_ack, tcp_hdr_len_raw, tcp_hdr_len, tcp_flags_raw, tcp_flags, tcp_flags_tree, tcp_window_size_value_raw, tcp_window_size_value, tcp_window_size_raw, tcp_window_size, tcp_window_size_scalefactor_raw, tcp_window_size_scalefactor, tcp_checksum_raw, tcp_checksum, tcp_checksum_status, tcp_urgent_pointer_raw, tcp_urgent_pointer, tcp_analysis, timestamps, tcp_payload_raw, tcp_payload)

    def to_dict(self) -> dict:
        result: dict = {}
        result["tcp.srcport_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_srcport_raw)
        result["tcp.srcport"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_srcport)
        result["tcp.dstport_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_dstport_raw)
        result["tcp.dstport"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_dstport)
        result["tcp.port_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_port_raw)
        result["tcp.port"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_port)
        result["tcp.stream"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_stream)
        result["tcp.len_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_len_raw)
        result["tcp.len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_len)
        result["tcp.seq_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_seq_raw)
        result["tcp.seq"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_seq)
        result["tcp.nxtseq"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_nxtseq)
        result["tcp.ack_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_ack_raw)
        result["tcp.ack"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_ack)
        result["tcp.hdr_len_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_hdr_len_raw)
        result["tcp.hdr_len"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_hdr_len)
        result["tcp.flags_raw"] = from_union([lambda x: from_list(from_int, x), from_none], self.tcp_flags_raw)
        result["tcp.flags"] = from_union([from_str, from_none], self.tcp_flags)
        result["tcp.flags_tree"] = from_union([lambda x: to_class(TCPFlagsTree, x), from_none], self.tcp_flags_tree)
        result["tcp.window_size_value_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_window_size_value_raw)
        result["tcp.window_size_value"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_window_size_value)
        result["tcp.window_size_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_window_size_raw)
        result["tcp.window_size"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_window_size)
        result["tcp.window_size_scalefactor_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_window_size_scalefactor_raw)
        result["tcp.window_size_scalefactor"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_window_size_scalefactor)
        result["tcp.checksum_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_checksum_raw)
        result["tcp.checksum"] = from_union([from_str, from_none], self.tcp_checksum)
        result["tcp.checksum.status"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_checksum_status)
        result["tcp.urgent_pointer_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_urgent_pointer_raw)
        result["tcp.urgent_pointer"] = from_union([lambda x: from_none((lambda x: is_type(type(None), x))(x)), lambda x: from_str((lambda x: str((lambda x: is_type(int, x))(x)))(x))], self.tcp_urgent_pointer)
        result["tcp.analysis"] = from_union([lambda x: to_class(TCPAnalysis, x), from_none], self.tcp_analysis)
        result["Timestamps"] = from_union([lambda x: to_class(Timestamps, x), from_none], self.timestamps)
        result["tcp.payload_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_payload_raw)
        result["tcp.payload"] = from_union([from_str, from_none], self.tcp_payload)
        return result


@dataclass
class Layers:
    frame_raw: Optional[List[Union[int, str]]]
    frame: Optional[Frame]
    eth_raw: Optional[List[Union[int, str]]]
    eth: Optional[Eth]
    ip_raw: Optional[List[Union[int, str]]]
    ip: Optional[IP]
    tcp_raw: Optional[List[Union[int, str]]]
    tcp: Optional[TCP]
    data_raw: Optional[List[Union[int, str]]]
    data: Optional[Data]

    @staticmethod
    def from_dict(obj: Any) -> 'Layers':
        assert isinstance(obj, dict)
        frame_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("frame_raw"))
        frame = from_union([Frame.from_dict, from_none], obj.get("frame"))
        eth_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("eth_raw"))
        eth = from_union([Eth.from_dict, from_none], obj.get("eth"))
        ip_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("ip_raw"))
        ip = from_union([IP.from_dict, from_none], obj.get("ip"))
        tcp_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("tcp_raw"))
        tcp = from_union([TCP.from_dict, from_none], obj.get("tcp"))
        data_raw = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], obj.get("data_raw"))
        data = from_union([Data.from_dict, from_none], obj.get("data"))
        return Layers(frame_raw, frame, eth_raw, eth, ip_raw, ip, tcp_raw, tcp, data_raw, data)

    def to_dict(self) -> dict:
        result: dict = {}
        result["frame_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.frame_raw)
        result["frame"] = from_union([lambda x: to_class(Frame, x), from_none], self.frame)
        result["eth_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.eth_raw)
        result["eth"] = from_union([lambda x: to_class(Eth, x), from_none], self.eth)
        result["ip_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.ip_raw)
        result["ip"] = from_union([lambda x: to_class(IP, x), from_none], self.ip)
        result["tcp_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.tcp_raw)
        result["tcp"] = from_union([lambda x: to_class(TCP, x), from_none], self.tcp)
        result["data_raw"] = from_union([lambda x: from_list(lambda x: from_union([from_int, from_str], x), x), from_none], self.data_raw)
        result["data"] = from_union([lambda x: to_class(Data, x), from_none], self.data)
        return result


@dataclass
class Source:
    layers: Optional[Layers]

    @staticmethod
    def from_dict(obj: Any) -> 'Source':
        assert isinstance(obj, dict)
        layers = from_union([Layers.from_dict, from_none], obj.get("layers"))
        return Source(layers)

    def to_dict(self) -> dict:
        result: dict = {}
        result["layers"] = from_union([lambda x: to_class(Layers, x), from_none], self.layers)
        return result


@dataclass
class MsgElement:
    index: Optional[str]
    type: Optional[str]
    score: None
    source: Optional[Source]

    @staticmethod
    def from_dict(obj: Any) -> 'MsgElement':
        assert isinstance(obj, dict)
        index = from_union([from_str, from_none], obj.get("_index"))
        type = from_union([from_str, from_none], obj.get("_type"))
        score = from_none(obj.get("_score"))
        source = from_union([Source.from_dict, from_none], obj.get("_source"))
        return MsgElement(index, type, score, source)

    def to_dict(self) -> dict:
        result: dict = {}
        result["_index"] = from_union([from_str, from_none], self.index)
        result["_type"] = from_union([from_str, from_none], self.type)
        result["_score"] = from_none(self.score)
        result["_source"] = from_union([lambda x: to_class(Source, x), from_none], self.source)
        return result


def msg_from_dict(s: Any) -> List[MsgElement]:
    return from_list(MsgElement.from_dict, s)


def msg_to_dict(x: List[MsgElement]) -> Any:
    return from_list(lambda x: to_class(MsgElement, x), x)


from Utilities.BytesToMessage import getMessageFromBytes

IN_FILE = '../../captures/export.json'
OUT_FILE_CSV = '../../captures/summary.csv'
OUT_FILE_JSON = '../../captures/messageList.json'
OUT_FILE_TXT = '../../captures/conversationOverview.txt'

with open(IN_FILE, 'r') as file:
    result = msg_from_dict(json.load(file))

foutCSV = open(OUT_FILE_CSV, 'w')
foutJSON = open(OUT_FILE_JSON, 'w')
foutTxt = open(OUT_FILE_TXT, 'w')

foutCSV.write("tcp.stream,ip.src,tcp.srcport,ip.dst,tcp.dstport,message 9XX,frame #,#\n")

msgList = []
rowNum = 1

last_ip = result[0].source.layers.ip.ip_src
last_stream = result[0].source.layers.tcp.tcp_stream
last_msgNum = getMessageFromBytes(bytearray([int(x, 16) for x in result[0].source.layers.tcp.tcp_payload.split(':')])).header.messageId.data

freqs = {}
msgCounts = []
currCount = -1

for res in result:
    ip_src = res.source.layers.ip.ip_src
    tcp_src_port = res.source.layers.tcp.tcp_srcport
    ip_dst = res.source.layers.ip.ip_dst
    tcp_dst_port = res.source.layers.tcp.tcp_dstport
    tcp_stream = res.source.layers.tcp.tcp_stream
    frameNum = res.source.layers.frame.frame_number
    # message = res.source.layers.data.data_data
    message = res.source.layers.tcp.tcp_payload
    split = message.split(':')
    byteList = bytearray([int(x, 16) for x in split])
    msgObj = getMessageFromBytes(byteList)
    msgNum = msgObj.header.messageId.data
    if msgNum not in freqs:
        freqs[msgNum] = 0
    freqs[msgNum] += 1
    dataRow = [tcp_stream, ip_src, tcp_src_port, ip_dst, tcp_dst_port, msgNum, frameNum, rowNum]
    dataString = ','.join(map(str, dataRow))
    dataString += '\n'
    if ip_src != last_ip or tcp_stream != last_stream:
        foutCSV.write('\n')
    if msgNum != last_msgNum:
        msgCounts.append((last_msgNum, currCount + 1))
        last_msgNum = msgNum
        currCount = 0
    else:
        currCount += 1
    last_ip = ip_src
    last_stream = tcp_stream
    foutCSV.write(dataString)

    msgDict = {}
    msgDict['ip.src'] = ip_src
    msgDict['ip_dst'] = ip_dst
    msgDict['frame_number'] = frameNum
    msgDict['msg'] = msgObj.getDataObject(useEnums=True)
    msgList.append(msgDict)
    rowNum += 1

msgCounts.append((last_msgNum, currCount + 1))

json.dump(msgList, foutJSON, indent=4, separators=(',', ': '))

foutCSV.write('\n\nmsg,freq\n')
for k,v in freqs.items():
    dataRow = [k,v]
    dataString = ','.join(map(str, dataRow))
    dataString += '\n'
    foutCSV.write(dataString)

for num,count in msgCounts:
    row = '' + str(num) + ' - ' + str(count) + '\n'
    foutTxt.write(row)
