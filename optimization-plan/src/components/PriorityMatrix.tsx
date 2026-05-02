import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { optimizationData } from "@/data/optimization-data"
import { getPriorityColor, getImpactColor } from "@/lib/utils"
import { ChevronDown, ChevronUp, CheckCircle2, Clock, AlertTriangle } from "lucide-react"
import { useState } from "react"

interface PrioritySectionProps {
  title: string
  items: typeof optimizationData.highPriority
  color: string
  icon: React.ReactNode
  defaultExpanded?: boolean
}

function PrioritySection({ title, items, color, icon, defaultExpanded = true }: PrioritySectionProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)
  
  return (
    <Card className="overflow-hidden">
      <CardHeader 
        className={`cursor-pointer transition-colors hover:bg-muted/50 ${color}`}
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {icon}
            <div>
              <CardTitle className="text-xl">{title}</CardTitle>
              <CardDescription>{items.length} 项任务</CardDescription>
            </div>
          </div>
          <Button variant="ghost" size="sm">
            {expanded ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
          </Button>
        </div>
      </CardHeader>
      
      {expanded && (
        <CardContent className="space-y-4 pt-6">
          {items.map((item) => (
            <OptimizationItem key={item.id} item={item} />
          ))}
        </CardContent>
      )}
    </Card>
  )
}

interface OptimizationItemProps {
  item: typeof optimizationData.highPriority[0]
}

function OptimizationItem({ item }: OptimizationItemProps) {
  const [showDetails, setShowDetails] = useState(false)
  
  return (
    <div className="border rounded-lg p-4 hover:shadow-md transition-shadow bg-card">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <h4 className="font-semibold text-lg">{item.title}</h4>
            <Badge className={getPriorityColor(item.priority)}>
              {item.priority === 'high' ? '高' : item.priority === 'medium' ? '中' : '低'}
            </Badge>
            <Badge variant="outline">{item.category}</Badge>
          </div>
          <p className="text-sm text-muted-foreground mb-3">{item.description}</p>
          
          <div className="flex flex-wrap gap-2 mb-3">
            <div className="flex items-center gap-1 text-xs">
              <Clock className="h-3 w-3" />
              <span>{item.estimatedTime}</span>
            </div>
            <div className="flex items-center gap-1 text-xs">
              <div className={`w-2 h-2 rounded-full ${getImpactColor(item.impact)}`} />
              <span>影响: {item.impact === 'high' ? '高' : item.impact === 'medium' ? '中' : '低'}</span>
            </div>
            <div className="flex items-center gap-1 text-xs">
              <AlertTriangle className="h-3 w-3" />
              <span>难度: {item.difficulty === 'easy' ? '简单' : item.difficulty === 'medium' ? '中等' : '困难'}</span>
            </div>
          </div>
          
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => setShowDetails(!showDetails)}
            className="text-xs"
          >
            {showDetails ? '收起详情' : '查看详情'}
            {showDetails ? <ChevronUp className="h-3 w-3 ml-1" /> : <ChevronDown className="h-3 w-3 ml-1" />}
          </Button>
        </div>
        
        <Button variant="outline" size="sm" className="shrink-0">
          <CheckCircle2 className="h-4 w-4 mr-2" />
          标记完成
        </Button>
      </div>
      
      {showDetails && (
        <div className="mt-4 pt-4 border-t space-y-4 animate-fade-in">
          <div>
            <h5 className="font-medium mb-2 text-sm">预期收益</h5>
            <ul className="space-y-1">
              {item.benefits.map((benefit, idx) => (
                <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                  <span className="text-green-500 mt-1">•</span>
                  {benefit}
                </li>
              ))}
            </ul>
          </div>
          
          {item.implementation && (
            <div>
              <h5 className="font-medium mb-2 text-sm">实施步骤</h5>
              <ol className="space-y-1">
                {item.implementation.map((step, idx) => (
                  <li key={idx} className="text-sm text-muted-foreground flex items-start gap-2">
                    <span className="text-primary font-medium">{idx + 1}.</span>
                    {step}
                  </li>
                ))}
              </ol>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export function PriorityMatrix() {
  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-2">优化任务优先级矩阵</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          根据影响程度和实施难度，将优化任务分为三个优先级层次，帮助团队合理分配资源
        </p>
      </div>
      
      <PrioritySection
        title="🔴 高优先级 - 立即处理"
        items={optimizationData.highPriority}
        color="border-l-4 border-l-red-500"
        icon={<div className="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center"><AlertTriangle className="h-5 w-5 text-red-600" /></div>}
      />
      
      <PrioritySection
        title="🟡 中优先级 - 近期处理"
        items={optimizationData.mediumPriority}
        color="border-l-4 border-l-yellow-500"
        icon={<div className="w-10 h-10 rounded-full bg-yellow-100 dark:bg-yellow-900/30 flex items-center justify-center"><Clock className="h-5 w-5 text-yellow-600" /></div>}
        defaultExpanded={false}
      />
      
      <PrioritySection
        title="🔵 低优先级 - 长期规划"
        items={optimizationData.lowPriority}
        color="border-l-4 border-l-blue-500"
        icon={<div className="w-10 h-10 rounded-full bg-blue-100 dark:bg-blue-900/30 flex items-center justify-center"><CheckCircle2 className="h-5 w-5 text-blue-600" /></div>}
        defaultExpanded={false}
      />
    </div>
  )
}
