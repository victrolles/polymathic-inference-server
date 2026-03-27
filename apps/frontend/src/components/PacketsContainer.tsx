import type { PacketsContainerProps } from "../types/interfaces";
import LoadingItem from "./LoadingItem";
import PacketItem from "./PacketItem";

function PacketsContainer({ packets, configDict, media_size, status }: PacketsContainerProps) {
    return (
        <div className="packets-container">
            {packets.length > 0 && packets.map((packet) => (
                <PacketItem
                    key={packet.modalities[0].media_file.id}
                    packet={packet}
                    configDict={configDict}
                    media_size={media_size}
                />
            ))}
            {packets.length === 0 && status === "loading" &&
                Array.from({ length: 1 }).map((_, i) => (
                    <LoadingItem
                        key={i}
                        media_size={media_size}
                    />
                ))}
        </div>
    );
}

export default PacketsContainer;