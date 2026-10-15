import type { Ticket } from '@/api/ticket'
import type { UserInfoResponse } from '@/api/auth'

export interface Transition {
    from: string,
    to: string,
    label: string,
    type: 'primary' | 'success' | 'warning' | 'info' | 'danger',
    roles: string[],
    requireCreator?: boolean,
    requireAssignee?: boolean,
    remarkRequired?: boolean
}

export const TRANSITION: Transition[] = [
    {
        from: 'pending',
        to: 'processing',
        label: '认领工单',
        type: 'primary',
        roles: ['handler', 'admin'],
    }, {
        from: 'processing',
        to: 'resolved',
        label: '标记已解决',
        type: 'primary',
        roles: ['handler', 'admin'],
        requireAssignee: true,
    }, {
        from: 'resolved',
        to: 'closed',
        label: '确认关闭',
        type: 'primary',
        roles: ['reporter', 'admin'],
        requireCreator: true,
    }, {
        from: 'resolved',
        to: 'processing',
        label: '打回重开',
        type: 'primary',
        roles: ['reporter', 'admin'],
        requireCreator: true,
        remarkRequired: true
    },
]   
export function getAvailableTransition(ticket, currentUser):Transition[] {
    return TRANSITION.filter(t => {
        if(!currentUser) return null 
        if (t.from !== ticket.status) return false
        if (currentUser.role === 'admin') return true
        if (!t.roles.includes(currentUser.role)) return false
        if (t.requireCreator && ticket.creator_id !== currentUser.id) return false
        if (t.requireAssignee && ticket.assignee_id !== currentUser.id) return false
        return true
    })
}