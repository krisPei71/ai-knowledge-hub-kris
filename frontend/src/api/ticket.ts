import request from './request'

export interface Ticket{
    id: number
    title: string
    description: string
    status: 'pending' | 'processing' | 'resolved' | 'closed'
    priority: 'low' | 'medium' | 'high'
    category: string | null
    ai_summary: string | null
    ai_confidence: number | null
    ai_category_raw: string | null
    creator_id: number
    creator_username: string
    assignee_id: number | null
    assignee_username: string | null
    created_at: string
    updated_at: string
}

export interface TicketListResponse{
    items: Ticket[]
    total: number
}

export interface TicketCreateRequest{
    title: string,
    decription: string,
}

export interface TicketQuery{
    keyword?:string
    status?:string,
    priority?:string,
    category?:string,
    page?:number,
    page_size?:number
}

export interface TicketLog{
    id:number
    ticket_id:number
    from_status:string
    to_status:string
    operator_id:number
    operator_username:string
    remark:string | null
    created_at:string
}

export interface TicketStatusUpdate{
    to_status:string,
    remark?:string | null
}

// 创建工单
export function createTicket(data:TicketCreateRequest){
    return request.post<Ticket>('/tickets',data)
}

// 获取工单列表
export function getTicketList(query:TicketQuery){
    return request.get<TicketListResponse>('/tickets',{params:query})
}

export function getTicketDetail(id:number){
    return request.get<Ticket>(`/tickets/${id}`)
}

export function getTicketLogs(id:number){
    return request.get<TicketLog>(`/tickets/${id}/logs`)
}

export function updateTicketStatus(id:number,data:TicketStatusUpdate){
    return request.patch<Ticket>(`/tickets/${id}/status`,data)
}
