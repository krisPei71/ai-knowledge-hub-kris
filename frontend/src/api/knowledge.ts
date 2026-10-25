import request from "./request";

export interface Knowledge {
  id: number;
  title: string;
  content: string;
  source_ticket_id: number | null;
  status: string;
  created_at: string;
}

export interface KnowledgeSearchResult {
  id: number;
  title: string;
  content: string;
  score: number;
}
export interface KnowledgeSearchRequest{
  query:string,
  top_k:number
}

export function getKnowledgeList(){
    return request.get<Knowledge[]>('/knowledge')
}

export function getKnowledgeDetail(id:number){
    return request.get<Knowledge>(`/knowledge/${id}`)
}

export function searchKnowledge(data:KnowledgeSearchRequest){
    return request.post<KnowledgeSearchResult[]>(`/knowledge/search`,data)
}
