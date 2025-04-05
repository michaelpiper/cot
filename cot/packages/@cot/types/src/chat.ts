export interface Chat {
    content: string
    blockId?: string
    type: "text" | "image" | "attachment"
    bubbles: ChatBubble[]
}
export class ChatBubble {
    protected type!: "link" | "button" | "text" | 'chip' | "input"
    constructor(public label: string, public value: string) {

    }
    
    static fromJson(json:Record<string, any>){
        return new ChatBubble(json['label'], json['value'])
        .setType(json['type'])
    }
    setType(type: "text" | "link" | "button" | "chip" | "input"){
        this.type = type
        return this
    }
    asButton() {
        this.type = "button"
        return this
    }
    asChip() {
        this.type = "chip"
        return this
    }
    asLink() {
        this.type = "link"
        return this
    }
    asText() {
        this.type = "text"
        return this
    }
    asInput() {
        this.type = "input"
        return this
    }
}
export class Chat {
    type!: "text" | "image" | "attachment" 
    public blockId?: string
    constructor(public content: string, public bubbles: ChatBubble[] = []) {

    }

    static fromJson(json: Record<string, any>) {
        return new Chat(json.content, (json.bubbles?? []).map(ChatBubble.fromJson))
        .setType(json['type'])
        .setBlockId(json['blockId'])
    }
    setType(type: "text" | "image" | "attachment" ) {
        this.type = type
        return this
    }
    setBlockId(blockId: string) {
        this.blockId = blockId
        return this
    }
    addBubble(bubble:ChatBubble) {
        this.bubbles.push(bubble)
        return this;
    }
    asText() {
        this.type = "text"
        return this
    }
    asImage() {
        this.type = "image"
        return this
    }
    asAttachment() {
        this.type = "attachment"
        return this
    }
}