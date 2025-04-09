
export class Prediction {
    constructor(readonly intent: string, readonly confidence?: number){
    }
  
    static fromJson(json:Record<string, any>){
        return new Prediction(json['intent'], json['confidence'])
    }
}