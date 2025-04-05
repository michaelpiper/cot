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
const MenuAction = new zeroant_ussd_1.Action((event) => __awaiter(void 0, void 0, void 0, function* () {
    console.log("", event);
    const result = yield ai.predictAPI('generate a welcome message');
    console.log("result", result);
    const chat = new types_1.Chat("WELCOME TO USSD TEST FRAMEWORK").setBlockId(event.data.blockId).asText();
    chat.addBubble(new types_1.ChatBubble("Buy Airtime", "Buy Airtime").asChip());
    chat.addBubble(new types_1.ChatBubble("Help", "Help").asChip());
    return new zeroant_ussd_1.EventPayload("CON", chat);
}));
// Default fallback menu
dispatcher.register("", MenuAction);
// Buy Airtime Menu
dispatcher.register("Buy Airtime", new zeroant_ussd_1.Action((event) => {
    const chat = new types_1.Chat("Buy Airtime").setBlockId(event.data.blockId).asText();
    chat.addBubble(new types_1.ChatBubble("For Myself", "For Myself").asChip());
    chat.addBubble(new types_1.ChatBubble("For Another Number", "For Another Number").asChip());
    return new zeroant_ussd_1.EventPayload("CON", chat);
}));
// Buy Airtime - For Myself
dispatcher.register("Buy Airtime*For Myself", new zeroant_ussd_1.Action((event) => {
    return event.con(`Enter Amount for Airtime`);
}));
// Buy Airtime - For Myself - Process Amount
dispatcher.register("Buy Airtime*For Myself*<amount:integer>", new zeroant_ussd_1.Action((event) => __awaiter(void 0, void 0, void 0, function* () {
    const amount = event.params.amount;
    return event.end(`You have successfully purchased ₦${amount} airtime for yourself.`);
})));
// Buy Airtime - For Another Number
dispatcher.register("Buy Airtime*For Another Number", new zeroant_ussd_1.Action((event) => {
    return event.con(`Enter Phone Number`);
}));
// Buy Airtime - For Another Number - Process Phone Number
dispatcher.register("Buy Airtime*For Another Number*<phoneNumber:string>", new zeroant_ussd_1.Action((event) => {
    const chat = new types_1.Chat("Enter Amount for Airtime").setBlockId(event.data.blockId).asText();
    chat.addBubble(new types_1.ChatBubble("100", "100").asChip());
    chat.addBubble(new types_1.ChatBubble("200", "200").asChip());
    chat.addBubble(new types_1.ChatBubble("300", "300").asChip());
    chat.addBubble(new types_1.ChatBubble("500", "500").asChip());
    return new zeroant_ussd_1.EventPayload("CON", chat);
}).on("before", (event) => {
    var _a, _b;
    if (!/^0(9|8|7|1)(0|1|2|3|4|5|7|8|9)[1-9][0-9]{7}$/.test((_b = (_a = event === null || event === void 0 ? void 0 : event.params) === null || _a === void 0 ? void 0 : _a.phoneNumber) !== null && _b !== void 0 ? _b : '')) {
        popIntent(event.data.sessionId);
        return event.con(`Enter A Valid Phone Number`);
    }
}));
// Buy Airtime - For Another Number - Process Amount
dispatcher.register("Buy Airtime*For Another Number*<phoneNumber:string>*<amount:integer>", new zeroant_ussd_1.Action((event) => {
    const phoneNumber = event.params.phoneNumber;
    const amount = event.params.amount;
    const chat = new types_1.Chat(`You have successfully purchased ₦${amount} airtime for ${phoneNumber}.`).asText();
    return new zeroant_ussd_1.EventPayload("END", chat);
}).on('after', (event) => (resetIntents(event.data.sessionId))));
// Help Menu
dispatcher.register("Help", new zeroant_ussd_1.Action((event) => {
    return event.con(`Welcome to the Help Page`, `Please enter your username:`);
}));
// Help Menu - Process Username
dispatcher.register("Help*<username:string>", new zeroant_ussd_1.Action((event) => {
    const username = event.params.username;
    return event.end(`Your username is ${username}`);
}));
// Default fallback for invalid actions
dispatcher.register("(.?)", new zeroant_ussd_1.Action((event) => __awaiter(void 0, void 0, void 0, function* () {
    return event.end(`Thank you for using USSD Test Framework`);
})).on('before', (event) => __awaiter(void 0, void 0, void 0, function* () {
    console.log("Event BEFORE START");
    // if (event.data) {
    //     return event.end(`An error occurred while trying to complete your request`);
    // }
})).on('after', (event) => {
    console.log(event, "Event Ended");
}));
const getIntentFromInput = (text) => __awaiter(void 0, void 0, void 0, function* () {
    const result = yield ai.predictAPI(text);
    return { intent: result.intent, text, resetSession: true };
});
const popIntent = (sessionId) => __awaiter(void 0, void 0, void 0, function* () {
    const history = yield redisClient.lRange(sessionId, 0, -1); // Get user's action history
    if (history.length >= 1) {
        yield redisClient.rPop(sessionId); // Remove the current action
    }
});
// Function to store an intent in Redis
const storeIntent = (sessionId, intent) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Validate the intent object
        if (!intent || typeof intent !== "object") {
            throw new Error("Invalid intent object");
        }
        // Convert the intent object to a JSON string
        const intentString = JSON.stringify(intent);
        // Push the intent into the Redis list for the session
        yield redisClient.rPush(sessionId, intentString);
        console.log(`Intent stored for session ${sessionId}`);
    }
    catch (error) {
        console.error("Error storing intent:", error);
    }
});
// Function to retrieve all intents for a session
const getLastIntent = (sessionId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Retrieve all items in the list (from start to end)
        const length = yield redisClient.lLen(sessionId);
        const intentString = yield redisClient.lIndex(sessionId, length - 1);
        if (intentString == null) {
            return null;
        }
        // Parse the JSON strings back into objects
        const intent = JSON.parse(intentString);
        console.log(`Retrieved last intent for session ${sessionId}:`, intent);
        return intent;
    }
    catch (error) {
        console.error("Error retrieving intents:", error);
        return null;
    }
});
// Function to retrieve all intents for a session
const getIntents = (sessionId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        // Retrieve all items in the list (from start to end)
        // const length = await redisClient.lLen(sessionId)
        const intentStrings = yield redisClient.lRange(sessionId, 0, -1);
        // Parse the JSON strings back into objects
        const intents = intentStrings.map((str) => JSON.parse(str));
        console.log(`Retrieved intents for session ${sessionId}:`, intents);
        return intents;
    }
    catch (error) {
        console.error("Error retrieving intents:", error);
        return [];
    }
});
const resetIntents = (sessionId) => __awaiter(void 0, void 0, void 0, function* () {
    try {
        yield redisClient.del(sessionId);
    }
    catch (error) {
        console.error("Error reseting intents:", error);
    }
});
// Request handler
dispatcher.on('request', (req) => __awaiter(void 0, void 0, void 0, function* () {
    const sessionId = req.query.sessionId; // Assuming session ID is available in the event
    console.log("sessionId", sessionId);
    const intent = yield getIntentFromInput(req.query.text); // Extract the user's input
    if (intent.resetSession == true) {
        yield resetIntents(sessionId);
    }
    if (intent.popLastSessionIntent === true) {
        const prev = yield getLastIntent(sessionId);
        if (prev) {
            yield popIntent(sessionId);
            intent.intent = prev.intent;
        }
    }
    else {
        // Store the current action in Redis
        // Push the current action to the user's history
        yield storeIntent(sessionId, intent);
    }
    const intents = yield getIntents(sessionId);
    req.params.content = {
        sessionId,
        intents
    };
    req.params.action = intents.map((content) => content.intent).join("*");
    console.log({
        content: req.params.content,
        action: req.params.action
    });
}));
// Response handler
dispatcher.on('response', (data, event) => __awaiter(void 0, void 0, void 0, function* () {
    if (data.isEnd) {
        queueMicrotask(() => __awaiter(void 0, void 0, void 0, function* () {
            yield resetIntents(event.data.sessionId);
        }));
    }
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
