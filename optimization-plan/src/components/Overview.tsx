import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Button } from "@/components/ui/button"
import { optimizationData } from "@/data/optimization-data"
import { CheckCircle2, AlertTriangle, TrendingUp, Clock, Target, Award } from "lucide-react"

export function Overview() {
  const { overview, highPriority, mediumPriority, lowPriority, codeQualityMetrics } = optimizationData
  
  const totalItems = highPriority.length + mediumPriority.length + lowPriority.length
  const completedItems = 0 // Can be updated based on actual progress
  
  return (
    <div className="space-y-6 animate-fade-in">
      {/* Hero Section */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-primary via-blue-600 to-purple-600 p-8 text-white shadow-2xl">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZGVmcz48cGF0dGVybiBpZD0iZ3JpZCIgd2lkdGg9IjQwIiBoZWlnaHQ9IjQwIiBwYXR0ZXJuVW5pdHM9InVzZXJTcGFjZU9uVXNlIj48cGF0aCBkPSJNIDQwIDAgTCAwIDAgMCAwIiBmaWxsPSJub25lIiBzdHJva2U9IndoaXRlIiBzdHJva2Utd2lkdGg9IjEiIG9wYWNpdHk9IjAuMSIvPjwvcGF0dGVybj48L2RlZnM+PHJlY3Qgd2lkdGg9IjEwMCUiIGhlaWdodD0iMTAwJSIgZmlsbD0idXJsKCNncmlkKSIvPjwvc3ZnPg==')] opacity-20" />
        <div className="relative z-10">
          <div className="flex items-center gap-3 mb-4">
            <Award className="h-8 w-8" />
            <Badge variant="secondary" className="bg-white/20 text-white border-white/30">
              综合评分: {overview.overallScore}/5.0
            </Badge>
          </div>
          <h2 className="text-3xl font-bold mb-2">项目优化方案</h2>
          <p className="text-lg opacity-90 mb-6 max-w-2xl">
            全面的代码质量提升、性能优化和用户体验改进计划，助力 llm-flow-dsl 从 MVP 迈向生产就绪
          </p>
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur px-4 py-2 rounded-lg">
              <CheckCircle2 className="h-5 w-5" />
              <span>{totalItems} 项优化任务</span>
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur px-4 py-2 rounded-lg">
              <Clock className="h-5 w-5" />
              <span>预计 40+ 小时工作量</span>
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur px-4 py-2 rounded-lg">
              <Target className="h-5 w-5" />
              <span>目标: v0.2 发布</span>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">代码行数</CardTitle>
            <CodeIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview.totalLinesOfCode.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">核心模块</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">模块数量</CardTitle>
            <BoxIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview.modules}</div>
            <p className="text-xs text-muted-foreground">核心功能模块</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">测试文件</CardTitle>
            <TestTubeIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview.testFiles}</div>
            <p className="text-xs text-muted-foreground">需要扩展</p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">示例文件</CardTitle>
            <FileIcon className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{overview.examples}</div>
            <p className="text-xs text-muted-foreground">参考实现</p>
          </CardContent>
        </Card>
      </div>

      {/* Priority Breakdown */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="border-l-4 border-l-red-500">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">高优先级</CardTitle>
              <Badge variant="destructive">{highPriority.length} 项</Badge>
            </div>
            <CardDescription>立即处理的关键问题</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={100 * completedItems / highPriority.length} className="mb-2" />
            <p className="text-sm text-muted-foreground">
              完成度: {completedItems}/{highPriority.length}
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-yellow-500">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">中优先级</CardTitle>
              <Badge variant="warning">{mediumPriority.length} 项</Badge>
            </div>
            <CardDescription>近期改进计划</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={0} className="mb-2" />
            <p className="text-sm text-muted-foreground">
              完成度: 0/{mediumPriority.length}
            </p>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-blue-500">
          <CardHeader>
            <div className="flex items-center justify-between">
              <CardTitle className="text-lg">低优先级</CardTitle>
              <Badge variant="info">{lowPriority.length} 项</Badge>
            </div>
            <CardDescription>长期优化方向</CardDescription>
          </CardHeader>
          <CardContent>
            <Progress value={0} className="mb-2" />
            <p className="text-sm text-muted-foreground">
              完成度: 0/{lowPriority.length}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Code Quality Metrics Preview */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            代码质量指标
          </CardTitle>
          <CardDescription>当前状态与目标对比</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {codeQualityMetrics.slice(0, 3).map((metric, index) => (
              <div key={index} className="space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-sm font-medium">{metric.name}</span>
                  <span className="text-sm text-muted-foreground">
                    {metric.current}{metric.unit} → {metric.target}{metric.unit}
                  </span>
                </div>
                <div className="relative">
                  <Progress value={metric.current} max={metric.target} className="h-2" />
                  <div 
                    className="absolute top-0 right-0 h-2 w-1 bg-green-500 rounded-full"
                    style={{ left: `${(metric.target / 100) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Quick Actions */}
      <div className="flex flex-wrap gap-3">
        <Button variant="gradient" size="lg">
          查看完整方案
        </Button>
        <Button variant="outline" size="lg">
          下载 PDF 报告
        </Button>
        <Button variant="secondary" size="lg">
          分享方案
        </Button>
      </div>
    </div>
  )
}

// Icon components
function CodeIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <polyline points="16 18 22 12 16 6" />
      <polyline points="8 6 2 12 8 18" />
    </svg>
  )
}

function BoxIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
      <polyline points="3.27 6.96 12 12.01 20.73 6.96" />
      <line x1="12" y1="22.08" x2="12" y2="12" />
    </svg>
  )
}

function TestTubeIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 2v17.5c0 1.4-1.1 2.5-2.5 2.5h0c-1.4 0-2.5-1.1-2.5-2.5V2" />
      <path d="M8.5 2h7" />
      <path d="M14.5 16h-5" />
    </svg>
  )
}

function FileIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg {...props} xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M14.5 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7.5L14.5 2z" />
      <polyline points="14 2 14 8 20 8" />
    </svg>
  )
}
