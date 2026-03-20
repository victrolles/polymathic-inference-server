import type { SelectablePackets, SelectablePacket, DatasetLocations, Packets } from "../types/types";


export function setPacketSelection(selectable_packets: SelectablePackets, selectable_packet: SelectablePacket, multiple_selection: boolean, index_modality: number) {
    if (multiple_selection) {
        return selectable_packets.map((smf) => {
            if (smf.packet.modalities[index_modality].media_file.id === selectable_packet.packet.modalities[index_modality].media_file.id) {
                return { ...smf, is_selected: !smf.is_selected };
            }
            return smf;
        });
    } else {
        return selectable_packets.map((smf) => {
            if (smf.packet.modalities[index_modality].media_file.id === selectable_packet.packet.modalities[index_modality].media_file.id) {
                return { ...smf, is_selected: true };
            }
            return { ...smf, is_selected: false };
        });
    }
}

export function getSelectedDatasetLocations(selectable_packets: SelectablePackets): DatasetLocations {
    return selectable_packets.filter((sp) => sp.is_selected).map((sp) => sp.packet.origin) as DatasetLocations;
}

export function getSelectedPackets(selectable_packets: SelectablePackets): Packets {
    return selectable_packets.filter((sp) => sp.is_selected).map((sp) => sp.packet) as Packets;
}

export function numberOfSelectedPackets(selectable_packets: SelectablePackets): number {
    return selectable_packets.filter((sp) => sp.is_selected).length;
}