import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

function Reader() {
  const { novelId, chapterId } = useParams()
  const navigate = useNavigate()
  const [novel, setNovel] = useState(null)
  const [chapters, setChapters] = useState([])
  const [currentChapter, setCurrentChapter] = useState(null)
  const [settings, setSettings] = useState({
    fontSize: 18,
    theme: 'light', // light, dark, sepia
    lineHeight: 1.8
  })

  useEffect(() => {
    loadNovel()
    loadChapters()
  }, [novelId])

  useEffect(() => {
    if (chapters.length > 0 && !chapterId) {
      // 默认显示第一章
      const firstChapter = chapters.find(c => c.status === 'generated' || c.status === 'published')
      if (firstChapter) {
        navigate(`/reader/${novelId}/chapter/${firstChapter.id}`, { replace: true })
      }
    }
  }, [chapters, chapterId, novelId, navigate])

  useEffect(() => {
    if (chapterId) {
      loadChapter(chapterId)
    }
  }, [chapterId])

  const loadNovel = async () => {
    try {
      const res = await axios.get(`${API_BASE}/reader/novel/${novelId}`)
      setNovel(res.data.data)
    } catch (error) {
      console.error('加载小说失败:', error)
    }
  }

  const loadChapters = async () => {
    try {
      const res = await axios.get(`${API_BASE}/reader/novel/${novelId}`)
      setChapters(res.data.data.chapters)
    } catch (error) {
      console.error('加载章节列表失败:', error)
    }
  }

  const loadChapter = async (id) => {
    try {
      const res = await axios.get(`${API_BASE}/reader/chapter/${id}`)
      setCurrentChapter(res.data.data)
    } catch (error) {
      console.error('加载章节失败:', error)
    }
  }

  const getThemeClass = () => {
    switch (settings.theme) {
      case 'dark':
        return 'bg-gray-900 text-gray-100'
      case 'sepia':
        return 'bg-amber-50 text-gray-800'
      default:
        return 'bg-white text-gray-800'
    }
  }

  if (!novel || !currentChapter) {
    return <div className="text-center py-10">加载中...</div>
  }

  return (
    <div className={`min-h-screen ${getThemeClass()}`}>
      {/* 顶部工具栏 */}
      <div className="sticky top-0 bg-white shadow z-10">
        <div className="max-w-4xl mx-auto px-4 py-3 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <Link to={`/novels/${novelId}`} className="text-blue-500 hover:text-blue-600">
              返回
            </Link>
            <span className="text-gray-400">|</span>
            <span className="font-medium">{novel.title}</span>
          </div>
          <div className="flex items-center space-x-3">
            <select
              value={settings.fontSize}
              onChange={(e) => setSettings({ ...settings, fontSize: Number(e.target.value) })}
              className="border rounded px-2 py-1"
            >
              <option value={14}>小号</option>
              <option value={16}>中号</option>
              <option value={18}>标准</option>
              <option value={20}>大号</option>
              <option value={24}>超大</option>
            </select>
            <select
              value={settings.theme}
              onChange={(e) => setSettings({ ...settings, theme: e.target.value })}
              className="border rounded px-2 py-1"
            >
              <option value="light">日间</option>
              <option value="dark">夜间</option>
              <option value="sepia">护眼</option>
            </select>
          </div>
        </div>
      </div>

      {/* 章节内容 */}
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-center mb-8">
          第{currentChapter.chapter_number}章 {currentChapter.title}
        </h1>
        
        <div
          className="reader-content"
          style={{
            fontSize: `${settings.fontSize}px`,
            lineHeight: settings.lineHeight
          }}
        >
          {currentChapter.content?.split('\n').map((para, idx) => (
            <p key={idx}>{para}</p>
          ))}
        </div>

        {/* 上下章导航 */}
        <div className="flex justify-between items-center mt-12 pt-6 border-t">
          {currentChapter.prev_chapter_id ? (
            <button
              onClick={() => navigate(`/reader/${novelId}/chapter/${currentChapter.prev_chapter_id}`)}
              className="text-blue-500 hover:text-blue-600"
            >
              ← 上一章
            </button>
          ) : (
            <div></div>
          )}
          
          {currentChapter.next_chapter_id ? (
            <button
              onClick={() => navigate(`/reader/${novelId}/chapter/${currentChapter.next_chapter_id}`)}
              className="text-blue-500 hover:text-blue-600"
            >
              下一章 →
            </button>
          ) : (
            <div></div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Reader
