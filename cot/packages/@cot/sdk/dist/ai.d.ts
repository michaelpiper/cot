import { Chat } from '@cot/types';
export declare class AI {
    client: import("axios").AxiosInstance;
    constructor();
    predictAPI: (prompt: string) => Promise<any>;
    callChatAPI: (userInput: string, sessionId: string) => Promise<Chat>;
    callQwenAPI: (userInput: string, sessionId: string) => Promise<any>;
}
