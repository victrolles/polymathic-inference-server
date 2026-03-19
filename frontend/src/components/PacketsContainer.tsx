import type { PacketsContainerProps } from "../types/interfaces";
import PacketItem from "./PacketItem";

function PacketsContainer({ packets, configDict, media_size }: PacketsContainerProps) {

    console.log("packets", packets);

    return (
        <div className="packets-container">
            {packets.map((packet) => (
                <PacketItem
                    key={packet.modalities[0].media_file.id}
                    packet={packet}
                    configDict={configDict}
                    media_size={media_size}
                />
            ))}
        </div>
    );
}

export default PacketsContainer;