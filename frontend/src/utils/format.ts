export function formatTime(iso:string|null|undefined):string{
    if(!iso) return '-'
    const date = new Date(iso)
    const pad = (num:number) => num.toString().padStart(2,'0')
    return `${date.getFullYear()}-${pad(date.getMonth()+1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`
}