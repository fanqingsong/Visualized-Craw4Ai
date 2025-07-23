import { Routes, Route } from 'react-router-dom'

import AppHeader from '@/components/layout/AppHeader'
import AppSidebar from '@/components/layout/AppSidebar'
import HomePage from '@/pages/HomePage'
import CrawlerPage from '@/pages/CrawlerPage'
import TasksPage from '@/pages/TasksPage'
import ProjectsPage from '@/pages/ProjectsPage'

function App() {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      <AppSidebar />
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column' }}>
        <AppHeader />
        <main style={{ flex: 1, padding: '24px', background: '#f0f2f5' }}>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/crawler" element={<CrawlerPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}

export default App 