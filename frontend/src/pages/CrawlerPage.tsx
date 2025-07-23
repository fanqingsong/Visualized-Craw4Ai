import React, { useState } from 'react'
import { 
  Card, 
  Form, 
  Input, 
  Button, 
  Space, 
  Switch, 
  Select, 
  InputNumber,
  Tabs,
  Alert,
  Spin,
  Typography,
  Row,
  Col,

  message
} from 'antd'
import { 
  RobotOutlined, 
  PlayCircleOutlined, 

  FileTextOutlined,
  CopyOutlined,
  DownloadOutlined
} from '@ant-design/icons'

const { TextArea } = Input
const { Title, Paragraph, Text } = Typography
const { TabPane } = Tabs

// 爬虫配置接口
interface CrawlConfig {
  word_count_threshold?: number
  cache_mode?: string
  wait_until?: string
  page_timeout?: number
  only_text?: boolean
  screenshot?: boolean
  pdf?: boolean
  deep_crawl?: boolean
  crawl_depth?: number
  exclude_external_links?: boolean
  magic?: boolean
}

// 爬取结果接口
interface CrawlResult {
  url: string
  success: boolean
  status_code?: number
  title?: string
  markdown?: string
  cleaned_html?: string
  execution_time?: number
  error_message?: string
}

