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

export interface ChatSource{
    id:number,
    title:string
}

export interface ChatChunk{
    type:"source"|"text"|"done",
    data?:any
}

export interface ChatHistory{
    role:string,
    content:string
}

export function classifyTicket(data:AIClassifyRequest){
    return request.post<AIAnalysisResult>('/ai/classify',data)
}

export async function streamChat(query: string,history:ChatHistory[], onMessage: (chunk: ChatChunk) => void) {
  const token = localStorage.getItem("token")
  
  const response = await fetch("/api/ai/chat", {
    method: "POST",
    headers: {
      'Content-Type': "application/json",
      // 👇 修复：Bearer 后面必须加空格
      'Authorization': `Bearer ${token}` 
    },
    body: JSON.stringify({ query,history })
  })

  if (!response.ok) {
    throw new Error("网络请求失败")
  }

  const reader = response.body?.getReader()
  if (!reader) return 

  const decoder = new TextDecoder("utf-8") 
  let buffer = ""

  while (true) {
    const { done, value } = await reader.read()
    if (done) break; // 👇 修复：用 break 而不是 return

    const text = decoder.decode(value, { stream: true })
    buffer += text

    // 按标准的 SSE 结束符切割
    const lines = buffer.split('\n\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      // 👇 修复：先 trim 一下，防止有不可见的回车符
      const trimmedLine = line.trim()
      
      if (trimmedLine.startsWith('data:')) {
        // 👇 修复：slice(6) 后加 trim()，确保拿到的 JSON 没有前导空格
        const dataStr = trimmedLine.replace(/^data:\s*/, '')
        if (!dataStr) continue; // 跳过空数据
        try {
          const data = JSON.parse(dataStr)
          onMessage(data)
        } catch (error) {
          console.error("解析数据流失败，原始数据:", dataStr, error)
        }
      }
    }
  }
}