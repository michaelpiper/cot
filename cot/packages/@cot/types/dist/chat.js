"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.Chat = exports.ChatBubble = void 0;
class ChatBubble {
    constructor(label, value) {
        this.label = label;
        this.value = value;
    }
    static fromJson(json) {
        return new ChatBubble(json['label'], json['value'])
            .setType(json['type']);
    }
    setType(type) {
        this.type = type;
        return this;
    }
    asButton() {
        this.type = "button";
        return this;
    }
    asChip() {
        this.type = "chip";
        return this;
    }
    asLink() {
        this.type = "link";
        return this;
    }
    asText() {
        this.type = "text";
        return this;
    }
    asInput() {
        this.type = "input";
        return this;
    }
}
exports.ChatBubble = ChatBubble;
class Chat {
    constructor(content, bubbles = []) {
        this.content = content;
        this.bubbles = bubbles;
    }
    static fromJson(json) {
        var _a;
        return new Chat(json.content, ((_a = json.bubbles) !== null && _a !== void 0 ? _a : []).map(ChatBubble.fromJson))
            .setType(json['type'])
            .setBlockId(json['blockId']);
    }
    setType(type) {
        this.type = type;
        return this;
    }
    setBlockId(blockId) {
        this.blockId = blockId;
        return this;
    }
    addBubble(bubble) {
        this.bubbles.push(bubble);
        return this;
    }
    asText() {
        this.type = "text";
        return this;
    }
    asImage() {
        this.type = "image";
        return this;
    }
    asAttachment() {
        this.type = "attachment";
        return this;
    }
}
exports.Chat = Chat;
