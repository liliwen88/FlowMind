import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { optimizationData } from "@/data/optimization-data"
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import { TestTube, AlertTriangle, CheckCircle2, Plus } from "lucide-react"

export function TestCoverage() {
  const { testCoverage } = optimizationData
  
  // Calculate overall coverage
  const totalTests = testCoverage.reduce((sum, item) => sum + item.tests, 0)
  const avgCoverage = testCoverage.reduce((sum, item) => sum + item.coverage, 0) / testCoverage.length
  
  // Prepare chart data
  const pieData = [
    { name: '已覆盖', value: avgCoverage, color: 'hsl(var(--success))' },
    { name: '未覆盖', value: 100 - avgCoverage, color: 'hsl(var(--muted-foreground))' }
  ]
  
  const barData = testCoverage.map(item => ({
    name: item.module.replace('.py', ''),
    coverage: item.coverage,
    tests: item.tests
  }))

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold mb-2">测试覆盖率分析</h2>
        <p className="text-muted-foreground max-w-2xl mx-auto">
          详细分析各模块测试覆盖情况，识别测试缺口，制定补充计划
        </p>
      </div>

      {/* Overall Stats */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <TestTube className="h-4 w-4 text-primary" />
              平均覆盖率
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{avgCoverage.toFixed(1)}%</div>
            <Progress value={avgCoverage} className="h-2 mb-2" />
            <p className="text-xs text-muted-foreground">目标: 90%</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <CheckCircle2 className="h-4 w-4 text-green-500" />
              总测试数
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">{totalTests}</div>
            <p className="text-xs text-muted-foreground">分布在 {testCoverage.length} 个模块</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
              待补充测试
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-4xl font-bold mb-2">
              {testCoverage.reduce((sum, item) => sum + item.missing.length, 0)}
            </div>
            <p className="text-xs text-muted-foreground">关键测试场景</p>
          </CardContent>
        </Card>
      </div>

      {/* Coverage Chart */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>覆盖率分布</CardTitle>
            <CardDescription>各模块测试覆盖百分比</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {pieData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>模块对比</CardTitle>
            <CardDescription>各模块测试数量与覆盖率</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={barData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="coverage" name="覆盖率(%)" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Module Details */}
      <Card>
        <CardHeader>
          <CardTitle>模块详细分析</CardTitle>
          <CardDescription>每个模块的测试覆盖情况和缺失测试</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-6">
            {testCoverage.map((module, index) => (
              <div key={index} className="border rounded-lg p-4 hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      <TestTube className="h-5 w-5 text-primary" />
                    </div>
                    <div>
                      <h4 className="font-semibold">{module.module}</h4>
                      <p className="text-xs text-muted-foreground">{module.tests} 个测试</p>
                    </div>
                  </div>
                  <Badge 
                    variant={module.coverage >= 80 ? 'success' : module.coverage >= 60 ? 'warning' : 'destructive'}
                  >
                    {module.coverage}%
                  </Badge>
                </div>
                
                <Progress value={module.coverage} className="h-2 mb-3" />
                
                {module.missing.length > 0 && (
                  <div>
                    <h5 className="text-sm font-medium mb-2 flex items-center gap-2">
                      <AlertTriangle className="h-4 w-4 text-yellow-500" />
                      缺失测试场景
                    </h5>
                    <div className="space-y-2">
                      {module.missing.map((missing, idx) => (
                        <div key={idx} className="flex items-center justify-between bg-muted/50 rounded px-3 py-2">
                          <span className="text-sm">{missing}</span>
                          <Button variant="ghost" size="sm" className="h-7 px-2">
                            <Plus className="h-3 w-3" />
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Action Items */}
      <Card className="bg-gradient-to-br from-green-50 to-blue-50 dark:from-green-950/20 dark:to-blue-950/20 border-green-200 dark:border-green-800">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-green-900 dark:text-green-100">
            <CheckCircle2 className="h-5 w-5" />
            测试补充行动计划
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div>
              <h4 className="font-semibold mb-3 text-green-900 dark:text-green-100">立即补充（高优先级）</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-red-500 mt-1">•</span>
                  <span>创建 test_runner.py - runner.py 当前仅 45% 覆盖率</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-500 mt-1">•</span>
                  <span>添加深度嵌套表达式测试 - 防止递归溢出</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-red-500 mt-1">•</span>
                  <span>为所有示例文件编写集成测试</span>
                </li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-3 text-green-900 dark:text-green-100">近期补充（中优先级）</h4>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>扩展 lexer 边界条件测试</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>添加性能基准测试</span>
                </li>
                <li className="flex items-start gap-2">
                  <span className="text-blue-500 mt-1">•</span>
                  <span>补充 validator 类型检查测试</span>
                </li>
              </ul>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
