export interface Chat {
    content: string;
    blockId?: string;
    type: "text" | "image" | "attachment";
    bubbles: ChatBubble[];
}
export declare class ChatBubble {
    label: string;
    value: string;
    protected type: "link" | "button" | "text" | 'chip' | "input";
    constructor(label: string, value: string);
    static fromJson(json: Record<string, any>): ChatBubble;
    setType(type: "text" | "link" | "button" | "chip" | "input"): this;
    asButton(): this;
    asChip(): this;
    asLink(): this;
    asText(): this;
    asInput(): this;
}
export declare class Chat {
    content: string;
    bubbles: ChatBubble[];
    type: "text" | "image" | "attachment";
    blockId?: string;
    constructor(content: string, bubbles?: ChatBubble[]);
    static fromJson(json: Record<string, any>): Chat;
    setType(type: "text" | "image" | "attachment"): this;
    setBlockId(blockId: string): this;
    addBubble(bubble: ChatBubble): this;
    asText(): this;
    asImage(): this;
    asAttachment(): this;
}
