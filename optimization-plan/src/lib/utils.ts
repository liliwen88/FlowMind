import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatPercentage(value: number): string {
  return `${value.toFixed(1)}%`
}

export function getPriorityColor(priority: string): string {
  switch (priority) {
    case 'high':
      return 'text-red-600 bg-red-50 dark:bg-red-950/20'
    case 'medium':
      return 'text-yellow-600 bg-yellow-50 dark:bg-yellow-950/20'
    case 'low':
      return 'text-blue-600 bg-blue-50 dark:bg-blue-950/20'
    default:
      return 'text-gray-600 bg-gray-50'
  }
}

export function getImpactColor(impact: string): string {
  switch (impact) {
    case 'high':
      return 'bg-green-500'
    case 'medium':
      return 'bg-yellow-500'
    case 'low':
      return 'bg-blue-500'
    default:
      return 'bg-gray-500'
  }
}
