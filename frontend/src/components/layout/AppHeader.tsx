const AppHeader = () => {
  return (
    <header 
      style={{ 
        background: '#fff', 
        padding: '0 24px',
        borderBottom: '1px solid #f0f0f0',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        height: '64px'
      }}
    >
      <h4 style={{ margin: 0, color: '#1890ff' }}>
        🤖 Crawl4AI 可视化工具
      </h4>
      
      <div style={{ display: 'flex', gap: '16px' }}>
        <a 
          href="/docs" 
          target="_blank" 
          style={{ color: '#666', textDecoration: 'none' }}
        >
          ❓ 帮助文档
        </a>
        <a 
          href="https://github.com/unclecode/crawl4ai" 
          target="_blank"
          style={{ color: '#666', textDecoration: 'none' }}
        >
          🔗 GitHub
        </a>
      </div>
    </header>
  )
}

export default AppHeader 