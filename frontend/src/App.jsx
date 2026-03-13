import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import { useState, useEffect } from 'react'
import axios from 'axios'
import NovelList from './pages/NovelList'
import NovelDetail from './pages/NovelDetail'
import ChapterEditor from './pages/ChapterEditor'
import Reader from './pages/Reader'
import Dashboard from './pages/Dashboard'

const API_BASE = 'http://localhost:5000/api'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* 导航栏 */}
        <nav className="bg-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex justify-between h-16">
              <div className="flex items-center space-x-8">
                <Link to="/" className="flex items-center space-x-2">
                  <span className="text-2xl">📚</span>
                  <span className="font-bold text-xl text-gray-800">AI 小说系统</span>
                </Link>
                <div className="hidden md:flex space-x-4">
                  <Link to="/" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md font-medium">
                    工作台
                  </Link>
                  <Link to="/novels" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md font-medium">
                    小说管理
                  </Link>
                  <Link to="/reader" className="text-gray-600 hover:text-gray-900 px-3 py-2 rounded-md font-medium">
                    本地阅读
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </nav>

        {/* 主内容 */}
        <main className="max-w-7xl mx-auto py-6 px-4">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/novels" element={<NovelList />} />
            <Route path="/novels/:id" element={<NovelDetail />} />
            <Route path="/chapters/:id/edit" element={<ChapterEditor />} />
            <Route path="/reader/:novelId" element={<Reader />} />
            <Route path="/reader/:novelId/chapter/:chapterId" element={<Reader />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
