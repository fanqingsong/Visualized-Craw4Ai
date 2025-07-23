import { useLocation, useNavigate } from 'react-router-dom'

const AppSidebar = () => {
  const location = useLocation()
  const navigate = useNavigate()

  const menuItems = [
    { key: '/', icon: '🏠', label: '首页' },
    { key: '/crawler', icon: '🤖', label: '爬虫工具' },
    { key: '/tasks', icon: '📋', label: '任务管理' },
    { key: '/projects', icon: '📁', label: '项目管理' }
  ]

  const handleMenuClick = (key: string) => {
    navigate(key)
  }

  return (
    <aside
      style={{
        width: '200px',
        background: '#fff',
        borderRight: '1px solid #f0f0f0',
        height: '100vh'
      }}
    >
      <div style={{ 
        padding: '16px', 
        textAlign: 'center', 
        borderBottom: '1px solid #f0f0f0' 
      }}>
        <div style={{ fontSize: '18px', fontWeight: 'bold', color: '#1890ff' }}>
          Crawl4AI
        </div>
        <div style={{ fontSize: '12px', color: '#666', marginTop: '4px' }}>
          可视化工具
        </div>
      </div>
      
      <nav style={{ padding: '16px 0' }}>
        {menuItems.map(item => (
          <div
            key={item.key}
            onClick={() => handleMenuClick(item.key)}
            style={{
              padding: '12px 24px',
              cursor: 'pointer',
              backgroundColor: location.pathname === item.key ? '#e6f7ff' : 'transparent',
              borderRight: location.pathname === item.key ? '3px solid #1890ff' : 'none',
              color: location.pathname === item.key ? '#1890ff' : '#666'
            }}
          >
            <span style={{ marginRight: '8px' }}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </nav>
    </aside>
  )
}

export default AppSidebar 