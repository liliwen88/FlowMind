import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Github, Star, Zap, BarChart3, Code2, TestTube } from "lucide-react"

interface HeaderProps {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export function Header({ activeTab, setActiveTab }: HeaderProps) {
  const tabs = [
    { id: "overview", label: "总览", icon: BarChart3 },
    { id: "priority", label: "优先级矩阵", icon: Zap },
    { id: "quality", label: "代码质量", icon: Code2 },
    { id: "testing", label: "测试覆盖", icon: TestTube },
  ]

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gradient-to-br from-primary to-blue-600 shadow-lg">
            <Code2 className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gradient">llm-flow-dsl</h1>
            <p className="text-xs text-muted-foreground">优化方案 v0.1</p>
          </div>
          <Badge variant="success" className="ml-2">
            MVP 完成
          </Badge>
        </div>

        <nav className="hidden md:flex items-center gap-1">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <Button
                key={tab.id}
                variant={activeTab === tab.id ? "default" : "ghost"}
                size="sm"
                onClick={() => setActiveTab(tab.id)}
                className="gap-2"
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </Button>
            )
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" className="gap-2">
            <Github className="h-4 w-4" />
            GitHub
          </Button>
          <Button variant="gradient" size="sm" className="gap-2">
            <Star className="h-4 w-4" />
            开始优化
          </Button>
        </div>
      </div>
    </header>
  )
}
