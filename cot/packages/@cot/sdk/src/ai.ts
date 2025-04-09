
import axios from 'axios';
import { Chat, Prediction } from '@cot/types';
// Replace with your actual API key
const API_KEY: string = 'your_api_key_here';
const API_URL: string = 'http://localhost:4000';  // Example endpoint (check docs for the correct one)

// Define the request payload
interface PredictResponse {
    intent: string;
    confidence?: number;
}



export class AI {
    client;
    constructor(options:{baseUrl?: string, apiKey?: string }){
        this.client = axios.create({
                baseURL: options?.baseUrl?? API_URL,
            })
            this.client.interceptors.request.use((req)=>{
                req.headers.set("authorization", `Bearer ${ options?.apiKey ?? API_KEY}`)
                return req
            })
    }
    // Helper Function to Call Qwen API
    predictAPI = async (userInput: string, sessionId?: string): Promise<PredictResponse> => {
        try {
            const response = await this.client.post('/predict', {
                message: userInput,  
                converstion_id: sessionId,
            })
            return Prediction.fromJson(response.data);
        } catch (error) {
            console.error('Error calling predictAPI:', error);
            throw error;
        }
    }
    callChatAPI = async (userInput: string, sessionId: string) => {
        try {
            const response = await this.client.post('/chat', {
                message: userInput,
                conversation_id: sessionId
            })
            return Chat.fromJson(response.data);
        } catch (error) {
            console.error('Error calling callChatAPI:', error);
            throw error;
        }
    }
}