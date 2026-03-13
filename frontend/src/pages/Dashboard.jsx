import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

function Dashboard() {
  const [stats, setStats] = useState({
    totalNovels: 0,
    totalChapters: 0,
    totalWords: 0,
    publishedChapters: 0
  })

  useEffect(() => {
    loadStats()
  }, [])

  const loadStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/novels/`)
      const novels = res.data.data
      let totalChapters = 0
      let totalWords = 0
      let publishedChapters = 0

      for (const novel of novels) {
        totalChapters += novel.total_chapters
        totalWords += novel.total_words
        if (novel.status === 'publishing') publishedChapters++
      }

      setStats({
        totalNovels: novels.length,
        totalChapters,
        totalWords,
        publishedChapters
      })
    } catch (error) {
      console.error('加载统计数据失败:', error)
    }
  }

  return (
    <div className="space-y-6">
      {/* 欢迎信息 */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">欢迎来到 AI 小说自动化系统</h1>
        <p className="text-blue-100">智能化创作，自动化发布，让写作更轻松</p>
      </div>

      {/* 统计卡片 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="text-3xl mr-4">📖</div>
            <div>
              <div className="text-sm text-gray-500">小说数量</div>
              <div className="text-2xl font-bold">{stats.totalNovels}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="text-3xl mr-4">📝</div>
            <div>
              <div className="text-sm text-gray-500">总章节</div>
              <div className="text-2xl font-bold">{stats.totalChapters}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="text-3xl mr-4">✍️</div>
            <div>
              <div className="text-sm text-gray-500">总字数</div>
              <div className="text-2xl font-bold">{stats.totalWords.toLocaleString()}</div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center">
            <div className="text-3xl mr-4">🚀</div>
            <div>
              <div className="text-sm text-gray-500">已发布</div>
              <div className="text-2xl font-bold">{stats.publishedChapters}</div>
            </div>
          </div>
        </div>
      </div>

      {/* 快捷操作 */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Link to="/novels" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div className="text-center">
            <div className="text-5xl mb-3">📚</div>
            <h3 className="text-lg font-semibold mb-2">小说管理</h3>
            <p className="text-gray-600 text-sm">创建和管理你的小说作品</p>
          </div>
        </Link>

        <Link to="/novels/new" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div className="text-center">
            <div className="text-5xl mb-3">✨</div>
            <h3 className="text-lg font-semibold mb-2">AI 创作</h3>
            <p className="text-gray-600 text-sm">使用 AI 生成章节内容</p>
          </div>
        </Link>

        <Link to="/reader" className="bg-white rounded-lg shadow p-6 hover:shadow-lg transition-shadow">
          <div className="text-center">
            <div className="text-5xl mb-3">📖</div>
            <h3 className="text-lg font-semibold mb-2">本地阅读</h3>
            <p className="text-gray-600 text-sm">舒适的本地阅读体验</p>
          </div>
        </Link>
      </div>

      {/* 当前项目 */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold mb-4">当前项目：《代码掘金者》</h2>
        <div className="space-y-4">
          <div className="flex justify-between items-center">
            <span className="text-gray-600">类型：科幻小说</span>
            <span className="text-gray-600">主题：一个普通人如何通过AI赚了第一桶金</span>
          </div>
          <div className="flex space-x-3">
            <Link
              to="/novels/1"
              className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
            >
              查看详情
            </Link>
            <button className="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 transition-colors">
              开始创作
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
