"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const zeroant_ussd_1 = require("zeroant-ussd");
const redis_1 = require("redis");
const fs_1 = __importDefault(require("fs"));
const types_1 = require("@cot/types");
const sdk_1 = require("@cot/sdk");
const app = (0, express_1.default)();
const dispatcher = new zeroant_ussd_1.Dispatcher({
    delimiter: "*"
});
// Create a Redis client
const redisClient = (0, redis_1.createClient)();
// Handle Redis connection errors
redisClient.on("error", (err) => {
    console.error("Redis Client Error:", err);
});
const ai = new sdk_1.AI();
// Connect to Redis
redisClient.connect();
// Help Menu - Process Username
dispatcher.register("Help*<username:string>", new zeroant_ussd_1.Action((event) => {
    const username = event.params.username;
    return event.end(`Your username is ${username}`);
}));
// Default fallback for invalid actions
dispatcher.register("(.?)", new zeroant_ussd_1.Action((event) => __awaiter(void 0, void 0, void 0, function* () {
    const result = yield ai.callChatAPI(event.data.text, event.data.sessionId);
    return new zeroant_ussd_1.EventPayload("CON", result, "application/json");
})).on('before', (event) => __awaiter(void 0, void 0, void 0, function* () {
    console.log("Event BEFORE START");
    // if (event.data) {
    //     return event.end(`An error occurred while trying to complete your request`);
    // }
})).on('after', (event) => {
    console.log(event, "Event Ended");
}));
// Request handler
dispatcher.on('request', (req) => __awaiter(void 0, void 0, void 0, function* () {
    const sessionId = req.query.sessionId; // Assuming session ID is available in the event
    console.log("sessionId", sessionId);
    const intents = [];
    req.params.content = {
        sessionId,
        intents,
        text: req.query.text
    };
    req.params.action = req.query.text;
    console.log({
        content: req.params.content,
        action: req.params.action
    });
}));
// Response handler
dispatcher.on('response', (data, event) => __awaiter(void 0, void 0, void 0, function* () {
    if (data instanceof zeroant_ussd_1.EventPayload) {
        return data;
    }
    return new zeroant_ussd_1.EventPayload(data.type, new types_1.Chat(data.text).setBlockId(event.data.blockId).asText(), 'text/plain');
}));
app.get("/api", express_1.default.json(), (0, zeroant_ussd_1.expressDispatcher)(dispatcher, "params"));
app.use(express_1.default.static(__dirname + "/../static"));
app.use("", (_req, res) => {
    res.send(fs_1.default.createReadStream(__dirname + "/../static/index.html"));
});
app.listen(process.env.PORT || 3000, () => {
    console.log(`Application listening on port ${process.env.PORT || 3000}`);
});
