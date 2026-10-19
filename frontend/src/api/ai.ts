import request from "./request";

export interface AIClassifyRequest{
    title:string,
    description:string
}

export interface AIAnalysisResult{
    category:string,
    priority:string,
    confidence:number,
    summary:string
}

export function classifyTicket(data:AIClassifyRequest){
    return request.post<AIAnalysisResult>('/ai/classify',data)
}