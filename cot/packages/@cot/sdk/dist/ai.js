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
exports.AI = void 0;
const axios_1 = __importDefault(require("axios"));
const types_1 = require("@cot/types");
// Replace with your actual API key
const API_KEY = 'your_api_key_here';
const API_URL = 'http://localhost:4000'; // Example endpoint (check docs for the correct one)
class AI {
    constructor() {
        // Helper Function to Call Qwen API
        this.predictAPI = (prompt) => __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield this.client.post('/predict', {
                    prompt
                });
                return response.data;
            }
            catch (error) {
                console.error('Error calling Qwen API:', error);
                throw error;
            }
        });
        this.callChatAPI = (userInput, sessionId) => __awaiter(this, void 0, void 0, function* () {
            try {
                const response = yield this.client.post('/chat', {
                    message: userInput,
                    conversation_id: sessionId
                });
                return types_1.Chat.fromJson(response.data);
            }
            catch (error) {
                console.error('Error calling Qwen API:', error);
                throw error;
            }
        });
        this.callQwenAPI = (userInput, sessionId) => __awaiter(this, void 0, void 0, function* () {
            const qwenEndpoint = 'https://chat.deepseek.com/api/v0/chat/completion';
            const qwenApiKey = 'VC/X3qHg/LxAgtZ+E2aXyiqUcpA0kIA1+gseJbWwBLKfS6ljAROcvXFrctmZjouX'; // Replace with your Qwen API key
            const payload = {
                prompt: userInput,
                max_tokens: 50, // Limit the response length
                temperature: 0.7 // Control randomness
            };
            try {
                const response = yield axios_1.default.post(qwenEndpoint, {
                    "chat_session_id": sessionId,
                    "parent_message_id": 2,
                    prompt: payload.prompt,
                    "ref_file_ids": [],
                    "search_enabled": false,
                    "thinking_enabled": false
                }, {
                    headers: {
                        accept: "*/*",
                        authorization: "Bearer VC/X3qHg/LxAgtZ+E2aXyiqUcpA0kIA1+gseJbWwBLKfS6ljAROcvXFrctmZjouX",
                        "content-type": "application/json",
                        Cookie: "Hm_lvt_1fff341d7a963a4043e858ef0e19a17c=1738049270; smidV2=20250128082749beca00ffbe0b7bb4247fea17bdd5a28b00237a30e09466760; intercom-device-id-guh50jw4=48d14789-c11e-42d9-bc65-f670cd6f0353; .thumbcache_6b2e5483f9d858d7c661c5e276b6a6ae=h9j6v1nwGZiHcQzV8gD3fdd4nkbWQXDBRMXgaazrEpAU7p1P6zFV4DHZU2tZzbiUqQi2yfDYKehm69YB6/p3Sg%3D%3D; cf_clearance=Y6SqFO_GNrmE7NT6CfA3dx7QRju8XHxfXp0SweCE7v4-1742424717-1.2.1.1-6UtvG.WLYdOOdnSfpRcGY06UpmF3Wgxb3WM5mq4VkM7ImqZiCs2Hk8qoF2KgNXzYYZORa57C9uWtEDCV3v9Bg5.oge7w2BdouYm8uDDU4wC38OfvMMXmH_83XZCMRBO2.DrX0lRkY9QxTxMpddwkk4FAEKdRRj6J62NbVGq3l7cdOP5FtDFKI7VFP.P6Vo1ofxm0P_oARxUqcrLquzUzPR5HxyVKQDFaIPEleeIY30zC11HUQBOv1ouv0ErwxSlpI9lqvHpd5E_pRxnetNsmcuYn3xcuwRVyYzIEr1g0X4iqEGH7mU4WmqpXUhpAAU06sTqXC0st.ny.zfax_cDyjz6T8TPQbRX_hORY77qMfHbmfz2JotqBGTfIyBMmGwfE; HWWAFSESID=2fca65530d27c854508; HWWAFSESTIME=1742424714726; ds_session_id=9996072dbdac4639a78bf06f62066122; ds_cookie_preference=%257B%2522level%2522%253A%2522all%2522%257D; cf_clearance=3rtK1_KbG82o6TXXKC2g7MpPNeWHSMGKIEb.qO8qhUg-1742426684-1.2.1.1-XZF0xz8NHBZCJr4AcrQOie7cVsue34aUbpWEbi8Ci98WMjzkhCv6dzOJt_.ymtzX1JRUfGpYqMkvm8s8eetDwGkGigGJzsrKocFrD77j0_dSK.LIXoqWeVtvktJ5E53EW9k8SOu3.6vCeNDCVh3qc6VI8K_IAHckRbn.9dYstjO.KnHaxVaSbmYMoW7CAAmOPaxAHm92vehTtrNvlWWl3xRZ7LaLWtyflFyDgFDIm1rGBkPc33yx5ohsJTAh8d09qOP9FFiDUEDy8J1l1NdWr19vdmEYk1OaMceL9kSfFwKoDgJR4u32iF.ZYPltS8K_LcDHXFXOsynmoTy6c0slqQfkmKxjcHmlE6P9NVLAqm7OtBEWKGq_JLs8V.wdYf_D; cf_chl_rc_m=1; intercom-session-guh50jw4=engvVWJkN2YxVkx1eTN6cVFtekpCcFRSQ1MyRjBzNGNvMmRsWFZZWTJBb2lCcWgzOENSSFRUbkx1c3lSVkxaTFl0WWNEMk5pWVgyYUcvRlRZbkx5N3ZmbDY3OUMxT2JrV3JCL3BFVEgrR1U9LS1vckMrUXJycGZpVmM1UmtuNHROMEFnPT0=--626c60069c984a06bddcf06e1010a3281b98b853; __cf_bm=oX1.Sog616mWs4iEQtrounNIh0i.N_O34d2qmMmi2qI-1742427773-1.0.1.1-SuEkId5mNtu2KKGPy_b5C85DzCXkiAQTpzzfzZgywdtCRUbDCKuaa565TZ0b9LOUFz_BF2_swpsYzPpmtTcFg7vbUehFelezZu8_XcFH_8s",
                        origin: "https://chat.deepseek.com",
                        referer: `https://chat.deepseek.com/a/chat/s/${sessionId}`,
                        "sec-ch-ua": `"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"`,
                        "sec-ch-ua-arch": "arm",
                        "sec-ch-ua-bitness": "64",
                        "sec-ch-ua-full-version": "134.0.6998.89",
                        "sec-ch-ua-full-version-list": `"Chromium";v="134.0.6998.89", "Not:A-Brand";v="24.0.0.0", "Google Chrome";v="134.0.6998.89"`,
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-model": `""`,
                        "sec-ch-ua-platform": `"macOS"`,
                        "sec-ch-ua-platform-version": "14.5.0",
                        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
                        "x-app-version": "20241129.1",
                        "x-client-locale": "en_US",
                        "x-client-platform": "web",
                        "x-client-version": '1.0.0-always',
                        "x-ds-pow-response": "eyJhbGdvcml0aG0iOiJEZWVwU2Vla0hhc2hWMSIsImNoYWxsZW5nZSI6IjMyYjdlYmUyYjkyMGQwYjJjMDk0ODcwZDBhYjVhN2M3NGFjNzU4ODNlMzk0ZmRjODAzNWE0ZDQ1NTAwNjcxZjEiLCJzYWx0IjoiYTM4MWJiMGM2OThlNjVlOTRhODciLCJhbnN3ZXIiOjM1ODYxLCJzaWduYXR1cmUiOiI2ZWNjNmM3OTc3MmRjZjUwMmY2OGIxMWI0ZWJiZGEwMzFkM2U0YjkwYjdhZmRkOGU2ZWUyYjFhMWNlMjAzODg0IiwidGFyZ2V0X3BhdGgiOiIvYXBpL3YwL2NoYXQvY29tcGxldGlvbiJ9"
                    }
                });
                return response.data;
            }
            catch (error) {
                console.error('Error calling Qwen API:', error);
                throw error;
            }
        });
        this.client = axios_1.default.create({
            baseURL: API_URL,
        });
        this.client.interceptors.request.use((req) => {
            req.headers.set("authorization", `Bearer ${API_KEY}`);
            return req;
        });
    }
}
exports.AI = AI;
