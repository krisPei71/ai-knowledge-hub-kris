// src/utils/constants.ts

export const STATUS_MAP: Record<string, { label: string; type: string }> = {
  pending:    { label: '待处理', type: 'warning' },
  processing: { label: '处理中', type: 'primary' },
  resolved:   { label: '已解决', type: 'success' },
  closed:     { label: '已关闭', type: 'info' },
}

export const PRIORITY_MAP: Record<string, { label: string; type: string }> = {
  low:    { label: '低', type: 'info' },
  medium: { label: '中', type: 'warning' },
  high:   { label: '高', type: 'danger' },
}