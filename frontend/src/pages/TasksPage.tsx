import React, { useState, useEffect } from 'react'
import { 
  Card, 
  Table, 
  Button, 
  Space, 
  Tag, 
  Progress, 
  Modal,
  Typography,
  Row,
  Col,
  Statistic,
  Alert,
  Popconfirm,
  message,
  Input,
  Form,
  Divider
} from 'antd'
import { 
  UnorderedListOutlined,
  ReloadOutlined,
  DeleteOutlined,
  StopOutlined,
  EyeOutlined,
  PlusOutlined,

} from '@ant-design/icons'

const { Title, Text } = Typography
const { TextArea } = Input

// 任务状态枚举
enum TaskStatus {
  PENDING = 'pending',
  RUNNING = 'running', 
  COMPLETED = 'completed',
  FAILED = 'failed',
  CANCELLED = 'cancelled'
}

// 任务信息接口
interface TaskInfo {
  task_id: string
  status: TaskStatus
  progress: number
  total_urls: number
  completed_urls: number
  failed_urls: number
  created_at: string
  updated_at?: string
  completed_at?: string
  error_message?: string
  results?: any[]
}

const TasksPage: React.FC = () => {
  const [tasks, setTasks] = useState<TaskInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedTask, setSelectedTask] = useState<TaskInfo | null>(null)
  const [detailVisible, setDetailVisible] = useState(false)
  const [batchModalVisible, setBatchModalVisible] = useState(false)
  const [batchForm] = Form.useForm()

  // 获取任务列表
  const fetchTasks = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/v1/tasks/')
      const data = await response.json()
      if (data.success) {
        setTasks(Array.isArray(data.data) ? data.data : [])
      }
    } catch (error) {
      console.error('获取任务列表失败:', error)
      message.error('获取任务列表失败')
    } finally {
      setLoading(false)
    }
  }

  // 取消任务
  const cancelTask = async (taskId: string) => {
    try {
      const response = await fetch(`/api/v1/tasks/${taskId}/cancel`, {
        method: 'POST'
      })
      const data = await response.json()
      if (data.success) {
        message.success('任务已取消')
        fetchTasks()
      } else {
        message.error(data.message || '取消任务失败')
      }
    } catch (error) {
      console.error('取消任务失败:', error)
      message.error('取消任务失败')
    }
  }

  // 删除任务
  const deleteTask = async (taskId: string) => {
    try {
      const response = await fetch(`/api/v1/tasks/${taskId}`, {
        method: 'DELETE'
      })
      const data = await response.json()
      if (data.success) {
        message.success('任务已删除')
        fetchTasks()
      } else {
        message.error(data.message || '删除任务失败')
      }
    } catch (error) {
      console.error('删除任务失败:', error)
      message.error('删除任务失败')
    }
  }

  // 清理已完成任务
  const cleanupTasks = async () => {
    try {
      const response = await fetch('/api/v1/tasks/cleanup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ max_age_hours: 24 })
      })
      const data = await response.json()
      if (data.success) {
        message.success('已清理完成的任务')
        fetchTasks()
      } else {
        message.error(data.message || '清理任务失败')
      }
    } catch (error) {
      console.error('清理任务失败:', error)
      message.error('清理任务失败')
    }
  }

  // 创建批量任务
  const createBatchTask = async (values: any) => {
    try {
      const urls = values.urls.split('\n').filter((url: string) => url.trim())
      const response = await fetch('/api/v1/crawler/batch', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          urls: urls,
          config: {},
          concurrent_limit: values.concurrent_limit || 3
        })
      })
      const data = await response.json()
      if (data.success) {
        message.success('批量任务已创建')
        setBatchModalVisible(false)
        batchForm.resetFields()
        fetchTasks()
      } else {
        message.error(data.message || '创建批量任务失败')
      }
    } catch (error) {
      console.error('创建批量任务失败:', error)
      message.error('创建批量任务失败')
    }
  }

  // 状态标签颜色
  const getStatusColor = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING: return 'orange'
      case TaskStatus.RUNNING: return 'blue'
      case TaskStatus.COMPLETED: return 'green'
      case TaskStatus.FAILED: return 'red'
      case TaskStatus.CANCELLED: return 'default'
      default: return 'default'
    }
  }

  // 状态标签文本
  const getStatusText = (status: TaskStatus) => {
    switch (status) {
      case TaskStatus.PENDING: return '等待中'
      case TaskStatus.RUNNING: return '运行中'
      case TaskStatus.COMPLETED: return '已完成'
      case TaskStatus.FAILED: return '失败'
      case TaskStatus.CANCELLED: return '已取消'
      default: return '未知'
    }
  }

  // 表格列定义
  const columns = [
    {
      title: '任务ID',
      dataIndex: 'task_id',
      key: 'task_id',
      width: 120,
      render: (text: string) => (
        <Text code style={{ fontSize: '12px' }}>
          {text.substring(0, 8)}...
        </Text>
      )
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 100,
      render: (status: TaskStatus) => (
        <Tag color={getStatusColor(status)}>
          {getStatusText(status)}
        </Tag>
      )
    },
    {
      title: '进度',
      key: 'progress',
      width: 200,
      render: (record: TaskInfo) => (
        <div>
          <Progress 
            percent={record.progress} 
            size="small" 
            status={record.status === TaskStatus.FAILED ? 'exception' : 'active'}
          />
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.completed_urls}/{record.total_urls} 完成
          </Text>
        </div>
      )
    },
    {
      title: '创建时间',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 150,
      render: (text: string) => new Date(text).toLocaleString()
    },
    {
      title: '操作',
      key: 'actions',
      width: 200,
      render: (record: TaskInfo) => (
        <Space size="small">
          <Button
            size="small"
            icon={<EyeOutlined />}
            onClick={() => {
              setSelectedTask(record)
              setDetailVisible(true)
            }}
          >
            详情
          </Button>
          
          {record.status === TaskStatus.RUNNING && (
            <Popconfirm
              title="确定要取消这个任务吗？"
              onConfirm={() => cancelTask(record.task_id)}
              okText="确定"
              cancelText="取消"
            >
              <Button size="small" icon={<StopOutlined />} danger>
                取消
              </Button>
            </Popconfirm>
          )}
          
          {[TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.CANCELLED].includes(record.status) && (
            <Popconfirm
              title="确定要删除这个任务吗？"
              onConfirm={() => deleteTask(record.task_id)}
              okText="确定"
              cancelText="取消"
            >
              <Button size="small" icon={<DeleteOutlined />} danger>
                删除
              </Button>
            </Popconfirm>
          )}
        </Space>
      )
    }
  ]

  // 统计数据
  const stats = {
    total: tasks.length,
    running: tasks.filter(t => t.status === TaskStatus.RUNNING).length,
    completed: tasks.filter(t => t.status === TaskStatus.COMPLETED).length,
    failed: tasks.filter(t => t.status === TaskStatus.FAILED).length
  }

  // 初始加载任务
  useEffect(() => {
    fetchTasks()
  }, [])

  // 自动刷新运行中的任务
  useEffect(() => {
    const interval = setInterval(() => {
      const hasRunningTasks = tasks.some(t => t.status === TaskStatus.RUNNING)
      if (hasRunningTasks) {
        fetchTasks()
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [tasks])

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={2}>
          <UnorderedListOutlined style={{ color: '#1890ff', marginRight: '8px' }} />
          任务管理
        </Title>

        {/* 统计卡片 */}
        <Row gutter={16} style={{ marginBottom: '24px' }}>
          <Col span={6}>
            <Card size="small">
              <Statistic title="总任务数" value={stats.total} />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic 
                title="运行中" 
                value={stats.running} 
                valueStyle={{ color: '#1890ff' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic 
                title="已完成" 
                value={stats.completed} 
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card size="small">
              <Statistic 
                title="失败" 
                value={stats.failed} 
                valueStyle={{ color: '#ff4d4f' }}
              />
            </Card>
          </Col>
        </Row>

        {/* 操作按钮 */}
        <div style={{ marginBottom: '16px' }}>
          <Space>
            <Button 
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => setBatchModalVisible(true)}
            >
              创建批量任务
            </Button>
            <Button 
              icon={<ReloadOutlined />}
              onClick={fetchTasks}
              loading={loading}
            >
              刷新
            </Button>
            <Button 
              icon={<DeleteOutlined />}
              onClick={cleanupTasks}
            >
              清理已完成
            </Button>
          </Space>
        </div>

        {/* 任务表格 */}
        <Table
          columns={columns}
          dataSource={tasks}
          rowKey="task_id"
          loading={loading}
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total) => `共 ${total} 个任务`
          }}
        />
      </Card>

      {/* 任务详情模态框 */}
      <Modal
        title="任务详情"
        visible={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={null}
        width={800}
      >
        {selectedTask && (
          <div>
            <Row gutter={16}>
              <Col span={12}>
                <p><strong>任务ID:</strong> {selectedTask.task_id}</p>
                <p><strong>状态:</strong> 
                  <Tag color={getStatusColor(selectedTask.status)} style={{ marginLeft: '8px' }}>
                    {getStatusText(selectedTask.status)}
                  </Tag>
                </p>
                <p><strong>总URL数:</strong> {selectedTask.total_urls}</p>
                <p><strong>已完成:</strong> {selectedTask.completed_urls}</p>
                <p><strong>失败数:</strong> {selectedTask.failed_urls}</p>
              </Col>
              <Col span={12}>
                <p><strong>创建时间:</strong> {new Date(selectedTask.created_at).toLocaleString()}</p>
                {selectedTask.updated_at && (
                  <p><strong>更新时间:</strong> {new Date(selectedTask.updated_at).toLocaleString()}</p>
                )}
                {selectedTask.completed_at && (
                  <p><strong>完成时间:</strong> {new Date(selectedTask.completed_at).toLocaleString()}</p>
                )}
                <p><strong>进度:</strong> {selectedTask.progress}%</p>
              </Col>
            </Row>

            <Divider />
            
            <div>
              <Progress 
                percent={selectedTask.progress} 
                status={selectedTask.status === TaskStatus.FAILED ? 'exception' : 'active'}
              />
            </div>

            {selectedTask.error_message && (
              <Alert
                message="错误信息"
                description={selectedTask.error_message}
                type="error"
                style={{ marginTop: '16px' }}
              />
            )}
          </div>
        )}
      </Modal>

      {/* 批量任务创建模态框 */}
      <Modal
        title="创建批量爬取任务"
        visible={batchModalVisible}
        onCancel={() => setBatchModalVisible(false)}
        onOk={() => batchForm.submit()}
        width={600}
      >
        <Form
          form={batchForm}
          layout="vertical"
          onFinish={createBatchTask}
        >
          <Form.Item
            name="urls"
            label="URL列表"
            rules={[{ required: true, message: '请输入要爬取的URL列表' }]}
          >
            <TextArea
              rows={10}
              placeholder="请输入URL，每行一个&#10;例如：&#10;https://example1.com&#10;https://example2.com&#10;https://example3.com"
            />
          </Form.Item>

          <Form.Item
            name="concurrent_limit"
            label="并发限制"
            initialValue={3}
          >
            <Input type="number" min={1} max={10} />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  )
}

export default TasksPage 