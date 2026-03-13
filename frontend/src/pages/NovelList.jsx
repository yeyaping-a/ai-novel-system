import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

function NovelList() {
  const [novels, setNovels] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadNovels()
  }, [])

  const loadNovels = async () => {
    try {
      const res = await axios.get(`${API_BASE}/novels/`)
      setNovels(res.data.data)
    } catch (error) {
      console.error('加载小说列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="text-center py-10">加载中...</div>
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">小说管理</h1>
        <Link
          to="/novels/new"
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          创建小说
        </Link>
      </div>

      {novels.length === 0 ? (
        <div className="text-center py-20 bg-white rounded-lg shadow">
          <div className="text-6xl mb-4">📚</div>
          <p className="text-gray-600 mb-4">还没有创建小说</p>
          <Link
            to="/novels/new"
            className="text-blue-500 hover:text-blue-600"
          >
            创建第一部小说
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {novels.map(novel => (
            <div key={novel.id} className="bg-white rounded-lg shadow overflow-hidden">
              <div className="p-6">
                <h3 className="text-xl font-bold mb-2">{novel.title}</h3>
                <p className="text-gray-600 text-sm mb-4">
                  {novel.genre || '未分类'} · {novel.author}
                </p>
                <div className="flex justify-between text-sm text-gray-500 mb-4">
                  <span>章节: {novel.total_chapters}</span>
                  <span>字数: {novel.total_words.toLocaleString()}</span>
                </div>
                <div className="flex space-x-2">
                  <Link
                    to={`/novels/${novel.id}`}
                    className="flex-1 text-center bg-gray-100 text-gray-700 px-4 py-2 rounded hover:bg-gray-200"
                  >
                    管理
                  </Link>
                  <Link
                    to={`/reader/${novel.id}`}
                    className="flex-1 text-center bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                  >
                    阅读
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default NovelList
