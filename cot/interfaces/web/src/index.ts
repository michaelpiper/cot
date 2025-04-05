import express from "express";
import { expressDispatcher, Action, Dispatcher, EventText, EventPayload } from "zeroant-ussd";
import { createClient } from "redis";
import fs from "fs";
import { Chat, ChatBubble } from '@cot/types';
import { AI } from '@cot/sdk';
const app = express();
const dispatcher = new Dispatcher({
    delimiter: "*"
});

// Create a Redis client
const redisClient = createClient();

// Handle Redis connection errors
redisClient.on("error", (err) => {
    console.error("Redis Client Error:", err);
});
const ai = new AI()

// Connect to Redis
redisClient.connect();
// Help Menu - Process Username
dispatcher.register("Help*<username:string>", new Action((event) => {
    const username = event.params.username;
    return event.end(`Your username is ${username}`);
}));


// Default fallback for invalid actions
dispatcher.register("(.?)", new Action(async (event) => {
    const  result= await ai.callChatAPI(event.data.text, event.data.sessionId)
    return new EventPayload("CON", result, "application/json")
}).on('before', async (event) => {
    console.log("Event BEFORE START");
    // if (event.data) {
    //     return event.end(`An error occurred while trying to complete your request`);
    // }
}).on('after', (event) => {
    console.log(event, "Event Ended");
}));
// Request handler
dispatcher.on('request', async (req) => {
    const sessionId = req.query.sessionId as string; // Assuming session ID is available in the event
    console.log("sessionId", sessionId);
    const intents: string[] = []
    req.params.content = {
        sessionId,
        intents,
        text: req.query.text
    };
    req.params.action =  req.query.text
    console.log({
        content: req.params.content,
        action: req.params.action
    });
});

// Response handler
dispatcher.on('response', async (data: EventText | EventPayload<unknown>, event) => {
    if (data instanceof EventPayload) {
        return data;
    }
    return new EventPayload(data.type, new Chat(data.text).setBlockId(event.data.blockId).asText(), 'text/plain');
});

app.get("/api", express.json(), expressDispatcher(dispatcher, "params") as never);
app.use(express.static(__dirname + "/../static"))
app.use("", (_req, res) => {
    res.send(fs.createReadStream(__dirname + "/../static/index.html"))
});
app.listen(process.env.PORT || 3000, () => {
    console.log(`Application listening on port ${process.env.PORT || 3000}`);
});