import React, { useState, useEffect } from 'react'
import { Card, Row, Col, Statistic, Button, Typography, Space, Spin } from 'antd'
import { useNavigate } from 'react-router-dom'
import {
  RobotOutlined,
  UnorderedListOutlined,
  FolderOutlined,
  ThunderboltOutlined
} from '@ant-design/icons'

const { Title, Paragraph } = Typography

interface Stats {
  totalCrawls: number
  activeTasks: number
  totalProjects: number
  successRate: number
}

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const [stats, setStats] = useState<Stats>({
    totalCrawls: 0,
    activeTasks: 0,
    totalProjects: 0,
    successRate: 0
  })
  const [loading, setLoading] = useState(true)

  // 获取统计数据
  const fetchStats = async () => {
    try {
      // 并行获取任务和项目数据
      const [tasksResponse, projectsResponse] = await Promise.all([
        fetch('/api/v1/tasks/'),
        fetch('/api/v1/projects/')
      ])

      const tasksData = await tasksResponse.json()
      const projectsData = await projectsResponse.json()

      if (tasksData.success && projectsData.success) {
        const tasks = Array.isArray(tasksData.data) ? tasksData.data : []
        const projects = Array.isArray(projectsData.data) ? projectsData.data : []

        // 计算统计数据
        const totalCrawls = tasks.reduce((sum: number, task: any) => sum + (task.completed_urls || 0), 0)
        const activeTasks = tasks.filter((task: any) => task.status === 'running').length
        const completedTasks = tasks.filter((task: any) => task.status === 'completed').length

        const successRate = tasks.length > 0 ? Math.round((completedTasks / tasks.length) * 100) : 0

        setStats({
          totalCrawls,
          activeTasks,
          totalProjects: projects.length,
          successRate
        })
      }
    } catch (error) {
      console.error('获取统计数据失败:', error)
      // 保持默认值
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
    
    // 每30秒刷新一次统计数据
    const interval = setInterval(fetchStats, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div>
      {/* 欢迎区域 */}
      <Card style={{ marginBottom: 24 }}>
        <Row gutter={24} align="middle">
          <Col span={16}>
            <Title level={2} style={{ margin: 0 }}>
              欢迎使用 Crawl4AI 可视化工具 🎉
            </Title>
            <Paragraph style={{ fontSize: '16px', marginTop: '16px', marginBottom: '24px' }}>
              这是一个基于 Crawl4AI 构建的专业级网页内容提取工具，支持单个/批量 URL 爬取、
              智能内容提取、深度爬取等功能。无需编写代码，通过可视化界面即可完成复杂的爬取任务。
            </Paragraph>
            <Space size="large">
              <Button 
                type="primary" 
                size="large"
                icon={<RobotOutlined />}
                onClick={() => navigate('/crawler')}
              >
                开始爬取
              </Button>
              <Button 
                size="large"
                icon={<UnorderedListOutlined />}
                onClick={() => navigate('/tasks')}
              >
                查看任务
              </Button>
            </Space>
          </Col>
          <Col span={8} style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '120px', color: '#1890ff', opacity: 0.8 }}>
              🤖
            </div>
          </Col>
        </Row>
      </Card>

      {/* 统计卡片 */}
      <Row gutter={24} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : (
              <Statistic
                title="总爬取次数"
                value={stats.totalCrawls}
                prefix={<ThunderboltOutlined />}
                valueStyle={{ color: '#3f8600' }}
              />
            )}
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : (
              <Statistic
                title="活跃任务"
                value={stats.activeTasks}
                prefix={<UnorderedListOutlined />}
                valueStyle={{ color: '#1890ff' }}
              />
            )}
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : (
              <Statistic
                title="项目数量"
                value={stats.totalProjects}
                prefix={<FolderOutlined />}
                valueStyle={{ color: '#722ed1' }}
              />
            )}
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            {loading ? (
              <div style={{ textAlign: 'center', padding: '20px' }}>
                <Spin />
              </div>
            ) : (
              <Statistic
                title="成功率"
                value={stats.successRate}
                suffix="%"
                valueStyle={{ 
                  color: stats.successRate >= 80 ? '#3f8600' : stats.successRate >= 60 ? '#faad14' : '#cf1322'
                }}
              />
            )}
          </Card>
        </Col>
      </Row>

      {/* 功能介绍 */}
      <Row gutter={24}>
        <Col span={8}>
          <Card 
            title="🚀 核心功能"
            style={{ height: '300px' }}
          >
            <ul style={{ paddingLeft: '20px' }}>
              <li style={{ marginBottom: '8px' }}>单个/批量 URL 爬取</li>
              <li style={{ marginBottom: '8px' }}>智能内容提取</li>
              <li style={{ marginBottom: '8px' }}>深度爬取支持</li>
              <li style={{ marginBottom: '8px' }}>异步任务管理</li>
              <li style={{ marginBottom: '8px' }}>多种导出格式</li>
              <li style={{ marginBottom: '8px' }}>实时进度追踪</li>
            </ul>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            title="🎯 高级配置"
            style={{ height: '300px' }}
          >
            <ul style={{ paddingLeft: '20px' }}>
              <li style={{ marginBottom: '8px' }}>爬取策略选择</li>
              <li style={{ marginBottom: '8px' }}>内容过滤规则</li>
              <li style={{ marginBottom: '8px' }}>自定义提取指令</li>
              <li style={{ marginBottom: '8px' }}>代理支持</li>
              <li style={{ marginBottom: '8px' }}>浏览器配置</li>
              <li style={{ marginBottom: '8px' }}>JavaScript 执行</li>
            </ul>
          </Card>
        </Col>
        <Col span={8}>
          <Card 
            title="📊 可视化界面"
            style={{ height: '300px' }}
          >
            <ul style={{ paddingLeft: '20px' }}>
              <li style={{ marginBottom: '8px' }}>直观配置面板</li>
              <li style={{ marginBottom: '8px' }}>实时监控界面</li>
              <li style={{ marginBottom: '8px' }}>结果预览展示</li>
              <li style={{ marginBottom: '8px' }}>项目管理系统</li>
              <li style={{ marginBottom: '8px' }}>历史记录查看</li>
              <li style={{ marginBottom: '8px' }}>数据可视化图表</li>
            </ul>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default HomePage 