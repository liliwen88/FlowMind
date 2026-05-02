import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { optimizationData } from "@/data/optimization-data"
import { formatPercentage } from "@/lib/utils"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import { TrendingUp, AlertCircle, CheckCircle2, FileText, Code, Shield } from "lucide-react"

export function CodeQuality() {
  const { codeQualityMetrics, performanceBottlenecks } = optimizationData
  
  const chartData = codeQualityMetrics.map(metric => ({
    name: metric.name,
    current: metric.current,
    target: metric.target,
    unit: metric.unit
  }))

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-2">代码质量分析</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          全面评估当前代码质量状况，识别改进空间，制定提升目标
        </p>
      </div>

      {/* Metrics Overview */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-5">
        {codeQualityMetrics.map((metric, index) => {
          const percentage = (metric.current / metric.target) * 100
          const isGood = percentage >= 80
          const isWarning = percentage >= 60 && percentage < 80
          
          return (
            <Card key={index} className="hover:shadow-lg transition-shadow">
              <CardHeader className="pb-3">
                <CardTitle className="text-sm font-medium flex items-center gap-2">
                  {index === 0 && <CheckCircle2 className="h-4 w-4 text-green-500" />}
                  {index === 1 && <Shield className="h-4 w-4 text-blue-500" />}
                  {index === 2 && <FileText className="h-4 w-4 text-purple-500" />}
                  {index === 3 && <AlertCircle className="h-4 w-4 text-yellow-500" />}
                  {index === 4 && <Code className="h-4 w-4 text-red-500" />}
                  {metric.name}
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="text-3xl font-bold mb-2">
                  {metric.current}<span className="text-lg text-muted-foreground">{metric.unit}</span>
                </div>
                <Progress value={percentage} className="h-2 mb-2" />
                <div className="flex items-center justify-between text-xs">
                  <span className="text-muted-foreground">目标: {metric.target}{metric.unit}</span>
                  <Badge variant={isGood ? "success" : isWarning ? "warning" : "destructive"} className="text-xs">
                    {formatPercentage(percentage)}
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground mt-2">{metric.description}</p>
              </CardContent>
            </Card>
          )
        })}
      </div>

      {/* Chart */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrendingUp className="h-5 w-5" />
            质量指标对比
          </CardTitle>
          <CardDescription>当前状态 vs 目标值</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip 
                formatter={(value: number, name: string) => [`${value}%`, name === 'current' ? '当前' : '目标']}
              />
              <Bar dataKey="current" name="当前" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
              <Bar dataKey="target" name="目标" fill="hsl(var(--success))" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      {/* Performance Bottlenecks */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <AlertCircle className="h-5 w-5 text-orange-500" />
            性能瓶颈分析
          </CardTitle>
          <CardDescription>识别并优化关键性能问题</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {performanceBottlenecks.map((bottleneck, index) => (
              <div key={index} className="border rounded-lg p-4 hover:bg-muted/50 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <h4 className="font-semibold mb-1">{bottleneck.name}</h4>
                    <p className="text-sm text-muted-foreground">{bottleneck.location}</p>
                  </div>
                  <Badge 
                    variant={bottleneck.severity === 'high' ? 'destructive' : bottleneck.severity === 'medium' ? 'warning' : 'info'}
                  >
                    {bottleneck.severity === 'high' ? '严重' : bottleneck.severity === 'medium' ? '中等' : '轻微'}
                  </Badge>
                </div>
                <p className="text-sm mb-3">{bottleneck.impact}</p>
                <div className="bg-muted/50 rounded p-3">
                  <p className="text-sm font-medium mb-1">解决方案:</p>
                  <p className="text-sm text-muted-foreground">{bottleneck.solution}</p>
                </div>
                <div className="mt-2 text-xs text-green-600 dark:text-green-400">
                  预期改进: {bottleneck.estimatedImprovement}
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recommendations */}
      <Card className="bg-gradient-to-br from-blue-50 to-purple-50 dark:from-blue-950/20 dark:to-purple-950/20 border-blue-200 dark:border-blue-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-blue-900 dark:text-blue-100">
            <TrendingUp className="h-5 w-5" />
            优化建议总结
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="space-y-3">
              <h4 className="font-semibold text-blue-900 dark:text-blue-100">短期目标（1-2周）</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>添加依赖管理和 CI/CD 配置</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>实现递归深度保护机制</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>补充关键测试用例</span>
                </li>
              </ul>
            </div>
            <div className="space-y-3">
              <h4 className="font-semibold text-blue-900 dark:text-blue-100">中期目标（1-2月）</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-purple-500 mt-1">•</span>
                  <span>完善文档和 API 参考</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-500 mt-1">•</span>
                  <span>配置代码质量工具链</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-purple-500 mt-1">•</span>
                  <span>优化错误提示体验</span>
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
