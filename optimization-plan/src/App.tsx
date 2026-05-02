import { useState } from 'react'
import { Header } from './components/Header'
import { Overview } from './components/Overview'
import { PriorityMatrix } from './components/PriorityMatrix'
import { CodeQuality } from './components/CodeQuality'
import { TestCoverage } from './components/TestCoverage'

function App() {
  const [activeTab, setActiveTab] = useState('overview')

  const renderContent = () => {
    switch (activeTab) {
      case 'overview':
        return <Overview />
      case 'priority':
        return <PriorityMatrix />
      case 'quality':
        return <CodeQuality />
      case 'testing':
        return <TestCoverage />
      default:
        return <Overview />
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Header activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="container py-8">
        {renderContent()}
      </main>
      
      {/* Footer */}
      <footer className="border-t bg-muted/50 mt-12">
        <div className="container py-8">
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <div className="text-sm text-muted-foreground">
              © 2026 llm-flow-dsl Optimization Plan. Generated with Lingma.
            </div>
            <div className="flex gap-4 text-sm text-muted-foreground">
              <span>版本: v0.1</span>
              <span>•</span>
              <span>最后更新: 2026-05-02</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
