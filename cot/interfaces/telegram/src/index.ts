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
const MenuAction = new Action(async (event) => {
    console.log("", event);
     const result = await ai.predictAPI('generate a welcome message')
     console.log("result", result);
     const chat =  new Chat("WELCOME TO USSD TEST FRAMEWORK").setBlockId(event.data.blockId).asText()
     chat.addBubble(new ChatBubble("Buy Airtime", "Buy Airtime").asChip())
     chat.addBubble(new ChatBubble("Help", "Help").asChip())
    return  new EventPayload("CON", chat);
});
// Default fallback menu
dispatcher.register("", MenuAction);

// Buy Airtime Menu
dispatcher.register("Buy Airtime", new Action((event) => {
    const chat =  new Chat("Buy Airtime").setBlockId(event.data.blockId).asText()
    chat.addBubble(new ChatBubble("For Myself", "For Myself").asChip())
    chat.addBubble(new ChatBubble("For Another Number", "For Another Number").asChip())
    return new EventPayload("CON", chat);
}));

// Buy Airtime - For Myself
dispatcher.register("Buy Airtime*For Myself", new Action((event) => {
    return event.con(`Enter Amount for Airtime`);
}));

// Buy Airtime - For Myself - Process Amount
dispatcher.register("Buy Airtime*For Myself*<amount:integer>", new Action(async (event) => {
    const amount = event.params.amount;
    return event.end(`You have successfully purchased ₦${amount} airtime for yourself.`);
}));

// Buy Airtime - For Another Number
dispatcher.register("Buy Airtime*For Another Number", new Action((event) => {
    return event.con(`Enter Phone Number`);
}));

// Buy Airtime - For Another Number - Process Phone Number
dispatcher.register("Buy Airtime*For Another Number*<phoneNumber:string>", new Action((event) => {
    const chat =  new Chat("Enter Amount for Airtime").setBlockId(event.data.blockId).asText()
    chat.addBubble(new ChatBubble("100", "100").asChip())
    chat.addBubble(new ChatBubble("200", "200").asChip())
    chat.addBubble(new ChatBubble("300", "300").asChip())
    chat.addBubble(new ChatBubble("500", "500").asChip())
    return new EventPayload("CON", chat);
}).on("before", (event) => {
    if (!/^0(9|8|7|1)(0|1|2|3|4|5|7|8|9)[1-9][0-9]{7}$/.test(event?.params?.phoneNumber as string ?? '')) {
        popIntent(event.data.sessionId)
        return event.con(`Enter A Valid Phone Number`);
    }
}));

// Buy Airtime - For Another Number - Process Amount
dispatcher.register("Buy Airtime*For Another Number*<phoneNumber:string>*<amount:integer>", new Action((event) => {
    const phoneNumber = event.params.phoneNumber;
    const amount = event.params.amount;
    const chat = new Chat(`You have successfully purchased ₦${amount} airtime for ${phoneNumber}.`).asText()
    
    return new EventPayload("END", chat)
}).on('after', (event) => (resetIntents(event.data.sessionId))));

// Help Menu
dispatcher.register("Help", new Action((event) => {
    return event.con(`Welcome to the Help Page`, `Please enter your username:`);
}));

// Help Menu - Process Username
dispatcher.register("Help*<username:string>", new Action((event) => {
    const username = event.params.username;
    return event.end(`Your username is ${username}`);
}));


// Default fallback for invalid actions
dispatcher.register("(.?)", new Action(async (event) => {
    return event.end(`Thank you for using USSD Test Framework`);
}).on('before', async (event) => {
    console.log("Event BEFORE START");
    // if (event.data) {
    //     return event.end(`An error occurred while trying to complete your request`);
    // }
}).on('after', (event) => {
    console.log(event, "Event Ended");
}));
interface Intent {
    intent: string;
    text: string;
    resetSession?: boolean;
    popLastSessionIntent?: boolean;
}

const getIntentFromInput = async (text: string): Promise<Intent> => {
    const result = await ai.predictAPI(text)
    
        return { intent:result.intent, text, resetSession: true };
    
   
};

const popIntent = async (sessionId: string) => {
    const history = await redisClient.lRange(sessionId, 0, -1); // Get user's action history
    if (history.length >= 1) {
        await redisClient.rPop(sessionId); // Remove the current action
    }
}
// Function to store an intent in Redis
const storeIntent = async (sessionId: string, intent: Intent) => {
    try {
        // Validate the intent object
        if (!intent || typeof intent !== "object") {
            throw new Error("Invalid intent object");
        }

        // Convert the intent object to a JSON string
        const intentString = JSON.stringify(intent);

        // Push the intent into the Redis list for the session
        await redisClient.rPush(sessionId, intentString);
        console.log(`Intent stored for session ${sessionId}`);
    } catch (error) {
        console.error("Error storing intent:", error);
    }
}

// Function to retrieve all intents for a session
const getLastIntent = async (sessionId: string): Promise<Intent | null> => {
    try {
        // Retrieve all items in the list (from start to end)
        const length = await redisClient.lLen(sessionId)
        const intentString = await redisClient.lIndex(sessionId, length - 1);
        if (intentString == null) {
            return null
        }
        // Parse the JSON strings back into objects
        const intent = JSON.parse(intentString);
        console.log(`Retrieved last intent for session ${sessionId}:`, intent);
        return intent;
    } catch (error) {
        console.error("Error retrieving intents:", error);
        return null;
    }
}
// Function to retrieve all intents for a session
const getIntents = async (sessionId: string): Promise<Intent[]> => {
    try {
        // Retrieve all items in the list (from start to end)
        // const length = await redisClient.lLen(sessionId)
        const intentStrings = await redisClient.lRange(sessionId, 0, -1);

        // Parse the JSON strings back into objects
        const intents = intentStrings.map((str) => JSON.parse(str));
        console.log(`Retrieved intents for session ${sessionId}:`, intents);
        return intents;
    } catch (error) {
        console.error("Error retrieving intents:", error);
        return [];
    }
}
const resetIntents = async (sessionId: string): Promise<void> => {
    try {
        await redisClient.del(sessionId);
    } catch (error) {
        console.error("Error reseting intents:", error);
    }
}
// Request handler
dispatcher.on('request', async (req) => {
    const sessionId = req.query.sessionId as string; // Assuming session ID is available in the event
    console.log("sessionId", sessionId);
    const intent = await getIntentFromInput(req.query.text as string); // Extract the user's input
    if (intent.resetSession == true) {
        await resetIntents(sessionId);
    }
    if (intent.popLastSessionIntent === true) {
        const prev = await getLastIntent(sessionId);
        if (prev) {
            await popIntent(sessionId)
            intent.intent = prev.intent;
        }
    } else {
        // Store the current action in Redis
        // Push the current action to the user's history
        await storeIntent(sessionId, intent);
    }
    const intents = await getIntents(sessionId)
    req.params.content = {
        sessionId,
        intents
    };
    req.params.action = intents.map((content) => content.intent).join("*")
    console.log({
        content: req.params.content,
        action: req.params.action
    });
});

// Response handler
dispatcher.on('response', async (data: EventText | EventPayload<unknown>, event) => {
    if (data.isEnd) {
        queueMicrotask(async () => {
            await resetIntents(event.data.sessionId);
        })
    }
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