const CrawlerPage: React.FC = () => {
  const [form] = Form.useForm()
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<CrawlResult | null>(null)
  const [activeTab, setActiveTab] = useState('basic')

  // 单个URL爬取
  const handleSingleCrawl = async (values: any) => {
    setLoading(true)
    try {
      const config: CrawlConfig = {
        word_count_threshold: values.word_count_threshold,
        cache_mode: values.cache_mode,
        wait_until: values.wait_until,
        page_timeout: values.page_timeout,
        only_text: values.only_text,
        screenshot: values.screenshot,
        pdf: values.pdf,
        deep_crawl: values.deep_crawl,
        crawl_depth: values.crawl_depth,
        exclude_external_links: values.exclude_external_links,
        magic: values.magic
      }

      const response = await fetch('/api/v1/crawler/single', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: values.url,
          config: config
        }),
      })

      const data = await response.json()
      
      if (data.success && data.data) {
        setResult(data.data)
        if (data.data.success) {
          message.success('爬取成功！')
        } else {
          message.error(data.data.error_message || '爬取失败')
        }
      } else {
        message.error(data.message || '爬取失败')
      }
    } catch (error) {
      console.error('爬取错误:', error)
      message.error('网络错误，请检查后端服务是否正常')
    } finally {
      setLoading(false)
    }
  }

  // 复制结果到剪贴板
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      message.success('已复制到剪贴板')
    })
  }

  // 下载结果
  const downloadResult = (content: string, filename: string) => {
    const blob = new Blob([content], { type: 'text/plain' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
  }

  return (
    <div style={{ padding: '24px' }}>
      <Card>
        <Title level={2}>
          <RobotOutlined style={{ color: '#1890ff', marginRight: '8px' }} />
          网页内容爬取工具
        </Title>
        <Paragraph>
          输入网页 URL，配置爬取参数，获取结构化的网页内容。支持 JavaScript 渲染、深度爬取、智能内容提取等高级功能。
        </Paragraph>

        <Row gutter={24}>
          <Col span={12}>
            <Card title="爬取配置" size="small">
              <Form
                form={form}
                layout="vertical"
                onFinish={handleSingleCrawl}
                initialValues={{
                  cache_mode: 'enabled',
                  wait_until: 'domcontentloaded',
                  page_timeout: 30000,
                  word_count_threshold: 10,
                  crawl_depth: 2,
                  only_text: false,
                  screenshot: false,
                  pdf: false,
                  deep_crawl: false,
                  exclude_external_links: true,
                  magic: true
                }}
              >
                <Form.Item
                  name="url"
                  label="目标 URL"
                  rules={[
                    { required: true, message: '请输入要爬取的 URL' },
                    { type: 'url', message: '请输入有效的 URL' }
                  ]}
                >
                  <Input 
                    placeholder="https://example.com" 
                    size="large"
                  />
                </Form.Item>

                <Tabs activeKey={activeTab} onChange={setActiveTab}>
                  <TabPane tab="基础配置" key="basic">
                    <Form.Item name="cache_mode" label="缓存模式">
                      <Select>
                        <Select.Option value="enabled">启用缓存</Select.Option>
                        <Select.Option value="disabled">禁用缓存</Select.Option>
                        <Select.Option value="bypass">绕过缓存</Select.Option>
                      </Select>
                    </Form.Item>

                    <Form.Item name="wait_until" label="等待条件">
                      <Select>
                        <Select.Option value="domcontentloaded">DOM 加载完成</Select.Option>
                        <Select.Option value="load">页面完全加载</Select.Option>
                        <Select.Option value="networkidle">网络空闲</Select.Option>
                      </Select>
                    </Form.Item>

                    <Form.Item name="page_timeout" label="页面超时 (毫秒)">
                      <InputNumber min={5000} max={120000} style={{ width: '100%' }} />
                    </Form.Item>

                    <Form.Item name="word_count_threshold" label="最小字数">
                      <InputNumber min={1} max={1000} style={{ width: '100%' }} />
                    </Form.Item>
                  </TabPane>

                  <TabPane tab="内容选项" key="content">
                    <Form.Item name="only_text" valuePropName="checked">
                      <Switch /> 仅提取文本内容
                    </Form.Item>

                    <Form.Item name="screenshot" valuePropName="checked">
                      <Switch /> 生成页面截图
                    </Form.Item>

                    <Form.Item name="pdf" valuePropName="checked">
                      <Switch /> 生成 PDF
                    </Form.Item>

                    <Form.Item name="magic" valuePropName="checked">
                      <Switch /> 启用智能提取
                    </Form.Item>
                  </TabPane>

                  <TabPane tab="深度爬取" key="deep">
                    <Form.Item name="deep_crawl" valuePropName="checked">
                      <Switch /> 启用深度爬取
                    </Form.Item>

                    <Form.Item name="crawl_depth" label="爬取深度">
                      <InputNumber min={1} max={5} style={{ width: '100%' }} />
                    </Form.Item>

                    <Form.Item name="exclude_external_links" valuePropName="checked">
                      <Switch /> 排除外部链接
                    </Form.Item>
                  </TabPane>
                </Tabs>

                <Form.Item>
                  <Button 
                    type="primary" 
                    htmlType="submit" 
                    size="large" 
                    loading={loading}
                    icon={<PlayCircleOutlined />}
                    block
                  >
                    {loading ? '爬取中...' : '开始爬取'}
                  </Button>
                </Form.Item>
              </Form>
            </Card>
          </Col>

          <Col span={12}>
            <Card title="爬取结果" size="small">
              {loading && (
                <div style={{ textAlign: 'center', padding: '50px' }}>
                  <Spin size="large" />
                  <div style={{ marginTop: '16px' }}>
                    <Text>正在爬取网页内容...</Text>
                  </div>
                </div>
              )}

              {result && !loading && (
                <div>
                  {result.success ? (
                    <Alert
                      message="爬取成功"
                      description={`耗时: ${result.execution_time?.toFixed(2)}s | 状态码: ${result.status_code}`}
                      type="success"
                      style={{ marginBottom: '16px' }}
                    />
                  ) : (
                    <Alert
                      message="爬取失败"
                      description={result.error_message}
                      type="error"
                      style={{ marginBottom: '16px' }}
                    />
                  )}

                  {result.success && (
                    <Tabs defaultActiveKey="markdown">
                      <TabPane tab="Markdown 内容" key="markdown">
                        <div style={{ marginBottom: '8px' }}>
                          <Space>
                            <Button 
                              size="small" 
                              icon={<CopyOutlined />}
                              onClick={() => copyToClipboard(result.markdown || '')}
                            >
                              复制
                            </Button>
                            <Button 
                              size="small" 
                              icon={<DownloadOutlined />}
                              onClick={() => downloadResult(result.markdown || '', 'content.md')}
                            >
                              下载
                            </Button>
                          </Space>
                        </div>
                        <TextArea
                          value={result.markdown}
                          rows={20}
                          readOnly
                          style={{ fontFamily: 'monospace' }}
                        />
                      </TabPane>

                      <TabPane tab="HTML 内容" key="html">
                        <div style={{ marginBottom: '8px' }}>
                          <Space>
                            <Button 
                              size="small" 
                              icon={<CopyOutlined />}
                              onClick={() => copyToClipboard(result.cleaned_html || '')}
                            >
                              复制
                            </Button>
                            <Button 
                              size="small" 
                              icon={<DownloadOutlined />}
                              onClick={() => downloadResult(result.cleaned_html || '', 'content.html')}
                            >
                              下载
                            </Button>
                          </Space>
                        </div>
                        <TextArea
                          value={result.cleaned_html}
                          rows={20}
                          readOnly
                          style={{ fontFamily: 'monospace' }}
                        />
                      </TabPane>

                      <TabPane tab="页面信息" key="info">
                        <div>
                          <p><strong>页面标题:</strong> {result.title}</p>
                          <p><strong>URL:</strong> {result.url}</p>
                          <p><strong>状态码:</strong> {result.status_code}</p>
                          <p><strong>执行时间:</strong> {result.execution_time?.toFixed(2)}s</p>
                        </div>
                      </TabPane>
                    </Tabs>
                  )}
                </div>
              )}

              {!result && !loading && (
                <div style={{ textAlign: 'center', padding: '50px', color: '#999' }}>
                  <FileTextOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
                  <div>配置参数并点击"开始爬取"来获取网页内容</div>
                </div>
              )}
            </Card>
          </Col>
        </Row>
      </Card>
    </div>
  )
}

export default CrawlerPage 