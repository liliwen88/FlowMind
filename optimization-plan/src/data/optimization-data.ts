// 优化方案数据结构定义

export interface OptimizationItem {
  id: string;
  title: string;
  description: string;
  priority: 'high' | 'medium' | 'low';
  impact: 'high' | 'medium' | 'low';
  difficulty: 'easy' | 'medium' | 'hard';
  category: string;
  status?: 'pending' | 'in-progress' | 'completed';
  estimatedTime?: string;
  benefits: string[];
  implementation?: string[];
}

export interface CodeQualityMetric {
  name: string;
  current: number;
  target: number;
  unit: string;
  description: string;
}

export interface TestCoverage {
  module: string;
  coverage: number;
  tests: number;
  missing: string[];
}

export const optimizationData = {
  overview: {
    projectName: "llm-flow-dsl",
    version: "MVP v0.1",
    totalLinesOfCode: 1825,
    modules: 9,
    testFiles: 1,
    examples: 5,
    overallScore: 4.0,
  },
  
  highPriority: [
    {
      id: "hp-1",
      title: "添加依赖管理文件",
      description: "创建 pyproject.toml 或 requirements.txt，明确项目依赖",
      priority: "high" as const,
      impact: "high" as const,
      difficulty: "easy" as const,
      category: "工程化",
      estimatedTime: "30分钟",
      benefits: [
        "明确的依赖版本控制",
        "简化安装流程",
        "支持自动化构建",
        "团队协作一致性"
      ],
      implementation: [
        "创建 pyproject.toml 定义项目元数据",
        "声明 pytest>=7.0 等开发依赖",
        "配置 black、flake8、mypy 工具",
        "添加 README 中的安装说明"
      ]
    },
    {
      id: "hp-2",
      title: "添加 CI/CD 配置",
      description: "配置 GitHub Actions 自动测试和代码质量检查",
      priority: "high" as const,
      impact: "high" as const,
      difficulty: "medium" as const,
      category: "工程化",
      estimatedTime: "2小时",
      benefits: [
        "自动化测试执行",
        "代码覆盖率报告",
        "Linting 自动检查",
        "防止回归问题"
      ],
      implementation: [
        "创建 .github/workflows/test.yml",
        "配置 Python 环境矩阵（3.8, 3.9, 3.10, 3.11）",
        "添加 pytest 运行和覆盖率收集",
        "集成 mypy 类型检查",
        "配置 flake8/black 代码风格检查"
      ]
    },
    {
      id: "hp-3",
      title: "添加递归深度保护",
      description: "在 Pratt 解析器中添加递归深度限制，防止栈溢出",
      priority: "high" as const,
      impact: "high" as const,
      difficulty: "easy" as const,
      category: "性能与安全",
      estimatedTime: "1小时",
      benefits: [
        "防止恶意输入导致崩溃",
        "提高系统稳定性",
        "更好的错误提示",
        "生产环境安全性"
      ],
      implementation: [
        "在 parser.py 中定义 MAX_RECURSION_DEPTH = 100",
        "修改 _parse_expression 添加 depth 参数",
        "超过限制时抛出 ParseError",
        "添加测试用例验证保护机制"
      ]
    },
    {
      id: "hp-4",
      title: "补充关键测试",
      description: "填补边界条件、集成测试和所有示例文件的测试覆盖",
      priority: "high" as const,
      impact: "high" as const,
      difficulty: "medium" as const,
      category: "测试",
      estimatedTime: "4小时",
      benefits: [
        "提高代码可靠性",
        "发现潜在 bug",
        "支持安全重构",
        "提升用户信心"
      ],
      implementation: [
        "创建 test_lexer.py 专门测试词法分析",
        "添加深度嵌套表达式测试",
        "为所有 5 个示例文件编写集成测试",
        "添加边界条件测试（空 flow、超大文件）",
        "测试错误恢复机制"
      ]
    }
  ] as OptimizationItem[],

  mediumPriority: [
    {
      id: "mp-1",
      title: "添加 docstrings",
      description: "为所有公共 API 添加详细的文档字符串",
      priority: "medium" as const,
      impact: "medium" as const,
      difficulty: "medium" as const,
      category: "文档",
      estimatedTime: "6小时",
      benefits: [
        "改善开发者体验",
        "支持自动生成 API 文档",
        "降低学习成本",
        "提高代码可维护性"
      ],
      implementation: [
        "使用 Google 风格 docstrings",
        "为每个类添加描述和属性说明",
        "为公共方法添加参数和返回值文档",
        "添加模块级 docstrings"
      ]
    },
    {
      id: "mp-2",
      title: "添加 linting 和 type checking",
      description: "配置 mypy、flake8、black 等代码质量工具",
      priority: "medium" as const,
      impact: "medium" as const,
      difficulty: "medium" as const,
      category: "工程化",
      estimatedTime: "3小时",
      benefits: [
        "统一代码风格",
        "捕获类型错误",
        "提高代码质量",
        "减少人为疏忽"
      ],
      implementation: [
        "配置 pyproject.toml 中的 mypy 设置",
        "启用 strict 模式逐步修复类型错误",
        "配置 black 格式化规则",
        "添加 pre-commit hooks"
      ]
    },
    {
      id: "mp-3",
      title: "优化错误提示",
      description: "改进 CLI 错误输出格式，提供更友好的用户体验",
      priority: "medium" as const,
      impact: "medium" as const,
      difficulty: "medium" as const,
      category: "用户体验",
      estimatedTime: "3小时",
      benefits: [
        "降低用户困惑",
        "加速问题排查",
        "提升产品专业度",
        "改善第一印象"
      ],
      implementation: [
        "设计人类可读的错误格式模板",
        "添加代码片段和指针标记",
        "提供可能的修复建议",
        "支持 --verbose 详细模式"
      ]
    },
    {
      id: "mp-4",
      title: "性能基准测试",
      description: "建立性能基准并监控回归",
      priority: "medium" as const,
      impact: "medium" as const,
      difficulty: "medium" as const,
      category: "性能",
      estimatedTime: "4小时",
      benefits: [
        "量化性能表现",
        "及时发现性能退化",
        "指导优化方向",
        "建立性能基线"
      ],
      implementation: [
        "创建 test_performance.py",
        "测试不同大小 flow 文件的解析时间",
        "监控内存使用情况",
        "设置性能阈值告警"
      ]
    }
  ] as OptimizationItem[],

  lowPriority: [
    {
      id: "lp-1",
      title: "交互式 REPL 模式",
      description: "添加命令行交互模式实时测试 flow 语法",
      priority: "low" as const,
      impact: "medium" as const,
      difficulty: "hard" as const,
      category: "用户体验",
      estimatedTime: "8小时",
      benefits: [
        "快速原型开发",
        "学习 DSL 语法",
        "调试 flow 文件",
        "提升开发效率"
      ],
      implementation: [
        "实现 readline 交互式输入",
        "支持语法高亮显示",
        "添加自动补全功能",
        "支持历史记录和撤销"
      ]
    },
    {
      id: "lp-2",
      title: "Flow 可视化",
      description: "生成流程图（DOT/Mermaid 格式）和执行轨迹",
      priority: "low" as const,
      impact: "medium" as const,
      difficulty: "hard" as const,
      category: "工具",
      estimatedTime: "10小时",
      benefits: [
        "直观理解流程逻辑",
        "辅助代码审查",
        "文档自动生成",
        "教学演示用途"
      ],
      implementation: [
        "遍历 AST 生成节点关系图",
        "输出 DOT 格式文件",
        "支持 Mermaid 语法",
        "添加执行路径高亮"
      ]
    },
    {
      id: "lp-3",
      title: "DSL 语法增强",
      description: "添加导入/复用机制、内置函数库和类型系统增强",
      priority: "low" as const,
      impact: "high" as const,
      difficulty: "hard" as const,
      category: "语言特性",
      estimatedTime: "16小时",
      benefits: [
        "提高表达力",
        "减少重复代码",
        "支持复杂场景",
        "扩展应用场景"
      ],
      implementation: [
        "实现 import 语句解析",
        "添加内置函数 len()、contains() 等",
        "支持枚举和联合类型",
        "实现默认值语法"
      ]
    }
  ] as OptimizationItem[],

  codeQualityMetrics: [
    {
      name: "测试覆盖率",
      current: 65,
      target: 90,
      unit: "%",
      description: "代码行覆盖率"
    },
    {
      name: "类型标注率",
      current: 85,
      target: 100,
      unit: "%",
      description: "函数和变量的类型提示覆盖"
    },
    {
      name: "文档覆盖率",
      current: 15,
      target: 80,
      unit: "%",
      description: "公共 API 的 docstring 覆盖"
    },
    {
      name: "代码复杂度",
      current: 12,
      target: 8,
      unit: "分",
      description: "平均圈复杂度（越低越好）"
    },
    {
      name: "重复代码率",
      current: 8,
      target: 3,
      unit: "%",
      description: "重复代码块占比"
    }
  ] as CodeQualityMetric[],

  testCoverage: [
    {
      module: "lexer.py",
      coverage: 70,
      tests: 4,
      missing: ["边界字符处理", "Unicode 支持", "超长 token"]
    },
    {
      module: "parser.py",
      coverage: 75,
      tests: 6,
      missing: ["深度嵌套表达式", "错误恢复", "大文件性能"]
    },
    {
      module: "runner.py",
      coverage: 45,
      tests: 2,
      missing: ["LLM 调用模拟", "状态隔离", "并发安全", "异常处理"]
    },
    {
      module: "validator.py",
      coverage: 80,
      tests: 5,
      missing: ["成员访问类型检查", "schema 完整性验证"]
    },
    {
      module: "cli.py",
      coverage: 85,
      tests: 6,
      missing: ["交互式模式", "管道输入"]
    }
  ] as TestCoverage[],

  performanceBottlenecks: [
    {
      name: "递归深度问题",
      severity: "high",
      location: "parser.py::_parse_expression()",
      impact: "深层嵌套表达式可能导致栈溢出",
      solution: "添加递归深度限制或转换为迭代实现",
      estimatedImprovement: "消除崩溃风险"
    },
    {
      name: "copy.deepcopy 开销",
      severity: "medium",
      location: "runner.py::run_flow()",
      impact: "大型状态对象拷贝性能差",
      solution: "使用浅拷贝或不可变数据结构",
      estimatedImprovement: "30-50% 性能提升"
    },
    {
      name: "线性搜索符号表",
      severity: "low",
      location: "validator.py",
      impact: "大型 flow 文件查找效率低",
      solution: "使用集合或字典优化查找",
      estimatedImprovement: "O(n) → O(1)"
    }
  ]
};

export default optimizationData;
